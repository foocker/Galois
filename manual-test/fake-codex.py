#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import re
import sys
import time
import uuid


def main() -> int:
    args = sys.argv[1:]
    workspace = Path.cwd()
    if "-C" in args:
        index = args.index("-C")
        if index + 1 < len(args):
            workspace = Path(args[index + 1])
    prompt = args[-1] if args else ""
    match = re.search(r"problem_id=([A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*)", prompt)
    problem_id = match.group(1) if match else "problem"
    sleep_seconds = float(os.getenv("FAKE_CODEX_SLEEP", "3"))
    time.sleep(sleep_seconds)
    output_dir = workspace / "results" / problem_id
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "blueprint.md").write_text(
        f"# Solution\n\nfake run for {problem_id}\n",
        encoding="utf-8",
    )
    print(f"session id: {uuid.uuid4()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
