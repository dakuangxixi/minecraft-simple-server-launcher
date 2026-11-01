# Minecraft 一键开服启动器

一个给“完全不想背命令行”的人用的 Minecraft 开服工具：新建服务器 → 下载核心 → 一键开服 → 看日志 / 装插件 / 装 Java，全在一个窗口里点完。

- 版本：**1.0**（3.x 那一整串是开发版，统称 Development3.5，见 [CHANGELOG.md](CHANGELOG.md)）
- 平台：Windows 10 / 11
- 形态：单个 `minecraft-simple-server-launcher.py` 文件（约 1 万行），不需要安装器、不写注册表，删掉文件夹就干净了
- 界面：customtkinter；右侧有可折叠的后台任务栏（下载进度、✕ 取消）

## 功能

| 页面 | 能干什么 |
| --- | --- |
| 🖥 服务器 | 多服务器并存：新建 / 导入已有服务端文件夹（原地使用，不动你的文件）/ 重命名 / 删除进回收站 / 切换当前服务器 |
| 🏠 概览 | 一键启动 / 停止，看核心版本、内存、端口、在线人数 |
| 🌐 联机 | 自动检测本机地址、一键开放 Windows 防火墙端口、复制连接地址 |
| 📁 文件 | 浏览服务端目录，核心 / 插件 / 存档一目了然 |
| 📥 下载核心 | Vanilla / Paper / Purpur / Fabric 官方源直下；多连接加速 + 断点续传 + 校验；**默认新建服务器，不会覆盖现有核心**；也能检查已有服务器的核心更新（旧核心存 `server.jar.bak`） |
| 🧩 插件 / 模组 | Modrinth + Hangar 搜索，按游戏版本 / 加载器筛选，直接装进 `plugins/`、`mods/`、`world/datapacks/` |
| ⚙ 配置 | `server.properties` 表单化（属性表跟着服务端版本走），写入前自动备份 |
| 🔧 设置 | 主题 / 缩放 / Java 路径；一键安装 JRE（Adoptium + 清华镜像，sha256 校验，装完会真跑一次 `java -version`） |
| 💻 控制台 | 彩色日志、常见崩溃自动诊断（直接给结论，不猜谜）、玩家加入/退出提示、查看玩家背包（离线读 `world/playerdata`） |
| 🎨 文字 | Minecraft 颜色代码（`&a` 这种）编辑 + 实时预览，用来做 MOTD / 告示牌文本 |

## 怎么跑（源码方式）

需要 Python 3.10+（开发环境是 3.14）。

```bat
pip install -r requirements.txt
python minecraft-simple-server-launcher.py
```

首次运行会在 `minecraft-simple-server-launcher.py` 同目录创建：

```
servers/               每台服务器一个文件夹（存档、插件、核心都在里面）
launcher_settings.json 启动器设置（含本机 Java 路径）
.trash/                删除的服务器先挪到这里，可恢复
```

> 这些**都是运行时数据，不要提交到 git**（`.gitignore` 已经排除了）。
> 也可以直接从「🖥 服务器」页导入你已有的服务端文件夹，启动器不会搬动或改写它。

## 打包成 exe

```bat
pip install pyinstaller
pyinstaller wow.spec
```

产物是 `dist/wow.exe`（单文件、带控制台）。第一次启动会比源码慢几秒（解包），内存也会高一些。

## 网络说明

程序会访问这些地方，全都不需要登录：

- GitHub API / Paper API / Purpur API / Fabric Meta / Mojang —— 查版本、下核心
- Modrinth API、Hangar API —— 搜插件
- `mirrors.tuna.tsinghua.edu.cn` / `api.adoptium.net` —— 一键装 Java

国内网络下官方源可能很慢，Java 安装已经默认走清华镜像；核心下载有多连接加速，失败可以断点续传。

## 已知限制

- 只支持 Windows（大量用到 `netsh`、`taskkill`、进程路径查询等 Windows 能力）
- 单文件、没有自动化测试目录；作者是边学边写的，代码风格以“能跑”为先
- 目前没有启动器自更新，升级方式就是换掉 `minecraft-simple-server-launcher.py` / `wow.exe`

## 为什么是单文件（约 1 万行）

这是刻意的取舍，不是没拆：

- **用户侧**：复制一个 `minecraft-simple-server-launcher.py` 就能跑，不用理解项目结构；打包 exe 也只要一个入口
- **作者侧**：作者是边学边写的，单文件改一处不用在十几个文件之间跳，好掌控
- **代价**：文件长、不同时期写的命名和注释风格不完全统一。如果你要基于它二次开发，建议按功能找函数（每个功能区都有 `# ==================== xxx ====================` 分隔），不要从头读
- **没有自带自动化测试**：开发期的验证脚本是临时的，没有放进仓库；这个仓库只放能直接跑的东西

## 许可

MIT，见 [LICENSE](LICENSE)。Minecraft 是 Mojang Studios 的商标，本项目与 Mojang 无关。
