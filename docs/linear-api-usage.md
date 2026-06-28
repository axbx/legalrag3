# Linear API Usage

Routine Linear updates should use the API helper, not the browser.

The browser is reserved for:

- first-time workspace setup;
- login and authorization flows;
- visual inspection of the cockpit;
- recovery when API access is unavailable.

## Setup

Create a personal Linear API key in Linear:

```text
Settings -> API -> Personal API keys
```

Store it only in your local `.env` file or expose it in your local shell:

```bash
cp .env.example .env
# then fill LINEAR_API_KEY in .env
```

or:

```bash
export LINEAR_API_KEY="lin_api_..."
```

Do not commit API keys. `.env` files are ignored by Git; `.env.example` is safe and contains no secret value.
`scripts/linear_cli.py` automatically reads `.env`.

Verify access:

```bash
python3 scripts/linear_cli.py whoami
```

## Common Commands

Show an issue:

```bash
python3 scripts/linear_cli.py issue DEV-2
```

Create a new implementation issue:

```bash
python3 scripts/linear_cli.py create \
  --team DEV \
  --title "Change Hello World subtitle" \
  --description-file /tmp/linear-issue.md \
  --status "Shaping" \
  --label "Implementation" \
  --label "Repo/legalrag3"
```

Move an issue through the workflow:

```bash
python3 scripts/linear_cli.py status DEV-2 "Codex Running"
python3 scripts/linear_cli.py status DEV-2 "Done"
```

Add a completion comment:

```bash
python3 scripts/linear_cli.py comment DEV-2 --body-file /tmp/linear-comment.md
```

## Agent Rule

For normal work, Codex should:

1. Read issue scope from Linear through `scripts/linear_cli.py`.
2. Move the issue to `Codex Running` while working.
3. Post a completion comment with summary, checks, OpenSpec status, GitHub state, and blockers.
4. Move the issue to `Done`, `Review`, or `Blocked`.

If `LINEAR_API_KEY` is missing, Codex should stop and ask the human to configure it rather than silently falling back to browser automation for routine work.
