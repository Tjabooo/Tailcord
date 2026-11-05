# Tailcord

A small Python script that shows which of your Tailscale devices are online in your Discord profile bio. Every 30 seconds it reads `tailscale status --json`, compares the online state of three chosen devices with what the bio currently says, and updates the bio when something changed.

Proof of concept, made for educational purposes.

> **Warning:** it authenticates to Discord's API with a *user account token*. Automating a user account this way is against Discord's Terms of Service and can get the account banned. Use at your own risk, and never share or commit your token.

## Requirements
- Python 3
- `tailscale` CLI installed and logged in on the machine running the script
- `pip install -r requirements.txt` (`requests`, `python-dotenv`)

## Configuration
Copy `.env.example` to `.env` and fill it in:

| Variable | Meaning |
| --- | --- |
| `TOKEN` | Discord user token |
| `USER_ID` | Your Discord user ID |
| `NODE_KEY_1..3` | Tailscale node keys (the keys under `Peer` in `tailscale status --json`) of the three devices to track |

## Run
```bash
python3 main.py
```

## Limitations
- The bio must already end with a status block in the format the script writes (a `> system status -` line followed by three device lines), otherwise parsing the current status fails. The device labels (Desktop (Win11), Laptop (Arch), Laptop (Win11)) are hard-coded in `main.py`.
- Exactly three devices are supported.
