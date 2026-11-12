"""Mi Home voice-command handlers for Microduck duck-echo.

Extracted from the duck-echo voice command module running on a Radxa Zero 3W
(Microduck). These handlers let the duck open/close a curtain and switch
lights on/off by voice, through the mijia-api library.

Setup:
  1. Install mijia-api (https://github.com/Do1e/mijia-api, GPL-3.0),
     e.g. pip install mijiaAPI, and log in once so it writes its auth file.
  2. Fill in your own device DIDs below. Find them with:
         python3 -m mijiaAPI --list
     (or the equivalent CLI in your mijia-api version). The DID is the
     number shown for each device; light groups look like "group.<number>".
  3. Import the three mihome_* functions into your duck-echo
     voice_commands.py and wire them into the phrase router and the
     executor (see the snippets at the bottom of this file).
  4. Make sure duck-echo can read the mijia-api library and its auth file
     (see mihome/duck-echo-mihome.conf for the systemd drop-in that
     relaxes the service sandbox for this).

No credentials are stored in this file. The auth token lives in the
mijia-api auth file on your own device, never in this repo.
"""

import sys

# --- Fill in your own device DIDs -------------------------------------------
# Curtain: a single curtain motor. Find its DID with the mijia-api CLI.
_MIHOME_CURTAIN_DID = 'YOUR_CURTAIN_DID'  # e.g. yeelink.curtain.*

# Chandelier: one gang of a multi-gang wall switch. The prop below (on-4)
# is the gang number; change it to match your own switch (on-1, on-2...).
_MIHOME_CHANDELIER_DID = 'YOUR_CHANDELIER_DID'
_MIHOME_CHANDELIER_PROP = 'on-4'

# Cabinet lights: list every light you want switched together as
# (did, prop) pairs. A light group uses prop 'on'; a switch gang uses
# the gang prop such as 'on-2'.
_MIHOME_CABINET_LIGHTS = [
    ('YOUR_CABINET_DID_1', 'on-2'),       # e.g. cabinet pendant light
    ('YOUR_CABINET_DID_2', 'on-2'),       # e.g. cabinet switch
    ('YOUR_CABINET_GROUP_DID', 'on'),     # e.g. a light group
]

_MIHOME_API = None


def _mihome_api():
    """Lazy Mi Home client, reused across commands."""
    global _MIHOME_API
    if _MIHOME_API is None:
        sys.path.insert(0, '/home/radxa/mijia-api')
        from mijiaAPI import mijiaAPI
        _MIHOME_API = mijiaAPI(
            auth_data_path='/home/radxa/.config/mijia-api/auth.json')
    return _MIHOME_API


def mihome_curtain(open_it):
    """Open (True) or close (False) the curtain. motor-control: 0=open, 1=close."""
    api = _mihome_api()
    from mijiaAPI.devices import mijiaDevice
    dev = mijiaDevice(api, did=_MIHOME_CURTAIN_DID)
    dev.set('motor-control', 0 if open_it else 1)


def mihome_chandelier(on):
    """Turn the chandelier (one switch gang) on/off."""
    api = _mihome_api()
    from mijiaAPI.devices import mijiaDevice
    dev = mijiaDevice(api, did=_MIHOME_CHANDELIER_DID)
    dev.set(_MIHOME_CHANDELIER_PROP, bool(on))


def mihome_cabinet(on):
    """Turn all cabinet lights on/off together."""
    api = _mihome_api()
    from mijiaAPI.devices import mijiaDevice
    for did, prop in _MIHOME_CABINET_LIGHTS:
        mijiaDevice(api, did=did).set(prop, bool(on))


# --- Wiring snippets (adapt to your voice_commands.py) ----------------------
#
# 1. Phrase router — map recognised text to a command name:
#
#     if text in ('开窗帘', '打开窗帘', '拉开窗帘', '开客厅窗帘', '打开客厅窗帘'):
#         return 'curtain_open'
#     if text in ('关窗帘', '关客厅窗帘'):
#         return 'curtain_close'
#     if text in ('开吊灯', '打开吊灯', '开客厅吊灯'):
#         return 'diaodeng_on'
#     if text in ('关吊灯', '关闭吊灯', '关客厅吊灯'):
#         return 'diaodeng_off'
#     if text in ('开柜子灯', '打开柜子灯', '开柜子吊灯'):
#         return 'guizi_on'
#     if text in ('关柜子灯', '关闭柜子灯', '关柜子吊灯'):
#         return 'guizi_off'
#
# 2. Executor dispatch — inside your command executor:
#
#     if command in ('curtain_open', 'curtain_close'):
#         mihome_curtain(command == 'curtain_open')
#     if command in ('diaodeng_on', 'diaodeng_off'):
#         mihome_chandelier(command == 'diaodeng_on')
#     if command in ('guizi_on', 'guizi_off'):
#         mihome_cabinet(command == 'guizi_on')
#
# 3. Speech grammar — the recognised phrases must also be added to the
#    Vosk COMMAND_GRAMMAR, otherwise the recogniser returns [unk].
#    See mihome/speech_grammar_snippet.md.
