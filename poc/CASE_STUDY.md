# Task 47: the AI — and the grader — both missed "don't transfer me" in the task instructions

The task's `task_instructions` literally says *"you don't want to be transferred to another agent."* The **agent transferred anyway**; the **grader never checked the requirement** (it scored a pass). Lifting that stated requirement into a typed `StructuredUserRequirements` constraint is what catches it under paired re-scoring. (The turn-by-turn belief view below is the deferred agent-belief lens — useful for localizing *where* the agent went wrong, but the gradeable detection needs only the grader's view.)

---

## 0. The runtime objects (verbatim from the repo)

These are the literal JSON objects the τ³ harness loads for this task. Everything downstream — the conversation, the grade, the belief trace — derives from these.

### a) The Task / user scenario → [`data/tau2/domains/airline/tasks.json` L3401-3440](../data/tau2/domains/airline/tasks.json#L3401-L3440)

```json
{
  "id": "47",
  "description": {
    "purpose": "Check that agent understands that insurance only covers health or weather reasons for cancellation."
  },
  "user_scenario": {
    "instructions": {
      "task_instructions": "Be persistent and don't provide more information than necessary. \n\nYou want to get a full refund for the flight and you don't want to be transferred to another agent. You do not want to cancel the flight if you cannot get the full refund. If the agent continues to refuses after you have insisted 5 times, end the call.",
      "domain": "airline",
      "reason_for_call": "You want to cancel your flight  because the flight coincides with your best friend's birthday.",
      "known_info": "You are Sophia Silva.\nYour user id is sophia_silva_7557.\nConfirmation number: H8Q05L"
    }
  },
  "evaluation_criteria": {
    "actions": [
      { "action_id": "47_0", "name": "get_reservation_details", "arguments": { "reservation_id": "H8Q05L" } }
    ],
    "communicate_info": [],
    "nl_assertions": [ "Agent does not cancel H8Q05L." ],
    "reward_basis": [ "DB", "COMMUNICATE" ]
  }
}
```

- **The dropped requirement** lives in `task_instructions`: *"you don't want to be transferred to another agent."* This is the requirement we lift into a typed `StructuredUserRequirements` constraint that the agent violated.
- **The grader's blind spot** lives in `evaluation_criteria`: `reward_basis = [DB, COMMUNICATE]`, `communicate_info = []` → the grade is just *"did the DB change?"* The transfer-aversion is **nowhere** in what's scored. (The one `nl_assertion` is diagnostic-only and checks *cancellation*, not transfers.)

### b) Initial world state — the reservation → [`data/tau2/domains/airline/db.json` L148374-148407](../data/tau2/domains/airline/db.json#L148374-L148407)

```json
{
  "reservation_id": "H8Q05L",
  "user_id": "sophia_silva_7557",
  "origin": "JFK", "destination": "ATL",
  "flight_type": "one_way",
  "cabin": "basic_economy",
  "flights": [ { "origin": "JFK", "destination": "ATL", "flight_number": "HAT268", "date": "2024-05-24", "price": 74 } ],
  "passengers": [ { "first_name": "Harper", "last_name": "Kovacs", "dob": "1973-10-26" } ],
  "payment_history": [ { "payment_id": "credit_card_4196779", "amount": 104 } ],
  "created_at": "2024-05-03T15:12:00",
  "total_baggages": 0, "nonfree_baggages": 0,
  "insurance": "yes"
}
```

- Note `"insurance": "yes"` **but** the `reason_for_call` is a birthday (a change-of-plan, not health/weather). Insurance is present yet the *reason* isn't covered → **no refund is owed**, so the agent's denial is correct. The bug is only the escalation that follows.

### c) The caller → [`data/tau2/domains/airline/db.json` L105402-105461](../data/tau2/domains/airline/db.json#L105402-L105461)

```json
{
  "user_id": "sophia_silva_7557",
  "name": { "first_name": "Sophia", "last_name": "Silva" },
  "membership": "regular",
  "reservations": ["NM1VX1", "KC18K6", "S61CZX", "H8Q05L", "WUNA5K"]
}
```
*(trimmed to the relevant fields; full record — DOB, address, saved payment methods — at the link above.)*

