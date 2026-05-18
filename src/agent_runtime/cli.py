"""Command-line entrypoint for the backend-neutral research runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib import request as urlrequest

from .service import serve


DEFAULT_BASE_URL = "http://127.0.0.1:8765"


def _file_payload(path: Path) -> dict[str, str]:
    return {"name": path.name, "content": path.read_text(encoding="utf-8")}


def _post_json(base_url: str, path: str, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urlrequest.Request(
        f"{base_url.rstrip('/')}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlrequest.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def _get_json(base_url: str, path: str) -> dict:
    with urlrequest.urlopen(f"{base_url.rstrip('/')}{path}") as response:
        return json.loads(response.read().decode("utf-8"))


def _print_payload(payload: dict, *, output_json: bool) -> None:
    if output_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False))


def _add_client_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--json", dest="output_json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Research runtime service.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="Serve the research runtime HTTP API.")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.add_argument("--runtime-root", type=Path, default=Path.cwd() / ".research-runtime")
    serve_parser.add_argument("--max-concurrency", type=int, default=None)

    create_parser = subparsers.add_parser("create", help="Create a research project and start its first run.")
    _add_client_options(create_parser)
    create_parser.add_argument("--problem-file", type=Path, required=True)
    create_parser.add_argument("--title", default=None)
    create_parser.add_argument("--instruction", dest="instructions", type=Path, action="append", default=[])
    create_parser.add_argument("--reference", dest="references", type=Path, action="append", default=[])
    create_parser.add_argument("--model", default=None)
    create_parser.add_argument("--reasoning-effort", default=None)
    create_parser.add_argument("--no-verification", dest="verification", action="store_false", default=True)

    continue_parser = subparsers.add_parser("continue", help="Continue an existing research project.")
    _add_client_options(continue_parser)
    continue_parser.add_argument("project_id")
    continue_parser.add_argument("--prompt", required=True)
    continue_parser.add_argument("--instruction", dest="instructions", type=Path, action="append", default=[])
    continue_parser.add_argument("--reference", dest="references", type=Path, action="append", default=[])
    continue_parser.add_argument("--model", default=None)
    continue_parser.add_argument("--reasoning-effort", default=None)
    continue_parser.add_argument("--no-verification", dest="verification", action="store_false", default=None)

    status_parser = subparsers.add_parser("status", help="Fetch run status.")
    _add_client_options(status_parser)
    status_parser.add_argument("run_id")

    artifacts_parser = subparsers.add_parser("artifacts", help="Fetch run artifacts.")
    _add_client_options(artifacts_parser)
    artifacts_parser.add_argument("run_id")

    events_parser = subparsers.add_parser("events", help="Fetch run events.")
    _add_client_options(events_parser)
    events_parser.add_argument("run_id")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "serve":
        serve(runtime_root=args.runtime_root, host=args.host, port=args.port, max_concurrency=args.max_concurrency)
        return 0
    if args.command == "create":
        payload = {
            "title": args.title,
            "problem": {"format": "markdown", "content": args.problem_file.read_text(encoding="utf-8")},
            "instructions": [_file_payload(path) for path in args.instructions],
            "references": [_file_payload(path) for path in args.references],
            "execution": {
                "verification": args.verification,
                "model": args.model,
                "reasoning_effort": args.reasoning_effort,
            },
        }
        _print_payload(_post_json(args.base_url, "/v1/projects", payload), output_json=args.output_json)
        return 0
    if args.command == "continue":
        execution = None
        if args.verification is not None or args.model or args.reasoning_effort:
            execution = {
                "verification": True if args.verification is None else args.verification,
                "model": args.model,
                "reasoning_effort": args.reasoning_effort,
            }
        payload = {
            "prompt": args.prompt,
            "instructions": [_file_payload(path) for path in args.instructions],
            "references": [_file_payload(path) for path in args.references],
            "execution": execution,
        }
        _print_payload(
            _post_json(args.base_url, f"/v1/projects/{args.project_id}/runs", payload),
            output_json=args.output_json,
        )
        return 0
    if args.command == "status":
        _print_payload(_get_json(args.base_url, f"/v1/runs/{args.run_id}"), output_json=args.output_json)
        return 0
    if args.command == "artifacts":
        _print_payload(_get_json(args.base_url, f"/v1/runs/{args.run_id}/artifacts"), output_json=args.output_json)
        return 0
    if args.command == "events":
        _print_payload(_get_json(args.base_url, f"/v1/runs/{args.run_id}/events"), output_json=args.output_json)
        return 0
    raise SystemExit(f"unknown runtime command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
