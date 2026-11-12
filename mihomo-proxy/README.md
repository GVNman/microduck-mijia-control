# 代理（mihomo-proxy）

> **这个文件夹是干嘛的：一句话——给鸭子装一个透明代理，让它的网络一直通着。**
>
> [English version](README.en.md) · [回总览](../README.md)

## 先说清楚：这是可选的

鸭子有些服务需要走代理才能连上。如果你没有代理订阅，**这个文件夹可以整个跳过**，
只装 [米家语音控制](../mihome-voice/) 那部分就行。

## 这个文件夹里每个文件是干嘛的

| 文件 | 作用 | 放到鸭子的哪里 |
|---|---|---|
| `config.example.yaml` | 代理配置模板：写了代理怎么连、走哪个节点、选哪个国家。里面全是 `YOUR_*` 占位符，要换成你自己的 | 填好后放到 `/home/radxa/mihomo-config.yaml` |
| `mihomo.service` | 系统服务配置：让代理开机自动启动、一直跑着 | `/etc/systemd/system/mihomo.service` |

## 工作原理（不用懂也能用）

- **mihomo**：一个开源代理软件。装好后，它在鸭子本地监听 `127.0.0.1:7890`，
  鸭子上需要联网的服务都走这里出去。
- 配置文件里 `profile.store-selected: true` 的意思是：你手动选的节点，重启后还保留，
  不会悄悄换成别的节点。
- `US` 分组会自动按延迟挑最快的美国节点。

本文件夹不包含 mihomo 这个软件本身，你需要另外安装（下面第 1 步）。

## 开始之前，你需要

- [ ] 一只 Microduck 机器人（Radxa Zero 3W），官方软件 **2026.11.4 或更新版本**。
- [ ] 一台能 SSH 连上鸭子的电脑。
- [ ] 一个代理订阅（有节点地址，没有就跳过本文件夹）。

## 详细步骤

### 第 1 步：安装 mihomo

在鸭子上安装 [mihomo](https://github.com/MetaCubeX/mihomo)（按官方文档装到鸭子上，
能跑 `mihomo -v` 打印出版本号就行）。

### 第 2 步：放配置文件

把本文件夹的 `config.example.yaml` 复制到鸭子的 `/home/radxa/mihomo-config.yaml`，
把里面所有的 `YOUR_*` 占位符换成你自己的代理节点信息。

> 只在你自己的鸭子上填真实信息，填完的配置文件**永远不要**提交到公开仓库。

### 第 3 步：装服务并启动

```bash
sudo cp mihomo.service /etc/systemd/system/mihomo.service
sudo systemctl enable --now mihomo
```

`enable` 是开机自启，`--now` 是现在就启动。

### 第 4 步：确认代理在工作

```bash
curl -x http://127.0.0.1:7890 -s -o /dev/null -w "%{http_code}\n" https://www.google.com
```

返回 `200` 就是通了。如果返回 `000` 或超时，先检查：

1. `sudo systemctl status mihomo` 看服务是不是在跑。
2. 配置文件里的节点地址、端口、密码有没有填错。
3. 鸭子本身的网络是不是通的（先不走代理直接 curl 一下）。

## 怎么验证装好了

1. `sudo systemctl is-active mihomo` 显示 `active`。
2. 上面第 4 步的 curl 返回 `200`。
3. 重启鸭子一次，代理自动起来，不用手动再开。

## 常见问题

**Q：服务起不来，报错说配置文件有问题？**

A：先看配置文件是不是 YAML 格式错了：缩进只能用空格，不能用 Tab；
`YOUR_*` 占位符是不是还有没换掉的。改完跑 `sudo systemctl restart mihomo` 再试。

**Q：代理通了，但鸭子的某个服务还是连不上？**

A：那个服务可能没走代理。检查它是不是用了 `127.0.0.1:7890`，
还是直接连的外网。有些服务要在自己的配置里单独指定代理地址。

**Q：节点怎么选？手动选了重启会丢吗？**

A：不会丢。配置文件里 `profile.store-selected: true` 就是保住你手动选的节点。
`US` 分组会自动按延迟挑最快的美国节点，不用每次手动挑。

## 安全提醒

- **这个文件夹里没有任何真实凭据。** 代理地址、密码一律是 `YOUR_*` 占位符。
- 只在你自己的鸭子上填真实信息，填完的配置文件**永远不要**提交到公开仓库。
