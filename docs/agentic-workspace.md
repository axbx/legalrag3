# Agentic Workspace

This project is set up for solo agentic development with Codex Desktop as the local workspace, Linear as the planning cockpit, OpenSpec as the specification layer, and GitHub PR/CI as the verification layer.

## Boundaries

All agent work for this project must stay inside `/Users/albert/Projects/legalrag3`.

Sibling projects in the parent Codex Desktop projects directory are out of scope. Agents should not inspect or modify them unless the user explicitly asks and gives the target path.

## Roles

- Linear tracks visible work, status, priorities, and follow-up decisions.
- OpenSpec records proposed and accepted behavior for this project.
- Codex Desktop performs local inspection, edits, test runs, and review preparation.
- GitHub pull requests collect reviewable diffs and CI results when the project has Git metadata and a configured remote.

## Standard Flow

1. Start from a Linear issue or a clear user request.
2. Inspect this project locally before changing files.
3. If behavior or requirements are changing, create or update an OpenSpec change first.
4. Implement the smallest scoped change that satisfies the request.
5. Run available local checks.
6. Prepare a reviewable diff for GitHub PR review and CI.
7. Update Linear with outcome, blockers, and links to the spec or PR when available.

## Current Repository State

OpenSpec is initialized in `openspec/` with `openspec/config.yaml`.

At bootstrap time, this folder does not expose Git metadata to local commands, so GitHub PR and CI verification cannot be performed directly from this workspace until Git setup is available here.

## Agent Expectations

- Keep changes small and easy to review.
- Do not mix workflow documentation with production behavior changes.
- Do not create cross-project dependencies without explicit approval.
- Document missing setup instead of assuming external services are already connected.
- Report verification gaps clearly.
