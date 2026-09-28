# NightShift Traction Gauntlet

This document captures the first competitive/product pressure test and acts as a hard gate for future features.

## Positioning

NightShift is **not another coding agent**.

NightShift is the autonomous maintenance layer that wakes up when a repository fails, investigates the incident, produces the smallest repair it can verify, and leaves a reviewable PR with evidence.

## Primary customer wedge

Start with:

- Solo developers
- Small SaaS teams
- Agencies maintaining multiple client repositories
- Technical founders with limited maintenance bandwidth

Do **not** start enterprise-first. Enterprise platforms already compete aggressively on governance and broad developer-platform automation.

## Core pain we are solving

The enemy is not only competing AI tools. It is also:

> "I'll just fix it myself in ten minutes."

NightShift must consistently reduce **human supervision per verified repair**.

## Repeated market complaints

### 1. Babysitting
Coding agents often require constant supervision, repeated prompting, and diff inspection.

**Requirement:** optimize for unattended progress, not token output.

### 2. Technical-debt generation
Agents can make broad changes, shallow tests, or architecturally poor fixes that appear productive.

**Requirement:** prefer minimal patches and existing-test verification.

### 3. Scope violations
Autonomous agents can touch unrelated files, configuration, workflows, or dependencies.

**Requirement:** every mission has explicit path, command, dependency, network, and file-count boundaries.

### 4. Sandbox reliability
An autonomous maintenance product cannot itself be unreliable.

**Requirement:** clean-room sandbox checks and deterministic startup health tests.

### 5. False positives and noisy output
Review tools already struggle with excessive suggestions and low-value findings.

**Requirement:** mission-scoped repairs. Unrelated findings are recorded separately and never mixed into the requested fix.

### 6. Pricing and rate-limit resentment
Opaque throttling and surprise usage destroy trust.

**Requirement:** visible per-mission cost, usage counters, hard spending caps, and BYOK support.

### 7. Provider brittleness
Model/API changes can break product behavior.

**Requirement:** provider-neutral model abstraction.

## NightShift product constitution

1. PR-only by default.
2. Snapshot before mutation.
3. Failed repair => automatic rollback.
4. Mission boundaries are explicit and enforceable.
5. Evidence outranks model confidence.
6. BYOK and multiple model providers.
7. Failed strategies are remembered.
8. Repository memory is inspectable and deletable.
9. Every release passes a clean-room repair benchmark.
10. Every modification is explainable.
11. Onboarding must reach first useful result quickly.
12. Benchmarks measure repair quality continuously.
13. Minimal patch size is preferred.
14. High-risk files require stronger approval.
15. No autonomous production deployment in v1.

## Success metrics

Primary:

- Human minutes per verified repair
- Verified repair rate
- Regression-free repair rate
- Rollback success rate
- Median mission cost
- Median mission duration
- Mean files/lines changed per successful repair

Secondary:

- User intervention count
- False-positive rate
- Mission-boundary violations
- Repeat-failure reduction from memory

## Kill-test questions for every new feature

- Does a competitor already do this well?
- Does it reduce supervision?
- Does it increase trust?
- Does it improve verified outcomes?
- Can it introduce dangerous scope expansion?
- Can it increase surprise cost?
- Can the user understand why it acted?
- Would we pay for this ourselves?
