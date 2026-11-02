# Anime Dice Daily Reward Helper

A Windows prototype that processes account labels sequentially and clicks a visible Daily Reward Claim button.

## Authentication limitation

This project does **not** log Roblox Player in with a pasted `.ROBLOSECURITY` cookie. A browser cookie is not automatically inherited by the official Roblox Player. Sign in to each account through the official Roblox login flow. This helper never reads, exports, sends, or stores cookies.

## Setup

1. Install Python 3.10 or newer.
2. Clone or download this repository.
3. Open PowerShell in the project folder.
4. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Copy `accounts.example.txt` to `accounts.txt` and edit the labels. Labels are for tracking only, not credentials.
6. Create an `assets` folder if it does not exist.
7. Capture a small screenshot of the actual Daily Reward **Claim** button and save it as `assets/claim_button.png`. Crop tightly around the button.
8. Find the Anime Dice Place ID from its Roblox game URL and run:

   ```powershell
   py anime_dice_daily.py --place-id YOUR_PLACE_ID
   ```

## Current workflow

For each label, the helper pauses so you can sign in to that account using the official Roblox client. Press Enter to launch Anime Dice through the registered `roblox://` URI. It searches the screen for the Claim button and clicks it once. Then it asks you to switch accounts.

The helper does not automatically switch Roblox identities, verify the reward against game-server data, bypass verification, or guarantee a reward was granted. Verify the in-game success message and review `results.csv`.

## Safety

- Never commit `.ROBLOSECURITY`, passwords, recovery codes, or personal account data.
- Keep `accounts.txt` local; it is listed in `.gitignore`.
- Use only accounts you own or are authorized to manage.
- Respect Roblox and game-specific rules; automation may be restricted.
- PyAutoGUI's fail-safe is enabled: move the mouse to the upper-left corner to abort.
