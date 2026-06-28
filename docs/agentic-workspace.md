# Agentic Workspace

This project is aligned to the MVP solo agentic workflow. The goal is a small, reliable loop for local agent work before introducing Living Spec, gap tracking, custom skills, or drift reports.

## Current MVP

The repository currently contains the method layer and an initialized OpenSpec directory:

- `AGENTS.md`
- `docs/agentic-workspace.md`
- `docs/linear-setup.md`
- `docs/openspec-usage.md`
- `openspec/config.yaml`
- `openspec/specs/`
- `openspec/changes/`
- `openspec/changes/archive/`

## Roles

- Codex Desktop is the local workspace for inspection, editing, running checks, and preparing handoff notes.
- Linear is the planned visual cockpit for work status, task scope, blockers, and review queues.
- OpenSpec records intent for medium or large behavior, architecture, API, data, and security changes.
- GitHub PRs and CI verify reviewable changes when repository remotes and checks are configured.

## Boundaries

All work for this project stays inside `/Users/albert/Projects/legalrag3`.

Agents must not inspect or modify sibling projects unless the user explicitly provides another target path.

Method-layer work may update `AGENTS.md`, files under `docs/`, and existing OpenSpec setup/configuration documentation. It must not change production application behavior.

## Standard MVP Flow

1. Start from a clear user request or a future Linear issue.
2. Inspect this repository before editing.
3. Decide whether OpenSpec is required.
4. If OpenSpec is required, create or update one focused OpenSpec change before implementation.
5. Make the smallest reviewable change.
6. Run the most relevant local checks available.
7. Hand off with summary, changed files, checks, OpenSpec status, Linear updates, and blockers.

## OpenSpec Threshold

OpenSpec is required for medium or large changes that affect behavior, architecture, APIs, data shape, migrations, security, permissions, privacy, or other decisions that should survive beyond one coding session.

OpenSpec is not required for small documentation-only edits, local workflow notes, typo fixes, or narrow non-behavioral maintenance unless the user asks for it.

## Phase 2 Out Of Scope

Do not add the following during the MVP setup:

- Living Spec generator.
- Gap markers or gap sync.
- Custom Codex skills.
- Spec drift reports.
- Linear automation scripts.

These can be added later after the Linear -> Codex -> PR review loop has been smoke-tested.

## Handoff Expectations

At the end of a Codex run, report:

- what changed;
- which files changed;
- which checks ran;
- whether OpenSpec artifacts changed or were intentionally left unchanged;
- what Linear setup or issue updates still need a human;
- blockers and useful follow-ups.
