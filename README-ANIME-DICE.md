# Anime Dice Daily Reward Helper

## Project status

This repository currently contains a **manual-login screen-automation prototype**. It is not yet the one-command, multi-account cookie login bot discussed in chat.

### Files

- `anime_dice_daily.py` — launches Anime Dice in Roblox Player and looks for a visible Claim button.
- `requirements.txt` — Python dependencies for screen matching.
- `cookies.example.txt` — format example only; placeholders, not real credentials.
- `.gitignore` — keeps local cookies and results out of Git.

## Important cookie / Player limitation

A `.ROBLOSECURITY` cookie authenticates a Roblox web session. It is **not automatically a Roblox Player login**. This prototype does not consume cookies or switch Player accounts. Do not paste real cookies into GitHub, issues, commits, or chat.

The requested workflow — read many cookies, authenticate each account, launch the game as that account, claim the daily reward, then switch to the next — is **not implemented**. Do not treat the current script as an automatic cookie-login bot.

## Setup for the current prototype (Windows)

1. Install Python 3.10 or newer.
2. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Create an `assets` folder.
4. Capture a tight screenshot of the in-game Daily Reward Claim button and save it as `assets/claim_button.png`.
5. Find the Anime Dice Place ID from its Roblox game URL.
6. Run:

   ```powershell
   py anime_dice_daily.py --place-id YOUR_PLACE_ID
   ```

7. Sign in to the intended account using the official Roblox client when prompted.

The helper clicks the first matching visible Claim button. It cannot confirm from game-server data that the reward was granted; verify the in-game result.

## Local cookie file format (not consumed by this prototype)

If you keep a local list for future development, copy `cookies.example.txt` to `cookies.txt` and put one cookie value per line. Keep the real file local; `.gitignore` excludes it. The current Python script does not read this file.

## Safety

- Never commit `.ROBLOSECURITY`, passwords, recovery codes, or other account credentials.
- Use only accounts you own or are authorized to manage.
- Respect Roblox and game-specific rules; automation may be restricted.
- PyAutoGUI fail-safe is enabled: move the mouse to the upper-left corner to abort.
