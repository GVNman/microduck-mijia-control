# microduck-mijia-control

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **In one sentence: teach your Microduck robot duck to understand Chinese voice commands
> and turn on lights or close curtains for you — plus a built-in proxy that keeps
> the duck online.**
>
> [中文版](README.md)

## What is this?

Microduck is a 25 cm tall bipedal robot duck (powered by a Radxa Zero 3W board).
Out of the box, its voice features only control the robot itself — walking,
sitting down, quacking.

This project gives it two new abilities:

1. **Voice control for Mi Home devices**: say “开吊灯” (turn on the chandelier)
   to the duck, and the chandelier turns on; say “关窗帘” (close the curtain),
   and the curtain closes. Speech recognition runs locally on the duck —
   no internet, no cloud voice assistant.
2. **mihomo transparent proxy**: keeps the duck reliably online
   (some of its services need a proxy to connect).

## What can it do?

| Say to the duck (Chinese) | What happens |
|---|---|
| 开窗帘 / 打开窗帘 / 拉开窗帘 / 关窗帘 | Living-room curtain opens / closes |
| 开吊灯 / 打开吊灯 / 关吊灯 / 关闭吊灯 | Chandelier on / off |
| 开柜子灯 / 打开柜子灯 / 关柜子灯 / 关闭柜子灯 | All three cabinet lights on / off at once |

## Folder guide

Every folder has its own detailed guide (what each file does, where it goes,
step-by-step instructions, how to verify, FAQ) — just follow it:

| Folder | What it does | Detailed guide |
|---|---|---|
| `mihome-voice/` | Voice control for Mi Home devices: lights, curtains | [中文](mihome-voice/README.md) · [English](mihome-voice/README.en.md) |
| `mihomo-proxy/` | Proxy: keeps the duck online (optional — skip if you have no proxy subscription) | [中文](mihomo-proxy/README.md) · [English](mihomo-proxy/README.en.md) |

```
microduck-mijia-control/
├── README.md / README.en.md      Overview (this page)
├── LICENSE
├── mihome-voice/                 Mi Home voice control
│   ├── README.md / README.en.md  Detailed guide for this folder
│   ├── voice_commands_mihome.py  Core code: calls the Mi Home API on command
│   ├── speech_grammar_snippet.md Chinese phrases to recognize
│   └── duck-echo-mihome.conf    System config: grants the voice service access
└── mihomo-proxy/                 Proxy
    ├── README.md / README.en.md  Detailed guide for this folder
    ├── mihomo.service            Systemd service for the proxy
    └── config.example.yaml       Proxy config template (placeholders only — fill in yours)
```

## Quick start

1. Only want Mi Home voice control? Follow the [`mihome-voice/` guide](mihome-voice/README.en.md) — 5 steps.
2. Also want the proxy? Then follow the [`mihomo-proxy/` guide](mihomo-proxy/README.en.md) — 4 steps.
3. Before you start, make sure you have a Microduck (Radxa Zero 3W, software
   2026.11.4 or later), a computer that can SSH into the duck, and Mi Home
   devices already set up in the Mi Home app.

## Security

- **This repo contains no real credentials.** Device IDs, proxy addresses, and
  passwords are all `YOUR_*` placeholders.
- Fill in real values only on your own duck. Filled-in configs and the auth
  file (`auth.json`) must **never** be committed to a public repository.

## Licenses

- This project's own code: MIT (see `LICENSE`).
- Dependency [mijia-api](https://github.com/Do1e/mijia-api): GPL-3.0.
- Dependency [mihomo](https://github.com/MetaCubeX/mihomo): MIT.
