#!/usr/bin/env python3
"""Record the desktop while running ./all_in_one.sh.

- Captures monitor 1 + monitor 2 area by computing a bounding box from xrandr.
- Starts recording before all_in_one execution.
- Stops recording up to 5 seconds after all_in_one exits.
- Saves MP4 as YYYY-MM-DD_HH-MM-SS.mp4.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


STOP_TIMEOUT_SECONDS = 5


def _run_text(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def _get_x11_capture_region() -> tuple[int, int, int, int]:
    """Return (x, y, width, height) for the first two connected monitors.

    Uses xrandr output like:
      HDMI-1 connected primary 1920x1080+0+0
      DP-1 connected 1920x1080+1920+0
    """
    output = _run_text(["xrandr", "--query"])
    pattern = re.compile(
        r"^(?P<name>\S+)\s+connected(?:\s+primary)?\s+"
        r"(?P<w>\d+)x(?P<h>\d+)\+(?P<x>-?\d+)\+(?P<y>-?\d+)",
        re.MULTILINE,
    )

    monitors: list[tuple[int, int, int, int]] = []
    for match in pattern.finditer(output):
        w = int(match.group("w"))
        h = int(match.group("h"))
        x = int(match.group("x"))
        y = int(match.group("y"))
        monitors.append((x, y, w, h))

    if not monitors:
        raise RuntimeError(
            "No connected monitors with geometry found via xrandr. "
            "Ensure X11 session and xrandr availability."
        )

    selected = monitors[:2]
    min_x = min(m[0] for m in selected)
    min_y = min(m[1] for m in selected)
    max_x = max(m[0] + m[2] for m in selected)
    max_y = max(m[1] + m[3] for m in selected)

    return min_x, min_y, max_x - min_x, max_y - min_y


def _start_ffmpeg_recording(display: str, x: int, y: int, width: int, height: int, output_file: Path) -> subprocess.Popen:
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "x11grab",
        "-framerate",
        "30",
        "-video_size",
        f"{width}x{height}",
        "-i",
        f"{display}+{x},{y}",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        str(output_file),
    ]

    return subprocess.Popen(
        ffmpeg_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _stop_recorder(recorder: subprocess.Popen) -> None:
    if recorder.poll() is not None:
        return

    try:
        if recorder.stdin:
            recorder.stdin.write(b"q\n")
            recorder.stdin.flush()
        recorder.wait(timeout=STOP_TIMEOUT_SECONDS)
    except Exception:
        recorder.terminate()
        try:
            recorder.wait(timeout=STOP_TIMEOUT_SECONDS)
        except Exception:
            recorder.kill()
            recorder.wait(timeout=2)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    all_in_one = repo_root / "all_in_one.sh"
    recordings_dir = repo_root / "recordings"
    recordings_dir.mkdir(parents=True, exist_ok=True)

    if not all_in_one.exists():
        print(f"ERROR: Script not found: {all_in_one}", file=sys.stderr)
        return 1

    if not os.access(all_in_one, os.X_OK):
        print(f"ERROR: Script is not executable: {all_in_one}", file=sys.stderr)
        print("Run: chmod +x all_in_one.sh", file=sys.stderr)
        return 1

    if shutil.which("ffmpeg") is None:
        print("ERROR: ffmpeg not found. Install with: sudo apt install -y ffmpeg", file=sys.stderr)
        return 1

    if shutil.which("xrandr") is None:
        print("ERROR: xrandr not found. Install with: sudo apt install -y x11-xserver-utils", file=sys.stderr)
        return 1

    display = os.environ.get("DISPLAY")
    if not display:
        print("ERROR: DISPLAY is not set. This recorder requires a graphical X11 session.", file=sys.stderr)
        return 1

    try:
        x, y, width, height = _get_x11_capture_region()
    except Exception as exc:
        print(f"ERROR: Could not detect monitor geometry: {exc}", file=sys.stderr)
        return 1

    timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = recordings_dir / f"{timestamp}.mp4"

    print(f"[recorder] Capture region: {width}x{height}+{x}+{y} on DISPLAY {display}")
    print(f"[recorder] Output file: {output_file}")

    recorder = _start_ffmpeg_recording(display, x, y, width, height, output_file)
    if recorder.poll() is not None:
        print("ERROR: Failed to start ffmpeg recorder.", file=sys.stderr)
        return 1

    all_in_one_rc = 1
    try:
        run_proc = subprocess.run(["./all_in_one.sh"], cwd=repo_root)
        all_in_one_rc = run_proc.returncode
    finally:
        _stop_recorder(recorder)

    if all_in_one_rc == 0:
        print(f"[recorder] Finished successfully. Video saved to: {output_file}")
    else:
        print(f"[recorder] all_in_one.sh failed with code {all_in_one_rc}. Video saved to: {output_file}")

    return all_in_one_rc


if __name__ == "__main__":
    raise SystemExit(main())
