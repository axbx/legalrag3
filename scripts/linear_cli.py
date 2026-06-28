#!/usr/bin/env python3
"""Small Linear GraphQL helper for the MVP solo agentic workflow."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ENDPOINT = "https://api.linear.app/graphql"

ISSUE_FIELDS = """
id
identifier
title
description
url
state {
  id
  name
  type
}
labels {
  nodes {
    id
    name
  }
}
comments(first: 10) {
  nodes {
    id
    body
    createdAt
    user {
      name
    }
  }
}
"""


class LinearError(RuntimeError):
    pass


def graphql(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    token = os.environ.get("LINEAR_API_KEY")
    if not token:
        raise LinearError("LINEAR_API_KEY is not set")

    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={
            "Authorization": token,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise LinearError(f"Linear API HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise LinearError(f"Linear API request failed: {exc.reason}") from exc

    if body.get("errors"):
        messages = "; ".join(error.get("message", str(error)) for error in body["errors"])
        raise LinearError(messages)

    return body["data"]


def read_text(value: str | None, file_path: str | None) -> str:
    if value and file_path:
        raise LinearError("pass either inline text or a file path, not both")
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    return value or ""


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def get_viewer(_: argparse.Namespace) -> None:
    data = graphql(
        """
        query Viewer {
          viewer {
            id
            name
            email
          }
        }
        """
    )
    print_json(data["viewer"])


def get_team_by_key(team_key: str) -> dict[str, Any]:
    data = graphql(
        """
        query TeamByKey($key: String!) {
          teams(filter: { key: { eq: $key } }) {
            nodes {
              id
              key
              name
              states {
                nodes {
                  id
                  name
                  type
                }
              }
            }
          }
        }
        """,
        {"key": team_key},
    )
    teams = data["teams"]["nodes"]
    if not teams:
        raise LinearError(f"team not found: {team_key}")
    return teams[0]


def get_state_id(team: dict[str, Any], status_name: str | None) -> str | None:
    if not status_name:
        return None
    for state in team["states"]["nodes"]:
        if state["name"].lower() == status_name.lower():
            return state["id"]
    available = ", ".join(state["name"] for state in team["states"]["nodes"])
    raise LinearError(f"status not found for {team['key']}: {status_name}. Available: {available}")


def get_label_id(label_name: str) -> str:
    data = graphql(
        """
        query LabelByName($name: String!) {
          issueLabels(filter: { name: { eq: $name } }) {
            nodes {
              id
              name
            }
          }
        }
        """,
        {"name": label_name},
    )
    labels = data["issueLabels"]["nodes"]
    if not labels:
        raise LinearError(f"label not found: {label_name}")
    return labels[0]["id"]


def get_issue(identifier: str) -> dict[str, Any]:
    data = graphql(
        f"""
        query IssueById($id: String!) {{
          issue(id: $id) {{
            {ISSUE_FIELDS}
          }}
        }}
        """,
        {"id": identifier},
    )
    issue = data.get("issue")
    if issue:
        return issue

    match = re.fullmatch(r"([A-Z][A-Z0-9]*)-(\d+)", identifier)
    if not match:
        raise LinearError(f"issue not found: {identifier}")

    team_key, number = match.group(1), int(match.group(2))
    data = graphql(
        f"""
        query IssueByTeamNumber($teamKey: String!, $number: Float!) {{
          issues(
            first: 1
            filter: {{
              team: {{ key: {{ eq: $teamKey }} }}
              number: {{ eq: $number }}
            }}
          ) {{
            nodes {{
              {ISSUE_FIELDS}
            }}
          }}
        }}
        """,
        {"teamKey": team_key, "number": float(number)},
    )
    issues = data["issues"]["nodes"]
    if not issues:
        raise LinearError(f"issue not found: {identifier}")
    return issues[0]


def show_issue(args: argparse.Namespace) -> None:
    print_json(get_issue(args.issue))


def create_issue(args: argparse.Namespace) -> None:
    team = get_team_by_key(args.team)
    state_id = get_state_id(team, args.status)
    label_ids = [get_label_id(label) for label in args.label]
    description = read_text(args.description, args.description_file)

    input_data: dict[str, Any] = {
        "teamId": team["id"],
        "title": args.title,
        "description": description,
    }
    if state_id:
        input_data["stateId"] = state_id
    if label_ids:
        input_data["labelIds"] = label_ids

    data = graphql(
        f"""
        mutation IssueCreate($input: IssueCreateInput!) {{
          issueCreate(input: $input) {{
            success
            issue {{
              {ISSUE_FIELDS}
            }}
          }}
        }}
        """,
        {"input": input_data},
    )
    print_json(data["issueCreate"]["issue"])


def update_status(args: argparse.Namespace) -> None:
    issue = get_issue(args.issue)
    team_key = issue["identifier"].split("-", 1)[0]
    team = get_team_by_key(team_key)
    state_id = get_state_id(team, args.status)
    data = graphql(
        f"""
        mutation IssueUpdate($id: String!, $input: IssueUpdateInput!) {{
          issueUpdate(id: $id, input: $input) {{
            success
            issue {{
              {ISSUE_FIELDS}
            }}
          }}
        }}
        """,
        {"id": issue["id"], "input": {"stateId": state_id}},
    )
    print_json(data["issueUpdate"]["issue"])


def add_comment(args: argparse.Namespace) -> None:
    issue = get_issue(args.issue)
    body = read_text(args.body, args.body_file)
    if not body.strip():
        raise LinearError("comment body is empty")
    data = graphql(
        """
        mutation CommentCreate($input: CommentCreateInput!) {
          commentCreate(input: $input) {
            success
            comment {
              id
              url
              body
            }
          }
        }
        """,
        {"input": {"issueId": issue["id"], "body": body}},
    )
    print_json(data["commentCreate"]["comment"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Linear API helper for legalrag3")
    sub = parser.add_subparsers(dest="command", required=True)

    whoami = sub.add_parser("whoami", help="verify LINEAR_API_KEY")
    whoami.set_defaults(func=get_viewer)

    issue = sub.add_parser("issue", help="show one issue by identifier or UUID")
    issue.add_argument("issue")
    issue.set_defaults(func=show_issue)

    create = sub.add_parser("create", help="create an issue")
    create.add_argument("--team", default="DEV", help="Linear team key")
    create.add_argument("--title", required=True)
    create.add_argument("--description")
    create.add_argument("--description-file")
    create.add_argument("--status")
    create.add_argument("--label", action="append", default=[])
    create.set_defaults(func=create_issue)

    status = sub.add_parser("status", help="update issue status")
    status.add_argument("issue")
    status.add_argument("status")
    status.set_defaults(func=update_status)

    comment = sub.add_parser("comment", help="add an issue comment")
    comment.add_argument("issue")
    comment.add_argument("--body")
    comment.add_argument("--body-file")
    comment.set_defaults(func=add_comment)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except LinearError as exc:
        print(f"linear_cli: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
