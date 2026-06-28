# Linear Setup

Linear is the visual cockpit for the MVP solo agentic workflow.

The browser is only for initial setup, login, and visual inspection. After setup, routine issue creation, comments, and status changes should use the Linear API helper documented in `docs/linear-api-usage.md`.

## MVP Goal

Linear should make it obvious:

- what is being shaped;
- what is ready for Codex;
- what Codex is working on;
- what is blocked;
- what is waiting for review;
- what is done.

## Team

Create one team:

```text
Name: DEV
Key: DEV
```

## Statuses

Use a small workflow:

```text
Inbox
Shaping
Ready for Codex
Codex Running
Blocked
Review
Done
Canceled
```

## Labels

Create a `Deliverable` label group:

```text
Planning
Spec
Implementation
Review
Research
Method
```

Create a `Repo` label group:

```text
Repo/legalrag3
```

## Views

Create these MVP views:

```text
Cockpit
  Status is not Done
  Status is not Canceled
  Group by Status
```

```text
Ready for Codex
  Status = Ready for Codex
  Repo = Repo/legalrag3
```

```text
Blocked
  Status = Blocked
  Repo = Repo/legalrag3
```

```text
Review
  Status = Review
  Repo = Repo/legalrag3
```

```text
Method Work
  Deliverable = Method
  Status is not Done
  Status is not Canceled
  Repo = Repo/legalrag3
```

## Issue Template: Implementation

```md
## Goal

## Context

## Linked OpenSpec change

Use "Not required" for small non-behavioral work.

## Acceptance criteria

## Expected files or areas

## Verification

## Done when

- Code or docs are updated.
- Relevant checks are run.
- OpenSpec status is recorded.
- PR or reviewable diff is ready, when GitHub is available.
```

## Issue Template: Method

```md
## Workflow issue

## Desired MVP behavior

## Affected artifacts

## Non-goals

## Verification

## Done when

- Method docs are updated.
- Production application behavior is unchanged.
- Relevant checks are run.
```

## Codex Delegation Comment

```text
@Codex work on this in legalrag3.

Use this Linear issue as the task scope.
Use OpenSpec only if the task affects medium/large behavior, architecture, API, data, or security concerns.
Keep the diff focused.
Update this issue with summary, files changed, checks run, OpenSpec status, PR link if available, and blockers.
```

## First Smoke Test

After Linear is configured, create one Method issue:

```text
Title: Verify MVP agentic workflow documentation
Deliverable: Method
Status: Ready for Codex
Repo: Repo/legalrag3
```

Acceptance criteria:

- `AGENTS.md` describes the MVP workflow.
- `docs/agentic-workspace.md`, `docs/linear-setup.md`, and `docs/openspec-usage.md` exist.
- OpenSpec is explicitly limited to medium/large behavior, architecture, API, data, and security changes.
- No production application behavior changes.
- Local documentation checks pass.

## API Handoff

After the MVP cockpit exists, configure `LINEAR_API_KEY` locally and verify:

```bash
python3 scripts/linear_cli.py whoami
```

Normal Codex work should use `scripts/linear_cli.py` rather than browser clicks for Linear issue reads, comments, and status changes.
