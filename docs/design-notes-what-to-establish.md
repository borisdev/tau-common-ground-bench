# Design notes: what a preflight check must establish

> **Working notes — capture, not doctrine.** These bank the conceptual model behind the preflight checklist so nothing is lost. To be pruned and refined later; nothing here is load-bearing yet.

## Two senses of "epistemic" — don't conflate them

- **Epistemic precondition (agent-side — our mechanism; Moore 1985).** The *agent* must *know* X before acting. Ontic (DB-queryable) vs. epistemic (must **probe the user**). Keep this term for the mechanism.
- **User's epistemic state (user-side).** What the *user* knows / understands / believes. This is a **component of the user**, not the mechanism.

Using "epistemic" for both invites confusion. Reserve **"epistemic precondition"** for the agent-side rule; when talking about the *user's* understanding, say **"understanding"** or **"informed consent."**

## What the agent must establish — the four content types

The thing the agent must know (the X) is one of a few kinds — worth naming so the term does real work:

- **Requirement / goal** — the outcome the user needs (*arrive before 6pm*).
- **Preference** — what they'd rather have (*window seat, nonstop*).
- **Understanding** *(the user's epistemic state)* — does the user grasp a material consequence? (*changing the flight forfeits the fare*).
- **Consent / authorization** — what the user explicitly approved (*yes, cancel it*; *yes, charge this card*).

Umbrella = **the agent's model of the user** (goals · preferences · understanding · consent) — *not* "epistemic state," which is only the *understanding* slice. Task 47 = **consent**. The fare-forfeit case = **understanding**.

## Understanding = a bounded slice of causal-model alignment

The "understanding" check reaches toward a deep idea: does the user's implicit **causal model** of the action match reality?

- User's causal model: *"change flight → I get a new flight."*
- Actual causal model: *"change flight → new flight **and** fare forfeited **and** return leg dropped."*
- The gap between them is what the agent must close (by disclosing) **before** committing.

That's potentially **unbounded** (you can't model a user's whole causal understanding of the world). Two disciplines keep it tractable — the same moves that bound everything else here:

1. **Per-action, not global.** Check *"before `change_flight`, is consequence Z established,"* never *"is the user's causal model correct."*
2. **Grade the disclosure, not the mind.** Understanding is unobservable, so grade the agent's **observable** act — *did it state the fare-forfeit and get acknowledgment?* — as the checkable **proxy**. Exactly how consent grades the explicit "yes," not the mental state. So "understanding" rows are no less gradeable than consent rows; they just check a disclosure step.
3. **Failure patterns bound the scope.** Enumerate the consequences that actually cause harm/failures (Pattern B) or that an expert flags as material (Pattern A) — not every possible misunderstanding.

**Paper stance:** the framework *reaches* causal-model alignment but *bounds* it. Don't claim to solve it (the pilot demonstrates **consent**, task 47); claim **informed consent** as a bounded, gradeable slice. Lead with crisp consent/scope checks; treat understanding as the harder, sophisticated second tier.

## The SME elicitation pipeline (Phase 2)

For one **bounded action**, ask the subject-matter expert:

> *"Before the agent fires **this** action, what must it verify about the user — their goal, preferences, understanding, and consent — **so the user isn't harmed?**"*

Why this design works:

- **Bounded action** keeps it answerable — not "how should agents behave in general" (unbounded), but "before *this tool call*, what must be true" (finite, concrete).
- **The harm anchor** (*"so we don't hurt the user"*) does triple duty: **anti-circularity** (a check earns its place by the harm it prevents, not by being invented), **prioritization** (author high-harm checks first), and it yields the *"example failure caught"* column for free.
- **SME prose → LLM → checklist.** SMEs carry tacit domain knowledge but shouldn't hand-write predicates; an LLM converts their prose into `belief.X == True` predicates. This mirrors the task-47 move (prose `task_instructions` → checkable `StructuredUserRequirements`), just sourced from an expert instead of a task.
- **Verification loop.** Don't trust the LLM's structuring — verify the generated checklist faithfully captures the SME's intent (same rigor as `poc/verify_findings.py`).
- **Anchor to the domain policy.** Prefer checks traceable to the airline policy document the agent is already given, over invented ones (keeps Pattern A honest).

## The product framing

Not merely a benchmark: an **expert-authored preflight policy pack**, usable across surfaces from one artifact —

- **Evaluation** (grade whether the agent ran the check),
- **Runtime gating** (halt-and-ask before firing),
- **Monitoring** (flag deployed agents that skip a check),
- and — *carefully* — **training signal** (keep the RL framing at arm's length; the pack can supply supervision, but that's downstream).
