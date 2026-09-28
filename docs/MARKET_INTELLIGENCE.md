# NightShift Market Intelligence Scan

This document captures the final cross-community scan across GitHub issues/discussions, Reddit, developer social channels, product reviews, and competitor direction.

## Strongest market signal

Developers are not mainly asking for "smarter code generation."

They are asking for:

- Less babysitting
- Better repository navigation
- Tighter scope control
- Transparent cost
- Reliable sandboxes
- Proof that a fix actually works
- Fewer noisy/unrelated changes

That reinforces NightShift's wedge:

> **Verified autonomous maintenance, not generic autonomous coding.**

## Product insights

### Existing tests should outrank agent-generated tests
An agent must not define its own success criteria.

Verification trust order:

1. Pre-existing tests
2. Independent generated tests
3. Agent-authored tests
4. No deterministic verification = failure

### Repository Intelligence must be a core subsystem
Agents waste context by dumping large files, repeatedly searching the same directories, and retaining stale context.

NightShift should expose agent-native repository operations such as:

- Symbol lookup
- Targeted file slices
- Caller/callee relationships
- Test relationships
- Recent git changes
- Dependency neighbors
- Architecture map

### Agent-native CLI compression is a product opportunity
Raw tool output is often too noisy for agents.

NightShift should normalize outputs from:

- pytest
- Jest/Vitest
- Git
- GitHub Actions
- Docker
- linters
- typecheckers
- logs

Example:

```text
TEST RESULT
137 passed
3 failed

FAILURES
1. checkout.test.ts::expired_card
   payment.ts:184
   checkout.ts:91
```

instead of streaming thousands of irrelevant lines into model context.

### Failure classification must happen before repair
Do not assume every CI failure requires editing application code.

Classify first:

```text
CI FAILED
├── Application bug      -> Repair Agent
├── Test bug             -> Test Repair Agent
├── Flaky test           -> Flake Analyzer
├── Dependency change    -> Dependency Agent
├── Infrastructure       -> Do not edit app code
└── Unknown              -> Escalate
```

This prevents production code being modified to satisfy a broken test.

### Mission scope beats "fix everything"
If the mission is "fix checkout regression", NightShift stops when that regression is verified fixed.

Unrelated findings go into a separate queue.

### Minimal patches are a trust feature
For equal verified outcomes, fewer changed lines/files are better.

A useful internal metric:

```text
repair efficiency = verified problem resolution / change surface
```

### Visible trust boundaries
Every mission should display both allowed scope and actual behavior.

Before:

```text
Allowed: src/payments/**, tests/payments/**
Forbidden: .github/**, infra/**, .env*, migrations/**
Dependency install: NO
Network writes: NO
Max changed files: 5
```

After:

```text
Files changed: 2 / 5
Forbidden paths touched: 0
Dependencies changed: 0
Secrets accessed: 0
Boundary status: PASS
```

### Transparent economics
Do not hide usage behind vague "unlimited" plans.

Show:

- Included missions
- Current usage
- Estimated mission cost
- Model-provider cost
- NightShift fee
- Hard spending cap

### Multi-provider is mandatory
The orchestration and verification layer is the product, not one model.

Target providers:

- OpenAI-compatible APIs
- Anthropic
- Gemini
- OpenRouter
- Ollama/local
- Future custom providers

Use role-specific routing later:

- Scout -> cheap model
- Repair -> strong coding model
- Reviewer -> independent model
- Classifier -> small model

## Sticky product direction: Maintenance Inbox

Longer-term retention can come from consolidating maintenance signals:

```text
HIGH   CI failure          Repair ready
MED    Dependency CVE      Migration available
MED    Flaky test          7 failures / 200 runs
LOW    Migration warning   No action required
```

Actions:

- Fix
- Investigate
- Ignore
- Schedule

## Organic distribution opportunity

Useful public GitHub artifacts can become acquisition:

```text
nightshift-bot:

Root cause identified.

Attempt #1
FAILED — rolled back.

Attempt #2
PASS

Evidence:
✓ tests
✓ typecheck
✓ lint

Draft PR opened.
```

Public open-source users can discover NightShift inside the workflow itself.

## Product moat

The moat is not model access.

It is accumulated repository-specific maintenance intelligence:

- Repository understanding
- Failure -> cause -> fix history
- Verification strategies
- Risk boundaries
- Failed approaches
- Known fragile modules

A NightShift instance that has maintained a repository for months should outperform a fresh generic coding agent on that repository.

## V1 requirements frozen by the scan

1. Failure classification before repair
2. Reproduce before edit
3. Transactional snapshot and rollback
4. Mission/path/command boundaries
5. Minimal-patch preference
6. Existing-tests-first verification
7. Independent reviewer
8. Structured evidence report
9. Provider abstraction / BYOK
10. Transparent cost accounting
11. Agent-native compressed repo/CLI retrieval
12. Failure memory
13. Draft PR only
14. Optional findings stay separate
15. Clean sandbox execution

## Explicitly not v1

- Autonomous merges
- Autonomous production deployment
- Giant agent swarms
- Complex billing
- Enterprise governance suite
- Many Git providers
- Elaborate dashboards
- "Fix everything" mode

## Final product statement

**NightShift automatically investigates failed software, produces the smallest verified repair it can prove, and leaves you a PR — not a mess.**
