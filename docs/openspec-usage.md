# OpenSpec Usage

OpenSpec is the project-local spec layer for `legalrag3`. In the MVP workflow, it is used selectively, not as a gate for every small edit.

## Local Setup

OpenSpec is initialized in `openspec/`.

Expected structure:

- `openspec/config.yaml`
- `openspec/specs/`
- `openspec/changes/`
- `openspec/changes/archive/`

## When To Use OpenSpec

Create or update an OpenSpec change before implementation when the work is medium or large and affects:

- user-visible behavior;
- architecture or cross-module design;
- public APIs, data contracts, or integrations;
- persistent data shape, migrations, or storage semantics;
- security, permissions, privacy, or compliance-sensitive behavior;
- a product or technical decision that should be visible after the coding session ends.

## When OpenSpec Is Not Required

Do not create an OpenSpec change for:

- small documentation-only updates;
- local workflow or setup notes;
- typo fixes;
- narrow refactors that preserve behavior;
- test-only changes that do not redefine expected behavior;
- repository cleanup that does not affect application behavior.

The user may still explicitly request an OpenSpec change for any task.

## Change Shape

Use one short kebab-case change ID per outcome:

```text
openspec/changes/<change-id>/
  proposal.md
  tasks.md
  specs/<capability>/spec.md
```

Add `design.md` only when the design tradeoffs are large enough to justify it.

## Simple Rules

- Keep each OpenSpec change focused on one outcome.
- Check existing specs and active changes before adding a new change.
- Keep project specs under `openspec/specs/`.
- Keep proposed changes under `openspec/changes/`.
- Archive completed changes under `openspec/changes/archive/`.
- Do not use this OpenSpec tree for sibling projects.

## Agent Checklist

Before implementation:

- Decide whether the task crosses the OpenSpec threshold.
- If yes, create or update the relevant OpenSpec change.
- If no, state that OpenSpec was intentionally left unchanged.

Before handoff:

- State which OpenSpec files changed.
- State whether the change is active, synced, archived, or intentionally absent.
- Run `openspec validate --strict` when the OpenSpec CLI is available and OpenSpec artifacts changed.
- If validation cannot run, state the blocker clearly.
