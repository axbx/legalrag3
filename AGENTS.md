# Agent Guide

This project is configured for solo agentic development inside Codex Desktop.

## Scope

- Work only inside `/Users/albert/Projects/legalrag3`.
- Do not read from, write to, rename, clean, or otherwise modify sibling projects.
- Treat this repository as the complete project boundary unless the user explicitly provides another path.
- Do not change production application behavior as part of workspace setup or documentation work.

## Project Workflow

- Linear is the visual cockpit for planning and tracking work.
- OpenSpec is the local spec layer for this project only.
- GitHub pull requests and CI are the verification layer when Git metadata and remotes are available.
- Codex Desktop is the local agent workspace for inspection, editing, and verification.

## OpenSpec

- OpenSpec is initialized in `openspec/`.
- Use `openspec/changes/` for proposed changes before implementation.
- Use `openspec/specs/` for accepted project capabilities and requirements.
- Keep OpenSpec artifacts focused on this project. Do not share specs across sibling projects.

## Working Rules

- Inspect the existing project before editing.
- Prefer small, reviewable diffs.
- Separate specification changes from implementation changes when possible.
- Keep documentation and workflow bootstrap changes separate from app behavior changes.
- Preserve user changes already present in the workspace.
- Run the most relevant local checks available before handing work back.

## Review Handoff

When finishing a task, report:

- What changed.
- Whether OpenSpec artifacts were added, updated, or intentionally left unchanged.
- What verification was run.
- Any missing setup that prevents GitHub PR or CI verification.
