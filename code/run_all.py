"""Run every task and capture each task's console output."""
from contextlib import redirect_stdout
from pathlib import Path
import sys

from runner import TASKS, ROOT

runs = ROOT / "results" / "runs"
runs.mkdir(parents=True, exist_ok=True)
failures = []
for number, function in TASKS.items():
    log = runs / f"Task_{number:02d}.txt"
    try:
        with log.open("w", encoding="utf-8") as stream, redirect_stdout(stream):
            print(f"=== BIT 2118 Task {number} ===")
            function()
        print(f"Task {number}: OK ({log.relative_to(ROOT)})")
    except Exception as exc:
        failures.append((number, repr(exc)))
        print(f"Task {number}: FAILED ({exc!r})")
if failures:
    sys.exit(1)
print(f"All {len(TASKS)} tasks completed successfully.")
