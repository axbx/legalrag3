# Agentic Workspace

This project is aligned to the MVP solo agentic workflow. The goal is a small, reliable loop for Linear-driven Codex Cloud work, with Codex Desktop available for local follow-up when needed.

## Current MVP

The repository currently contains the method layer and a small demo page:

- `AGENTS.md`
- `docs/agentic-workspace.md`
- `docs/linear-setup.md`
- `docs/linear-api-usage.md`
- `index.html`

## Roles

- Linear is the visual cockpit for work status, task scope, blockers, and review queues.
- Codex Cloud is the preferred execution path for work delegated from Linear through `@Codex`.
- Codex Desktop is the local workspace for inspection, editing, running checks, and preparing handoff notes when local work is explicitly needed.
- GitHub PRs and CI verify reviewable changes when repository remotes and checks are configured.

## Boundaries

All work for this project stays inside `/Users/albert/Projects/legalrag3`.

Agents must not inspect or modify sibling projects unless the user explicitly provides another target path.

Method-layer work may update `AGENTS.md`, files under `docs/`, helper scripts, and workflow notes. It must not change production application behavior unless the issue explicitly asks for an application change.

## Standard MVP Flow

1. Start from a clear user request or Linear issue.
2. For cloud delegation, comment in Linear with `@Codex` and explicitly name `axbx/legalrag3` when useful.
3. For local work, inspect this repository before editing.
4. Make the smallest reviewable change.
5. Run the most relevant checks available.
6. Hand off with summary, changed files, checks, Linear updates, GitHub/CI state, and blockers.

## Cloud Trigger

`Ready for Codex` is a queue signal, not an execution trigger by itself. Work starts when:

- a Linear issue is assigned to Codex; or
- a Linear comment mentions `@Codex`.

For this repository, prefer comments shaped like:

```text
@Codex implement this in axbx/legalrag3 on branch main.
Follow AGENTS.md. Keep the diff focused.
Open a PR when done, unless this is explicitly an inspection-only task.
```

## Phase 2 Out Of Scope

Do not add the following during the MVP setup:

- Living Spec generator.
- Gap markers or gap sync.
- Custom Codex skills.
- Drift reports.
- Extra automation scripts beyond the existing Linear helper.

These can be added later after the Linear -> Codex Cloud -> GitHub PR loop is stable.

## Handoff Expectations

At the end of a Codex run, report:

- what changed;
- which files changed;
- which checks ran;
- what Linear setup or issue updates still need a human;
- PR or CI status, when available;
- blockers and useful follow-ups.