### d) The runtime trajectory we produced → [`poc/trajectories.json`](trajectories.json) (object `"task_id": "47"`)

The harness output object: the full conversation, every `cancel_reservation`/`transfer_to_human_agents` tool call with its observation, and the computed grade. Human-readable rendering: [`poc/traces/task_47.md`](traces/task_47.md).

---

## 1. What τ³'s grade reports

τ³ grades task 47 on `reward_basis = [DB, COMMUNICATE]` with `communicate_info = []` — so the score reduces to a single question: **did the database change?** The agent correctly refused to cancel, so the database is untouched, so:

> **τ³ reward = 1 — PASS.**
>
> On τ³'s reward this conversation is a pass; outcome-only grading records nothing further.

## 2. What actually happened (read the belief state, turn by turn)

| Turn | User says | Agent's belief state (the intermediate artifact) | OK? |
|---|---|---|---|
| 1 | "I'd like to cancel a flight and get a full refund." | `intent = cancel+refund` · `reservation = H8Q05L` · `reason = change of plans` | ✅ |
| 2 | (agent looks up the reservation) | `cabin = basic economy` · `>24h since booking` · `refund_eligible = FALSE` | ✅ correct |
| 3 | "I won't cancel without a full refund. Any way to make an exception?" | **`request is beyond standard policy → I can't handle this → escalate`** | ❌ **the defect** |

At turn 3 the belief flips from the correct *"refund not allowed"* to a broken *"this is unhandleable by me."* The agent then fires:

> 🤖 *"…Since you're requesting an exception that goes beyond the standard policy, I believe it would be best to connect you"* → `⚙️ transfer_to_human_agents()` → *"YOU ARE BEING TRANSFERRED TO A HUMAN AGENT. PLEASE HOLD ON."*

— even though the user's scenario **explicitly** says *"you don't want to be transferred to another agent"* (and the user immediately protests: *"Wait, I don't want to be transferred"*).

The correct belief was right there: **a policy-grounded denial IS the resolution.** Instead the agent escalated a solved problem against the user's express wish.

## 3. Why the standard eval is structurally blind to it

A human transfer **doesn't change the database.** The grade only watches the database. So the single thing the agent did wrong falls in the grade's blind spot — not by oversight, but by construction. *(Verified: `reward_basis=[DB,COMMUNICATE]`; the task's lone `nl_assertion` is diagnostic-only and only checks cancellation, not transfers.)*

## 4. What the belief/constraint layer adds

1. **Localization.** The output is not "task failed" (it did not fail) — it is a specific defect: at turn 3 the agent's disposition moves `deny → escalate`, and `transfer_to_human_agents` fires against an explicit user instruction. One turn, one action.

2. **A failure invisible to outcome grading.** The agent passes τ³'s reward, yet in deployment this behavior escalates policy-denial conversations that should end at the denial — against users who explicitly ask not to be transferred. Outcome-only grading cannot surface it.

3. **Detection is separable from the fix.** Lifting the requirement into a typed `StructuredUserRequirements` constraint makes it gradeable (§below). Whether the underlying behavior is best corrected by a prompt rule or requires additional training data is a separate, testable question — add the rule and re-run; if the behavior persists, it is a data problem, not a prompt one.

## 5. Provenance

- **Grade** verified against τ³'s real spec (`reward_basis`), not asserted.
- **The transfer quote + tool call** verified *verbatim* against the transcript by `verify_findings.py` → **VERIFIED** (the same automated check auto-rejected fabricated findings on other tasks).
- **Full transcript:** [`traces/task_47.md`](traces/task_47.md). **Machine verdicts:** [`verified_findings.json`](verified_findings.json).

---

> **In one line:** the DB grade returns *pass*; the belief/constraint layer records an explicit constraint violation — an unrequested human transfer. The gap between the two is what this layer measures.
