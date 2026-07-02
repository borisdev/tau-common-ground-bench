# Framing & related work

A customer-service dialogue is *partially observable*: the user's objective is a **latent variable** the agent infers from partial, incrementally-revealed evidence. τ-bench applies **outcome supervision** (it scores the terminal state); this layer adds **process supervision over the belief state**.

## 1. The agent's belief converging to the hidden problem

The task is *partially observable*: the agent maintains a **belief state** — a posterior over a **latent variable** (the user's true objective) that it updates from partial, incrementally-revealed evidence.

- **Belief-state tracking under partial observability (POMDP).** The hidden problem is the latent state; the agent's estimate is the belief state. "Belief state" is also the term of art in **dialogue-state tracking (DST)** for task-oriented dialogue (Young et al.), so tracking a `ProblemSpecBelief` here is native, not a metaphor.
- **Assistance games / CIRL** (Hadfield-Menell & Russell). Names *why* task 47 fails: an agent uncertain about the human's objective should be deferential / information-gathering, not act decisively. Acting while the objective is `UNKNOWN` is the canonical assistance-game failure — acting under epistemic uncertainty instead of reducing it.
- **Grounding / common ground** (Clark). The dialogue-pragmatics term for two parties converging on shared understanding.
- **Theory of Mind / intent inference / user modeling.** Modeling the user's goal as a hidden mental state.
- **The convergence itself:** posterior contraction / concentration (Bayesian); identifiability (whether the truth can be recovered from the observations at all).

## 2. Decompose into structured parts; grade the process, not just the outcome

- **Process supervision vs. outcome supervision** — process reward models (PRM) vs. outcome reward models (ORM) (OpenAI, *Let's Verify Step by Step*). We propose a **PRM over the belief trajectory**: grade how well the agent extracted the truth, not only the terminal state.
- **The structure experts define:** semantic frames / slot filling / a domain ontology (dialogue systems). The "hydrated problem spec" is a filled semantic frame / grounded specification.
- **Structured prediction** — the `ProblemSpec` is a structured output, not a scalar.
- **Why structure makes the grader more accurate:** factored / decomposed evaluation and scalable oversight (Christiano's IDA, Irving's debate, Ought's factored cognition; Anthropic's scalable-oversight agenda). Decomposition raises inter-rater reliability — the reason rubric-based grading beats holistic scoring.

## Beyond AI

- **The Good Regulator theorem** (Conant & Ashby, 1970): *"Every good regulator of a system must be a model of that system."* To act well on a hidden problem you must model it — so to *grade* whether an agent will act well, grade its **model of the problem**, not just its final move.
- **Control theory:** state estimation / observer design / the separation principle (estimate the hidden state, then act) — task 47 violates it by acting before estimating.
- **Epistemology:** Bayesian convergence to truth; abduction (inference to the best explanation).

## The crux, in one sentence

Customer-service dialogue is a **partially observable assistance game**: the agent must **ground** a **latent objective** by tracking a **belief state** that should **converge** to the truth — so evaluate it with **process supervision over the belief trajectory**, against an **expert-authored ontology (semantic frame)**, which also makes the grader more reliable via **factored / decomposed evaluation**.
