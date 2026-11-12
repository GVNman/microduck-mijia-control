# microduck-mijia-control

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **一句话：让你的 Microduck 鸭子机器人听懂中文语音，帮你开灯、拉窗帘；同时自带代理，让鸭子一直在线。**
>
> [English version](README.en.md)

## 这是什么？

Microduck 是一只 25 厘米高、会走路的鸭子机器人（主控是 Radxa Zero 3W 开发板）。
它自带语音功能，但默认只能控制机器人自己——比如走路、坐下、叫一声。

这个项目给它加了两个本事：

1. **语音控制米家设备**：对鸭子说“开吊灯”，家里的吊灯就亮了；说“关窗帘”，窗帘就合上。
   语音识别在鸭子本地完成，不用联网、不用云端语音助手。
2. **mihomo 透明代理**：让鸭子稳定联网（鸭子有些服务需要走代理才能连上）。

## 能做什么？

| 你对鸭子说 | 鸭子帮你做 |
|---|---|
| 开窗帘 / 打开窗帘 / 拉开窗帘 / 关窗帘 | 客厅窗帘打开 / 合上 |
| 开吊灯 / 打开吊灯 / 关吊灯 / 关闭吊灯 | 吊灯开 / 关 |
| 开柜子灯 / 打开柜子灯 / 关柜子灯 / 关闭柜子灯 | 三盏柜子灯同时开 / 关 |

## 文件夹说明

每个文件夹里都有一份详细的说明（每个文件是干嘛的、放到哪里、一步一步怎么做、怎么验证、常见问题），
照着做就行：

| 文件夹 | 是干嘛的 | 详细说明 |
|---|---|---|
| `mihome-voice/` | 语音控制米家设备：开灯、拉窗帘 | [中文](mihome-voice/README.md) · [English](mihome-voice/README.en.md) |
| `mihomo-proxy/` | 代理：让鸭子稳定联网（可选，没有代理订阅可以跳过） | [中文](mihomo-proxy/README.md) · [English](mihomo-proxy/README.en.md) |

```
microduck-mijia-control/
├── README.md / README.en.md      总览（就是本页）
├── LICENSE
├── mihome-voice/                 米家语音控制
│   ├── README.md / README.en.md  本文件夹详细说明
│   ├── voice_commands_mihome.py  核心代码：收到命令就调米家接口
│   ├── speech_grammar_snippet.md 要识别的中文词表
│   └── duck-echo-mihome.conf    系统配置：给语音服务开权限
└── mihomo-proxy/                 代理
    ├── README.md / README.en.md  本文件夹详细说明
    ├── mihomo.service            代理服务的系统配置
    └── config.example.yaml       代理配置模板（全是占位符，填自己的）
```

## 快速开始

1. 只想语音控制米家？看 [`mihome-voice/` 的说明](mihome-voice/README.md)，5 步装好。
2. 还想要代理？再看 [`mihomo-proxy/` 的说明](mihomo-proxy/README.md)，4 步装好。
3. 开始之前，先确认你有一只 Microduck（Radxa Zero 3W，软件 2026.11.4 或更新）、
   一台能 SSH 连上鸭子的电脑、家里米家设备已在米家 App 里配好。

## 安全提醒

- **仓库里没有任何真实凭据。** 设备编号、代理地址、密码一律是 `YOUR_*` 占位符。
- 只在你自己的鸭子上填真实信息，填完的配置和授权文件（`auth.json`）**永远不要**提交到公开仓库。

## 许可证

- 本项目自己的代码：MIT（见 `LICENSE`）。
- 依赖 [mijia-api](https://github.com/Do1e/mijia-api)：GPL-3.0。
- 依赖 [mihomo](https://github.com/MetaCubeX/mihomo)：MIT。
