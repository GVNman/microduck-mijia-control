# Mi Home Voice Control (mihome-voice)

> **What this folder does, in one sentence: teach the duck to understand your
> spoken words and turn on lights or close curtains for you.**
>
> [中文版](README.md) · [Back to overview](../README.en.md)

## At a glance: what it can do

| Say to the duck (Chinese) | What happens |
|---|---|
| 开窗帘 / 打开窗帘 / 拉开窗帘 / 关窗帘 | Living-room curtain opens / closes |
| 开吊灯 / 打开吊灯 / 关吊灯 / 关闭吊灯 | Chandelier on / off |
| 开柜子灯 / 打开柜子灯 / 关柜子灯 / 关闭柜子灯 | All three cabinet lights on / off at once |

Tips: prefixes like “鸭子”, “小鸭子”, “请”, “吧” all work, e.g. “鸭子，开吊灯”.
Negative forms (“不要开灯”, “别开灯”) are recognized but intentionally ignored.

## What each file in this folder does

| File | Purpose | Where it goes on the duck |
|---|---|---|
| `voice_commands_mihome.py` | Core code: when it hears “开吊灯” it calls the Mi Home API; when it hears “关窗帘” it closes the curtain motor. It contains the three devices' IDs (DIDs) — replace them with yours | Wire it into the duck's own `voice_commands.py` following the notes in the file (do not overwrite it) |
| `speech_grammar_snippet.md` | The Chinese words to recognize: it tells the duck which phrases are commands. Words not in this list come back as not understood | Add its phrases to `COMMAND_GRAMMAR` in the duck's `speech_control.py` |
| `duck-echo-mihome.conf` | System config: the duck's voice service cannot read `/home` or reach the network by default; this file grants it that access, or every command fails | `/etc/systemd/system/duck-echo.service.d/mihome.conf` |

## How it works (you don't need to understand this to use it)

```
You speak → the duck recognizes speech locally (Vosk, offline, no internet)
         → it finds the matching command → calls the Mi Home API (mijia-api)
         → the light / curtain acts
```

- **Vosk**: the duck's built-in offline speech recognizer. Your voice never leaves the device.
- **mijia-api**: an open-source library for controlling Mi Home devices. This project
  uses it to talk to the devices in your home. This folder does **not** include it —
  you install it separately (step 2 below).

## Before you start, you need

- [ ] A Microduck robot (Radxa Zero 3W) running official software **2026.11.4 or
  later**, with voice (duck-echo) working.
- [ ] A computer that can SSH into the duck (you need it to copy files and edit configs).
- [ ] Mi Home devices (curtain, lights, etc.) already set up in the Mi Home app
  and controllable from it.

## Detailed steps

### Step 1: Place the system config file

Copy `duck-echo-mihome.conf` from this folder to
`/etc/systemd/system/duck-echo.service.d/mihome.conf` on the duck,
then reload the system configuration:

```bash
sudo systemctl daemon-reload
```

> Why this step: the duck's voice service runs in a sandbox that by default
> cannot read `/home` or reach the network. Without this config file it cannot
> find the Mi Home library, and every voice command fails with
> `No module named 'mijiaAPI'`.

### Step 2: Install the Mi Home control library

Install [mijia-api](https://github.com/Do1e/mijia-api) on the duck (either way works):

```bash
pip install mijiaAPI
```

or copy the library to `/home/radxa/mijia-api`.

Then log in once so it writes its auth file (`~/.config/mijia-api/auth.json`):

```bash
python3 -m mijiaAPI --login
```

> The auth file stays on your duck only. **Never** upload it anywhere or put it
> in this repo.

### Step 3: Find your devices' IDs (DIDs)

Every Mi Home device has an ID, called a DID. List them:

```bash
python3 -m mijiaAPI --list
```

Write down the DIDs of the devices you want to control (curtain, chandelier,
cabinet lights). A light group shows up as `group.<number>`.

### Step 4: Fill the IDs into the code

Open `voice_commands_mihome.py` and fill in the DIDs you found
(the comments in the file mark where the curtain, chandelier, and cabinet
lights go).

Then wire the handlers into the duck's own `voice_commands.py` following the
notes at the bottom of that file (phrase router + executor dispatch), and add
the phrases from `speech_grammar_snippet.md` to `COMMAND_GRAMMAR`
in `speech_control.py`.

> This step is required: speech recognition only knows the words in its
> vocabulary. Words not in it come back as `[unk]` (not understood).

### Step 5: Restart the voice service and try it

```bash
sudo systemctl restart duck-echo
```

Then say “开吊灯” to the duck and watch the light.

## How to verify it works

1. Say “开吊灯” — the chandelier turns on; say “关吊灯” — it turns off.
2. Say “开窗帘” — the curtain opens; say “关窗帘” — it closes.
3. Say “不要开灯” — the duck does nothing (negatives are recognized, not executed).

## FAQ

**Q: I gave a command and the duck did nothing?**

A: Check two things: ① is the phrase in `COMMAND_GRAMMAR`? Missing words come
back as `[unk]`; ② is `duck-echo-mihome.conf` in the right place, and did you
run `daemon-reload` after placing it? Also check the log for
`No module named 'mijiaAPI'`, which means the Mi Home library isn't installed.

**Q: The command ran, but the app doesn't show the new state / reading the device timed out?**

A: Some devices (curtain motors, Mesh switches) are slow to move, and reading
a Mesh switch back often times out even though the write went through. Trust
the physical device, not the immediate reply.

**Q: A switch has several gangs — how do I pick one?**

A: Use the property after the ID, e.g. `on-4` means gang 4 of that switch.
Change it to match your own wiring.

**Q: Voice control disappeared after a duck software update?**

A: That's expected. A duck update overwrites duck-echo. Before updating, copy
your patched `voice_commands.py`, `speech_control.py`, and this folder's files
off the duck as a backup, then re-apply them after the update.

**Q: What about privacy? Does my voice go to the cloud?**

A: No. Speech recognition runs locally on the duck. Mi Home control goes over
your own home network and your Mi Home account — no third-party voice cloud
is involved.

## Security

- **This folder contains no real credentials.** Device IDs are all `YOUR_*`
  placeholders.
- Fill in real values only on your own duck. Filled-in configs and the auth
  file (`auth.json`) must **never** be committed to a public repository.
