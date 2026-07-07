# Multi-option discernment — the Pareto frontier of non-stupid choices

*A research note extending τ-discernment from grading a **single** action to selecting among **competing
alternatives**. Same three objectives; a second shape of "golden discernment."*

## Where this fits

The bench grades a single consequential decision — *proceed / ask / verify / warn / escalate / refuse* —
against a **harm-vs-hassle** matrix, on the three objectives it already names: **maximize effectiveness,
minimize harm, minimize hassle.** Many real decisions are a different shape: **choose among competing
alternatives** (which drug, diet, procedure, remediation). This note keeps the three objectives and adds
the structure for the *selection* case — the **Pareto frontier**.

> **Dominated options are the stupid options** — worse somewhere, better nowhere.
> **Frontier options are the non-stupid options** — each keeps a meaningful advantage.
> **Discernment chooses among the non-stupid options** (SME judgment · user preference · n-of-1 trial).

So the golden label for a selection decision is **not one answer** — it is *the frontier + the rationale
for what remains ambiguous.* That is a richer supervision signal than a single "right choice," and it
localizes disagreement to exactly the trade-offs that are genuinely contestable.

## Pipeline

```
candidate options
  → feasibility filter   — explicit + context-dependent, WITH reasons (not a silent binary)
  → score each objective — effectiveness · harm · hassle, WITH confidence + evidence
  → dominance filter     — prune only ROBUSTLY-dominated options
  → Pareto frontier      — the non-stupid set
  → discernment          — human weighs the frontier; residual ambiguity = the experiment signal
```

## Why naive pruning is wrong for medicine (the part to be skeptical about)

The Pareto math is five lines; the **scoring is 100% of the work and the risk.** A clean pipeline can
manufacture false confidence. Three amendments keep it honest:

1. **Uncertainty-aware dominance.** Scores are synthesized from heterogeneous evidence (RCT vs anecdote)
   and personalized guesses. An option "dominated" on *point estimates* may not be dominated once the
   confidence intervals are carried. Prune only when dominance survives uncertainty; otherwise keep it,
   flagged low-confidence. Discarding live options on soft numbers is the main failure mode.
2. **Option value / sequencing.** A gentler option (lower effectiveness, lower harm, lower hassle) is
   often *dominated on the static board* yet is the right **reversible / cheap / diagnostic first move.**
   Pruning it kills the very n-of-1 experiment discernment should surface. A dominated option **survives**
   if it has option value.
3. **Feasibility is graded, not binary.** Cost, access, contraindication, "how big a step" — often the
   real driver. Record *why*, don't silently drop.

And a modeling rule: **never collapse the objectives into one weighted utility.** That pre-commits the
weights and destroys the frontier — the whole point is that you *don't* pick weights; the human does.
Keep the vector; a per-option **scoring dossier** (evidence + context + confidence behind each axis)
is what makes a prune *auditable*.

## A temporal wrinkle worth a scenario

Effectiveness can be **conditional on continuation**. A GLP-1 for weight loss scores high on *immediate*
effectiveness and low on *durable* effectiveness (stop the drug → weight returns). The current medicine
rows treat effectiveness as static; splitting it into **immediate vs durable** is a small change that
exposes a large class of real trade-offs (chronic-therapy dependence vs one-time or habit-forming
alternatives).

## Worked sketch — "durable weight loss," one patient

| Option | Effectiveness | Harm↓ | Hassle↓ | Verdict |
|---|:--:|:--:|:--:|---|
| semaglutide / tirzepatide | **5** (high immediate, low *durable* — regain on stop) | 3 | 3 | frontier — most effective *while on it* |
| ketogenic diet | 3 | 4 | 2 | frontier — safer; **reversible/cheap first trial** (option value) |
| resistance training + protein | 3 | 5 | 2 | frontier — safest; **diagnostic of effort tolerance** |
| bariatric surgery | 5 (most durable) | 2 | 4 | **feasibility-gated** — big, needs eligibility |
| very-low-calorie crash diet | 2 | 2 | 2 | **dominated** — worse everywhere = the stupid option |

The frontier keeps a real tension (drug efficacy vs reversible, safer lifestyle options); the crash diet
is pruned; bariatric is bracketed as a separate feasibility conversation. *Golden discernment = that
frontier + "which to try first depends on the patient's side-effect tolerance and durability goal" —
an explicit n-of-1 signal, not a single decree.*

## Belief tracking is still the enabling layer

Every score here is *in this person's context* — their tolerance, routine, fears, durability goal. That
context is exactly the **belief state** the bench already reconstructs per turn. Multi-option discernment
is a consumer of belief tracking, not a competitor to it: the frontier is only as good as the belief
about the user that personalizes each axis.

---

*Applied context: this frame drives the "weigh your options" artifact in a clinical-evidence-audit
workflow (alongside a flagged-claims table and a causal diagram). Feedback / corrections welcome.*
