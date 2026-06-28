# OpenSpec Usage

OpenSpec is the spec layer for this project only.

## Local Setup

OpenSpec is initialized in `openspec/`.

Current files:

- `openspec/config.yaml`
- `openspec/specs/`
- `openspec/changes/`
- `openspec/changes/archive/`

## When To Use OpenSpec

Use OpenSpec before implementation when a change affects:

- User-visible behavior.
- Public APIs or data contracts.
- Security, permissions, or privacy.
- Persistent data shape or migrations.
- Cross-module architecture.
- Any decision that should survive beyond one coding session.

Small documentation-only updates, typo fixes, and local workspace notes may be made without a new OpenSpec change.

## Simple Rules

- Keep each change focused on one outcome.
- Name changes with short kebab-case identifiers.
- Put proposed work under `openspec/changes/<change-id>/`.
- Update accepted project behavior under `openspec/specs/` only after the change is accepted or intentionally synced.
- Archive completed changes under `openspec/changes/archive/`.
- Keep specs project-local. Do not reuse this `openspec/` directory for sibling projects.

## Suggested Change Shape

A typical OpenSpec change should include:

- `proposal.md` for intent, scope, and non-goals.
- `tasks.md` for the implementation checklist.
- `specs/<capability>/spec.md` for requirement deltas when behavior changes.

## Agent Checklist

Before coding behavior changes:

- Confirm the request needs an OpenSpec change.
- Check existing specs and active changes for overlap.
- Create or update the relevant change.
- Keep implementation aligned with the accepted proposal.

Before handoff:

- State which OpenSpec files changed.
- State whether specs were synced or the change remains pending.
- Note any follow-up needed in Linear or GitHub.
