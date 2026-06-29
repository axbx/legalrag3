# Agent Guide

This repository uses the MVP solo agentic workflow with Linear, Codex Cloud, Codex Desktop, and GitHub.

## Scope

- Work only inside `/Users/albert/Projects/legalrag3`.
- Do not inspect, edit, rename, clean, or otherwise modify sibling projects.
- Treat this repository as the complete project boundary unless the user explicitly provides another path.
- Do not change production application behavior as part of workspace setup or documentation work.

## Operating Model

- Linear is the cockpit for tasks, statuses, blockers, and review queues.
- Codex Cloud is the preferred execution path for issue-driven implementation through Linear `@Codex`.
- Codex Desktop is the local workspace for inspection, edits, checks, and handoff when local work is explicitly needed.
- GitHub pull requests and CI are the verification layer when repository remotes and checks are available.

## Working Rules

- Inspect the existing project before editing.
- Prefer small, reviewable diffs.
- Keep method/workflow changes separate from application behavior changes.
- Preserve user changes already present in the workspace.
- Run the most relevant local checks available before handing work back.
- Use `scripts/linear_cli.py` for routine Linear reads, comments, and status changes when `LINEAR_API_KEY` is configured.
- Use the browser for Linear only during initial setup, login/authorization, visual inspection, or API-access recovery.
- For cloud work, trigger Codex from Linear with `@Codex` and explicitly name `axbx/legalrag3` when the repository might be ambiguous.
- State clearly when GitHub, CI, Linear, or Codex Cloud verification cannot be completed.

## Completion Handoff

Every task should end with:

- Summary.
- Files changed.
- Checks run.
- Linear updates still required, if any.
- PR or CI status, if available.
- Blockers or follow-ups.
