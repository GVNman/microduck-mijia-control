# Vosk speech-grammar snippet (Mi Home commands)

duck-echo uses a constrained Vosk grammar (`COMMAND_GRAMMAR` in
`speech_control.py`, model `vosk-model-small-cn-0.22`). **Any word or
phrase that is not in the grammar comes back as `[unk]`**, so every new
voice command must be added here as well as in the phrase router.

Add these lines to `COMMAND_GRAMMAR`, next to the other action phrases.
Spaces between words are required — Vosk matches on space-separated tokens.

```python
# Curtain (窗帘)
'开 窗帘', '打开 窗帘', '拉开 窗帘', '关 窗帘',
'鸭子 开 窗帘', '鸭子 关 窗帘',
'小 鸭子 开 窗帘', '小 鸭子 关 窗帘',
'请 开 窗帘', '请 关 窗帘',
'开 窗帘 吧', '关 窗帘 吧',
'不要 开 窗帘', '不要 关 窗帘',
'别 开 窗帘', '别 关 窗帘',

# Chandelier (吊灯)
'开 吊灯', '打开 吊灯', '关 吊灯', '关闭 吊灯',
'鸭子 开 吊灯', '鸭子 关 吊灯',
'小 鸭子 开 吊灯', '小 鸭子 关 吊灯',
'请 开 吊灯', '请 关 吊灯',
'开 吊灯 吧', '关 吊灯 吧',
'不要 开 吊灯', '不要 关 吊灯',
'别 开 吊灯', '别 关 吊灯',

# Cabinet lights (柜子灯)
'开 柜子 灯', '打开 柜子 灯', '关 柜子 灯', '关闭 柜子 灯',
'开 柜子 吊灯', '关 柜子 吊灯',
'鸭子 开 柜子 灯', '鸭子 关 柜子 灯',
'小 鸭子 开 柜子 灯', '小 鸭子 关 柜子 灯',
'请 开 柜子 灯', '请 关 柜子 灯',
'开 柜子 灯 吧', '关 柜子 灯 吧',
'不要 开 柜子 灯', '不要 关 柜子 灯',
'别 开 柜子 灯', '别 关 柜子 灯',
```

Notes:

- The spoken text the recogniser returns has no spaces (`开窗帘`), while
  the grammar entries have spaces (`开 窗帘`). Both forms are needed:
  grammar entries for recognition, plain phrases for the router in
  `voice_commands_mihome.py`.
- Adding a new device word (e.g. `柜子`) only works if that word exists
  in the Vosk model vocabulary. Test it: if the word comes back as
  `[unk]`, pick a synonym that is in the model.
- Some devices are slow to respond (curtain motors and Mesh switches in
  particular). The command itself usually goes through even if the
  read-back times out — check the physical device rather than trusting
  the immediate reply.
