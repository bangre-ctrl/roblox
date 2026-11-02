"""
Anime Dice Daily Reward screen helper (Windows).

CURRENT LIMITATION:
- Manual Roblox account sign-in is required.
- cookies.txt is NOT read or used by this script.
- Roblox web cookies are not automatically inherited by Roblox Player.

This helper launches the game URI and clicks a visible Claim button using
a screenshot reference. It is a prototype, not a multi-account cookie bot.
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import pyautogui
except ImportError:
    print("Missing dependency. Run: py -m pip install -r requirements.txt")
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent
CLAIM_IMAGE = ROOT / "assets" / "claim_button.png"
RESULTS_FILE = ROOT / "results.csv"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25


def log_result(status: str, detail: str = "") -> None:
    new_file = not RESULTS_FILE.exists()
    with RESULTS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp_utc", "status", "detail"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), status, detail])


def launch_game(place_id: str) -> None:
    if not place_id.isdigit():
        raise ValueError("Pass the Anime Dice Place ID using --place-id.")
    if os.name != "nt":
        raise RuntimeError("This prototype currently supports Windows only.")
    os.startfile(f"roblox://experiences/start?placeId={place_id}")  # type: ignore[attr-defined]


def wait_for_claim(timeout: int) -> bool:
    if not CLAIM_IMAGE.exists():
        raise FileNotFoundError(
            f"Missing {CLAIM_IMAGE}. Save a tight screenshot of the visible "
            "Daily Reward Claim button at that path."
        )

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            location = pyautogui.locateOnScreen(
                str(CLAIM_IMAGE), confidence=0.86, grayscale=True
            )
        except Exception as exc:
            if exc.__class__.__name__ != "ImageNotFoundException":
                raise
            location = None

        if location:
            center = pyautogui.center(location)
            pyautogui.click(center.x, center.y)
            time.sleep(2)
            return True
        time.sleep(2)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manual-login Anime Dice daily reward screen helper"
    )
    parser.add_argument("--place-id", required=True, help="Anime Dice Place ID")
    parser.add_argument("--timeout", type=int, default=240, help="Seconds to search for Claim")
    args = parser.parse_args()

    print("NOTICE: this prototype does not read cookies or switch Roblox accounts.")
    input("Sign in to the intended account in the official Roblox client, then press Enter...")
    try:
        launch_game(args.place_id)
        print("Roblox Player launched. Waiting for the visible Claim button...")
        if wait_for_claim(max(10, args.timeout)):
            print("Claim button clicked. Verify the in-game success message.")
            log_result("claim_clicked", "Manual verification required")
        else:
            print("Claim button was not detected before timeout.")
            log_result("not_detected", "Claim button not found")
    except KeyboardInterrupt:
        print("\nStopped by user.")
        return 130
    except Exception as exc:
        print(f"Error: {exc}")
        log_result("error", str(exc))
        return 1

    print(f"Results saved to {RESULTS_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
