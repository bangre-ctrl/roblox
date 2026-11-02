"""
Anime Dice Daily Reward helper (Windows).

This prototype does not inject or store .ROBLOSECURITY cookies.
Sign in to each account through the official Roblox login flow first.
The helper launches the Roblox game URI and clicks a visible Claim button
using a screenshot reference.
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import pyautogui
except ImportError:
    print("Missing dependency. Run: py -m pip install -r requirements.txt")
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent
ACCOUNTS_FILE = ROOT / "accounts.txt"
CLAIM_IMAGE = ROOT / "assets" / "claim_button.png"
RESULTS_FILE = ROOT / "results.csv"
DEFAULT_PLACE_ID = "PLACE_ID_HERE"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25


@dataclass
class Account:
    label: str


def read_accounts() -> list[Account]:
    if not ACCOUNTS_FILE.exists():
        ACCOUNTS_FILE.write_text(
            "# One account label per line. Never put passwords or cookies here.\n"
            "account_01\n",
            encoding="utf-8",
        )
        print(f"Created {ACCOUNTS_FILE}. Add account labels, one per line.")
        return []

    accounts = []
    for raw in ACCOUNTS_FILE.read_text(encoding="utf-8").splitlines():
        label = raw.strip()
        if label and not label.startswith("#"):
            accounts.append(Account(label))
    return accounts


def log_result(account: str, status: str, detail: str = "") -> None:
    new_file = not RESULTS_FILE.exists()
    with RESULTS_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp_utc", "account", "status", "detail"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), account, status, detail])


def launch_game(place_id: str) -> None:
    if not place_id.isdigit():
        raise ValueError("Set the Anime Dice Place ID with --place-id.")
    os.startfile(f"roblox://experiences/start?placeId={place_id}")  # Windows


def wait_for_claim(timeout: int) -> bool:
    if not CLAIM_IMAGE.exists():
        raise FileNotFoundError(
            f"Missing {CLAIM_IMAGE}. Save a cropped screenshot of the visible "
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


def process_accounts(accounts: list[Account], place_id: str, timeout: int) -> None:
    print(f"Loaded {len(accounts)} account labels.")
    print("Process is sequential; Roblox account switching remains manual.")
    print("Sign in through the official Roblox client. Do not paste cookies here.")

    for index, account in enumerate(accounts, start=1):
        print(f"\n[{index}/{len(accounts)}] {account.label}")
        input(
            "Sign in to THIS account in the official Roblox client, then press Enter "
            "to launch Anime Dice..."
        )
        try:
            launch_game(place_id)
            print("Roblox Player launched. Looking for the Claim button...")
            if wait_for_claim(timeout):
                print("Claim button clicked. Verify the in-game success message.")
                log_result(account.label, "claim_clicked", "Manual verification required")
            else:
                print("Claim button was not detected.")
                log_result(account.label, "not_detected", "Claim button not found")
        except Exception as exc:
            print(f"Error: {exc}")
            log_result(account.label, "error", str(exc))

        input("Close/log out, switch to the next account in the official client, then press Enter...")

    print(f"Finished. Results saved to {RESULTS_FILE}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sequential Anime Dice daily reward helper")
    parser.add_argument("--place-id", default=DEFAULT_PLACE_ID, help="Anime Dice Place ID")
    parser.add_argument("--timeout", type=int, default=240, help="Seconds to search for Claim")
    args = parser.parse_args()

    accounts = read_accounts()
    if not accounts:
        print("No account labels configured.")
        return 0

    try:
        process_accounts(accounts, args.place_id, max(10, args.timeout))
    except KeyboardInterrupt:
        print("\nStopped by user.")
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
