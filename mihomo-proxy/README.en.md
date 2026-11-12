# Proxy (mihomo-proxy)

> **What this folder does, in one sentence: install a transparent proxy on the
> duck so its network connection stays up.**
>
> [中文版](README.md) · [Back to overview](../README.en.md)

## First: this is optional

Some of the duck's services need a proxy to connect. If you don't have a proxy
subscription, **skip this whole folder** and install only the
[Mi Home voice control](../mihome-voice/) part.

## What each file in this folder does

| File | Purpose | Where it goes on the duck |
|---|---|---|
| `config.example.yaml` | Proxy config template: how to connect, which node, which country. All `YOUR_*` placeholders — replace them with your own | After filling it in, place it at `/home/radxa/mihomo-config.yaml` |
| `mihomo.service` | System service config: starts the proxy automatically at boot and keeps it running | `/etc/systemd/system/mihomo.service` |

## How it works (you don't need to understand this to use it)

- **mihomo**: open-source proxy software. Once installed, it listens on the duck
  at `127.0.0.1:7890`, and duck services that need the internet go through it.
- `profile.store-selected: true` in the config means a node you pick manually
  stays picked after a reboot instead of silently falling back to another node.
- The `US` group automatically picks the fastest US node by latency test.

This folder does **not** include mihomo itself — you install it separately
(step 1 below).

## Before you start, you need

- [ ] A Microduck robot (Radxa Zero 3W) running official software **2026.11.4
  or later**.
- [ ] A computer that can SSH into the duck.
- [ ] A proxy subscription (with node addresses — skip this folder if you
  don't have one).

## Detailed steps

### Step 1: Install mihomo

Install [mihomo](https://github.com/MetaCubeX/mihomo) on the duck (follow its
official docs; `mihomo -v` should print a version number when it works).

### Step 2: Place the config file

Copy `config.example.yaml` from this folder to `/home/radxa/mihomo-config.yaml`
on the duck, and replace every `YOUR_*` placeholder with your own proxy node
details.

> Fill in real values only on your own duck. The filled-in config must
> **never** be committed to a public repository.

### Step 3: Install the service and start it

```bash
sudo cp mihomo.service /etc/systemd/system/mihomo.service
sudo systemctl enable --now mihomo
```

`enable` makes it start at boot; `--now` starts it right away.

### Step 4: Confirm the proxy works

```bash
curl -x http://127.0.0.1:7890 -s -o /dev/null -w "%{http_code}\n" https://www.google.com
```

A `200` means it works. If you get `000` or a timeout, check:

1. `sudo systemctl status mihomo` — is the service running?
2. Did you fill in the node address, port, and password correctly?
3. Is the duck's own network up (try curl without the proxy first)?

## How to verify it works

1. `sudo systemctl is-active mihomo` shows `active`.
2. The curl in step 4 returns `200`.
3. Reboot the duck once — the proxy comes up by itself, no manual start needed.

## FAQ

**Q: The service won't start — it complains about the config file?**

A: Check the YAML formatting first: indentation must be spaces, never tabs;
make sure no `YOUR_*` placeholder is left unfilled. Then run
`sudo systemctl restart mihomo` and try again.

**Q: The proxy works, but one of the duck's services still can't connect?**

A: That service may not be going through the proxy. Check whether it uses
`127.0.0.1:7890` or connects directly. Some services need the proxy address
set in their own config.

**Q: How are nodes picked? Does my manual pick survive a reboot?**

A: Yes. `profile.store-selected: true` in the config keeps your manual pick.
The `US` group automatically picks the fastest US node by latency, so you
don't have to choose one by hand each time.

## Security

- **This folder contains no real credentials.** Proxy addresses and passwords
  are all `YOUR_*` placeholders.
- Fill in real values only on your own duck. The filled-in config must
  **never** be committed to a public repository.
