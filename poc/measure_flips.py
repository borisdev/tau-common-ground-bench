"""Pass 2 — paired re-scoring across the full airline suite.

Loads the recorded trajectories (poc/trajectories_all.json) and the lifted, provenance-
grounded fixtures (poc/lifted_requirements.json). For each task that carries >=1 constraint,
runs the PreflightRequirementsEvaluator against the SAME recorded trajectory and compares its
verdict to tau3's DB grade. A "flip" = tau3 PASS but preflight FAIL (a stated requirement the
DB grader could not see was violated). Writes poc/flip_report.md.
"""
import sys, types, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
for name, sub in [("tau2", "src/tau2"), ("tau2.domains", "src/tau2/domains"),
                  ("tau2.domains.airline", "src/tau2/domains/airline"),
                  ("tau2.environment", "src/tau2/environment"),
                  ("tau2.data_model", "src/tau2/data_model")]:
    m = types.ModuleType(name); m.__path__ = [os.path.join(ROOT, sub)]; m.__package__ = name
    sys.modules[name] = m

from tau2.data_model.preflight_requirements import UserPreflightRequirements
from tau2.data_model.fixtures_preflight import _load_airline_task_instructions
from tau2.evaluator.preflight_requirements_evaluator import PreflightRequirementsEvaluator

trajs = {str(t["task_id"]): t for t in json.load(open(os.path.join(ROOT, "poc/trajectories_all.json")))}
lifted = json.load(open(os.path.join(ROOT, "poc/lifted_requirements.json")))
ev = PreflightRequirementsEvaluator()

rows, flips, graded = [], [], 0
for tid, dump in lifted.items():
    upr = UserPreflightRequirements.model_validate(dump)
    if not upr.constraints or tid not in trajs:
        continue
    traj = trajs[tid]
    instr = _load_airline_task_instructions(tid).model_copy(update={"user_preflight_requirements": upr})
    res = ev.evaluate_instructions(traj["trajectory"], instr)
    graded += 1
    tau3 = "PASS" if traj.get("reward", 0) >= 1 else "FAIL"
    pf = "PASS" if (res is None or res.passed) else "FAIL"
    vios = [v.action for v in (res.violations if res else [])]
    flip = tau3 == "PASS" and pf == "FAIL"
    if flip:
        flips.append((tid, vios, res.violations))
    rows.append((int(tid), tau3, pf, "**FLIP**" if flip else ("agree" if tau3 == pf else ""), vios))

rows.sort()
lines = [
    "# Full-suite paired re-scoring (airline)\n",
    f"- 50 tasks run; **{sum(1 for t in trajs.values() if t.get('reward',0)>=1)} tau3 PASS / "
    f"{sum(1 for t in trajs.values() if t.get('reward',0)<1)} FAIL**",
    f"- **{len(lifted)}** tasks lifted; **{graded}** carry a grounded constraint and were paired re-scored",
    f"- **{len(flips)} flips** (tau3 PASS -> preflight FAIL): a stated requirement the DB grade missed\n",
    "| task | tau3 | preflight | | violated action(s) |",
    "|---|:--:|:--:|---|---|",
]
for tid, tau3, pf, mark, vios in rows:
    lines.append(f"| {tid} | {tau3} | {pf} | {mark} | {', '.join(sorted(set(vios))) or '—'} |")
lines.append("\n## Flips (the revealed-but-missed set)\n")
for tid, vios, violations in flips:
    lines.append(f"### task {tid}")
    for v in violations:
        lines.append(f"- `{v.action}` fired at turn {v.turn}; authorization DENIED — "
                     f"source: *\"{v.source_quote}\"*")
report = "\n".join(lines) + "\n"
open(os.path.join(ROOT, "poc/flip_report.md"), "w").write(report)
print(report)
