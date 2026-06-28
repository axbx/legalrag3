# Agent Guide

This repository uses the MVP solo agentic workflow for Codex Desktop.

## Scope

- Work only inside `/Users/albert/Projects/legalrag3`.
- Do not inspect, edit, rename, clean, or otherwise modify sibling projects.
- Treat this repository as the complete project boundary unless the user explicitly provides another path.
- Do not change production application behavior as part of workspace setup or documentation work.

## Operating Model

- Codex Desktop is the local workspace for inspection, edits, checks, and handoff.
- Linear is the cockpit for tasks, statuses, blockers, and review queues.
- OpenSpec is the local spec layer for this project only.
- GitHub pull requests and CI are the verification layer when repository remotes and checks are available.

## OpenSpec Gate

Use OpenSpec before implementation only for medium or large changes that affect:

- user-visible behavior;
- architecture or cross-module design;
- public APIs, data contracts, or integrations;
- persistent data, migrations, or storage shape;
- security, permissions, privacy, or compliance-sensitive behavior.

Do not create an OpenSpec change for small documentation edits, local workflow notes, typo fixes, or narrow implementation work that does not change behavior unless the user asks for one.

## Working Rules

- Inspect the existing project before editing.
- Prefer small, reviewable diffs.
- Keep method/workflow changes separate from application behavior changes.
- Preserve user changes already present in the workspace.
- Run the most relevant local checks available before handing work back.
- Use `scripts/linear_cli.py` for routine Linear reads, comments, and status changes when `LINEAR_API_KEY` is configured.
- Use the browser for Linear only during initial setup, login/authorization, visual inspection, or API-access recovery.
- State clearly when GitHub, CI, Linear, or OpenSpec validation cannot be verified locally.

## Completion Handoff

Every task should end with:

- Summary.
- Files changed.
- Checks run.
- OpenSpec status.
- Linear updates still required, if any.
- PR or CI status, if available.
- Blockers or follow-ups.
