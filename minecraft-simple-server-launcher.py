"""
Minecraft 轮椅级一键开服启动器 1.0
依赖: pip install customtkinter pillow （拖拽另需 tkinterdnd2，可选）
运行: python minecraft-simple-server-launcher.py

版本线：3.x 那一整串（v3.0 ~ v3.5.17）都是开发版，统称 Development3.5；
        1.0 是第一个正式版。下面的更新记录保留原样，都是开发期写下的。

v3.5 更新（0-9 降低空闲时的资源占用）：
- 【性能】5 条独立轮询链（日志 100ms / 进程 500ms / 概览 1500ms / 状态栏 2000ms /
  懒加载 120ms）合并成 1 条统一心跳：服务端在跑·启动中 100ms（日志跟手），
  空闲且窗口在前台 500ms，窗口切到后台或最小化 2000ms，用户一动手立刻回快档。
  实测空闲 10 秒的轮询回调次数：217 次 → 102 次（前台）/ 32 次（后台）
- 【性能】状态栏与概览的文字标签「内容没变就不重绘」（Tk 每次 configure 都要重排重绘）
- 【性能】概览读 server.properties 取端口会按 (路径, 修改时间, 大小) 缓存，不再每 1.5 秒读盘
- 【修复】老的 5 条轮询链里任何一条抛异常就永久停摆；现在每个活单独 try，互不牵连

v3.3 更新：
- 【新功能】一键更新：插件/模组按 Modrinth 项目记录比对最新版本，没有记录的 jar 用文件
  sha1 反查项目；一键升级并替换旧文件。每个服务器可单独开关自动更新（插件/模组），
  切换服务器时自动执行
- 【新功能】MOD 打包：一键把 mods/ 与 config/ 打成 zip 放到 exports/，文件页可查看、删除
- 【新功能】控制台常用指令下拉栏：可收藏当前指令、可删除，存 console_cmds.json
- 【新功能】「🔧 设置」页 = 启动器设置（Java 路径 / JVM 参数 / 外观 / 启动检查更新）
  + 服务器设置（该服自动更新开关、该服内存、该服 JVM 参数），启动命令会真正使用它们
- 【新功能】「⚙ 配置」页改成完整 server.properties 编辑器：内置 58 项属性表（含
  enforce-secure-profile / hide-online-players / log-ips / pause-when-empty-seconds /
  accepts-transfers / region-file-compression 等新版本键），按服务端游戏版本自动增减；
  文件里已有的其它键也会照原样显示，不会被丢掉；切换服务器会按新版本重建
- 【新功能】下载界面筛选：游戏版本 / 加载器 / 排序（下载量·最近更新·最新发布·相关度）
  +「只看适配当前核心」开关，筛选条件直接进 Modrinth 请求
- 【新功能】核心一键更新：用远端校验值（Paper sha256 / Purpur md5 / 原版 sha1）比对本地
  server.jar，精确判断是不是最新构建，一键升级（旧核心自动存成 server.jar.bak）；
  打开「核心自动更新」开关后，切换服务器时会自动完成
- 【性能】启动加速：标签页懒加载（启动只构建 2 个页面，控件构建时间约省 40%），
  版本列表与 Modrinth 请求推迟到首次打开对应页面时才发起
- 【修复】懒加载带来的连环崩溃：控制台日志先缓存后补写、配置页未建时不读写 properties、
  切换服务器时不再访问未构建的控件

v3.2 更新：
- 【新功能】「🌐 联机」页：自动检测内网 IPv4 / 公网 IPv4 / IPv6，一键复制连接地址；
  一键开放 Windows 防火墙端口（非管理员会自动弹 UAC 提权）；
  联机设置（server-ip / 端口 / 正版验证）直接写进 server.properties；
  并给出人话建议（IPv6 直连可行、CGNAT 大内网、online-mode 正版验证等）
- 【新功能】可以把任意文件夹「📂 指定为服务器」原地使用（不动你的文件），
  也可以「📦 导入（复制进来）」复制一份到 servers/
- 【新功能】服务器识别内置 6 种算法，应对不同部署方案：
  ①目录结构（server.jar / Forge 的 libraries+run 布局）
  ②jar 文件名（paper/purpur/spigot/fabric/forge/neoforge/mohist… + 版本号）
  ③jar 内部元数据（version.json、patch.properties、pom.properties、MANIFEST.MF）
  ④logs/latest.log 头部（现存服务器最可靠）
  ⑤启动脚本 .bat/.sh 里的 -jar 与 -Xmx
  ⑥配置文件与目录特征（server.properties 端口、world/、eula.txt、plugins/mods 数量）
- 【新功能】底部常驻状态栏显示 CPU、内存占用；服务端运行时额外显示它的内存
  （纯 ctypes 调 Win32 API，没有新增第三方依赖）
- 【新功能】拖拽 / 选择文件导入：自动识别是插件(plugin.yml)、模组
  (fabric.mod.json / mods.toml)、还是服务端核心；认不出来就问你；zip 可选解压或存为备份
- 【安全】外部文件夹只登记路径：删除时只从列表移除，绝不删除你的文件

v3.0 更新：
- 【新功能】多服务器管理：每个服务器一个独立目录 servers/<名称>/，各自拥有核心、插件、
  模组、配置与存档，互不覆盖；支持新建 / 切换 / 重命名 / 删除，删除先移入回收站可恢复；
  老版本遗留的 mc_server 目录会自动迁移成 servers/默认服务器/
- 【新功能】文件管理页面：查看并删除已装插件/模组、打开服务器文件夹、一键备份与恢复 world
  存档（zip）、查看与删除服务端核心、查看各部分占用空间
- 【性能】列表滚动大幅优化（实测，3 轮取中位数）：滚轮每格从 20 像素提升到 80 像素；
  每格重绘耗时 24.17ms → 约 1.0ms（约 24 倍）；综合滚动速度提升约 95 倍
- 【性能】结果行控件扁平化（去掉两层嵌套 CTkFrame，改用 grid 排布，Tk 控件数 421→381）
- 【性能】封面改为固定 3 线程池 + 缩略图缓存，翻页不再重复下载和重复缩放图片
- 【修复】翻页后旧行的封面回填会操作已销毁的控件（现在先判断控件是否还存在）
- 【改进】切换服务器时自动清空控制台、重新读取该服务器的配置与核心信息

v2.9 更新（本次修复）：
- 【关键修复】Paper 版本列表改为数字排序：原字符串排序会把 1.9/1.8/1.7 排到 1.21 前面，
  导致下拉框顺序错乱、且 1.13 及更早版本被截断而选不到；同时过滤掉 -rc/-pre 预发布版
- 【关键修复】中文 Windows 控制台 GBK 编码下，print 里的 ✅/❌/⚠ 会抛 UnicodeEncodeError
  把后台线程直接搞死（表现：封面永远加载不出来、错误提示卡在“加载中…”），现已统一兜底
- 【修复】服务器目录不再随“当前工作目录”漂移，换启动方式也不会“丢存档”
- 【新增】启动前按游戏版本校验 Java（1.20.5+ 需 Java 21，1.16 及更早需 Java 8）
- 【改进】不再静默替用户同意 EULA；内存填写增加合法性校验
- 【改进】服务端强制 UTF-8 输出，中文日志不再乱码；头像颜色不再每次随机变化

v2.8 更新：
- 【关键修复】Paper 核心全面迁移至 Fill v3 API，解决 HTTP 410 Gone 报错
- Paper 版本列表和下载链接均使用 fill.papermc.io/v3
- User-Agent 已填写联系方式，符合 Fill v3 API 要求
"""

import customtkinter as ctk
import subprocess
import sys
import threading
import queue
import json
import ssl
import re
import io
import importlib
import os
import socket
import shutil
import time
import hashlib
import zipfile
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error
import tkinter
import tkinter.font
from tkinter import messagebox, filedialog
from pathlib import Path

# ==================== 控制台编码兜底 ====================
# v2.9 修复：中文 Windows 控制台默认 GBK，程序里 print 的 ✅/❌/⚠ 等字符无法编码，
# 会抛 UnicodeEncodeError 把后台线程直接搞死（表现：封面永远加载不出来、
# 错误提示卡在“加载中…”）。这里改成出错字符用 ? 代替，保证 print 永不抛异常。
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except Exception:
        pass

# ==================== 全局禁用 SSL 验证 ====================
try:
    ssl._create_default_https_context = ssl._create_unverified_context
    print("[启动器] 已关闭 SSL 证书验证（用于兼容本机缺根证书的环境）")
except Exception as _e:
    print(f"[启动器] 无法修改默认 SSL 上下文: {_e}")

# ==================== Pillow 可选依赖 + 自动安装 ====================
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    Image = None
    HAS_PIL = False

_pillow_checked = False


def ensure_pillow():
    global HAS_PIL, Image, _pillow_checked
    if getattr(sys, "frozen", False):
        # 打包成 exe 后 sys.executable 就是 exe 自己，pip 装不了，直接跳过
        _pillow_checked = True
        return HAS_PIL
    if _pillow_checked:
        return HAS_PIL
    _pillow_checked = True

    if HAS_PIL:
        return True

    print("[启动器] 未检测到 Pillow，正在自动安装（首次可能需要 10~30 秒）...")

    attempts = [
        [sys.executable, "-m", "pip", "install", "pillow",
         "--quiet", "--disable-pip-version-check"],
        [sys.executable, "-m", "pip", "install", "pillow",
         "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
         "--quiet", "--disable-pip-version-check"],
    ]

    for i, cmd in enumerate(attempts, 1):
        try:
            print(f"[启动器] 尝试第 {i} 次安装...")
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=300, **hidden_console_kwargs())
            if result.returncode != 0:
                print(f"[启动器] pip 返回码 {result.returncode}")
                if result.stderr:
                    print(f"[启动器] {result.stderr[:400]}")
                continue

            importlib.invalidate_caches()
            for mod in ("PIL", "PIL.Image", "PIL.ImageTk"):
                if mod in sys.modules:
                    del sys.modules[mod]

            from PIL import Image as PILImage  # noqa
            Image = PILImage
            HAS_PIL = True
            print("[启动器] ✅ Pillow 安装成功！封面已启用。")
            return True
        except Exception as e:
            print(f"[启动器] 第 {i} 次安装失败: {e}")

    print("[启动器] ❌ 自动安装 Pillow 失败。可在终端手动执行: pip install pillow")
    return False


# ==================== 全局配置 ====================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==================== 平滑滚动 (v3.1) ====================
def _install_smooth_scroll():
    """把 customtkinter 的“一格直接跳 80 像素”换成带缓动的平滑滚动。

    注意：CTkScrollableFrame.__init__ 里用 self._mouse_wheel_all 注册了 bind_all，
    已经绑定的回调改不了，所以要在创建窗口之前替换掉这个类方法——
    这样整个程序所有 CTkScrollableFrame 都自动变成平滑滚动，一劳永逸。
    """
    def _smooth_tick(self):
        try:
            if not self.winfo_exists():
                self._smooth_running = False
                return
            pending = getattr(self, "_smooth_pending", 0.0)
            if abs(pending) < 0.5:
                self._smooth_pending = 0.0
                self._smooth_running = False
                return
            # 缓动：每帧走剩余距离的 35%，并限制单帧上限，越接近目标越慢
            step = max(-26.0, min(26.0, pending * 0.35))
            units = int(round(step))
            if units == 0:
                units = 1 if step > 0 else -1
            self._parent_canvas.yview_scroll(units, "units")
            self._smooth_pending = pending - units
            self.after(16, self._smooth_tick)          # ≈60 FPS
        except Exception:
            self._smooth_running = False

    def _smooth_wheel(self, event):
        try:
            if not self._check_if_valid_scroll(event.widget):
                return
        except Exception:
            pass

        canvas = self._parent_canvas
        try:
            canvas.configure(yscrollincrement=2)       # 2 像素/单位，粒度够细才平滑
            if canvas.yview() == (0.0, 1.0):
                return                                 # 没有可滚内容
        except Exception:
            return

        if getattr(event, "num", None) in (4, 5):      # Linux
            notches = 1.0 if event.num == 4 else -1.0
        else:                                          # Windows / macOS
            notches = float(getattr(event, "delta", 0)) / 120.0
        if notches == 0:
            return

        # 一格滚轮 = 40 单位 = 80 像素；连续快滚时距离累加，动画不会互相打架
        self._smooth_pending = (getattr(self, "_smooth_pending", 0.0)
                               - notches * 40.0)
        if not getattr(self, "_smooth_running", False):
            self._smooth_running = True
            self._smooth_tick()

    ctk.CTkScrollableFrame._smooth_tick = _smooth_tick
    ctk.CTkScrollableFrame._mouse_wheel_all = _smooth_wheel


_install_smooth_scroll()

# ==================== 版本 ====================
# 版本线：3.x 那一整串都是开发版，统一叫 Development3.5；
# 1.0 是第一个正式版（功能齐了才发的）。
APP_VERSION = "1.0"

# ==================== 多服务器目录结构 (v3.2) ====================
# 服务器可以是 <工程根>/servers/<名称>/（本启动器管理），
# 也可以是用户指定的任意外部文件夹（原地使用，绝不改动你的文件）。
# 打包成 exe 之后 __file__ 指向 PyInstaller 的临时解包目录（退出即删），
# 必须改成 exe 所在的真实目录，否则 servers/、存档、配置全都留不下来。
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent
    # minecraft-simple-server-launcher.py 目前放在 .venv 里；若检测到脚本位于虚拟环境内，就把数据目录放到工程根目录，
    # 而不是藏进 .venv（PyCharm 会把 .venv 标成 excluded，文件会“找不到”）。
    if (BASE_DIR / "pyvenv.cfg").exists():
        BASE_DIR = BASE_DIR.parent

SERVERS_ROOT = BASE_DIR / "servers"      # 本启动器管理的服务器
TRASH_ROOT = BASE_DIR / ".trash"         # 删除的服务器先挪到这里（可恢复）
SERVERS_INDEX = SERVERS_ROOT / "servers.json"

CURRENT_SERVER = None
SERVER_PATHS = {}                        # 名称 -> 绝对路径（可能是外部目录）

# 下面这些路径由 activate_server() 按“当前服务器”重新绑定。
# 其它方法都是在运行时读取这些全局名，所以切换服务器不需要改别处代码。
SERVER_DIR = SERVERS_ROOT / "默认服务器"
SERVER_JAR = SERVER_DIR / "server.jar"
PLUGINS_DIR = SERVER_DIR / "plugins"
MODS_DIR = SERVER_DIR / "mods"
EULA_FILE = SERVER_DIR / "eula.txt"
PROPERTIES_FILE = SERVER_DIR / "server.properties"
STATE_FILE = SERVER_DIR / "launcher_state.json"


def server_path(name):
    """服务器目录：既支持 servers/ 里的，也支持用户指定的外部文件夹。"""
    p = SERVER_PATHS.get(name)
    return Path(p) if p else (SERVERS_ROOT / name)


def is_external_server(name):
    try:
        return server_path(name).resolve() != (SERVERS_ROOT / name).resolve()
    except Exception:
        return False


def list_servers():
    return sorted(SERVER_PATHS.keys())


def load_index():
    try:
        return json.loads(SERVERS_INDEX.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_index(data=None):
    """保存注册表。兼容旧写法 save_index({"current": x})。"""
    global CURRENT_SERVER
    if isinstance(data, dict) and data.get("current"):
        CURRENT_SERVER = data["current"]
    try:
        SERVERS_ROOT.mkdir(parents=True, exist_ok=True)
        SERVERS_INDEX.write_text(json.dumps(
            {"current": CURRENT_SERVER, "servers": SERVER_PATHS},
            ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[启动器] 保存服务器列表失败: {e}")


def register_server(name, path):
    SERVER_PATHS[name] = str(Path(path).resolve())
    save_index()


def unregister_server(name):
    SERVER_PATHS.pop(name, None)
    save_index()


def unique_server_name(base):
    name = (base or "导入的服务器").strip() or "导入的服务器"
    i = 1
    while name in SERVER_PATHS:
        name = f"{base}_{i}"
        i += 1
    return name


def activate_server(name):
    """把“当前服务器”切换到 name，并重绑所有相关路径全局变量。"""
    global CURRENT_SERVER, SERVER_DIR, SERVER_JAR, PLUGINS_DIR, MODS_DIR
    global EULA_FILE, PROPERTIES_FILE, STATE_FILE
    CURRENT_SERVER = name
    SERVER_DIR = server_path(name)
    SERVER_JAR = SERVER_DIR / "server.jar"
    PLUGINS_DIR = SERVER_DIR / "plugins"
    MODS_DIR = SERVER_DIR / "mods"
    EULA_FILE = SERVER_DIR / "eula.txt"
    PROPERTIES_FILE = SERVER_DIR / "server.properties"
    STATE_FILE = SERVER_DIR / "launcher_state.json"
    SERVER_DIR.mkdir(parents=True, exist_ok=True)
    return SERVER_DIR


def bootstrap_servers():
    """建立 servers/、迁移老 mc_server、把 servers/ 下已有目录收进注册表。"""
    SERVERS_ROOT.mkdir(parents=True, exist_ok=True)
    idx = load_index()
    saved = idx.get("servers")
    if isinstance(saved, dict):
        for k, v in saved.items():
            try:
                SERVER_PATHS[str(k)] = str(v)
            except Exception:
                pass

    found = sorted([p.name for p in SERVERS_ROOT.iterdir() if p.is_dir()])
    if not found and not SERVER_PATHS:
        for cand in (BASE_DIR / "mc_server", Path.cwd() / "mc_server"):
            if cand.exists() and cand.is_dir():
                try:
                    shutil.move(str(cand),
                                str(SERVERS_ROOT / "默认服务器"))
                    print(f"[启动器] 已把老目录 {cand.name}/ 迁移为 "
                          f"servers/默认服务器/")
                except Exception as e:
                    print(f"[启动器] ⚠ 迁移老目录失败: {e}")
                break

    # v3.3：你手动删掉的 servers/xxx 目录，别再被登记表“复活”成空服务器
    for k in list(SERVER_PATHS):
        try:
            p = Path(SERVER_PATHS[k])
            is_internal = p.resolve().parent == SERVERS_ROOT.resolve()
        except Exception:
            continue
        if is_internal and not p.exists():
            SERVER_PATHS.pop(k, None)

    found = sorted([p.name for p in SERVERS_ROOT.iterdir() if p.is_dir()])
    for n in found:
        SERVER_PATHS.setdefault(n, str((SERVERS_ROOT / n).resolve()))
    if not SERVER_PATHS:
        d = SERVERS_ROOT / "默认服务器"
        d.mkdir(parents=True, exist_ok=True)
        SERVER_PATHS["默认服务器"] = str(d.resolve())

    current = idx.get("current")
    if current not in SERVER_PATHS:
        current = sorted(SERVER_PATHS)[0]
    activate_server(current)
    save_index()
    return current


# ==================== 服务器识别：多种算法（v3.2） ====================
# 应对不同部署方案：①目录结构 ②jar 文件名 ③jar 内部元数据
# ④logs/latest.log ⑤启动脚本(.bat/.sh) ⑥配置文件与目录特征
CORE_BY_NAME = [
    (r"purpur", "purpur"), (r"paper", "paper"), (r"spigot", "spigot"),
    (r"craftbukkit|bukkit", "bukkit"), (r"fabric", "fabric"),
    (r"neoforge", "neoforge"), (r"forge", "forge"), (r"mohist", "mohist"),
    (r"magma", "magma"), (r"arclight", "arclight"),
    (r"minecraft_server|^server(\.jar)?$", "vanilla"),
]
MC_VER_RE = re.compile(r"(\d+\.\d+(?:\.\d+)?)")
PLUGIN_MARKERS = ("plugin.yml", "paper-plugin.yml", "bungee.yml",
                  "velocity-plugin.json")
MOD_MARKERS = (("fabric.mod.json", "fabric"),
               ("META-INF/mods.toml", "forge"),
               ("META-INF/neoforge.mods.toml", "neoforge"))


def _core_from_name(name):
    low = str(name).lower()
    for pat, core in CORE_BY_NAME:
        if re.search(pat, low):
            return core
    return None


def _zip_names(path, limit=6000):
    try:
        with zipfile.ZipFile(path) as zf:
            return set(zf.namelist()[:limit])
    except Exception:
        return set()


def jar_features(path):
    """看 jar 内部特征文件，判断是插件还是模组。"""
    info = _zip_names(path)
    if not info:
        return None, None
    for m in PLUGIN_MARKERS:
        if m in info:
            return "plugin", m
    for m, kind in MOD_MARKERS:
        if m in info:
            return "mod", f"{m}（{kind}）"
    low = [n.lower() for n in list(info)[:3000]]
    if any(n.startswith("net/fabricmc/") for n in low):
        return "mod", "net/fabricmc/ 类路径"
    return None, None


def _jar_meta(path):
    """算法③：读 jar 内部元数据（version.json / patch.properties / pom / MANIFEST）。"""
    out = {"core": None, "version": None, "evidence": []}
    info = _zip_names(path)
    if not info:
        return out
    try:
        with zipfile.ZipFile(path) as zf:
            for cand in ("version.json", "META-INF/version.json"):
                if cand in info:
                    try:
                        data = json.loads(zf.read(cand).decode("utf-8", "ignore"))
                        if data.get("id"):
                            out["version"] = data["id"]
                            out["evidence"].append(f"jar 内 {cand}")
                    except Exception:
                        pass
            if "patch.properties" in info:
                try:
                    txt = zf.read("patch.properties").decode("utf-8", "ignore")
                    m = re.search(r"^version=(.+)$", txt, re.M)
                    if m:
                        out["version"] = m.group(1).strip()
                        out["core"] = out["core"] or "paper"
                        out["evidence"].append("jar 内 patch.properties")
                except Exception:
                    pass
            for n in list(info):
                if n.endswith("pom.properties") and "paper" in n.lower():
                    try:
                        txt = zf.read(n).decode("utf-8", "ignore")
                        m = re.search(r"^version=(.+)$", txt, re.M)
                        if m:
                            out["version"] = m.group(1).strip()
                            out["core"] = "paper"
                            out["evidence"].append("jar 内 pom.properties")
                    except Exception:
                        pass
            if "META-INF/MANIFEST.MF" in info:
                txt = zf.read("META-INF/MANIFEST.MF").decode(
                    "utf-8", "ignore").lower()
                for key in ("purpur", "paper", "spigot", "bukkit",
                            "neoforge", "forge", "fabric"):
                    if key in txt:
                        out["core"] = out["core"] or key
                        out["evidence"].append("jar 内 MANIFEST.MF")
                        break
    except Exception:
        pass
    return out


def _detect_by_logs(folder):
    """算法④：读 logs/latest.log 头部（现存服务器最可靠的依据）。"""
    f = folder / "logs" / "latest.log"
    if not f.exists():
        return {"core": None, "version": None, "evidence": []}
    try:
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            head = "".join(fh.readline() for _ in range(40))
    except Exception:
        return {"core": None, "version": None, "evidence": []}
    low = head.lower()
    core = None
    for key in ("purpur", "paper", "spigot", "craftbukkit", "fabric",
                "neoforge", "forge", "mohist", "magma", "arclight"):
        if key in low:
            core = key
            break
    m = re.search(r"(?:version|minecraft)\s+(\d+\.\d+(?:\.\d+)?)", head, re.I)
    if not m:
        m = MC_VER_RE.search(head)
    return {"core": core, "version": m.group(1) if m else None,
            "evidence": ["logs/latest.log"]}


def _detect_by_scripts(folder):
    """算法⑤：解析启动脚本里的 -jar 与 -Xmx。"""
    out = {"jar": None, "xmx": None, "evidence": []}
    for pat in ("*.bat", "*.cmd", "*.sh"):
        for f in sorted(folder.glob(pat))[:6]:
            try:
                txt = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            m = re.search(r'-jar\s+"?([^"\s]+\.jar)', txt)
            if m and not out["jar"]:
                out["jar"] = m.group(1).replace("\\", "/").split("/")[-1]
                out["evidence"].append(f.name)
            m = re.search(r"-Xmx(\d+[MGg])", txt)
            if m and not out["xmx"]:
                out["xmx"] = m.group(1)
    return out


def detect_server_folder(folder):
    """综合 6 种算法识别一个文件夹：是不是服务器、什么核心、什么版本。"""
    folder = Path(folder)
    rep = {"path": str(folder), "is_server": False, "layout": "未知",
           "core": None, "version": None, "jar": None, "evidence": [],
           "plugins": 0, "mods": 0, "has_world": (folder / "world").is_dir(),
           "has_eula": (folder / "eula.txt").exists(),
           "has_properties": (folder / "server.properties").exists(),
           "port": None, "notes": []}

    # ① 目录结构
    if (folder / "server.jar").exists():
        rep["layout"] = "标准（server.jar 在根目录）"
        rep["jar"] = "server.jar"
    elif (folder / "libraries").is_dir() and (
            (folder / "run.bat").exists() or (folder / "run.sh").exists()
            or (folder / "user_jvm_args.txt").exists()):
        rep["layout"] = "Forge/NeoForge 现代布局（libraries/ + run 脚本）"
        rep["is_server"] = True
    else:
        rep["layout"] = "根目录没有 server.jar，用其它算法继续找"

    # ② jar 文件名（最多往下找 2 层）
    jars = []
    for depth in (0, 1, 2):
        try:
            pattern = "/".join(["*"] * depth + ["*.jar"]) if depth else "*.jar"
            jars = [p for p in folder.glob(pattern) if p.is_file()]
        except Exception:
            jars = []
        if jars:
            break
    server_jars = [j for j in jars if _core_from_name(j.name)]
    if not rep["jar"] and server_jars:
        rep["jar"] = str(server_jars[0].relative_to(folder))
        rep["is_server"] = True
        rep["notes"].append(f"按文件名找到核心: {server_jars[0].name}")

    target = (folder / rep["jar"]) if rep["jar"] else (
        server_jars[0] if server_jars else None)

    # ③ jar 内部元数据 + ②b 文件名里的版本
    if target is not None and target.exists():
        meta = _jar_meta(target)
        rep["core"] = meta["core"]
        rep["version"] = meta["version"]
        rep["evidence"] += meta["evidence"]
        if not rep["version"]:
            m = MC_VER_RE.search(target.name)
            if m:
                rep["version"] = m.group(1)
                rep["evidence"].append(f"文件名 {target.name}")
        if not rep["core"]:
            rep["core"] = _core_from_name(target.name)

    # ④ 日志
    logs = _detect_by_logs(folder)
    if logs["core"] or logs["version"]:
        rep["core"] = rep["core"] or logs["core"]
        rep["version"] = rep["version"] or logs["version"]
        rep["evidence"] += logs["evidence"]
        rep["is_server"] = True

    # ⑤ 启动脚本
    scr = _detect_by_scripts(folder)
    if scr["jar"]:
        rep["notes"].append(f"启动脚本引用 {scr['jar']}"
                            + (f"，内存 {scr['xmx']}" if scr["xmx"] else ""))
        rep["evidence"] += scr["evidence"]
        rep["is_server"] = True
        if rep["layout"].startswith("根目录没有") or rep["layout"] == "未知":
            rep["layout"] = f"启动脚本布局（引用 {scr['jar']}）"
        if not rep["jar"]:
            rep["jar"] = scr["jar"]
        if not rep["core"]:
            rep["core"] = _core_from_name(scr["jar"])

    # ⑥ 目录 / 配置文件
    for d, key in (("plugins", "plugins"), ("mods", "mods")):
        p = folder / d
        if p.is_dir():
            rep[key] = len([x for x in p.iterdir() if x.is_file()])
    if rep["has_properties"]:
        try:
            for line in (folder / "server.properties").read_text(
                    encoding="utf-8", errors="ignore").splitlines():
                if line.strip().startswith("server-port="):
                    rep["port"] = line.split("=", 1)[1].strip()
        except Exception:
            pass
    if rep["has_world"] or rep["has_eula"] or rep["has_properties"]:
        rep["is_server"] = True
    if not rep["core"] and rep["mods"] and not rep["plugins"]:
        rep["core"] = "fabric/forge（只有 mods/，通常是模组服）"
    return rep


def format_server_report(rep):
    lines = [f"目录: {rep['path']}",
             f"判定: {'看起来是服务器' if rep['is_server'] else '不太像服务器目录'}",
             f"布局: {rep['layout']}"]
    if rep["core"]:
        lines.append("核心: " + str(rep["core"])
                     + (f" {rep['version']}" if rep["version"] else ""))
    if rep["jar"]:
        lines.append(f"核心文件: {rep['jar']}")
    if rep["evidence"]:
        lines.append("识别依据: " + "、".join(dict.fromkeys(rep["evidence"])))
    lines.append(f"内容: plugins/ {rep['plugins']} 个 · mods/ {rep['mods']} 个"
                 + (" · world/ ✓" if rep["has_world"] else "")
                 + (" · eula.txt ✓" if rep["has_eula"] else "")
                 + (f" · 端口 {rep['port']}" if rep["port"] else ""))
    for n in rep["notes"]:
        lines.append("备注: " + n)
    return "\n".join(lines)


def classify_file(path):
    """判断拖进来 / 选中的文件是什么，并给出建议去向。"""
    p = Path(path)
    if p.is_dir():
        return {"kind": "folder", "detail": "文件夹"}
    ext = p.suffix.lower()
    if ext == ".jar":
        kind, why = jar_features(p)
        if kind == "plugin":
            return {"kind": "plugin", "detail": f"检测到 {why}",
                    "target": "plugins/"}
        if kind == "mod":
            return {"kind": "mod", "detail": f"检测到 {why}", "target": "mods/"}
        meta = _jar_meta(p)
        core = meta["core"] or _core_from_name(p.name)
        if core:
            return {"kind": "core", "core": core, "version": meta["version"],
                    "detail": f"像 {core} 服务端核心", "target": "server.jar"}
        return {"kind": "unknown_jar", "detail": "看不出是插件、模组还是核心"}
    if ext == ".zip":
        return {"kind": "zip", "detail": "压缩包（可能是存档/整合包）"}
    if ext == ".properties":
        return {"kind": "properties", "detail": "配置文件",
                "target": "server.properties"}
    if ext == ".txt":
        return {"kind": "text", "detail": "文本文件"}
    return {"kind": "other", "detail": f"未识别的类型 {ext or '(无扩展名)'}"}


# ==================== CPU / 内存监控（纯 ctypes，无新依赖） ====================
try:
    import ctypes
    from ctypes import wintypes

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _psapi = ctypes.WinDLL("psapi", use_last_error=True)

    class _MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [("dwLength", wintypes.DWORD),
                    ("dwMemoryLoad", wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

    class _FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD),
                    ("dwHighDateTime", wintypes.DWORD)]

    _HAS_WINAPI = True
except Exception:
    _HAS_WINAPI = False


def ram_info():
    """(已用字节, 总字节, 百分比)；非 Windows 返回 None。"""
    if not _HAS_WINAPI:
        return None
    st = _MEMORYSTATUSEX()
    st.dwLength = ctypes.sizeof(_MEMORYSTATUSEX)
    if not _k32.GlobalMemoryStatusEx(ctypes.byref(st)):
        return None
    total = st.ullTotalPhys
    used = total - st.ullAvailPhys
    return used, total, (used / total * 100 if total else 0.0)


_CPU_LAST = {"idle": None, "busy": None}


def cpu_percent():
    """整体 CPU 使用率（两次采样求差）；第一次调用返回 None。"""
    if not _HAS_WINAPI:
        return None
    try:
        idle, kernel, user = _FILETIME(), _FILETIME(), _FILETIME()
        if not _k32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel),
                                   ctypes.byref(user)):
            return None

        def _ft(f):
            return (f.dwHighDateTime << 32) | f.dwLowDateTime

        i, busy = _ft(idle), _ft(kernel) + _ft(user)
        prev_i, prev_b = _CPU_LAST["idle"], _CPU_LAST["busy"]
        _CPU_LAST["idle"], _CPU_LAST["busy"] = i, busy
        if prev_i is None:
            return None
        di, db = i - prev_i, busy - prev_b
        if db <= 0:
            return None
        return max(0.0, min(100.0, (1 - di / db) * 100))
    except Exception:
        return None


def process_ram_mb(pid):
    """某个进程占用的物理内存（MB）。"""
    if not _HAS_WINAPI or not pid:
        return None
    try:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

        class _PMC(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD),
                        ("PageFaultCount", wintypes.DWORD),
                        ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]

        h = _k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False,
                             int(pid))
        if not h:
            return None
        try:
            pmc = _PMC()
            pmc.cb = ctypes.sizeof(_PMC)
            if _psapi.GetProcessMemoryInfo(h, ctypes.byref(pmc), pmc.cb):
                return pmc.WorkingSetSize / 1024 / 1024
        finally:
            _k32.CloseHandle(h)
    except Exception:
        pass
    return None


# ==================== v3.5.12：识别"启动器关了但服务端还在跑"的幽灵进程 ====================
def pid_alive(pid):
    """这个 PID 还活着吗？"""
    if not pid or os.name != "nt":
        return False
    try:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = _k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False,
                             int(pid))
        if not h:
            return False
        try:
            code = wintypes.DWORD()
            if not _k32.GetExitCodeProcess(h, ctypes.byref(code)):
                return False
            return code.value == 259        # STILL_ACTIVE
        finally:
            _k32.CloseHandle(h)
    except Exception:
        return False


def pid_image_name(pid):
    """进程的可执行文件全路径（拿不到返回空串）。"""
    if not pid or os.name != "nt":
        return ""
    try:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = _k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False,
                             int(pid))
        if not h:
            return ""
        try:
            buf = ctypes.create_unicode_buffer(1024)
            size = wintypes.DWORD(1024)
            if not _k32.QueryFullProcessImageNameW(h, 0, buf,
                                                   ctypes.byref(size)):
                return ""
            return buf.value
        finally:
            _k32.CloseHandle(h)
    except Exception:
        return ""


def looks_like_java(pid):
    """是不是 java.exe / javaw.exe（用来确认"这个 PID 还真的是服务端"）。"""
    name = Path(pid_image_name(pid)).name.lower() if pid_image_name(pid) else ""
    return name in ("java.exe", "javaw.exe")


# ==================== 启动器设置 / 常用指令 / 更新（v3.3） ====================
LAUNCHER_SETTINGS_FILE = BASE_DIR / "launcher_settings.json"
CONSOLE_CMDS_FILE = BASE_DIR / "console_cmds.json"
EXPORTS_DIR = BASE_DIR / "exports"

DEFAULT_LAUNCHER_SETTINGS = {
    "java_path": "java",
    "jvm_args": "",
    "default_min_mem": 2,
    "default_max_mem": 4,
    "appearance": "dark",
    "auto_check_update": True,
}

DEFAULT_CONSOLE_CMDS = [
    "list", "say ", "op ", "deop ", "gamemode creative ", "gamemode survival ",
    "time set day", "time set night", "weather clear", "weather rain",
    "whitelist add ", "whitelist list", "kick ", "ban ", "save-all",
    "difficulty peaceful", "tp ", "stop",
    # v3.4：补一批常用且新手最需要的
    "whitelist on", "whitelist off", "pardon ", "gamerule keepInventory true",
    "seed", "plugins", "tps", "reload confirm",
]

# 指令中文说明（v3.4）：键 -> (这指令干嘛的, 用法)
# 支持前缀匹配：输入 "gamemode" 或 "gam" 都能查到
CMD_DESCRIPTIONS = {
    "list": ("列出当前在线的玩家", "list"),
    "say": ("全服广播一句话，所有人聊天框都能看到", "say <内容>"),
    "tell": ("单独给某个玩家发消息", "tell <玩家名> <内容>"),
    "op": ("把玩家设为管理员（能用全部指令）", "op <玩家名>"),
    "deop": ("取消管理员权限", "deop <玩家名>"),
    "gamemode": ("切换游戏模式", "gamemode <survival|creative|adventure|spectator> [玩家名]"),
    "time set": ("设置世界时间", "time set <day|night|noon|midnight>"),
    "weather": ("设置天气", "weather <clear|rain|thunder> [秒数]"),
    "whitelist add": ("把玩家加入白名单", "whitelist add <玩家名>"),
    "whitelist list": ("查看白名单里有谁", "whitelist list"),
    "whitelist on": ("开启白名单：只有名单内的人能进", "whitelist on"),
    "whitelist off": ("关闭白名单：谁都能进", "whitelist off"),
    "kick": ("把玩家踢下线（他还能重新进）", "kick <玩家名> [原因]"),
    "ban": ("封禁玩家（再也进不来）", "ban <玩家名> [原因]"),
    "pardon": ("解除封禁", "pardon <玩家名>"),
    "save-all": ("立刻把世界存档写到磁盘，防回档", "save-all"),
    "difficulty": ("设置游戏难度", "difficulty <peaceful|easy|normal|hard>"),
    "tp": ("传送玩家或实体", "tp <目标> 或 tp <玩家> <目标>"),
    "stop": ("安全关服：先存档再退出（别用窗口右上角的叉）", "stop"),
    "gamerule keepInventory": ("死亡不掉落物品", "gamerule keepInventory true"),
    "gamerule": ("查看或修改游戏规则", "gamerule <规则名> [true|false]"),
    "seed": ("查看当前世界的种子", "seed"),
    "plugins": ("列出已安装的插件", "plugins"),
    "tps": ("查看服务器流畅度（Paper/Purpur 才有）", "tps"),
    "reload confirm": ("重载插件配置（Paper 必须带 confirm）", "reload confirm"),
    "help": ("查看服务端自带的指令帮助", "help [指令名]"),
}


def describe_command(cmd):
    """给一条指令配中文说明。两条规则：

    ① 你输入的以某个说明键开头（＝你打的是完整指令，比如 "gamerule keepInventory true"）
       → 取**最长**的键，说明最具体；
    ② 某个说明键以你输入的开头（＝你还没打完，比如 "gam"）
       → 取**最短**的键，最接近你要找的（gam → gamemode，而不是 gamerule keepInventory）。
    """
    c = (cmd or "").strip().lower()
    if not c:
        return None
    # 大小写不敏感（键里有 gamerule keepInventory 这种大写）
    table = {k.lower(): v for k, v in CMD_DESCRIPTIONS.items()}
    if c in table:
        return table[c]
    pref = [k for k in table if c.startswith(k)]
    if pref:
        return table[max(pref, key=len)]
    ext = [k for k in table if k.startswith(c)]
    if ext:
        return table[min(ext, key=len)]
    return None


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path, data):
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        return True
    except Exception as e:
        print(f"[启动器] 写入 {path} 失败: {e}")
        return False


def load_launcher_settings():
    s = dict(DEFAULT_LAUNCHER_SETTINGS)
    s.update(_read_json(LAUNCHER_SETTINGS_FILE, {}) or {})
    return s


def save_launcher_settings(s):
    return _write_json(LAUNCHER_SETTINGS_FILE, s)


# v3.5（⑨）：配色主题 + 界面缩放（这俩要在建窗口之前套用，改完重启生效）
UI_THEMES = {"蓝（默认）": "blue", "深蓝": "dark-blue", "绿": "green"}
UI_THEME_LABELS = {v: k for k, v in UI_THEMES.items()}
UI_SCALES = {"80%": 0.8, "90%": 0.9, "100%": 1.0,
             "110%": 1.1, "120%": 1.2, "130%": 1.3}


def ui_scale_label(v):
    """把 1.2 这种数字换成 "120%" 这样的选项名。"""
    try:
        v = float(v)
    except Exception:
        return "100%"
    return min(UI_SCALES, key=lambda k: abs(UI_SCALES[k] - v))


def apply_ui_theme(settings):
    """按设置套主题与缩放，返回实际缩放倍数。必须在建任何控件之前调用。"""
    theme = str(settings.get("ui_theme", "blue"))
    if theme in ("blue", "dark-blue", "green"):
        try:
            ctk.set_default_color_theme(theme)
        except Exception:
            pass
    try:
        scale = float(settings.get("ui_scale", 1.0) or 1.0)
    except Exception:
        scale = 1.0
    scale = min(1.3, max(0.8, scale))
    try:
        ctk.set_widget_scaling(scale)
        ctk.set_window_scaling(scale)
    except Exception:
        pass
    return scale


def load_console_cmds():
    """读常用指令。

    v3.4：兼容旧格式（纯列表），新格式是 {"cmds": [...], "seeded": [...]}；
    "seeded" 记录已经给过的内置指令 —— 你删掉某条内置指令后，不会被偷偷塞回来。
    """
    data = _read_json(CONSOLE_CMDS_FILE, None)
    if isinstance(data, list):
        cmds, seeded = list(data), []
    elif isinstance(data, dict):
        cmds = list(data.get("cmds") or [])
        seeded = list(data.get("seeded") or [])
    else:
        cmds, seeded = [], []
    if not cmds:
        cmds = list(DEFAULT_CONSOLE_CMDS)
        seeded = list(DEFAULT_CONSOLE_CMDS)
        save_console_cmds(cmds, seeded)
        return cmds
    added = [c for c in DEFAULT_CONSOLE_CMDS
             if c not in seeded and c not in cmds]
    if added:
        cmds.extend(added)
        seeded.extend(added)
        save_console_cmds(cmds, seeded)
    return cmds


def save_console_cmds(cmds, seeded=None):
    if seeded is None:
        seeded = list(DEFAULT_CONSOLE_CMDS)
    return _write_json(CONSOLE_CMDS_FILE, {"cmds": list(cmds),
                                           "seeded": list(seeded)})


def sha1_of(path):
    """文件 sha1，用于向 Modrinth 反查“这个 jar 是哪个项目的哪个版本”。"""
    import hashlib
    h = hashlib.sha1()
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
    except Exception:
        return None
    return h.hexdigest()


def modrinth_versions(slug):
    """取某个 Modrinth 项目的全部版本（查更新用）。"""
    return http_get_json(f"{MODRINTH_API}/project/{slug}/version") or []


def _pub_ts(v):
    try:
        return int(re.sub(r"\D", "", v.get("date_published", ""))[:14] or 0)
    except Exception:
        return 0


def pick_newest_version(versions, game_version=None, loader=None):
    """挑最新的正式版；优先满足 游戏版本+加载器，其次只满足加载器。"""
    def pool(gv, ld):
        out = []
        for v in versions:
            if gv and gv not in v.get("game_versions", []):
                continue
            if ld and ld not in v.get("loaders", []):
                continue
            out.append(v)
        return out

    cands = pool(game_version, loader) or pool(None, loader) or list(versions)
    order = {"release": 0, "beta": 1, "alpha": 2}
    cands.sort(key=lambda v: (order.get(v.get("version_type"), 9),
                              -_pub_ts(v)))
    return cands[0] if cands else None


def installed_file(server_dir=None):
    return (Path(server_dir) if server_dir else SERVER_DIR) / "installed.json"


def load_installed(server_dir=None):
    return _read_json(installed_file(server_dir), {}) or {}


def save_installed(data, server_dir=None):
    return _write_json(installed_file(server_dir), data)


def export_mods_zip(server_dir=None, name=None):
    """把 mods/（连同 config/，如果有）打成 zip 放到 exports/。"""
    server_dir = Path(server_dir) if server_dir else SERVER_DIR
    mods = server_dir / "mods"
    if not mods.is_dir() or not any(mods.iterdir()):
        return None, "mods/ 是空的，没有可打包的模组"
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = EXPORTS_DIR / f"{name or server_dir.name}-mods-{stamp}.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for base in (mods, server_dir / "config"):
            if not base.is_dir():
                continue
            for p in base.rglob("*"):
                if p.is_file():
                    zf.write(p, p.relative_to(server_dir))
                    count += 1
    return out, f"{count} 个文件，{human_size(out.stat().st_size)}"


# ==================== 联机 / 网络助手（v3.2） ====================
FIREWALL_RULE_PREFIX = "MinecraftServerLauncher_"
_PUBLIC_IP_CACHE = {"v4": None, "v6": None}


def get_lan_ip():
    """内网 IPv4（UDP connect 取本机出口地址，不会真的发包）。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None


def get_public_ips(force=False):
    """返回 (公网IPv4, 公网IPv6)，取不到就是 None。"""
    if not force and (_PUBLIC_IP_CACHE["v4"] or _PUBLIC_IP_CACHE["v6"]):
        return _PUBLIC_IP_CACHE["v4"], _PUBLIC_IP_CACHE["v6"]
    v4 = v6 = None
    try:
        ip = (http_get_json("https://api64.ipify.org?format=json",
                            timeout=8) or {}).get("ip")
        if ip:
            if ":" in ip:
                v6 = ip
            else:
                v4 = ip
    except Exception:
        pass
    if v4 is None:
        try:
            v4 = (http_get_json("https://api.ipify.org?format=json",
                                timeout=8) or {}).get("ip")
        except Exception:
            pass
    if v6 is None:
        try:
            ip = (http_get_json("https://api6.ipify.org?format=json",
                                timeout=8) or {}).get("ip")
            if ip and ":" in ip:
                v6 = ip
        except Exception:
            pass
    _PUBLIC_IP_CACHE["v4"], _PUBLIC_IP_CACHE["v6"] = v4, v6
    return v4, v6


def get_local_ipv6():
    """本机全局 IPv6（排除 ::1、fe80 链路本地、fd/fc 私有）。"""
    out = []
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None,
                                       socket.AF_INET6):
            ip = info[4][0].split("%")[0]
            if ip and not ip.startswith(("::1", "fe80", "fd", "fc")):
                if ip not in out:
                    out.append(ip)
    except Exception:
        pass
    return out


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _netsh(args, timeout=25):
    try:
        r = subprocess.run(["netsh"] + args, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace",
                           **hidden_console_kwargs())
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, str(e)


def firewall_rule_exists(port):
    rc, out = _netsh(["advfirewall", "firewall", "show", "rule",
                      f"name={FIREWALL_RULE_PREFIX}{port}"])
    return str(port) in out


def _elevate(args):
    """用 UAC 提权执行 netsh（会弹一次系统授权框）。"""
    try:
        r = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "netsh", " ".join(args), None, 0)
        return r > 32, f"ShellExecuteW={r}"
    except Exception as e:
        return False, str(e)


def firewall_open_port(port):
    args = ["advfirewall", "firewall", "add", "rule",
            f"name={FIREWALL_RULE_PREFIX}{port}", "dir=in", "action=allow",
            "protocol=TCP", f"localport={port}"]
    if is_admin():
        rc, out = _netsh(args)
        return rc == 0, out
    return _elevate(args)


def firewall_close_port(port):
    args = ["advfirewall", "firewall", "delete", "rule",
            f"name={FIREWALL_RULE_PREFIX}{port}"]
    if is_admin():
        rc, out = _netsh(args)
        return rc == 0, out
    return _elevate(args)


def get_properties():
    """读 server.properties 成 dict。"""
    props = {}
    if PROPERTIES_FILE.exists():
        try:
            for line in PROPERTIES_FILE.read_text(
                    encoding="utf-8", errors="ignore").splitlines():
                s = line.strip()
                if s and not s.startswith("#") and "=" in s:
                    k, v = s.split("=", 1)
                    props[k.strip()] = v.strip()
        except Exception:
            pass
    return props


def set_properties(updates):
    """写入/更新 server.properties 的若干键，保留其它行与注释。"""
    lines = []
    if PROPERTIES_FILE.exists():
        lines = PROPERTIES_FILE.read_text(
            encoding="utf-8", errors="ignore").splitlines()
    done, out = set(), []
    for ln in lines:
        s = ln.strip()
        if s and not s.startswith("#") and "=" in s:
            k = s.split("=", 1)[0].strip()
            if k in updates:
                out.append(f"{k}={updates[k]}")
                done.add(k)
                continue
        out.append(ln)
    for k, v in updates.items():
        if k not in done:
            out.append(f"{k}={v}")
    PROPERTIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROPERTIES_FILE.write_text("\n".join(out).rstrip() + "\n",
                               encoding="utf-8")


def analyze_network(port):
    """联网体检：地址清单 + 人话建议。"""
    lan = get_lan_ip()
    pub4, pub6 = get_public_ips()
    local6 = get_local_ipv6()
    fw = firewall_rule_exists(port)
    props = get_properties()
    online_mode = str(props.get("online-mode", "true")).lower()
    server_ip = props.get("server-ip", "")
    tips = []

    if fw:
        tips.append(("ok", f"Windows 防火墙已放行端口 {port}"))
    else:
        tips.append(("warn", f"Windows 防火墙还没放行端口 {port}，"
                             f"点上面绿色按钮「🔓 一键开放防火墙端口」"))
    if lan:
        tips.append(("ok", f"同一个 Wi-Fi / 局域网的朋友连：{lan}:{port}"))
    if pub4:
        if pub4.startswith(("100.", "10.", "192.168.")):
            tips.append(("warn", f"公网出口 IP 是 {pub4}：属于运营商大内网(CGNAT)，"
                                 f"朋友没法直接连，需要在路由器做端口映射，"
                                 f"或借助内网穿透工具（这个启动器做不了）"))
        else:
            tips.append(("ok", f"公网 IPv4 是 {pub4}：在路由器上把 {port} 映射到本机，"
                               f"朋友连 {pub4}:{port}"))
    else:
        tips.append(("warn", "没取到公网 IPv4（可能没联网，或者被挡住了）"))
    v6 = pub6 or (local6[0] if local6 else None)
    if v6:
        tips.append(("ok", f"有 IPv6：{v6}\n"
                           f"   朋友用 [{v6}]:{port} 可直连，不需要端口映射"
                           f"（对方也得有 IPv6）"))
    else:
        tips.append(("warn", "没检测到可用的公网 IPv6（宽带没开或路由器没下发）"))
    if online_mode == "true":
        tips.append(("warn", "online-mode=true（正版验证）：朋友必须用正版账号；"
                             "离线/盗版服要改成 false"))
    if server_ip:
        tips.append(("warn", f"server-ip 现在填了 {server_ip}（只监听这一个地址）。"
                             f"想同时支持 IPv4+IPv6，建议留空"))
    else:
        tips.append(("ok", "server-ip 留空：监听所有网卡（含 IPv6），推荐"))
    tips.append(("ok", "内网穿透（frp / 樱花 / ngrok 这类）本启动器不做，"
                       "CGNAT 环境下得靠它们"))
    return {"lan": lan, "public4": pub4, "public6": pub6, "local6": local6,
            "port": port, "firewall": fw, "props": props, "tips": tips}


# ==================== 拖拽支持（可选依赖 tkinterdnd2） ====================
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_DND = True
except Exception:
    TkinterDnD = None
    DND_FILES = None
    HAS_DND = False

_DND_MIXIN = (TkinterDnD.DnDWrapper,) if HAS_DND else ()


def dir_size(path):
    """递归统计目录大小（字节）。用 os.scandir，比 Path.rglob 快很多。"""
    total = 0
    stack = [str(path)]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(cur) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry.path)
                        elif entry.is_file(follow_symlinks=False):
                            total += entry.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return total


def human_size(num):
    """把字节数说成人话：1536 → 1.5 KB，10MB → 10 MB（整数就不带 .0）。"""
    try:
        num = float(num)
    except Exception:
        return "?"
    if num < 1024:
        return f"{int(num)} B"
    for unit in ("KB", "MB", "GB", "TB"):
        num /= 1024
        if num < 1024 or unit == "TB":
            txt = f"{num:.1f}"
            if txt.endswith(".0"):        # v3.5.11：10.0 MB → 10 MB
                txt = txt[:-2]
            return f"{txt} {unit}"


def open_in_explorer(path):
    """在资源管理器里打开目录（Windows）。"""
    try:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        os.startfile(str(path))
    except Exception as e:
        print(f"[启动器] 打开文件夹失败: {e}")

# Fill v3 API 要求 User-Agent 必须包含联系方式
USER_AGENT = "MCServerLauncher/2.8 (3886954805@qq.com)"
HEADERS = {"User-Agent": USER_AGENT}

# ==================== v3.5.8：子进程别弹黑窗口 ====================
# 启动器是 GUI（pythonw），spawn 控制台程序（java / netsh / pip）时 Windows 会给它们
# 单开一个黑窗口。新手会以为那是"启动器的一部分"，一关就把服务器关了。
# 这里统一用 CREATE_NO_WINDOW + SW_HIDE 启动；输出照样走管道进「控制台」页。
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)


def hidden_console_kwargs():
    """给 Popen / run / check_output 用的"隐藏子进程窗口"参数（非 Windows 返回空）。"""
    if os.name != "nt":
        return {}
    kw = {"creationflags": CREATE_NO_WINDOW}
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0            # SW_HIDE
        kw["startupinfo"] = si
    except Exception:
        pass
    return kw


# ==================== v3.5.9：去掉日志里的颜色控制符 ====================
# 服务端/插件偶尔会往 stdout 里塞 ANSI 颜色码（\x1b[91m…\x1b[0m），
# 管道里读出来就是一堆 "[91m"，在「控制台」页看着像乱码。
# 这里统一剥掉：显示前剥、用正则判断（Done/玩家进服/报错）之前也剥。
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;?]*[0-9A-Za-z]")


def strip_ansi(text):
    """去掉 ANSI 转义序列（颜色/光标控制），其它字符原样保留。"""
    if not text or "\x1b" not in text:
        return text
    try:
        return ANSI_ESCAPE_RE.sub("", text)
    except Exception:
        return text

VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

# --- Paper (Fill v3 API) ---
PAPER_API_V3 = "https://fill.papermc.io/v3/projects/paper"

# --- Purpur ---
PURPUR_API = "https://api.purpurmc.org/v2/purpur"

# --- Fabric ---
FABRIC_META = "https://meta.fabricmc.net/v2"

# --- Modrinth ---
MODRINTH_API = "https://api.modrinth.com/v2"

CORE_LOADER_MAP = {
    "vanilla": None,
    "paper": "paper",
    "purpur": "purpur",
    "fabric": "fabric",
}

CORE_DISPLAY = {
    "Vanilla (官方)": "vanilla",
    "Paper (推荐)": "paper",
    "Purpur": "purpur",
    "Fabric": "fabric",
}

# v3.5.17：下载核心的“目标服务器”。默认是新建一个服务器，不再覆盖当前核心；
# 想给已有服务器换核心，就在「📥 下载核心」页把目标服务器选成它。
CORE_TARGET_NEW = "➕ 新建服务器"

IMAGE_CACHE = {}
# (url, size) -> 已缩放好的 PIL 图。避免翻页/重建列表时重复下载和重复缩放。
THUMB_CACHE = {}

# v3.4：图片相关调参（治“加载图片抢资源”）
IMG_CACHE_LIMIT = 300        # 缓存上限，超出按先进先出淘汰，防长会话内存膨胀
IMG_DECODE_HINT = 128        # 解码时先缩到这个尺寸（draft），省 70%+ 解码时间
IMG_QUIET_SECONDS = 3.0      # 启动后多久内完全不加载图片
IMG_THROTTLE_SECONDS = 0.04  # 每张封面之间的节流间隔
IMG_WORKERS = 2              # 封面下载线程数（原来 3 个太抢 CPU）
IMG_PUMP_MAX = 6             # 每次“滚到可见”最多排几张

# v3.5（0-9）：统一心跳调参。原来 5 条 after 链各跑各的，空闲时每秒醒 20 多次；
# 现在一条心跳带 5 个活，节拍按“有没有活干 + 窗口在不在前台”决定。
TICK_BUSY_MS = 100           # 服务端在跑/启动中：控制台日志要跟手
TICK_IDLE_MS = 500           # 空闲 + 窗口在前台（用户在看着，别太懒）
TICK_AWAY_MS = 2000         # 空闲 + 窗口在后台（用户没在看）→ 2 秒一次
TICK_LOG_IDLE_MS = 500       # 空闲时日志队列的检查间隔（没服务端时没啥可读）
TICK_PROC_MS = 500           # 服务端进程存活检查
TICK_STATS_MS = 2000         # 状态栏 CPU / 内存
TICK_OVERVIEW_MS = 1500      # 概览页刷新
TICK_LAZY_MS = 120           # 懒加载：切到哪个页面才建它（建完就不再跑）
TICK_BACKUP_MS = 60000       # v3.5（⑪）：自动备份的检查间隔（到点才真备份）
# v3.5.15：一次心跳最多占用 UI 线程这么久（毫秒）。拖窗口卡顿的根治点：
# 以前日志一刷屏，一次心跳能占几十 ms，窗口就跟不上鼠标了。
TICK_BUDGET_MS = 8.0
# 检测到"正在拖窗口"（位置变了但尺寸没变）时，这期间只做最关键的心跳
TICK_MOVE_SUSPEND_MS = 400

# v3.5（⑪）：自动备份间隔选项（分钟）
BACKUP_MINUTES = {"关闭": 0, "30 分钟": 30, "1 小时": 60,
                  "3 小时": 180, "6 小时": 360}
BACKUP_LABELS = {v: k for k, v in BACKUP_MINUTES.items()}

# v3.5（⑬）：内置编辑器认识的文件类型 / 上限
EDITABLE_EXTS = {".yml", ".yaml", ".properties", ".json", ".txt", ".conf",
                 ".cfg", ".toml", ".md", ".log", ".ini", ".sh", ".bat"}
EDIT_MAX_BYTES = 2 * 1024 * 1024

# v3.5（0-8）：大目录分块建行——一次建这么多，剩下的交给下一帧，界面不假死。
# 块大小实测：这机器上每行（6 个 CTk 控件）约 20ms，12 行 ≈ 250ms 一帧，
# 再大就会出现"点一下要等一秒"的感觉。
BROWSER_CHUNK = 12
BROWSER_CHUNK_MS = 1

# v3.5（③）：崩溃自动重启 / 定时重启
TICK_RESTART_MS = 60000
RESTART_MODES = {"关闭": "off", "每 6 小时": "6h",
                 "每 12 小时": "12h", "每天（24 小时）": "24h"}
RESTART_MODE_LABELS = {v: k for k, v in RESTART_MODES.items()}
CRASH_LIMITS = ["1", "3", "5"]


def cache_put(cache, key, value, limit=IMG_CACHE_LIMIT):
    """带先进先出淘汰的缓存写入。"""
    try:
        cache[key] = value
        while len(cache) > limit:
            cache.pop(next(iter(cache)))
    except Exception:
        pass

AVATAR_PALETTE = [
    "#e74c3c", "#3498db", "#2ecc71", "#f39c12",
    "#9b59b6", "#1abc9c", "#e91e63", "#00bcd4",
    "#ff5722", "#673ab7", "#009688", "#ff9800",
]

PAGE_SIZE = 20
MODRINTH_MAX_OFFSET = 1000


# ==================== 网络工具 ====================
def _make_unverified_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


UNVERIFIED_CTX = _make_unverified_ctx()


def http_get_json(url, timeout=30):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            if not raw:
                raise RuntimeError(f"服务器返回空内容: {url}")
            return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as he:
        raise RuntimeError(f"HTTP {he.code} {he.reason}")
    except urllib.error.URLError as ue:
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=UNVERIFIED_CTX) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            reason = ue.reason if ue.reason else "网络不可达"
            raise RuntimeError(f"网络错误: {reason}")
    except json.JSONDecodeError as je:
        raise RuntimeError(f"返回内容不是 JSON: {je}")
    except Exception as e:
        raise RuntimeError(f"[{type(e).__name__}] {e}")


# ==================== v3.5.5：IDM 式多连接下载 ====================
# 规则（按用户要求）：每 0.5 秒采样一次"文件进度推进速度"；
# 如果**每秒推进不到 15%**，就给最慢的那一段再拆一条连接，最多 8 条。
# 服务器不支持 Range / 文件小于 1MB → 不折腾，走原来的单连接（带断点续传）。
DL_MIN_MULTI_SIZE = 1024 * 1024        # 小于 1MB 不值得分段
DL_START_CONNS = 2                     # 一开始 2 条
DL_MAX_CONNS = 8                       # 最多 8 条
DL_SAMPLE_SEC = 0.5                    # 采样间隔（秒）
DL_ADD_CONNS_PCT = 15.0                # 每秒推进不到这个百分比 → 加连接
DL_MIN_SEG_BYTES = 256 * 1024          # 段小于 256KB 就不再拆
DL_SEG_RETRY = 3                       # 单段断线重连次数
DL_BUF = 256 * 1024
DL_LAST_STATS = {}                     # 上一次多连接下载的统计（测试/排查用）


def _should_add_conn(rate_pct, alive_conns):
    """要不要再加一条连接：速度不够（每秒推进 < 15%）且还没到上限。"""
    return rate_pct < DL_ADD_CONNS_PCT and alive_conns < DL_MAX_CONNS


def _probe_download(url, timeout=30):
    """问一下这个地址：总大小多少、支不支持 Range。返回 (total, range_ok)。"""
    req = urllib.request.Request(url, headers=dict(HEADERS))
    req.add_header("Range", "bytes=0-0")
    with urllib.request.urlopen(req, timeout=timeout, context=UNVERIFIED_CTX) as r:
        status = getattr(r, "status", 200)
        total = 0
        cr = r.headers.get("Content-Range") or ""
        if "/" in cr:
            try:
                total = int(cr.rsplit("/", 1)[1])
            except Exception:
                total = 0
        if status == 206 and total > 0:
            return total, True
        try:
            cl = int(r.headers.get("Content-Length") or 0)
        except Exception:
            cl = 0
        return cl, False


class TaskCancelled(Exception):
    """用户点了任务卡上的「✕ 取消」（v3.5.7）。"""


def _download_multi(url, dest, total, have=0, on_progress=None, timeout=60,
                    cancel_check=None):
    """多连接分段下载"剩下的部分"（have 之前是本机已有的前缀）。

    先下到 dest.part（按文件内偏移写），下完整了才追加到 dest：
    中途失败不会污染 dest，下次还能按老逻辑从断点续传。
    """
    import threading as _thr

    dest = Path(dest)
    part = Path(str(dest) + ".part")
    remain = max(0, total - have)
    try:
        part.unlink()
    except Exception:
        pass
    with open(part, "wb") as f:
        f.truncate(remain)

    lock = _thr.Lock()
    stop = _thr.Event()
    errors = []
    segs = []
    state = {"done": 0}

    def worker(seg):
        fh = None
        tries = 0
        try:
            fh = open(part, "r+b")
            while True:
                if stop.is_set():
                    return
                with seg["wlock"]:
                    a, b = seg["pos"], seg["end"]
                if a >= b:
                    return
                req = urllib.request.Request(url, headers=dict(HEADERS))
                req.add_header("Range", f"bytes={have + a}-{have + b - 1}")
                try:
                    with urllib.request.urlopen(req, timeout=timeout,
                                                context=UNVERIFIED_CTX) as r:
                        if getattr(r, "status", 200) != 206:
                            raise RuntimeError("服务器不支持分段下载")
                        while True:
                            if stop.is_set():
                                return
                            with seg["wlock"]:
                                a, b = seg["pos"], seg["end"]
                            if a >= b:
                                break
                            buf = r.read(min(DL_BUF, b - a))
                            if not buf:
                                raise RuntimeError("连接提前结束")
                            fh.seek(a)
                            fh.write(buf)
                            with seg["wlock"]:
                                seg["pos"] = a + len(buf)
                            with lock:
                                state["done"] += len(buf)
                    tries = 0
                except Exception as e:
                    if stop.is_set():
                        return
                    tries += 1
                    if tries > DL_SEG_RETRY:
                        errors.append(e)
                        stop.set()
                        return
                    time.sleep(0.5)
        except Exception as e:
            errors.append(e)
            stop.set()
        finally:
            try:
                if fh:
                    fh.close()
            except Exception:
                pass

    def add_seg(a, b):
        seg = {"pos": a, "end": b, "wlock": _thr.Lock()}
        segs.append(seg)
        seg["thread"] = _thr.Thread(target=worker, args=(seg,), daemon=True)
        seg["thread"].start()
        return seg

    n0 = max(1, min(DL_START_CONNS, DL_MAX_CONNS))
    step = max(1, remain // n0)
    for i in range(n0):
        a = i * step
        b = remain if i == n0 - 1 else min(remain, (i + 1) * step)
        if a < b:
            add_seg(a, b)
    if not segs:
        add_seg(0, remain)

    last_done, last_t = 0, time.time()
    samples = 0
    rates = []
    added = 0
    max_alive = len(segs)
    cancelled = False
    while True:
        if stop.is_set():
            break
        if cancel_check is not None:
            try:
                if cancel_check():
                    cancelled = True
                    stop.set()
                    break
            except Exception:
                pass
        time.sleep(DL_SAMPLE_SEC)
        with lock:
            done = state["done"]
        now = time.time()
        dt = max(1e-6, now - last_t)
        rate_pct = (done - last_done) * 100.0 / float(total) / dt
        last_done, last_t = done, now
        samples += 1
        rates.append(rate_pct)
        if on_progress:
            try:
                on_progress(min(total, have + done), total)
            except Exception:
                pass
        if done >= remain:
            break
        alive = [s for s in segs if s["thread"].is_alive()]
        max_alive = max(max_alive, len(alive))
        if not alive:
            break
        if _should_add_conn(rate_pct, len(alive)):
            seg = max(alive, key=lambda s: s["end"] - s["pos"])
            with seg["wlock"]:
                a, b = seg["pos"], seg["end"]
                if b - a >= 2 * DL_MIN_SEG_BYTES:
                    mid = a + (b - a) // 2
                    seg["end"] = mid
                    add_seg(mid, b)
                    added += 1

    for s in segs:
        try:
            s["thread"].join(timeout=10)
        except Exception:
            pass

    with lock:
        done = state["done"]
    DL_LAST_STATS.clear()
    DL_LAST_STATS.update({
        "total": total, "have": have, "remain": remain, "done": done,
        "conns_max": max_alive, "conns_created": len(segs),
        "conns_added": added, "samples": samples,
        "rate_min_pct": min(rates) if rates else 0.0,
        "rate_max_pct": max(rates) if rates else 0.0,
    })
    if cancelled:
        try:
            part.unlink()
        except Exception:
            pass
        raise TaskCancelled("已取消")
    if errors:
        try:
            part.unlink()
        except Exception:
            pass
        raise RuntimeError(f"多连接下载失败: {errors[0]}")
    if done < remain:
        try:
            part.unlink()
        except Exception:
            pass
        raise RuntimeError(f"多连接下载不完整: {done}/{remain} 字节")

    # 拼回去（本地顺序追加，很快）
    with open(dest, "ab") as out, open(part, "rb") as src:
        while True:
            buf = src.read(1024 * 1024)
            if not buf:
                break
            out.write(buf)
    try:
        part.unlink()
    except Exception:
        pass
    if on_progress:
        try:
            on_progress(total, total)
        except Exception:
            pass
    return dest


def http_download(url, dest, on_progress=None, timeout=60, resume=True,
                  cancel_check=None):
    """下载文件，支持断点续传与完整性校验。

    v3.1：以前是纯 "wb" 重下。网络一抖就白下几十 MB，而且失败提示只显示在
    「下载核心」页面的小字上，用户切到别的页面根本看不到，看起来就像“悄悄没反应”。
    现在：目标文件已存在时用 Range 接着下，服务器不支持续传就自动从头来，
    最后校验字节数，不完整会明确报错（下次点击可继续）。

    v3.5.5：先探一下大小/是否支持 Range，支持就上多连接（IDM 那套：
    每秒推进不到 15% 就给最慢的段再拆一条，最多 8 条）；多连接出错自动回退单连接。

    v3.5.7：多了 cancel_check（每读一块/每 0.5 秒问一次），用户点任务卡的 ✕
    就能中途停下，抛 TaskCancelled。
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    have = dest.stat().st_size if (resume and dest.exists()) else 0

    def _cancelled():
        if cancel_check is None:
            return False
        try:
            return bool(cancel_check())
        except Exception:
            return False

    if _cancelled():
        raise TaskCancelled("已取消")

    total_probe, range_ok = 0, False
    try:
        total_probe, range_ok = _probe_download(url, timeout=min(timeout, 30))
    except Exception:
        total_probe, range_ok = 0, False
    if have and total_probe and have >= total_probe:
        return dest                       # 本地已经是完整文件
    if range_ok and total_probe >= DL_MIN_MULTI_SIZE and total_probe > have:
        try:
            return _download_multi(url, dest, total_probe, have,
                                   on_progress=on_progress, timeout=timeout,
                                   cancel_check=cancel_check)
        except TaskCancelled:
            raise
        except Exception as e:
            print(f"[下载] 多连接失败，回退单连接: {e}")
            try:
                Path(str(dest) + ".part").unlink()
            except Exception:
                pass

    req = urllib.request.Request(url, headers=dict(HEADERS))
    if have:
        req.add_header("Range", f"bytes={have}-")

    try:
        resp = urllib.request.urlopen(req, timeout=timeout,
                                      context=UNVERIFIED_CTX)
    except urllib.error.HTTPError as he:
        if he.code == 416:            # 本地已经是完整文件了
            return dest
        raise

    with resp:
        status = getattr(resp, "status", 200)
        if have and status != 206:    # 服务器不支持续传 → 老实从头下
            have = 0
        total = int(resp.headers.get("Content-Length", 0)) + have
        mode = "ab" if (have and status == 206) else "wb"
        done = have
        chunk = 1024 * 64
        with open(dest, mode) as f:
            while True:
                if _cancelled():
                    raise TaskCancelled("已取消")
                buf = resp.read(chunk)
                if not buf:
                    break
                f.write(buf)
                done += len(buf)
                if on_progress and total:
                    on_progress(done, total)

    if total and done < total:
        raise RuntimeError(
            f"下载不完整: {done}/{total} 字节（再点一次会从断点继续）")
    return dest


def load_image(url, timeout=15):
    if not HAS_PIL or not url or Image is None:
        return None
    if url in IMAGE_CACHE:
        return IMAGE_CACHE[url]

    req = urllib.request.Request(url, headers=HEADERS)
    last_err = None

    for ctx in (None, UNVERIFIED_CTX):
        try:
            if ctx is None:
                resp = urllib.request.urlopen(req, timeout=timeout)
            else:
                resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            with resp:
                data = resp.read()
            img = Image.open(io.BytesIO(data))
            # v3.4：让解码器直接按接近目标的尺寸解码（webp/jpeg 能省 70%+ 时间），再 load
            try:
                if img.format in ("JPEG", "MPO", "WEBP", "PNG"):
                    img.draft("RGB", (IMG_DECODE_HINT, IMG_DECODE_HINT))
            except Exception:
                pass
            img.load()
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            cache_put(IMAGE_CACHE, url, img)
            print(f"[封面] ✅ 加载成功: {url[:80]}...")
            return img
        except Exception as e:
            last_err = e
            continue

    print(f"[封面] ❌ 加载失败: {type(last_err).__name__}: {last_err}")
    return None


# ==================== Vanilla (Mojang) ====================
def fetch_vanilla_versions():
    data = http_get_json(VERSION_MANIFEST_URL)
    return [v["id"] for v in data["versions"] if v["type"] == "release"]


def get_vanilla_url(version):
    data = http_get_json(VERSION_MANIFEST_URL)
    for v in data["versions"]:
        if v["id"] == version:
            detail = http_get_json(v["url"])
            return detail["downloads"]["server"]["url"]
    raise RuntimeError(f"找不到版本 {version}")


# ==================== Paper (Fill v3 API) ====================
def fetch_paper_versions():
    """
    获取 Paper 版本列表 (Fill v3 API)。
    API 返回格式: {"versions": {"1.21": ["1.21.11", "1.21.10", ...], ...}}
    需要展平为扁平列表，并保持最新版本在前。
    """
    data = http_get_json(PAPER_API_V3, timeout=20)

    versions_raw = data.get("versions", {})
    if not versions_raw:
        raise RuntimeError("Paper API 返回的版本列表为空")

    def _ver_key(v):
        # v2.9 修复：字符串排序会把 "1.9" 排在 "1.21" 前面（'9' > '2'），
        # 导致 1.9/1.8/1.7 混进列表顶部、并把 1.13 及更早版本挤出截断范围。
        core = str(v).split("-", 1)[0]
        nums = [int(p) if p.isdigit() else 0 for p in core.split(".")]
        tail = str(v)[len(core):]
        return (nums, 1 if tail else 0, tail)

    all_versions = []
    if isinstance(versions_raw, dict):
        for major in sorted(versions_raw.keys(), key=_ver_key, reverse=True):
            minor_list = versions_raw[major]
            if isinstance(minor_list, list):
                for v in sorted((str(x) for x in minor_list),
                                key=_ver_key, reverse=True):
                    all_versions.append(v)
    elif isinstance(versions_raw, list):
        all_versions = [str(v) for v in versions_raw]

    # 只保留正式版，过滤掉 -rc / -pre 预发布版（新手容易误装）
    all_versions = [v for v in all_versions
                    if re.match(r"^\d+(?:\.\d+)*$", v)]

    if not all_versions:
        raise RuntimeError("无法从 Paper API 解析出版本列表")

    return all_versions


def get_paper_url(version):
    """
    获取 Paper 下载地址 (Fill v3 API)。
    使用 /builds/latest 端点直接获取最新稳定构建。
    下载链接位于 downloads["server:default"].url
    """
    url = f"{PAPER_API_V3}/versions/{version}/builds/latest"

    try:
        data = http_get_json(url, timeout=20)
    except RuntimeError as e:
        if "404" in str(e):
            raise RuntimeError(f"Paper {version} 没有可用的构建")
        raise

    try:
        download_info = data["downloads"]["server:default"]
        download_url = download_info["url"]
        if not download_url:
            raise RuntimeError("下载链接为空")
        return download_url
    except (KeyError, TypeError):
        raise RuntimeError(
            f"解析 Paper {version} 的下载链接失败，API 返回格式可能已变更"
        )


# ==================== Purpur ====================
def fetch_purpur_versions():
    data = http_get_json(PURPUR_API)
    return list(reversed(data["versions"]))


def get_purpur_url(version):
    return f"{PURPUR_API}/{version}/latest/download"


# ==================== Fabric ====================
def fetch_fabric_versions():
    data = http_get_json(f"{FABRIC_META}/versions/game")
    return [v["version"] for v in data if v["stable"]]


def get_fabric_url(game_version):
    loaders = http_get_json(f"{FABRIC_META}/versions/loader")
    installers = http_get_json(f"{FABRIC_META}/versions/installer")
    loader = loaders[0]["version"]
    installer = installers[0]["version"]
    return (
        f"{FABRIC_META}/versions/loader/{game_version}/{loader}"
        f"/{installer}/server/jar"
    )


# ==================== server.properties 全量属性表（v3.3） ====================
# (键, 中文名, 类型, 默认值, 选项, 起始版本, 分类)
# “起始版本”用于随游戏版本变动：比当前服务端版本新的键会被隐藏；
# 如果文件里已经存在（比如你手动加过），仍会照原样显示出来，不会被丢掉。
PROP_CATALOG = [
    ("motd", "服务器描述 MOTD", "entry", "A Minecraft Server", None, None, "基础"),
    ("server-port", "服务器端口", "int", "25565", None, None, "基础"),
    ("server-ip", "绑定地址(留空=全部)", "entry", "", None, None, "基础"),
    ("online-mode", "正版验证", "bool", "true", None, None, "基础"),
    ("max-players", "最大玩家数", "int", "20", None, None, "基础"),
    ("white-list", "启用白名单", "bool", "false", None, None, "基础"),
    ("enforce-whitelist", "白名单外强制踢出", "bool", "false", None, "1.16", "基础"),
    ("gamemode", "默认游戏模式", "option", "survival",
     ["survival", "creative", "adventure", "spectator"], None, "玩法"),
    ("force-gamemode", "强制游戏模式", "bool", "false", None, None, "玩法"),
    ("difficulty", "难度", "option", "easy",
     ["peaceful", "easy", "normal", "hard"], None, "玩法"),
    ("hardcore", "极限模式", "bool", "false", None, "1.16.5", "玩法"),
    ("pvp", "允许 PvP", "bool", "true", None, None, "玩法"),
    ("allow-flight", "允许飞行(生存模式)", "bool", "false", None, None, "玩法"),
    ("player-idle-timeout", "挂机踢出(分钟)", "int", "0", None, None, "玩法"),
    ("spawn-protection", "出生点保护半径", "int", "16", None, None, "玩法"),
    ("enable-command-block", "启用命令方块", "bool", "false", None, None, "玩法"),
    ("op-permission-level", "OP 权限等级", "option", "4",
     ["1", "2", "3", "4"], None, "权限"),
    ("function-permission-level", "函数权限等级", "option", "2",
     ["1", "2", "3", "4"], None, "权限"),
    ("level-name", "世界文件夹名", "entry", "world", None, None, "世界"),
    ("level-seed", "世界种子", "entry", "", None, None, "世界"),
    ("level-type", "世界类型", "option", "minecraft:normal",
     ["minecraft:normal", "minecraft:flat", "minecraft:large_biomes",
      "minecraft:amplified", "minecraft:single_biome_surface"],
     None, "世界"),
    ("generate-structures", "生成结构", "bool", "true", None, None, "世界"),
    ("max-world-size", "世界边界半径", "int", "29999984", None, None, "世界"),
    ("spawn-animals", "生成动物", "bool", "true", None, None, "世界"),
    ("spawn-monsters", "生成怪物", "bool", "true", None, None, "世界"),
    ("spawn-npcs", "生成村民", "bool", "true", None, None, "世界"),
    ("allow-nether", "允许下界", "bool", "true", None, None, "世界"),
    ("initial-enabled-packs", "初始启用数据包", "entry", "vanilla",
     None, "1.19.3", "世界"),
    ("initial-disabled-packs", "初始禁用数据包", "entry", "",
     None, "1.19.3", "世界"),
    ("view-distance", "视距(区块)", "int", "10", None, None, "性能"),
    ("simulation-distance", "模拟距离(区块)", "int", "10",
     None, "1.18", "性能"),
    ("max-tick-time", "单 tick 超时(ms)", "int", "60000", None, None, "性能"),
    ("network-compression-threshold", "网络压缩阈值(-1 关闭)", "int", "256",
     None, None, "性能"),
    ("entity-broadcast-range-percentage", "实体广播范围 %", "int", "100",
     None, "1.16.5", "性能"),
    ("sync-chunk-writes", "同步区块写入", "bool", "true",
     None, "1.17", "性能"),
    ("use-native-transport", "Linux 原生传输", "bool", "true",
     None, None, "性能"),
    ("max-chained-neighbor-updates", "连锁更新上限", "int", "1000000",
     None, "1.19", "性能"),
    ("region-file-compression", "区域文件压缩算法", "option", "deflate",
     ["deflate", "lz4", "none"], "1.20.5", "性能"),
    ("pause-when-empty-seconds", "空服自动暂停(秒)", "int", "60",
     None, "1.21.2", "性能"),
    ("rate-limit", "连接速率限制(ms)", "int", "0", None, "1.16.4", "网络"),
    ("enable-status", "服务器列表显示在线", "bool", "true", None, None, "网络"),
    ("hide-online-players", "隐藏在线玩家列表", "bool", "false",
     None, "1.19.3", "网络"),
    ("prevent-proxy-connections", "阻止代理连接", "bool", "false",
     None, None, "网络"),
    ("enable-query", "启用 Query 协议", "bool", "false", None, None, "网络"),
    ("query.port", "Query 端口", "int", "25565", None, None, "网络"),
    ("enable-rcon", "启用 RCON", "bool", "false", None, None, "网络"),
    ("rcon.port", "RCON 端口", "int", "25575", None, None, "网络"),
    ("rcon.password", "RCON 密码", "entry", "", None, None, "网络"),
    ("broadcast-rcon-to-ops", "RCON 输出广播给 OP", "bool", "true",
     None, None, "网络"),
    ("enforce-secure-profile", "强制安全聊天签名", "bool", "true",
     None, "1.19", "网络"),
    ("log-ips", "日志记录玩家 IP", "bool", "true", None, "1.20.2", "网络"),
    ("accepts-transfers", "接受转移连接", "bool", "false",
     None, "1.20.5", "网络"),
    ("text-filtering-config", "聊天过滤配置", "entry", "",
     None, "1.16", "网络"),
    ("resource-pack", "资源包 URL", "entry", "", None, None, "资源包"),
    ("resource-pack-sha1", "资源包 SHA1", "entry", "", None, None, "资源包"),
    ("require-resource-pack", "强制使用资源包", "bool", "false",
     None, "1.17", "资源包"),
    ("resource-pack-prompt", "资源包提示语", "entry", "",
     None, "1.18", "资源包"),
    ("enable-jmx-monitoring", "启用 JMX 监控", "bool", "false",
     None, None, "高级"),
]


def _ver_parts(v):
    try:
        return [int(x) for x in str(v).split("-")[0].split(".")]
    except Exception:
        return []


def ver_at_least(version, since):
    """version >= since（按 1.20.5 这种形式比）；since 为空表示一直存在。"""
    if not since:
        return True
    a, b = _ver_parts(version), _ver_parts(since)
    if not a or not b:
        return True
    n = max(len(a), len(b))
    a += [0] * (n - len(a))
    b += [0] * (n - len(b))
    return a >= b


def catalog_for_version(version, extra_keys=()):
    """该版本该显示的属性行 + 文件里多出来的键（保留，方便你改回来）。"""
    rows, seen = [], set()
    for key, label, wtype, default, options, since, cat in PROP_CATALOG:
        if ver_at_least(version, since):
            rows.append((key, label, wtype, default, options, cat))
            seen.add(key)
    for k in extra_keys:
        if k not in seen:
            rows.append((k, f"{k}  （文件里的额外项）", "entry", "",
                         None, "文件里的其它项"))
            seen.add(k)
    return rows


# ==================== 核心更新比对（v3.3） ====================
def file_hash(path, algo):
    import hashlib
    try:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()
    except Exception:
        return None


def core_remote_info(core, version):
    """远端最新核心的下载地址 + 校验值（用于判断本地是不是最新构建）。"""
    core = (core or "").lower()
    if core == "paper":
        data = http_get_json(
            f"{PAPER_API_V3}/versions/{version}/builds/latest", timeout=20)
        dl = data["downloads"]["server:default"]
        return {"url": dl["url"],
                "hash": (dl.get("checksums") or {}).get("sha256"),
                "algo": "sha256",
                "note": f"Paper build {data.get('id')} / {data.get('channel')}"}
    if core == "purpur":
        data = http_get_json(f"{PURPUR_API}/{version}/latest", timeout=20)
        return {"url": f"{PURPUR_API}/{version}/latest/download",
                "hash": data.get("md5"), "algo": "md5",
                "note": f"Purpur build {data.get('build')}"}
    if core == "vanilla":
        data = http_get_json(VERSION_MANIFEST_URL)
        for v in data["versions"]:
            if v["id"] == version:
                detail = http_get_json(v["url"])
                s = detail["downloads"]["server"]
                return {"url": s["url"], "hash": s.get("sha1"),
                        "algo": "sha1", "note": f"官方原版 {version}"}
        raise RuntimeError(f"找不到版本 {version}")
    if core == "fabric":
        return {"url": get_fabric_url(version), "hash": None, "algo": None,
                "note": "Fabric 由 loader 版本决定，无法用哈希比对"}
    raise RuntimeError(f"不认识的核心类型: {core}")


def core_update_status(core, version, jar_path):
    info = core_remote_info(core, version)
    local = file_hash(jar_path, info["algo"]) if info["hash"] else None
    up = bool(info["hash"] and local
              and local.lower() == str(info["hash"]).lower())
    return dict(info, local_hash=local, up_to_date=up)


# ==================== Java 一键安装（v3.4） ====================
# v3.5：15 删掉（没有任何 MC 版本要求它，早 EOL），补上 16（1.16.5 真的要它）
JAVA_CHOICES = [8, 11, 16, 17, 21, 25]
JAVA_RUNTIME_DIR = BASE_DIR / "runtime"
ADOPTIUM_ASSETS = "https://api.adoptium.net/v3/assets/latest/{v}/hotspot"
# v3.5.7：GitHub 在国内基本下不动（实测官方 38KB/s，55MB 的 JRE 要 24 分钟，
# 中途一卡就 TimeoutError）。清华 TUNA 镜像同一个文件实测 640KB/s（×17），
# 所以优先走镜像，镜像没有/不对再回官方。文件本身用 Adoptium 给的 sha256 校验。
ADOPTIUM_MIRRORS = (
    "https://mirrors.tuna.tsinghua.edu.cn/Adoptium/{v}/jre/x64/windows/{name}",
)
# 这些版本 Adoptium 已经不提供 JRE 了 → 一键安装按钮会直接给一句人话，不去请求
JAVA_NO_INSTALL_REASON = {
    16: ("Adoptium 已经不提供 Java 16 的 JRE 下载了（16 是非 LTS，早就停止更新）。\n\n"
         "1.16.5 的服务端确实需要 Java 16：请自己去装一个 Java 16，"
         "再回「设置」把「Java 路径」指到它的 java.exe。"),
}


def java_download_info(feature_version):
    """问 Adoptium 要 Windows x64 JRE 的下载信息。

    返回 url / 文件名 / 体积 / 版本 / sha256 校验值 / 镜像候选地址。
    """
    url = (f"{ADOPTIUM_ASSETS.format(v=feature_version)}"
           f"?architecture=x64&image_type=jre&os=windows&vendor=eclipse")
    data = http_get_json(url, timeout=25)
    if not data:
        raise RuntimeError(f"Adoptium 没有 Java {feature_version} 的构建")
    entry = data[0]
    pkg = entry["binary"]["package"]
    name = pkg["name"]
    mirrors = []
    for tpl in ADOPTIUM_MIRRORS:
        try:
            mirrors.append(tpl.format(v=feature_version, name=name))
        except Exception:
            pass
    return {"url": pkg["link"], "name": name,
            "size": pkg.get("size"),
            "checksum": (pkg.get("checksum") or "").strip().lower(),
            "mirrors": mirrors,
            "version": entry.get("version_data", {}).get("semver", "?")}


def pick_fast_url(urls, probe_bytes=256 * 1024, timeout=20):
    """从候选地址里挑一个最快的（各拉 probe_bytes 测速）。全失败就返回第一个。

    只用于"同文件多处来源"的场景（例如 Adoptium 官方 vs 国内镜像）。
    """
    best, best_speed = None, -1.0
    for u in urls:
        if not u:
            continue
        got, t0, ok = 0, time.time(), False
        try:
            req = urllib.request.Request(u, headers=dict(HEADERS))
            req.add_header("Range", f"bytes=0-{probe_bytes - 1}")
            with urllib.request.urlopen(req, timeout=timeout,
                                        context=UNVERIFIED_CTX) as r:
                if getattr(r, "status", 200) not in (200, 206):
                    continue
                while got < probe_bytes:
                    buf = r.read(64 * 1024)
                    if not buf:
                        break
                    got += len(buf)
                ok = got > 0
        except Exception:
            ok = False
        dt = max(1e-3, time.time() - t0)
        speed = got / dt if ok else -1.0
        if ok and speed > best_speed:
            best, best_speed = u, speed
    return best or (urls[0] if urls else "")


def http_download_verified(url, dest, on_progress=None, checksum="",
                           attempts=4, timeout=60, cancel_check=None):
    """下载 + sha256 校验 + 失败自动续传重试（v3.5.7）。

    大文件（JRE 55MB / 核心 40MB）在慢网上一卡就 TimeoutError，以前一次就报错。
    现在：失败就等一会儿接着下（http_download 本来就支持断点续传），
    校验不对就删掉重下，最多 attempts 次。用户点 ✕ 取消则立刻停、不再重试。
    """
    dest = Path(dest)
    want = (checksum or "").strip().lower()
    last_err = None
    for i in range(max(1, int(attempts))):
        try:
            http_download(url, dest, on_progress=on_progress, timeout=timeout,
                          cancel_check=cancel_check)
            if want:
                h = hashlib.sha256()
                with open(dest, "rb") as f:
                    for chunk in iter(lambda: f.read(1024 * 1024), b""):
                        h.update(chunk)
                got = h.hexdigest()
                if got != want:
                    raise RuntimeError(
                        f"校验不一致（{got[:12]}… != {want[:12]}…）")
            return dest
        except TaskCancelled:
            raise
        except Exception as e:
            last_err = e
            print(f"[下载] 第 {i + 1}/{attempts} 次失败: "
                  f"{type(e).__name__}: {e}")
            if want and "校验不一致" in str(e):
                try:
                    dest.unlink()
                except Exception:
                    pass
            if i < attempts - 1:
                time.sleep(min(8, 2 * (i + 1)))
    raise RuntimeError(f"下载失败（已重试 {attempts} 次）: {last_err}")


def recommended_java(mc_version):
    """按服务端游戏版本算：需要哪个 Java，以及本站能装哪个。

    对照表来自 PaperMC 官方文档（docs.papermc.io/paper/getting-started）：
        1.7.10–1.11 → 8 ｜ 1.12–1.16.4 → 11 ｜ 1.16.5 → 16 ｜
        1.17–1.19 → 17 ｜ 1.20–1.21.11 → 21 ｜ **26.1+ → 25**
    （26.1 起 Mojang 的版本文件写的是 Java 25；用旧 Java 会直接报
      "requires running the server with Java 25 or above" 然后退出。）
    """
    try:
        nums = [int(p) for p in str(mc_version).split("-")[0].split(".")]
    except Exception:
        return None, None
    if not nums:
        return None, None
    major = nums[0]
    minor = nums[1] if len(nums) > 1 else 0
    patch = nums[2] if len(nums) > 2 else 0
    v = (major, minor, patch)
    if major >= 26:
        need = 25
    elif v >= (1, 20, 0):
        need = 21
    elif v >= (1, 17, 0):
        need = 17
    elif v >= (1, 16, 5):
        need = 16
    elif v >= (1, 12, 0):
        need = 11
    else:
        need = 8
    install = need if need in JAVA_CHOICES else next(
        (x for x in JAVA_CHOICES if x >= need), JAVA_CHOICES[-1])
    return need, install


def installed_javas():
    """列出本启动器装过的 Java（runtime/jre-*/bin/java.exe）。"""
    out = []
    try:
        if JAVA_RUNTIME_DIR.is_dir():
            for d in sorted(JAVA_RUNTIME_DIR.iterdir()):
                exe = d / "bin" / "java.exe"
                if exe.exists():
                    out.append((d.name, exe))
    except Exception:
        pass
    return out


def extract_jre(zip_path, dest_dir):
    """解压 JRE zip 并返回 bin/java.exe 的路径（兼容多套一层目录的包）。"""
    dest_dir = Path(dest_dir)
    if dest_dir.exists():
        shutil.rmtree(dest_dir, ignore_errors=True)
    dest_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)
    exe = dest_dir / "bin" / "java.exe"
    if not exe.exists():
        for p in dest_dir.rglob("java.exe"):
            if p.parent.name == "bin":
                exe = p
                break
    if not exe.exists():
        raise RuntimeError("解压后没找到 bin/java.exe")
    return exe


# ==================== 崩溃诊断知识库（v3.4 ⑮） ====================
# 参考来源：PaperMC 官方排查指南(docs.papermc.io/paper/basic-troubleshooting)、
# Minecraft Wiki(Crash)、开源日志分析器 patterns.json(85 条，偏客户端)，
# 再补齐服务端实际会遇到的：Java/端口/内存/存档/插件/加载器/权限/YAML 等。
#
# 每条规则 = (正则, 一句话原因, 怎么办, 严重度)
# 严重度：致命（起不来或崩了） / 警告（能跑但有隐患） / 提示（正常现象，别慌）
CRASH_RULES = [
    # ---------- Java 版本 ----------
    (r"requires running the server with Java (\d+)", "服务端要求的 Java 版本比你当前的高", "去「🔧 设置 → Java 运行时」点「⬇ 一键下载安装」，装需要的版本（装完自动切换）", "致命"),
    (r"requires Java (\d+) or above", "同上：Java 版本太低", "一键安装更高版本的 Java", "致命"),
    (r"UnsupportedClassVersionError.*class file version (\d+)", "用低版本 Java 跑高版本编译的 class（class 版本号能反推需要的 Java）", "class file version 61=Java17、65=Java21、69=Java25；装对应或更高版本", "致命"),
    (r"Unsupported Java detected", "Java 版本不被支持（太老或太新）", "改用推荐版本（概览页顶部会显示）", "致命"),
    (r"java\.lang\.NoSuchMethodError", "你装的插件/mod 是给另一个服务端版本编译的（方法签名对不上）", "把报错里出现的插件/mod 更新或换成适配当前服务端版本的", "致命"),
    (r"java\.lang\.NoClassDefFoundError", "缺依赖：某个类根本没被打进包，或依赖没装", "按崩溃栈里的类名判断缺哪个库，补装依赖；插件要一起装它的前置", "致命"),
    (r"java\.lang\.ClassNotFoundException", "找不到类：依赖缺失或版本不匹配", "补齐前置插件/库，或换适配版本", "致命"),
    (r"org\.bukkit\.plugin\.InvalidPluginException: Unsupported API version", "插件要求的 API 版本比服务端新（插件太新）", "降级插件或用适配当前服务端版本的插件", "警告"),

    # ---------- EULA / 首次启动 ----------
    (r"You need to agree to the EULA", "还没同意 Minecraft EULA（首次启动必须同意）", "点「一键启动」时启动器会自动写 eula=true；也可以自己在 eula.txt 里改成 true", "致命"),
    (r"Failed to load eula\.txt|eula\.txt.*not found", "eula.txt 丢失或损坏", "让启动器重新生成（本地页有个「写 EULA」按钮），或手动建一个 eula.txt 写 eula=true", "警告"),

    # ---------- 端口 / 网络 ----------
    (r"BindException: Address already in use|Cannot bind to port|FAILED TO BIND TO PORT|Perhaps a server is already running", "端口被占用（多半是这个服务器的另一个实例还在跑，或别的程序占了这个端口）", "看「🖥 服务器」页是不是有别的服在运行；或到「⚙ 配置」把服务器端口换一个（如 25566）", "致命"),
    (r"java\.net\.BindException", "绑端口失败", "换端口，或关掉占用该端口的程序", "致命"),
    (r"Failed to verify username", "Mojang 验证服务器连不上（或 online-mode 设置问题）", "先确认网络能通 Mojang；实在不行把 server.properties 的 online-mode 关掉（仅限朋友间玩）", "警告"),
    (r"Connection reset|Connection refused", "连接被重置/拒绝：对方没开服或防火墙拦了", "确认服务器在运行、端口已放行（「🌐 联机」页可一键开端口）", "警告"),
    (r"SocketTimeoutException|Read timed out", "网络超时（对方网络慢或丢包）", "检查网络；服务器卡顿时也会这样", "警告"),
    (r"Outdated server! I.m still on", "客户端版本比服务端新", "让朋友把客户端版本降到和服务端一致", "提示"),
    (r"Outdated client! Please use", "客户端版本比服务端旧", "让朋友升级客户端版本", "提示"),
    (r"This server is not running the correct version", "客户端和服务端版本对不上", "两边版本统一（可用 Via 系列插件做跨版本）", "提示"),

    # ---------- 内存 ----------
    (r"OutOfMemoryError: Java heap space", "内存不够：分配的堆内存太小或实体/区块太多", "到「🔧 设置」把该服最大内存调大（8GB 机器建议不超过 3GB）；或减少插件、限制视距", "致命"),
    (r"OutOfMemoryError: GC overhead limit exceeded", "内存几乎耗尽，GC 空转", "调大内存 + 检查是不是有插件内存泄漏", "致命"),
    (r"OutOfMemoryError: Metaspace", "元空间不足（插件/mod 类太多）", "加 JVM 参数 -XX:MaxMetaspaceSize=512m，或减少插件数量", "致命"),
    (r"OutOfMemoryError: unable to create new native thread", "线程数达到系统上限", "减少插件；调低 JVM 线程相关参数；重启机器", "致命"),
    (r"OutOfMemoryError: Requested array size exceeds VM limit", "单次申请的内存超过 JVM 上限", "多半是某个插件 bug；调大内存或移除该插件", "致命"),
    (r"Could not reserve enough space for object heap|Invalid maximum heap size", "内存参数不合法或系统没有那么多连续内存", "把最大内存调小（不能超过物理内存），关掉其他吃内存的程序", "致命"),
    (r"java\.lang\.OutOfMemoryError", "内存溢出", "调大内存 + 排查占用大户", "致命"),

    # ---------- 存档 / 世界 ----------
    (r"Chunk file at .* is missing|Region file .* is invalid|Chunk file .* is corrupt", "区块文件损坏或丢失（异常关机最容易造成）", "从「📁 文件」页的备份还原世界；以后定期自动备份", "致命"),
    (r"java\.io\.EOFException", "文件读到一半就结束了：多半是文件被写坏（下载中断/异常断电）", "重新下载对应文件；存档损坏就从备份恢复", "警告"),
    (r"Failed to load world|Failed to load level", "世界加载失败", "检查 world 目录是否完整；从备份恢复", "致命"),
    (r"java\.util\.zip\.ZipException: error in opening zip file|invalid LOC header", "jar/zip 文件损坏（下载不完整）", "删掉该 jar 重新下载（启动器的下载有断点续传和大小校验）", "警告"),
    (r"level\.dat.*(missing|not found)", "世界的 level.dat 不见了", "从备份恢复 world 目录", "致命"),
    (r"Ticking entity|Entity ticking error|Ticking block entity", "某个实体/方块实体在计算时抛错（常见于 mod 或红石机器）", "看崩溃栈里是哪个 mod/插件；用工具删掉出问题的实体，或先移除可疑 mod", "致命"),
    (r"Exception in server tick loop", "主循环里抛异常（通常是插件/mod 或配置问题）", "看崩溃栈第一行提到的组件，把最近新加的先去掉试试", "致命"),
    (r"Unknown or incomplete command", "指令写错了（拼写或参数不对）", "对照控制台的指令说明改一下", "提示"),

    # ---------- 插件 ----------
    (r"Could not load .*plugins[\\/].*\.jar|Could not load 'plugins", "插件加载失败", "看下面紧跟的 Caused by；多半是版本不匹配或缺前置", "警告"),
    (r"UnknownDependencyException|Unknown dependency", "插件缺前置依赖", "装上报错里点名的那几个前置插件", "警告"),
    (r"Ambiguous plugin name", "有两个插件用了同一个名字", "删掉重复的那个（文件页可删）", "警告"),
    (r"Circular plugin dependency", "插件互相依赖成环", "调整加载顺序或删掉其中一个", "警告"),
    (r"plugin\.yml.*(missing|not found)|Invalid plugin\.yml", "插件包不完整（少了 plugin.yml）", "重新下载该插件（八成是下载断了）", "警告"),
    (r"Could not pass event .* to", "插件在处理事件时崩了（事件名后面就是插件）", "更新这个插件；还崩就临时禁用", "警告"),
    (r"java\.lang\.NoSuchFieldError", "插件和当前服务端 API 不匹配（字段没了）", "更新插件到适配版本", "致命"),
    (r"java\.lang\.IncompatibleClassChangeError", "依赖冲突：同一个库出现了不兼容的两个版本", "找出重复的库（常见于多个插件打包了同一个依赖）", "致命"),
    (r"java\.lang\.VerifyError", "类校验失败：jar 被改过或编译目标不兼容", "替换该 jar；确认 Java 版本正确", "致命"),
    (r"java\.lang\.StackOverflowError", "无限递归（某个插件/mod 的 bug）", "更新或移除报错的组件", "致命"),
    (r"java\.util\.ConcurrentModificationException", "插件在多线程里乱改集合（代码 bug）", "更新该插件；避免同时执行冲突的指令", "警告"),

    # ---------- 加载器 / mod ----------
    (r"MissingModsException|Missing or unsupported mandatory dependencies", "缺少必需的前置 mod", "按日志里列出的 mod 名补齐依赖", "致命"),
    (r"Incompatible mod set|Mod resolution failed|requires .* of (fabric|minecraft)", "mod 版本组合不兼容", "按提示换版本；Fabric 要装对应游戏版本的 Fabric API", "致命"),
    (r"Mod file .* is missing mods\.toml", "mod 文件不完整或不是给 Forge/NeoForge 的包", "重新下载对应加载器的版本", "警告"),
    (r"@Mixin target .* was not found|InvalidMixinException|Mixin apply failed", "mixin 注入失败：目标类不存在或版本不匹配", "把报错里的 mod 更新到适配游戏版本；N 个 mod 里那个先单独去掉试", "致命"),
    (r"Mixin.*(conflict|Skipping)", "两个 mod 改了同一处代码（冲突）", "去掉其中一个，或找兼容补丁", "警告"),
    (r"Duplicate mod|Found mod file .* of type MOD", "mods 目录里有重复 mod", "删掉旧版本，只留一个", "警告"),
    (r"Registry entry .* was not realized|Missing registry", "注册表项没注册上（mod 加载顺序/兼容问题）", "更新相关 mod；清掉 config 里对应配置文件让它重建", "警告"),
    (r"Couldn't parse loot table|Failed to load model|File .* does not exist", "mod 自带的数据文件缺失或格式错误", "重装该 mod；确认下载完整", "提示"),
    (r"FAILED TO LOAD|Failed to load datapack|Couldn't load datapack", "数据包/资源加载失败", "检查 data packs 是否是给这个游戏版本的", "警告"),

    # ---------- 性能 / 卡顿 ----------
    (r"A single server tick took .* seconds|ServerHangWatchdog|server has not responded", "单次 tick 卡了太久（卡服/死循环）", "看是不是有插件死循环；把 server.properties 的 max-tick-time 调大或设 -1 可先不自动崩", "警告"),
    (r"Can't keep up! Is the server overloaded", "服务器跟不上（CPU 不够或实体太多）", "降视距、减实体、限制刷怪；确认内存和 CPU 够用", "提示"),
    (r"Loaded .* ticks behind", "服务器落后了很多 tick（严重卡顿）", "同上，另可装 Spark 分析性能瓶颈", "警告"),

    # ---------- 磁盘 / 权限 ----------
    (r"No space left on device", "磁盘满了", "清理日志/备份；日志和崩溃报告攒得很快", "致命"),
    (r"AccessDeniedException|Permission denied|Access is denied", "文件权限不足或被占用", "关掉占用的程序；把服务器目录换个有写权限的位置（别放 C:\\Program Files）", "致命"),
    (r"The process cannot access the file because it is being used by another process", "文件被别的程序占着（常见于没关服就删 jar / 备份）", "先停服再操作文件", "警告"),
    (r"Too many open files", "打开的文件数超限", "减少插件；调大系统文件句柄上限", "警告"),
    (r"java\.io\.FileNotFoundException", "找不到文件（路径写错或被删）", "核对文件名和路径；重新下载缺失文件", "警告"),
    (r"java\.io\.IOException", "读写文件出错", "看具体文件名；磁盘满、权限不足、文件损坏都会这样", "警告"),

    # ---------- 配置 / YAML ----------
    (r"mapping values are not allowed here|could not find expected ':'|found character '\\t' that cannot start any token", "YAML 配置写错了（缩进/冒号/用了 Tab）", "用「⚙ 配置」页改；YAML 只能用空格缩进，冒号后要有空格", "致命"),
    (r"while parsing YAML|Cannot load configuration|InvalidConfigurationException", "配置文件格式错误", "对照报错行号改；改坏了就删掉让它重新生成", "警告"),
    (r"Failed to load properties|Invalid properties format", "properties 文件格式错误", "检查有没有乱码或多余字符；必要时删掉重建", "警告"),
    (r"Unknown level type|Invalid level-type", "level-type 填了服务端不认识的类型", "用默认值或服务端支持的（如 minecraft:normal、flat）", "警告"),
    (r"Invalid escape sequence", "配置里的转义写错了（常见于路径里的反斜杠）", "Windows 路径要写成 \\\\ 或改用正斜杠", "提示"),

    # ---------- 视距 / 模拟距离参数（实测踩到：view-distance=128） ----------
    (r"Tick view distance must be a number between (\d+) and (\d+), got: (\d+)",
     "视距参数不合法：server.properties 的 view-distance / simulation-distance 只能 2~32",
     "到「⚙ 配置」页把 view-distance 和 simulation-distance 都改成 10（或删掉这两项，"
     "让服务端用默认值），保存后重新点「一键启动」",
     "致命"),
    (r"Invalid (?:view|simulation)[-_ ]?distance",
     "视距/模拟距离参数不合法",
     "「⚙ 配置」页把 view-distance / simulation-distance 改成 10（合法范围 2~32）",
     "致命"),

    # ---------- 其他常见 ----------
    (r"java\.lang\.NullPointerException", "空指针：某个组件代码有 bug", "看崩溃栈第一行提到的插件/mod，更新或临时移除它", "警告"),
    (r"java\.lang\.IllegalStateException", "状态非法（组件在不该运行的时机被调用）", "更新报错的组件；重启服务端试试", "警告"),
    (r"java\.lang\.IllegalArgumentException", "参数不合法（配置或指令传了错的值）", "看报错细节里提到的字段", "警告"),
    (r"java\.lang\.ArrayIndexOutOfBoundsException|IndexOutOfBoundsException", "数组越界（组件代码 bug）", "更新该组件", "警告"),
    (r"java\.lang\.ClassCastException", "类型转换失败（版本不匹配的典型症状）", "确认 Java 版本和插件/mod 版本都对得上", "警告"),
    (r"java\.lang\.NoSuchElementException|java\.util\.NoSuchElementException", "取不到想要的元素（配置缺项或数据缺失）", "检查配置完整；更新报错组件", "提示"),
    (r"Reached end of input|Unexpected end of", "数据读到一半没了（文件不完整）", "重新下载对应文件", "提示"),
    (r"Failed to authenticate|Invalid session|Failed to log in", "登录验证失败", "检查网络/代理；确认正版账号正常", "警告"),
    (r"You are not whitelisted|not white-listed", "该玩家不在白名单里", "控制台执行 whitelist add <玩家名>，或关掉白名单", "提示"),
    (r"Kicked: .*", "玩家被踢出（后面是原因）", "按提示处理（白名单/正版验证/超时等）", "提示"),
    (r"defineId called for", "同一个注册名被注册了两次（mod 冲突或重复安装）", "删掉重复/冲突的 mod；确认 mods 目录里没有同一 mod 的两个版本", "警告"),
    (r"SINYTRA CONNECTOR IS PRESENT", "装了 Sinytra Connector（让 Fabric mod 跑在 NeoForge 上）", "看到这个提示说明报错很可能来自它；排查时先把 Connector 和它带的 mod 一起停掉试", "提示"),
    (r"Shift\.BY=.*exceeds the maximum allowed", "mixin 的注入偏移超限（mod 与当前版本不匹配）", "更新报错的 mod；或用适配当前游戏版本的版本", "警告"),
    (r"Pack \".*\" is not valid! Can't load it", "资源包/光影包损坏或版本不对（客户端侧问题，一般不影响服务端）", "让客户端重新下载该资源包", "提示"),
    (r"Preparing spawn area: \d+%", "正在生成出生点（首次开服正常现象）", "等它跑完就行，别以为卡死了", "提示"),
    (r"Done \([\d.]+s\)! For help", "服务端启动成功", "可以进游戏了", "提示"),
    (r"Stopping server|Saving worlds", "服务端正在正常关闭/存档", "等它写完再关窗口", "提示"),
]

# 异常类型兜底字典：规则没命中时，按异常大类给解释（覆盖上百种异常）
EXC_TYPES = {
    "NullPointerException": ("代码访问了空对象——几乎总是某个插件/mod 的 bug", "定位崩溃栈里第一个第三方组件，更新或临时禁用", "警告"),
    "ClassNotFoundException": ("运行时找不到类：依赖缺失或版本不对", "补齐前置；确认 Java 版本", "致命"),
    "NoClassDefFoundError": ("类在编译时在、运行时没了：依赖没打包或冲突", "补依赖或换插件版本", "致命"),
    "NoSuchMethodError": ("调用了不存在的方法：组件和服务端版本不匹配", "更新组件到适配版本", "致命"),
    "NoSuchFieldError": ("访问了不存在的字段：同上", "更新组件", "致命"),
    "UnsupportedClassVersionError": ("Java 版本太低，跑不了高版本编译的类", "一键安装对应 Java", "致命"),
    "OutOfMemoryError": ("内存不够", "调大内存、减少插件/实体", "致命"),
    "StackOverflowError": ("无限递归", "更新报错组件", "致命"),
    "IllegalStateException": ("在不该发生的状态下调用了组件", "更新组件或重启", "警告"),
    "IllegalArgumentException": ("传了不合法的参数（多半是配置/指令写错）", "按报错细节改参数", "警告"),
    "ClassCastException": ("类型转换失败：版本不匹配的典型症状", "统一 Java 与组件版本", "警告"),
    "ConcurrentModificationException": ("多线程并发修改数据（代码 bug）", "更新组件；避免同时触发冲突操作", "警告"),
    "ArrayIndexOutOfBoundsException": ("数组越界（代码 bug）", "更新组件", "警告"),
    "IndexOutOfBoundsException": ("下标越界（代码 bug）", "更新组件", "警告"),
    "IOException": ("文件/网络读写失败", "看具体文件名：磁盘满、权限、损坏都可能", "警告"),
    "FileNotFoundException": ("文件不存在", "核对路径或重新下载", "警告"),
    "EOFException": ("文件被截断（写到一半断了）", "重新下载；存档损坏从备份恢复", "警告"),
    "ZipException": ("压缩包损坏", "重新下载该 jar/zip", "警告"),
    "BindException": ("端口被占用或没权限绑定", "换端口或关掉占用程序", "致命"),
    "ConnectException": ("连不上目标（服务未启动/防火墙）", "确认对端在跑、端口已放行", "警告"),
    "SocketTimeoutException": ("网络超时", "检查网络质量", "提示"),
    "InterruptedException": ("线程被中断（多在关服时出现）", "一般可忽略", "提示"),
    "TimeoutException": ("操作超时", "网络慢或服务器卡；看是哪一步", "提示"),
    "ExceptionInInitializerError": ("类初始化失败（静态代码块里抛错）", "更新报错组件", "致命"),
    "NoSuchElementException": ("取不到想要的元素（配置缺项）", "补全配置", "提示"),
    "UnsupportedOperationException": ("组件调用了不支持的操作", "更新组件或改配置", "警告"),
    "NumberFormatException": ("字符串转数字失败（配置里写了非数字）", "把该配置项改成数字", "警告"),
    "VerifyError": ("类校验失败（jar 被改坏或版本不兼容）", "换一份干净的 jar", "致命"),
    "IncompatibleClassChangeError": ("依赖里同一个类有两个不兼容版本", "找出重复依赖", "致命"),
    "LinkageError": ("链接错误（版本/依赖问题）", "统一依赖版本", "致命"),
    "RuntimeException": ("运行时异常（具体看下一行的 Caused by）", "按 Caused by 里的组件排查", "警告"),
}


def analyze_log(text, limit=6):
    """扫描日志文本 → 返回发现列表（已按严重度排序、去重）。

    返回 [{"sev","why","fix","match","detail"}]；没发现问题就返回 []。

    v3.5.10：修"谜语人"——有明确致命原因时，
      · 把"服务端正在正常关闭/存档"这类正常收尾的提示当噪音去掉；
      · 不再补一条大而全的异常类型说明（同一件事说两遍反而糊）。
    """
    if not text:
        return []
    order = {"致命": 0, "警告": 1, "提示": 2}
    found, seen = [], set()

    for pat, why, fix, sev in CRASH_RULES:
        try:
            m = re.search(pat, text, re.IGNORECASE)
        except re.error:
            continue
        if not m:
            continue
        if why in seen:
            continue
        seen.add(why)
        detail = "、".join(g for g in (m.groups() or ()) if g)[:100]
        found.append({"sev": sev, "why": why, "fix": fix,
                      "match": m.group(0)[:150].strip(), "detail": detail})

    has_fatal = any(f["sev"] == "致命" for f in found)

    # 异常类型兜底：日志里出现的任何 XxxException / XxxError 都试着解释一下
    for m in re.finditer(
            r"\b([A-Z][A-Za-z0-9_]*(?:Exception|Error|Throwable))\b", text):
        cls = m.group(1)
        if cls in EXC_TYPES:
            why, fix, sev = EXC_TYPES[cls]
            if has_fatal and sev != "致命":
                # 已经有更具体的致命结论了，别再补一句"参数不合法"凑条数
                continue
            key = f"{cls}:{why}"
            if key in seen:
                continue
            seen.add(key)
            found.append({"sev": sev, "why": f"{why}",
                          "fix": fix, "match": cls, "detail": cls})
        if len(found) > 40:
            break

    found.sort(key=lambda d: order.get(d["sev"], 3))
    found = _dedupe_findings(found)
    if any(f["sev"] == "致命" for f in found):
        found = [f for f in found if f["why"] not in DIAG_NOISE_WHY
                 and f["why"] not in DIAG_GENERIC_WHY]
    return found[:limit]


# 这些是"结果/正常收尾"，不是原因：有明确致命原因时从结论里去掉
DIAG_NOISE_WHY = {
    "服务端正在正常关闭/存档",
    "服务端启动成功",
    "正在生成出生点（首次开服正常现象）",
}

# 这些"大而全"的通用解释，有具体致命结论时就不说了（否则一件事说三遍，像谜语）
DIAG_GENERIC_WHY = {
    "参数不合法（配置或指令传了错的值）",
    "传了不合法的参数（多半是配置/指令写错）",
}

# 找"最该看的那一行报错"：异常类行 → 带 ERROR 的说明行 → 任意 ERROR 行
KEY_ERROR_PATTERNS = (
    re.compile(r"^\s*[a-zA-Z_$][\w.$]*(?:Exception|Error)\b[^\n]*$", re.MULTILINE),
    re.compile(r"\b(?:ERROR|FATAL)\b[^\n]*"
               r"(?:Exception|Error|failed|Failed|must be|Invalid|corrupt)[^\n]*"),
    re.compile(r"\b(?:ERROR|FATAL)\b[^\n]+"),
)


def key_error_line(text, limit=300):
    """从日志里揪出最该看的那一行报错（诊断结论第一行用）。"""
    if not text:
        return ""
    try:
        clean = strip_ansi(text)
    except Exception:
        clean = text
    for pat in KEY_ERROR_PATTERNS:
        m = pat.search(clean)
        if not m:
            continue
        line = m.group(0).strip()
        line = re.sub(r"^\[\d{2}:\d{2}:\d{2}\s+(?:ERROR|FATAL)\]:\s*", "", line)
        if len(line) > 8:
            return line[:limit]
    return ""


def _dedupe_findings(items):
    out, seen = [], set()
    for it in items:
        if it["why"] in seen:
            continue
        seen.add(it["why"])
        out.append(it)
    return out


def suspect_components(text):
    """从崩溃栈里找可疑的插件/mod（只看 plugins/ 和 mods/ 目录里的 jar）。

    v3.5.10：以前连 [ChunkTaskScheduler] 这种日志前缀都当成"可疑组件"，
    结果报的嫌疑对象其实是 Paper 自己的线程池名字 → 误导。现在宁缺毋滥：
    只认 plugins/mods 目录下的 jar 文件名。
    """
    names = []
    for pat in (r"plugins[\\/]([A-Za-z0-9_.\-]+\.jar)",
                r"mods[\\/]([A-Za-z0-9_.\-]+\.jar)",
                r"plugins[\\/][^\\/\n]{1,40}[\\/]([A-Za-z0-9_.\-]+\.jar)"):
        for m in re.finditer(pat, text, re.IGNORECASE):
            n = m.group(1)
            if n not in names:
                names.append(n)
            if len(names) >= 4:
                return names
    return names


def upload_log_to_mclogs(text, source="Minecraft 一键开服启动器"):
    """上传日志到 mclo.gs（第三方分析器），返回可分享的 URL。"""
    body = json.dumps({"content": text[:5 * 1024 * 1024],
                       "source": source}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.mclo.gs/1/log", data=body,
        headers={**HEADERS, "Content-Type": "application/json"})
    for ctx in (None, UNVERIFIED_CTX):
        try:
            kw = {"timeout": 40}
            if ctx is not None:
                kw["context"] = ctx
            with urllib.request.urlopen(req, **kw) as resp:
                data = json.loads(resp.read().decode("utf-8", "replace"))
            if data.get("success"):
                return data.get("url")
            raise RuntimeError(data.get("error") or "上传失败")
        except Exception as e:
            last = e
            continue
    raise RuntimeError(str(last))


# ==================== 主程序 ====================
# ==================== v3.5（⑳）彩色花样文字 ====================
# Minecraft 的颜色/格式代码：&0~&f 十六色、&k~&o 五种格式、&r 重置。
# 每项 = (代码, 中文名, 预览色, tellraw 里的英文名)
MC_COLORS = (
    ("0", "黑", "#000000", "black"),
    ("1", "深蓝", "#0000AA", "dark_blue"),
    ("2", "深绿", "#00AA00", "dark_green"),
    ("3", "深青", "#00AAAA", "dark_aqua"),
    ("4", "深红", "#AA0000", "dark_red"),
    ("5", "深紫", "#AA00AA", "dark_purple"),
    ("6", "金", "#FFAA00", "gold"),
    ("7", "灰", "#AAAAAA", "gray"),
    ("8", "深灰", "#555555", "dark_gray"),
    ("9", "蓝", "#5555FF", "blue"),
    ("a", "绿", "#55FF55", "green"),
    ("b", "青", "#55FFFF", "aqua"),
    ("c", "红", "#FF5555", "red"),
    ("d", "粉", "#FF55FF", "light_purple"),
    ("e", "黄", "#FFFF55", "yellow"),
    ("f", "白", "#FFFFFF", "white"),
)
MC_FORMATS = (
    ("l", "加粗", "bold"),
    ("o", "斜体", "italic"),
    ("n", "下划线", "underlined"),
    ("m", "删除线", "strikethrough"),
    ("k", "乱码", "obfuscated"),
)
MC_COLOR_HEX = {c: hx for c, _n, hx, _j in MC_COLORS}
MC_COLOR_JSON = {c: j for c, _n, _hx, j in MC_COLORS}
MC_FORMAT_JSON = {c: j for c, _n, j in MC_FORMATS}
MC_ALL_CODES = set(MC_COLOR_HEX) | set(MC_FORMAT_JSON) | {"r"}
MC_DEMO_TEXT = "&6&l我的服务器 &r&a生存 &7| &b1.21.11 &e欢迎来玩"


def _mc_parse(text):
    """解析带 &/§ 代码的文本 → [(文字, 颜色码或None, 格式码元组), ...]。

    规则跟游戏一致：颜色码会清掉之前的格式，&r 清掉颜色和格式，
    认不出来的代码当普通文字（不吞掉后面那个字）。
    """
    segs = []
    buf = []
    color = None
    fmts = []

    def flush():
        if buf:
            segs.append(("".join(buf), color, tuple(fmts)))
            del buf[:]

    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1].lower() if i + 1 < n else ""
        if ch in ("&", "§") and nxt:
            if nxt in MC_COLOR_HEX:
                flush()
                color, fmts = nxt, []
                i += 2
                continue
            if nxt in MC_FORMAT_JSON:
                flush()
                if nxt not in fmts:
                    fmts.append(nxt)
                i += 2
                continue
            if nxt == "r":
                flush()
                color, fmts = None, []
                i += 2
                continue
        buf.append(ch)
        i += 1
    flush()
    return segs


def _mc_convert(text, target):
    """把文本里的 & / § 代码统一成 target，认不出的代码原样留下。"""
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1].lower() if i + 1 < n else ""
        if ch in ("&", "§") and nxt in MC_ALL_CODES:
            out.append(target + nxt)
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def mc_preview_runs(text):
    """界面预览用：[(文字, 颜色HEX或None, 格式码元组), ...]。"""
    return [(t, MC_COLOR_HEX.get(c), f) for t, c, f in _mc_parse(text)]


def mc_section(text):
    """输出 § 码文本（进游戏、写 server.properties / MOTD 用）。"""
    return _mc_convert(text, "§")


def mc_amp(text):
    """输出 & 码文本（发帖、跟人交流、写插件配置用）。"""
    return _mc_convert(text, "&")


def mc_motd(text):
    """MOTD 只有一行：换行折成空格，去掉首尾空白。"""
    return _mc_convert(" ".join(text.splitlines()), "§").strip()


def mc_tellraw(text, prefix=""):
    """输出 /tellraw 的 JSON 组件（可直接接在 /tellraw @a 后面）。"""
    parts = [prefix] if prefix else []
    for seg, color, fmts in _mc_parse(text):
        item = {"text": seg}
        if color:
            item["color"] = MC_COLOR_JSON[color]
        for code in fmts:
            item[MC_FORMAT_JSON[code]] = True
        parts.append(item)
    return json.dumps(parts, ensure_ascii=False)


# ==================== v3.5（⑭）日志离线中文翻译 ====================
# 一条条正则，不联网。顺序有意义：越具体的放越前面，先匹配到就用它。
# \1 \2 会被替换成正则捕获到的内容。
LOG_TRANSLATIONS = (
    (r"Starting minecraft server version (.+)",
     "正在启动 Minecraft 服务端，版本 \1"),
    (r"Loading libraries, please wait", "正在加载依赖库，稍等"),
    (r"Loading properties", "读取 server.properties 配置"),
    (r"Default game type: (\w+)",
     "默认游戏模式：\1（0=生存 1=创造 2=冒险 3=旁观）"),
    (r"Generating keypair", "生成服务器密钥（首次启动会慢一点）"),
    (r"Starting Minecraft server on (.+)", "服务端开始监听 \1"),
    (r"Using (\w+) for I/O", "用 \1 做磁盘读写"),
    (r"Preparing level \"(.+)\"", "正在准备世界「\1」（首次启动要生成地形）"),
    (r"Preparing start region for dimension (\S+)", "生成出生点附近的地形：\1"),
    (r"Preparing spawn area: (\d+)%", "出生点生成进度 \1%"),
    (r"Time elapsed: (\d+) ms", "这一步用了 \1 毫秒"),
    (r"Done \(([\d.]+)s\)!.*", "✅ 服务端启动完成！用了 \1 秒，可以进游戏了"),
    (r"Done \(\d", "✅ 服务端启动完成"),
    (r"Stopping the server|Stopping server", "正在关闭服务器"),
    (r"Saving worlds|Saving chunks", "正在保存世界数据（先别关窗口）"),
    (r"Server stopped", "服务端已经停止"),
    (r"(?:^|\]: )([A-Za-z0-9_]{1,16}) joined the game", "玩家「\1」上线了"),
    (r"(?:^|\]: )([A-Za-z0-9_]{1,16}) left the game", "玩家「\1」下线了"),
    (r"(?:^|\]: )([A-Za-z0-9_]{1,16}) lost connection: (.+)",
     "玩家「\1」掉线了（\2）"),
    (r"<(\w+)> (.*)", "玩家「\1」说：\2"),
    (r"(\w+) has made the advancement \[(.+)\]", "玩家「\1」达成了进度「\2」"),
    (r"(\w+) issued server command: (.*)", "玩家「\1」执行了指令 \2"),
    (r"(\w+) was slain by (.+)", "玩家「\1」被 \2 打死了"),
    (r"(\w+) was shot by (.+)", "玩家「\1」被 \2 射死了"),
    (r"(\w+) was impaled by (.+)", "玩家「\1」被 \2 戳死了"),
    (r"(\w+) was fireballed by (.+)", "玩家「\1」被 \2 的火球打死了"),
    (r"(\w+) was killed by (.+)", "玩家「\1」被 \2 杀了"),
    (r"(\w+) drowned", "玩家「\1」淹死了"),
    (r"(\w+) (fell from a high place|fell to their death|hit the ground too hard)",
     "玩家「\1」摔死了"),
    (r"(\w+) burned to death|(\w+) went up in flames", "玩家「\1」被烧死了"),
    (r"(\w+) blew up", "玩家「\1」被炸死了"),
    (r"(\w+) starved to death", "玩家「\1」饿死了"),
    (r"(\w+) tried to swim in lava", "玩家「\1」掉进岩浆里了"),
    (r"(\w+) suffocated in a wall", "玩家「\1」卡在方块里窒息了"),
    (r"(\w+) withered away", "玩家「\1」被凋零效果弄死了"),
    (r"(\w+) froze to death", "玩家「\1」冻死了"),
    (r"Can't keep up!.*?Running (\d+)ms.*?(\d+) ticks behind",
     "⚠ 服务端跟不上：落后 \2 tick（\1 毫秒）——机器太忙或区块太多，会卡"),
    (r"Overloaded", "⚠ 服务端过载（会卡顿）"),
    (r"OutOfMemoryError",
     "内存不够了（Java 堆溢出）→ 去「设置 → 服务器设置」把该服最大内存调大"),
    (r"UnsupportedClassVersionError|requires Java \d+|class file version",
     "Java 版本不对 → 这个核心要更新的 Java，去「设置 → Java 运行时」一键装"),
    (r"Address already in use|Failed to bind to port|already running",
     "端口被占用 → 已经有一个服务端在跑了，先把那个关掉"),
    (r"agree to the EULA|eula\.txt",
     "还没同意 EULA → 把 eula.txt 里的 eula=false 改成 true"),
    (r"Unknown or incomplete command|Unknown command", "指令打错了（或这版本没这条指令）"),
    (r"That player does not exist|No player was found",
     "没找到这个玩家（名字打错或人不在线）"),
    (r"You do not have permission", "没有权限执行这条指令（你不是管理员）"),
    (r"Could not load '(?:plugins|mods)/(.+?)'",
     "这个插件/模组加载失败：\1（多半是版本对不上）"),
    (r"Exception in server tick loop|Encountered an unexpected exception",
     "服务端主循环异常 → 接下来多半会崩（看后面的 Caused by）"),
    (r"Caused by:", "↑ 上面那串报错的根本原因就是这一行"),
    (r"UUID of player (\w+) is", "玩家「\1」的身份编号（正版验证用）"),
    (r"RCON running on", "RCON 远程控制台已开启"),
    (r"Starting remote control listener", "正在启动 RCON"),
    (r"Loading (\d+) recipes|Loaded (\d+) recipes", "加载合成表"),
    (r"Reloading ResourceManager", "重新加载资源包"),
    (r"online-mode=false|not in online mode",
     "离线模式：不做正版验证，谁都能用你的名字进来"),
    (r"\[Server thread/WARN\]: (.+)", "⚠ 警告：\1"),
)


def _fix_repl(tpl):
    """模板里的 \\1 \\2 是"第几个捕获组"的占位符。

    但写成普通字符串时 Python 会把 \\1 读成控制字符 \\x01，这里统一还原成
    反斜杠+数字，再用 re.Match.expand 填内容（等于正则替换里的 \\1）。
    """
    return re.sub(r"[\x01-\x09]",
                  lambda m: "\\" + str(ord(m.group(0))), tpl)


# 预编译：控制台每来一行都要过一遍词库，别每次现编正则
LOG_TRANSLATIONS = tuple((re.compile(pat), _fix_repl(zh))
                         for pat, zh in LOG_TRANSLATIONS)


def translate_log_line(line):
    """把一行服务端日志翻译成中文。翻不出来返回空字符串。"""
    s = str(line).strip()
    if not s or s.startswith("[启动器]"):
        return ""
    # 去掉 "[12:34:56] [Server thread/INFO]:" / "[22:31:10 INFO]:" 这类前缀，只留正文
    # （v3.5.13：Paper 新版是 "[22:31:10 INFO]:" 单括号格式，以前没剥掉，
    #   结果"joined the game"那句翻成了「玩家「[22:31:10 INFO]: Steve」上线了」）
    for _pre in (r"^\[[\d:.]+\]\s*\[[^\]]+\]:\s*(.*)$",
                 r"^\[[\d:.]+\s+[A-Za-z]+\]:\s*(.*)$",
                 r"^\[[\d:.]+\]:\s*(.*)$"):
        m = re.match(_pre, s)
        if m:
            s = m.group(1).strip()
            break
    if not s:
        return ""
    for pat, zh in LOG_TRANSLATIONS:
        found = pat.search(s)
        if found:
            try:
                return found.expand(zh)
            except Exception:
                return zh
    return ""


# ==================== v3.5（⑧）离线 HTML 手册 ====================
# 整份手册内嵌在程序里：不联网也能看，打包成 exe 也带着走。
# 故意不引用任何外部 css/js/字体（离线打开不能有半张白页）。
MANUAL_HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>新手上路手册 · Git / GitHub + 开服</title>
<style>
body{font-family:"Microsoft YaHei",system-ui,sans-serif;max-width:860px;
margin:0 auto;padding:24px 18px 80px;line-height:1.75;color:#222;background:#fafafa}
h1{font-size:26px;border-bottom:3px solid #2ecc71;padding-bottom:8px}
h2{font-size:20px;margin-top:34px;color:#1f6aa5}
h3{font-size:16px;margin-top:20px}
code,pre{font-family:Consolas,monospace;background:#2b2b2b;color:#eee;
border-radius:6px}
code{padding:2px 6px;font-size:13px}
pre{padding:12px 14px;overflow-x:auto;font-size:13px;line-height:1.6}
.tip{background:#eafaf1;border-left:4px solid #2ecc71;padding:10px 14px;border-radius:4px}
.warn{background:#fdf3e7;border-left:4px solid #f39c12;padding:10px 14px;border-radius:4px}
.bad{background:#fdecea;border-left:4px solid #e74c3c;padding:10px 14px;border-radius:4px}
table{border-collapse:collapse;width:100%;margin:10px 0}
th,td{border:1px solid #ccc;padding:6px 10px;text-align:left;font-size:14px}
th{background:#eef3f8}
.small{color:#777;font-size:13px}
</style></head><body>

<h1>新手上路手册</h1>
<p class="small">这份手册是启动器自带的，离线也能看。前半是 Git / GitHub 从零开始，
后半是开服常见问题。看着长，其实只要会其中 6 条命令就够用了。</p>

<h2>0. 先搞明白三个词</h2>
<table>
<tr><th>词</th><th>人话解释</th></tr>
<tr><td><b>Git</b></td><td>装在你自己电脑上的"存档工具"。每存一次档叫一次提交(commit)，
随时能翻回以前的版本，改坏了不怕。</td></tr>
<tr><td><b>GitHub</b></td><td>一个放代码的网站。把本地存档"推"上去，换台电脑能"拉"下来，
也能分享给别人。</td></tr>
<tr><td><b>仓库(repo)</b></td><td>一个被 Git 管起来的文件夹，里面还藏着一个 .git 目录
（别删它，删了存档记录就没了）。</td></tr>
</table>

<h2>1. 装 Git（Windows）</h2>
<p>去 <b>https://git-scm.com/download/win</b> 下载安装，一路"下一步"就行。装完开
<b>Git Bash</b>（开始菜单里搜），或者用 Windows 自带的 PowerShell 也行。</p>
<pre>git --version</pre>
<p>能打印出版本号（例如 <code>git version 2.47.0</code>）就是装好了。</p>

<h2>2. 只做一次的两条设置</h2>
<pre>git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"</pre>
<p class="tip">这两条是"每次存档要签谁的名字"。不用和 GitHub 账号同名，但邮箱建议一致。</p>

<h2>3. 建仓库 + 第一次存档</h2>
<pre>cd 你的项目文件夹
git init                  # 把这个文件夹交给 Git 管
git status                # 看现在什么情况（最常用的命令）
git add .                 # 把所有改动放进"待存档"
git commit -m "第一次提交"  # 真正存档，并写一句说明</pre>
<p class="tip">口诀：<b>改完 → status 看一眼 → add → commit</b>。commit 只存在你电脑上，
不联网也能用。</p>

<h2>4. 连到 GitHub 并推上去</h2>
<pre># 先在网页上新建一个空仓库（不要勾选 README），然后：
git remote add origin https://github.com/你的账号/仓库名.git
git branch -M main
git push -u origin main</pre>
<p>第一次 push 会弹登录窗口：推荐用浏览器登录（Git Credential Manager），
不用手打密码。之后就不用再登了。</p>

<h2>5. 换电脑 / 拉别人的项目</h2>
<pre>git clone https://github.com/账号/仓库名.git   # 第一次下载
git pull                                        # 以后每次开工前先拉一下</pre>
<p class="warn">养成习惯：<b>先 pull，再改，再 commit，再 push</b>。
不 pull 就改，push 的时候十有八九被拒。</p>

<h2>6. 分支（够用就行的程度）</h2>
<pre>git switch -c 新功能      # 开一条新分支干活（旧写法 git checkout -b）
git switch main           # 切回主线
git merge 新功能          # 把那条分支合进当前分支</pre>
<p class="small">一个人用的话，分支不是必须的；想试危险改动又怕弄坏主线时用它最舒服。</p>

<h2>7. 常用命令速查</h2>
<table>
<tr><th>命令</th><th>干嘛的</th></tr>
<tr><td><code>git status</code></td><td>现在哪些文件改了、哪些已经待存档</td></tr>
<tr><td><code>git diff</code></td><td>具体改了哪几行</td></tr>
<tr><td><code>git log --oneline</code></td><td>存档历史（一行一条）</td></tr>
<tr><td><code>git add 文件名</code> / <code>git add .</code></td><td>把改动放进待存档</td></tr>
<tr><td><code>git commit -m "说明"</code></td><td>存档</td></tr>
<tr><td><code>git push</code> / <code>git pull</code></td><td>推到 GitHub / 从 GitHub 拉</td></tr>
<tr><td><code>git restore 文件名</code></td><td>把这个文件改回上次存档的样子（没提交的改动会丢）</td></tr>
<tr><td><code>git reset --hard HEAD</code></td><td>整个文件夹回到上次存档（危险，改动全丢）</td></tr>
<tr><td><code>git checkout 提交号 -- 文件</code></td><td>只把某个文件恢复到某次提交</td></tr>
</table>

<h2>8. 常见报错怎么办</h2>
<h3>① push 被拒：rejected ... non-fast-forward</h3>
<p class="bad">意思是：GitHub 上有你电脑上没有的提交（多半是在网页上改过，或者另一台电脑推过）。</p>
<pre>git pull --rebase origin main
git push</pre>

<h3>② 冲突：CONFLICT (content): Merge conflict in 某文件</h3>
<p class="bad">意思是：同一行你和别人（或你自己两次改）改得不一样，Git 不敢替你选。</p>
<p>打开那个文件，会看到这样的记号，把 <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code> 之间的内容
改成你想要的最终样子，然后把三行记号删掉：</p>
<pre>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD
你这边的写法
=======
另一边的写法
&gt;&gt;&gt;&gt;&gt;&gt;&gt; 分支名</pre>
<pre>git add 那个文件
git commit -m "解决冲突"</pre>

<h3>③ 认证失败：Authentication failed / Support for password authentication was removed</h3>
<p class="bad">GitHub 早就不让用账号密码推代码了。</p>
<p>解决办法：装 <b>Git Credential Manager</b>（新版 Git for Windows 自带），
然后 <code>git push</code> 会弹浏览器登录；或者用 Personal Access Token 当密码。</p>

<h3>④ 不小心 add 了不该传的东西（.jar / world / 密码）</h3>
<pre>git rm --cached 文件名      # 从 Git 里移除，但本地文件还在
echo "文件名" &gt;&gt; .gitignore  # 以后不再跟踪</pre>
<p class="warn">如果已经 push 上去了，光删文件不够——历史里还在。最省事的做法是：
改掉泄露的密码/令牌，然后把仓库设成私有。</p>

<h3>⑤ 提示 dubious ownership / 不安全目录</h3>
<pre>git config --global --add safe.directory 那个路径</pre>

<h2>9. 给 Minecraft 服主：哪些东西不该上传</h2>
<p class="tip">服务端目录动辄几个 G，世界上传上去又慢又占空间。建议只传
<b>配置文件</b>（server.properties、plugins 里插件的 .yml 配置），
不传 <b>jar / world / logs / cache</b>。在项目根放一个 <code>.gitignore</code>：</p>
<pre># 服务端
*.jar
world/
world_nether/
world_the_end/
logs/
cache/
backups/
# 启动器
launcher_state.json
console_cmds.json
.venv/
__pycache__/
*.pyc</pre>
<p class="small">plugins/ 里想只留配置、不留 jar，可以写
<code>plugins/*.jar</code>。</p>

<h2>10. 开服常见问题（启动器角度）</h2>
<table>
<tr><th>现象</th><th>怎么办</th></tr>
<tr><td>启动就退，日志说到 Java 版本</td><td>「设置 → Java 运行时 → 一键下载安装」，
按概览页提示的"推荐 Java 版本"装</td></tr>
<tr><td>卡在"正在启动"，半天没反应</td><td>首次启动要生成世界，等 1~3 分钟；
控制台看到 <code>Done</code> 才算好</td></tr>
<tr><td>提示端口被占用</td><td>已经有一个服务端在跑，先把它关掉；或到「配置」页换端口</td></tr>
<tr><td>内存不够 / OutOfMemoryError</td><td>「设置 → 服务器设置」把该服最大内存调大（8G 机器建议 ≤4）</td></tr>
<tr><td>玩家进不来</td><td>看「联机」页的网络检测与防火墙指引；正版服确认 online-mode</td></tr>
<tr><td>崩了不知道为啥</td><td>控制台点「🔍 分析日志找原因」；看不懂的日志会自动附中文翻译</td></tr>
</table>

<h2>11. 心里话</h2>
<p>Git 只有 6 条命令是天天用的：<code>status / add / commit / pull / push / log</code>。
其它的用到再查，忘光了也没关系，重新打开这份手册就行。</p>
<p class="small">—— 本手册由启动器内置（离线），随时在「设置」页点「打开离线手册」再看一遍。</p>
</body></html>
"""


def write_manual(dest=None):
    """把离线手册写成 HTML 文件，返回路径（失败返回 None）。"""
    try:
        dest = Path(dest) if dest else (BASE_DIR / "使用手册.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(MANUAL_HTML, encoding="utf-8")
        return dest
    except Exception as e:
        print(f"[启动器] 写手册失败: {e}")
        return None


def datapacks_dir():
    """当前服务器的数据包目录。数据包跟着世界存档走，所以放在 world/ 里。"""
    return SERVER_DIR / "world" / "datapacks"


# ==================== v3.5（⑲）玩家背包（只读） ====================
# nbtlib 是延迟导入的（不拖慢启动）。这里只读 .dat，绝不写。
ITEM_CN = {
    "minecraft:diamond": "钻石", "minecraft:diamond_sword": "钻石剑",
    "minecraft:diamond_pickaxe": "钻石镐", "minecraft:diamond_axe": "钻石斧",
    "minecraft:diamond_shovel": "钻石锹", "minecraft:diamond_helmet": "钻石头盔",
    "minecraft:diamond_chestplate": "钻石胸甲",
    "minecraft:diamond_leggings": "钻石护腿", "minecraft:diamond_boots": "钻石靴子",
    "minecraft:iron_ingot": "铁锭", "minecraft:iron_sword": "铁剑",
    "minecraft:iron_pickaxe": "铁镐", "minecraft:iron_helmet": "铁头盔",
    "minecraft:golden_apple": "金苹果", "minecraft:enchanted_golden_apple": "附魔金苹果",
    "minecraft:netherite_ingot": "下界合金锭",
    "minecraft:netherite_sword": "下界合金剑",
    "minecraft:emerald": "绿宝石", "minecraft:coal": "煤炭",
    "minecraft:charcoal": "木炭", "minecraft:redstone": "红石",
    "minecraft:lapis_lazuli": "青金石", "minecraft:quartz": "下界石英",
    "minecraft:ancient_debris": "远古残骸", "minecraft:nether_star": "下界之星",
    "minecraft:totem_of_undying": "不死图腾", "minecraft:elytra": "鞘翅",
    "minecraft:shield": "盾牌", "minecraft:bow": "弓", "minecraft:arrow": "箭",
    "minecraft:ender_pearl": "末影珍珠", "minecraft:blaze_rod": "烈焰棒",
    "minecraft:cobblestone": "圆石", "minecraft:stone": "石头",
    "minecraft:dirt": "泥土", "minecraft:grass_block": "草方块",
    "minecraft:oak_log": "橡木原木", "minecraft:oak_planks": "橡木木板",
    "minecraft:sand": "沙子", "minecraft:gravel": "沙砾",
    "minecraft:glass": "玻璃", "minecraft:torch": "火把",
    "minecraft:bread": "面包", "minecraft:cooked_beef": "牛排",
    "minecraft:apple": "苹果", "minecraft:gold_ingot": "金锭",
    "minecraft:bucket": "桶", "minecraft:water_bucket": "水桶",
    "minecraft:lava_bucket": "岩浆桶", "minecraft:obsidian": "黑曜石",
    "minecraft:experience_bottle": "附魔之瓶",
    "minecraft:shulker_box": "潜影盒", "minecraft:chest": "箱子",
}
ARMOR_SLOTS = {100: "靴子", 101: "护腿", 102: "胸甲", 103: "头盔"}


def nbtlib_module():
    """延迟导入 nbtlib；没装就返回 None（界面会提示一键安装）。"""
    try:
        import nbtlib
        return nbtlib
    except Exception:
        return None


def player_cache():
    """读 usercache.json → {玩家名: uuid(去掉短横线)}。服务器自己维护的名单。"""
    try:
        data = json.loads(
            (SERVER_DIR / "usercache.json").read_text(encoding="utf-8"))
        out = {}
        for e in data if isinstance(data, list) else []:
            if e.get("name") and e.get("uuid"):
                out[str(e["name"])] = str(e["uuid"]).replace("-", "").lower()
        return out
    except Exception:
        return {}


def playerdata_dir():
    return SERVER_DIR / "world" / "playerdata"


def slot_label(slot):
    """把槽位号翻成人话（-106 是副手，100~103 是盔甲）。"""
    try:
        slot = int(slot)
    except Exception:
        return "?"
    if 0 <= slot <= 8:
        return f"快捷栏 {slot + 1}"
    if 9 <= slot <= 35:
        return f"背包 {slot - 8}"
    if slot in ARMOR_SLOTS:
        return ARMOR_SLOTS[slot]
    if slot == -106:
        return "副手"
    return f"槽位 {slot}"


def item_display(item_id):
    """物品显示名：有中文名就用中文名，没有就把 minecraft: 前缀去掉。"""
    raw = str(item_id)
    return ITEM_CN.get(raw, raw.replace("minecraft:", ""))


def _nbt_items(seq):
    """把 NBT 里的物品列表整理成 [{'slot','id','count','display','extra'}]。"""
    out = []
    for it in (seq or []):
        try:
            slot = int(it.get("Slot", 0))
        except Exception:
            slot = 0
        try:
            count = int(it.get("Count", 1))
        except Exception:
            count = 1
        iid = str(it.get("id", "?"))
        extra = []
        try:
            dmg = it.get("Damage")
            if dmg:
                extra.append(f"耐久损失 {int(dmg)}")
        except Exception:
            pass
        try:
            for e in (it.get("Enchantments") or []):
                extra.append(str(e.get("id", "")).replace("minecraft:", ""))
        except Exception:
            pass
        try:
            name = it.get("display", {}).get("Name")
            if name:
                extra.append("改名了")
        except Exception:
            pass
        out.append({"slot": slot, "id": iid, "count": count,
                    "display": item_display(iid), "extra": extra})
    out.sort(key=lambda d: d["slot"])
    return out


def playerdata_path(uuid):
    """玩家存档路径 world/playerdata/<uuid>.dat（v3.5.16）。

    坑：MC 服务端存的文件名是**带短横线**的 uuid（如 3f2a91c4-7b1e-…），
    以前这里把短横线全删了去找，永远"找不到存档"（用户实测踩到）。
    现在三种写法都试：带短横线 / 去掉短横线 / 原样。
    """
    raw = str(uuid or "").strip()
    d = playerdata_dir()
    cands = []
    h = raw.replace("-", "").lower()
    if len(h) == 32:
        dashed = (f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}")
        cands.append(d / f"{dashed}.dat")
        cands.append(d / f"{h}.dat")
    if raw:
        cands.append(d / f"{raw}.dat")
    for p in cands:
        try:
            if p.exists():
                return p
        except Exception:
            pass
    return cands[0] if cands else d / f"{raw}.dat"


def read_player_inventory(uuid):
    """读 world/playerdata/<uuid>.dat 的背包 + 末影箱。

    返回 (背包列表, 末影箱列表, 备注)；出错时列表为 None，备注说明原因。
    只读：只 load，不 save，不改任何文件。
    """
    nbt = nbtlib_module()
    if nbt is None:
        return None, None, "没装 nbtlib（要装才能解析玩家存档）"
    path = playerdata_path(uuid)
    if not path.exists():
        return None, None, ("找不到这个玩家的存档（他可能还没进过服务器；"
                            "在线玩家的数据要等他退出/自动保存后才落盘）")
    try:
        data = nbt.load(str(path))
    except Exception as e:
        return None, None, f"读不了这个存档: {type(e).__name__}: {e}"
    try:
        inv = _nbt_items(data.get("Inventory"))
    except Exception:
        inv = []
    try:
        ender = _nbt_items(data.get("EnderItems"))
    except Exception:
        ender = []
    return inv, ender, ""


# ==================== v3.5（⑱）Hangar 插件源（Paper 官方站） ====================
# 真实接口（2026-10-11 实测）：
#   搜插件  /api/v1/projects?limit=&offset=&platform=PAPER&q=名字
#           → {pagination:{count}, result:[{name, namespace:{owner,slug},
#              description, avatarUrl, stats:{downloads}}]}
#   查版本  /api/v1/projects/{owner}/{slug}/versions?limit=&platform=PAPER
#           → {result:[{name, channel:{name}, platformDependencies:{PAPER:[版本...]},
#              downloads:{PAPER:{fileInfo:{name,sizeBytes}, downloadUrl}}}]}
HANGAR_API = "https://hangar.papermc.io/api/v1"
HANGAR_PAGE = 15


def hangar_search(query, limit=HANGAR_PAGE, offset=0):
    """在 Hangar 搜插件，返回 (统一格式的列表, 总数)。"""
    params = {"limit": int(limit), "offset": int(offset), "platform": "PAPER"}
    if query:
        params["q"] = query
    url = f"{HANGAR_API}/projects?" + urllib.parse.urlencode(params)
    data = http_get_json(url) or {}
    out = []
    for r in (data.get("result") or []):
        ns = r.get("namespace") or {}
        owner, slug = ns.get("owner") or "", ns.get("slug") or ""
        stats = r.get("stats") or {}
        out.append({
            "title": r.get("name") or "?",
            "owner": owner,
            "slug": f"{owner}/{slug}",
            "description": (r.get("description") or "").strip(),
            "downloads": stats.get("downloads") or 0,
            "icon": r.get("avatarUrl"),
            "versions": [],
            "_source": "hangar",
        })
    total = (data.get("pagination") or {}).get("count") or 0
    return out, int(total)


def hangar_pick_version(owner, slug, game_version=None):
    """挑一个能装的版本：优先 Release，其次 Snapshot；尽量卡住游戏版本。

    挑不到返回 None。
    """
    url = (f"{HANGAR_API}/projects/{owner}/{slug}/versions"
           f"?limit=25&platform=PAPER")
    data = http_get_json(url) or {}
    versions = data.get("result") or []
    release = [v for v in versions
               if str((v.get("channel") or {}).get("name")) == "Release"]
    for pool in (release, versions):
        for v in pool:
            deps = (v.get("platformDependencies") or {}).get("PAPER") or []
            if game_version and deps and game_version not in deps:
                continue
            dl = (v.get("downloads") or {}).get("PAPER") or {}
            info = dl.get("fileInfo") or {}
            if info.get("name") and dl.get("downloadUrl"):
                return {"version": v.get("name"),
                        "channel": (v.get("channel") or {}).get("name"),
                        "filename": info["name"],
                        "size": info.get("sizeBytes"),
                        "url": dl["downloadUrl"]}
    return None


class LauncherApp(ctk.CTk, *_DND_MIXIN):
    def __init__(self):
        _s0 = load_launcher_settings()
        self._ui_scale = apply_ui_theme(_s0)      # v3.5（⑨）：配色 + 缩放
        super().__init__()
        self.title("Minecraft 一键开服启动器")
        # v3.4：右侧加了后台任务栏，窗口加宽；v3.5：按缩放倍数放大
        self.geometry(f"{int(1330 * self._ui_scale)}x"
                      f"{int(760 * self._ui_scale)}")
        self.minsize(int(1150 * self._ui_scale), int(680 * self._ui_scale))

        # v3.0：先确定“当前服务器”，再绑定所有路径
        activate_server(bootstrap_servers())
        self._update_title()

        self.server_process = None
        self.log_queue = queue.Queue()
        self.is_running = False
        self.server_phase = "stopped"      # stopped / starting / running
        self.online_players = set()
        self.online_since = {}        # v3.5（③）：名字 → 上线时间
        self.last_seen = {}           # v3.5（③）：名字 → 最后下线时间
        self._img_workers_started = False
        self._img_queue = None
        self._img_pending = []          # v3.4：等“滚到可见”再加载的封面
        self._img_gen = 0               # v3.4：翻页代号，用于丢弃过期任务
        self._img_quiet_until = time.time() + IMG_QUIET_SECONDS
        self._dnd_ready = False
        # v3.4：后台任务侧边栏
        self.tasks = {}
        self._task_seq = 0
        self._task_collapsed = False
        self._task_refresh_pending = False

        self.launcher_state = self._load_state()
        self.settings = load_launcher_settings()      # v3.3
        self.console_cmds = load_console_cmds()
        try:
            ctk.set_appearance_mode(self.settings.get("appearance", "dark"))
        except Exception:
            pass

        # ---- 翻页状态 ----
        self.current_page = 0
        self.total_hits = 0
        self.last_query = None
        self.last_project_type = None

        self._build_ui()
        # v3.5（0-9）：原来这里是 5 条独立轮询链（日志/进程/概览/状态栏/懒加载），
        # 现在合并成一条统一心跳 _tick。
        self._tick_start()
        self._auto_check_java()
        self._setup_dnd()          # v3.2：拖拽导入

        # v3.3：版本列表 / Modrinth 热门列表改成“打开对应页面才请求”，加快启动
        if not HAS_PIL:
            self.after(1000, lambda: self._append_console(
                "[启动器] ⚠ Pillow 未安装，封面将使用字母头像。\n"))
        self._fade_in()            # v3.5（⑰）：开窗口淡入
        # v3.5.8：点 ✕ 关启动器时的确认（服务器还在跑就先问一句，别把服关了）
        try:
            self.protocol("WM_DELETE_WINDOW", self._on_window_close)
        except Exception:
            pass
        # v3.5.12：上次启动器被关/被杀，服务端可能还在后台跑（幽灵进程）→ 提示 + 一键结束
        try:
            self._orphan_server_pid = self._detect_orphan_server()
            if self._orphan_server_pid:
                self.after(1500, self._warn_orphan_server)
        except Exception:
            self._orphan_server_pid = 0

    # ---------- v3.5.12：残留服务端（幽灵进程） ----------
    def _detect_orphan_server(self):
        """上次记下的 server_pid 还活着且是 java → 认为有残留服务端。"""
        try:
            pid = int(self.launcher_state.get("server_pid") or 0)
        except Exception:
            pid = 0
        if not pid:
            return 0
        if not (pid_alive(pid) and looks_like_java(pid)):
            return 0
        proc = getattr(self, "server_process", None)
        if proc is not None and getattr(proc, "pid", None) == pid:
            return 0                 # 就是当前在管的那个，不算残留
        return pid

    def _warn_orphan_server(self):
        pid = getattr(self, "_orphan_server_pid", 0)
        if not pid:
            return
        self._append_console(
            f"[启动器] ⚠ 检测到上次的服务端还在后台运行（PID {pid}）。\n"
            "[启动器] 启动器管不到它，端口也会被它占着。\n"
            "[启动器] 处理办法：点下面的「🧹 结束后台残留服务端」，"
            "或进游戏执行 /stop。\n\n")
        try:
            self.lbl_hint.configure(
                text=f"⚠ 后台还有残留服务端（PID {pid}）："
                     f"控制台页有「结束残留服务端」按钮",
                text_color="#f39c12")
        except Exception:
            pass

    def _kill_orphan_server(self, pid):
        """强杀残留服务端并清掉记录。"""
        self._append_console(
            f"[启动器] 正在结束后台残留服务端（PID {pid}）...\n")
        ok = False
        try:
            r = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                               capture_output=True, text=True, timeout=20,
                               **hidden_console_kwargs())
            ok = r.returncode == 0
        except Exception as e:
            self._append_console(f"[启动器] 结束失败: {e}\n")
        time.sleep(0.3)
        try:
            self.launcher_state.pop("server_pid", None)
            self._save_state()
        except Exception:
            pass
        self._orphan_server_pid = 0
        if ok:
            self._append_console(
                "[启动器] 已结束。可以点「一键启动」重新开服。\n"
                "[启动器] （强杀可能丢掉最近没保存的几分钟存档，下次尽量用"
                "「关闭服务器」或 /stop 停服）\n")
            try:
                self.lbl_hint.configure(text="", text_color="gray")
            except Exception:
                pass
        return ok

    def _gui_kill_orphan_server(self):
        pid = self._detect_orphan_server()
        if not pid:
            self._append_console("[启动器] 没检测到后台残留的服务端。\n")
            messagebox.showinfo("没有残留", "没检测到后台还在跑的服务端进程。")
            return
        if not messagebox.askyesno(
                "结束残留服务端",
                f"检测到后台还在跑的服务端（PID {pid}）。\n\n"
                f"强制结束它，可能丢掉最近几分钟还没保存的存档。\n"
                f"更稳妥的做法：进服务器执行 /stop，等它保存完。\n\n"
                f"确定要结束吗？"):
            return
        self._kill_orphan_server(pid)

    def _on_window_close(self):
        """点右上角 ✕ 关启动器（v3.5.8）。

        服务器是独立进程：直接关窗口的话，用户会以为"启动器关了服务器也就关了"，
        实际上 java 可能还在后台占着端口 → 下次启动就报端口被占用。
        所以服务器在跑时先问一句，一起关掉（推荐）；选「否」就什么都不做。
        """
        server_running = bool(getattr(self, "is_running", False)
                              and getattr(self, "server_process", None))
        if server_running:
            if not messagebox.askyesno(
                    "服务器还在运行",
                    "服务器正在后台运行。\n\n"
                    "关掉启动器会**连服务器一起关掉**（存档不会丢，但玩家会掉线）。\n\n"
                    "确定要关吗？\n"
                    "  · 「是」= 先停服，再关启动器\n"
                    "  · 「否」= 什么都不做，继续玩"):
                return
            try:
                self._user_stopping = True
                self._stop_server()
                for _ in range(40):
                    if not getattr(self, "server_process", None):
                        break
                    self.update()
                    time.sleep(0.1)
            except Exception:
                pass
        try:
            self.destroy()
        except Exception:
            pass

    # ---------- 状态持久化 ----------
    def _load_state(self):
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    def _save_state(self):
        try:
            STATE_FILE.write_text(
                json.dumps(self.launcher_state, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

    # ==================== UI 构建 ====================
    def _build_ui(self):
        # v3.2：底部常驻状态栏（CPU / 内存 / 当前服务器）
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.pack(side="bottom", fill="x")
        self.lbl_stats = ctk.CTkLabel(
            self.status_bar, text="CPU --   |   内存 --",
            font=ctk.CTkFont(size=12), anchor="w")
        self.lbl_stats.pack(side="left", padx=14, pady=4)
        self.lbl_server_state = ctk.CTkLabel(
            self.status_bar, text="○ 未运行",
            font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_server_state.pack(side="right", padx=14)

        # v3.5.2：状态栏以上整块区域。侧栏改成"覆盖式"后，它和标签页都挂在这块上：
        # 侧栏用 place 浮在上面，不再挤占标签页宽度（容器宽度是死的，内容区永不重排）。
        self.content_wrap = ctk.CTkFrame(self, fg_color="transparent",
                                         corner_radius=0)
        self.content_wrap.pack(fill="both", expand=True)

        self._build_task_panel()       # v3.4：右侧后台任务栏（可折叠）

        self.tabview = ctk.CTkTabview(self.content_wrap, width=1010, height=640)
        self.tabview.pack(padx=(14, 6), pady=(14, 8), fill="both", expand=True)
        self.task_panel.lift()         # v3.5.2：侧栏是浮层，压在最上面

        self.tab_servers = self.tabview.add("🖥 服务器")
        self.tab_overview = self.tabview.add("🏠 概览")
        self.tab_net = self.tabview.add("🌐 联机")
        self.tab_files = self.tabview.add("📁 文件")
        self.tab_download = self.tabview.add("📥 下载核心")
        self.tab_mods = self.tabview.add("🧩 插件 / 模组")
        self.tab_config = self.tabview.add("⚙ 配置")
        self.tab_settings = self.tabview.add("🔧 设置")
        self.tab_console = self.tabview.add("💻 控制台")
        self.tab_coltext = self.tabview.add("🎨 文字")

        # v3.3：懒加载——启动时只建“服务器 + 概览”，其余页面第一次点开才建。
        # 这是启动变快的主要原因（原来一次性建 8 个页面几百个控件）。
        self._pending_tabs = {
            "🌐 联机": self._build_net_tab,
            "📁 文件": self._build_files_tab,
            "📥 下载核心": self._build_download_tab,
            "🧩 插件 / 模组": self._build_mods_tab,
            "⚙ 配置": self._build_config_tab,
            "🔧 设置": self._build_settings_tab,
            "💻 控制台": self._build_console_tab,
            "🎨 文字": self._build_coltext_tab,
        }
        self._build_servers_tab()
        self._build_overview_tab()
        # 懒加载不再单开一条 120ms 的链，改由统一心跳驱动（见 _tick）

    def _lazy_tick(self):
        """切到某个标签页时才构建它（懒加载）。由 _tick 按 TICK_LAZY_MS 调用。"""
        try:
            name = self.tabview.get()
        except Exception:
            name = None
        builder = self._pending_tabs.pop(name, None)
        if builder is not None:
            try:
                builder()
            except Exception as e:
                print(f"[启动器] 构建「{name}」页失败: {type(e).__name__}: {e}")

    # ==================== 统一心跳（v3.5 0-9：降空闲 CPU） ====================
    def _tick_start(self):
        """把 5 条独立轮询链合并成一条心跳。"""
        self._tick_job = None
        self._tick_step = TICK_BUSY_MS
        self._tick_due = {}
        self._tick_focused = True       # 拿不准时按“在前台”算，别把界面拖懒
        self._tick_focus_at = 0.0
        self._last_label = {}           # 标签文字缓存：没变就不 configure
        for seq, val in (("<FocusIn>", True), ("<FocusOut>", False)):
            try:
                self.bind(seq, lambda e, v=val: self._on_focus(v), add="+")
            except Exception:
                pass
        # 用户一动手就把心跳叫醒（心跳正处于 2 秒慢档时尤其重要）
        for seq in ("<Button-1>", "<KeyPress>", "<MouseWheel>"):
            try:
                self.bind(seq, self._tick_wake, add="+")
            except Exception:
                pass
        # v3.5.15：拖窗口时系统会连发 <Configure>（只有位置变、尺寸没变），
        # 靠它判断"正在拖窗口"，这期间心跳别干重活
        try:
            self._last_win_size = (self.winfo_width(), self.winfo_height())
            self._ui_moving_until = 0.0
            self.bind("<Configure>", self._on_root_configure, add="+")
        except Exception:
            pass
        self._tick()

    def _on_root_configure(self, event=None):
        """窗口位置变了但尺寸没变 → 认为用户正在拖窗口（v3.5.15）。"""
        try:
            if event is not None and getattr(event, "widget", None) not in (
                    None, self):
                return
            size = (self.winfo_width(), self.winfo_height())
            if getattr(self, "_last_win_size", None) == size:
                self._ui_moving_until = time.time() + \
                    TICK_MOVE_SUSPEND_MS / 1000.0
            else:
                self._last_win_size = size
        except Exception:
            pass

    def _on_focus(self, focused):
        self._tick_focused = bool(focused)

    def _tick_wake(self, _event=None):
        """用户操作了：立刻回到快档，别让界面显得发木。"""
        self._tick_focus_at = 0.0
        if self._tick_job is not None and self._tick_step > TICK_IDLE_MS:
            try:
                self.after_cancel(self._tick_job)
            except Exception:
                pass
            self._tick_job = None
            self._tick()

    def _tick_busy(self):
        """有没有“要跟手”的活：服务端在跑/在启动，或日志队列还有没读完的行。"""
        if self.is_running or getattr(self, "server_phase", "stopped") == "starting":
            return True
        try:
            return not self.log_queue.empty()
        except Exception:
            return False

    def _tick_is_focused(self, now):
        """窗口在不在前台。

        实测（_bench_idle/probe_focus.py）：窗口被切到后台、或最小化时，
        focus_get() 会变成 None；切回来又有值。所以每秒用它复查一次兜底，
        <FocusIn>/<FocusOut> 只是让反应更快的快路径。
        """
        if now - self._tick_focus_at >= 1.0:
            self._tick_focus_at = now
            try:
                self._tick_focused = self.focus_get() is not None
            except Exception:
                self._tick_focused = True
        return self._tick_focused

    def _tick(self):
        self._tick_job = None
        now = time.monotonic()
        busy = self._tick_busy()

        if busy:
            step = TICK_BUSY_MS
        elif self._tick_is_focused(now):
            step = TICK_IDLE_MS
        else:
            step = TICK_AWAY_MS
        self._tick_step = step

        jobs = (
            # v3.5.15：进程检查放最前（很便宜），日志搬运放后面，
            # 万一日志把预算吃光，至少进程状态还是新的
            ("proc", TICK_PROC_MS, self._poll_process),
            ("log", TICK_BUSY_MS if busy else TICK_LOG_IDLE_MS,
             self._poll_log_queue),
            ("stats", TICK_STATS_MS, self._poll_stats),
            ("overview", TICK_OVERVIEW_MS, self._refresh_overview),
            ("lazy", TICK_LAZY_MS, self._lazy_tick),
            ("backup", TICK_BACKUP_MS, self._auto_backup_tick),
            ("restart", TICK_RESTART_MS, self._sched_restart_tick),
        )
        moving = time.time() < getattr(self, "_ui_moving_until", 0.0)
        t_budget = time.perf_counter()
        for name, interval, fn in jobs:
            if name == "lazy" and not self._pending_tabs:
                continue                       # 页面都建完了，这个活退休
            if moving and name not in ("proc", "log"):
                continue                       # 正在拖窗口：只保留最关键的两个
            if now < self._tick_due.get(name, 0.0):
                continue
            self._tick_due[name] = now + interval / 1000.0
            try:
                fn()
            except Exception as e:
                # 单个活出错不能把整条心跳带走（老的 5 条链就有这毛病：
                # 一个异常没接住，那个循环就永远不再调度了）
                print(f"[启动器] 心跳任务 {name} 出错: {type(e).__name__}: {e}")
            # v3.5.15：这次心跳已经占了够多 UI 线程时间 → 剩下的留给下一次，
            # 别让拖窗口/点击被一次心跳卡住几十毫秒
            if (time.perf_counter() - t_budget) * 1000.0 >= TICK_BUDGET_MS:
                break
        self._tick_job = self.after(step, self._tick)

    def _set_label(self, widget, text, color=None):
        """只在文字真的变了才 configure。Tk 每 configure 一次都要重排重绘，
        空闲时反复写同样的字纯属白烧 CPU。"""
        try:
            key = id(widget)
            if self._last_label.get(key) == (text, color):
                return
            self._last_label[key] = (text, color)
            if color is None:
                widget.configure(text=text)
            else:
                widget.configure(text=text, text_color=color)
        except Exception:
            pass

    # ---------- 概览页 ----------
    def _build_overview_tab(self):
        frame = self.tab_overview

        # v3.4：最上方显示“推荐 Java 版本”（用户要求放最显眼的地方）
        self.lbl_java_banner = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#f39c12")
        self.lbl_java_banner.pack(pady=(8, 0))

        ctk.CTkLabel(frame, text="Minecraft 服务器",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(12, 15))

        card = ctk.CTkFrame(frame, corner_radius=18)
        card.pack(padx=60, pady=10, fill="x")

        self.lbl_status = ctk.CTkLabel(
            card, text="● 未运行",
            font=ctk.CTkFont(size=22, weight="bold"), text_color="gray"
        )
        self.lbl_status.pack(pady=(20, 12))

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(pady=(0, 20))

        self.lbl_core = ctk.CTkLabel(info, text="核心: 未安装",
                                     font=ctk.CTkFont(size=15))
        self.lbl_core.grid(row=0, column=0, padx=25, pady=6, sticky="w")

        self.lbl_version = ctk.CTkLabel(info, text="版本: -",
                                        font=ctk.CTkFont(size=15))
        self.lbl_version.grid(row=0, column=1, padx=25, pady=6, sticky="w")

        self.lbl_port = ctk.CTkLabel(info, text="端口: 25565",
                                     font=ctk.CTkFont(size=15))
        self.lbl_port.grid(row=1, column=0, padx=25, pady=6, sticky="w")

        self.lbl_players = ctk.CTkLabel(info, text="在线玩家: 0",
                                        font=ctk.CTkFont(size=15))
        self.lbl_players.grid(row=1, column=1, padx=25, pady=6, sticky="w")
        # v3.5（③）：点进去看名单（在线/来过、踢人、给 OP、看背包）
        ctk.CTkButton(info, text="👥 玩家列表", width=110, height=28,
                      fg_color="#2c3e50", hover_color="#34495e",
                      command=self._open_players_window).grid(
            row=1, column=2, padx=10, pady=6, sticky="w")

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(pady=30)

        self.btn_start = ctk.CTkButton(
            btns, text="▶  一键启动",
            width=230, height=65,
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#2ecc71", hover_color="#27ae60",
            command=self._start_server
        )
        self.btn_start.pack(side="left", padx=12)

        self.btn_stop = ctk.CTkButton(
            btns, text="■  停止",
            width=170, height=65,
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#e74c3c", hover_color="#c0392b",
            state="disabled",
            command=self._stop_server
        )
        self.btn_stop.pack(side="left", padx=12)

        # v3.2：内存改成滑块（原来是手打数字的输入框），并给出物理内存提示
        total_gb = 8
        ram = ram_info()
        if ram:
            total_gb = max(2, int(round(ram[1] / 1024 ** 3)))
        self.mem_max_limit = total_gb

        mem = ctk.CTkFrame(frame, fg_color="transparent")
        mem.pack(pady=(6, 2), fill="x", padx=140)

        row1 = ctk.CTkFrame(mem, fg_color="transparent")
        row1.pack(fill="x", pady=3)
        ctk.CTkLabel(row1, text="最小内存", width=80, anchor="w",
                     font=ctk.CTkFont(size=14)).pack(side="left")
        self.min_mem = ctk.CTkSlider(
            row1, from_=1, to=self.mem_max_limit,
            number_of_steps=max(1, self.mem_max_limit - 1),
            command=self._on_min_mem)
        self.min_mem.set(2)
        self.min_mem.pack(side="left", fill="x", expand=True, padx=10)
        self.lbl_min_mem = ctk.CTkLabel(row1, text="2 GB", width=60,
                                        font=ctk.CTkFont(size=14))
        self.lbl_min_mem.pack(side="left")

        row2 = ctk.CTkFrame(mem, fg_color="transparent")
        row2.pack(fill="x", pady=3)
        ctk.CTkLabel(row2, text="最大内存", width=80, anchor="w",
                     font=ctk.CTkFont(size=14)).pack(side="left")
        self.max_mem = ctk.CTkSlider(
            row2, from_=1, to=self.mem_max_limit,
            number_of_steps=max(1, self.mem_max_limit - 1),
            command=self._on_max_mem)
        suggest = max(2, min(4, total_gb // 2))
        self.max_mem.set(suggest)
        self.max_mem.pack(side="left", fill="x", expand=True, padx=10)
        self.lbl_max_mem = ctk.CTkLabel(row2, text=f"{suggest} GB", width=60,
                                        font=ctk.CTkFont(size=14))
        self.lbl_max_mem.pack(side="left")

        # v3.3：优先用该服务器上次保存的内存值（设置页 / 概览页是同一份数值）
        try:
            srv_min = int(self.launcher_state.get(
                "min_mem", self.settings.get("default_min_mem", 2)))
            srv_max = int(self.launcher_state.get(
                "max_mem", self.settings.get("default_max_mem", suggest)))
            self.min_mem.set(max(1, min(srv_min, self.mem_max_limit)))
            self.max_mem.set(max(1, min(srv_max, self.mem_max_limit)))
            self.lbl_min_mem.configure(text=f"{int(self.min_mem.get())} GB")
            self.lbl_max_mem.configure(text=f"{int(self.max_mem.get())} GB")
        except Exception:
            pass

        if ram:
            used_pct = ram[2]
            warn = used_pct > 80
            self.lbl_mem_hint = ctk.CTkLabel(
                frame,
                text=(f"{'⚠ ' if warn else ''}物理内存 {total_gb} GB，"
                      f"当前已用 {used_pct:.0f}%"
                      + (f"，建议最大内存不超过 {max(2, total_gb // 2 - 1)} GB"
                         if warn else "")),
                font=ctk.CTkFont(size=12),
                text_color=("#f39c12" if warn else "#888888"))
            self.lbl_mem_hint.pack(pady=(2, 0))

        java_row = ctk.CTkFrame(frame, fg_color="transparent")
        java_row.pack(pady=(12, 2))
        self.lbl_java = ctk.CTkLabel(java_row, text="Java: 检测中...",
                                     font=ctk.CTkFont(size=13),
                                     text_color="orange")
        self.lbl_java.pack(side="left", padx=6)
        ctk.CTkButton(java_row, text="重新检测", width=90, height=26,
                      font=ctk.CTkFont(size=12),
                      fg_color="#4a4a4a", hover_color="#5a5a5a",
                      command=self._auto_check_java).pack(side="left", padx=6)

        self.lbl_hint = ctk.CTkLabel(frame, text="",
                                     font=ctk.CTkFont(size=14),
                                     text_color="#f39c12")
        self.lbl_hint.pack(pady=8)

    # ---------- 内存滑块联动（v3.2） ----------
    def _on_min_mem(self, value):
        v = int(round(float(value)))
        self.lbl_min_mem.configure(text=f"{v} GB")
        if v > int(round(float(self.max_mem.get()))):
            self.max_mem.set(v)
            self.lbl_max_mem.configure(text=f"{v} GB")

    def _on_max_mem(self, value):
        v = int(round(float(value)))
        self.lbl_max_mem.configure(text=f"{v} GB")
        if v < int(round(float(self.min_mem.get()))):
            self.min_mem.set(v)
            self.lbl_min_mem.configure(text=f"{v} GB")

    # ---------- 下载核心：目标服务器（v3.5.17） ----------
    @staticmethod
    def _read_server_state(sdir):
        try:
            p = Path(sdir) / "launcher_state.json"
            data = json.loads(p.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    @staticmethod
    def _write_server_state(sdir, core, version):
        try:
            sdir = Path(sdir)
            sdir.mkdir(parents=True, exist_ok=True)
            p = sdir / "launcher_state.json"
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    data = {}
            except Exception:
                data = {}
            data["core"] = core
            data["version"] = version
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")
            return True
        except Exception as e:
            print(f"[启动器] 保存服务器状态失败: {e}")
            return False

    def _core_target_values(self):
        return [CORE_TARGET_NEW] + list_servers()

    def _select_core_target(self, name):
        """让「下载核心」页默认选到某个服务器（新建服务器后紧接着用）。"""
        self._want_core_target = name
        if not hasattr(self, "core_target"):
            return                  # 页面还没建，建的时候再用 _want_core_target
        if name in self._core_target_values():
            self.core_target.set(name)
            self._on_core_target_change()

    def _refresh_core_targets(self):
        """服务器列表变了（新建/删除/改名/导入）就刷新下拉框。"""
        if not hasattr(self, "core_target"):
            return
        vals = self._core_target_values()
        cur = self.core_target.get()
        try:
            self.core_target.configure(values=vals)
        except Exception:
            return
        self.core_target.set(cur if cur in vals else CORE_TARGET_NEW)
        self._on_core_target_change()

    def _on_core_target_change(self):
        """切换目标服务器时，把“会发生什么”直接写在旁边，别让人靠猜。"""
        if not hasattr(self, "lbl_core_target_hint"):
            return
        sel = self.core_target.get()
        if sel == CORE_TARGET_NEW:
            hint = "→ 新建一个服务器（名字自动取），不会动任何现有核心"
            text = "⬇ 下载并新建"
        else:
            state = self._read_server_state(server_path(sel))
            core = state.get("core") or ""
            ver = state.get("version") or ""
            now = "（当前服务器）" if sel == CURRENT_SERVER else ""
            if core and ver:
                hint = f"⚠ 会覆盖它的 {core} {ver} 核心{now}"
            else:
                hint = f"它还没有核心，会直接装上{now}"
            text = "⬇ 换上这个核心"
        self.lbl_core_target_hint.configure(text=hint)
        btn = getattr(self, "btn_download", None)
        if btn is not None:
            try:
                btn.configure(text=text)
            except Exception:
                pass

    # ---------- 下载核心页 ----------
    def _build_download_tab(self):
        frame = self.tab_download

        ctk.CTkLabel(frame, text="下载服务端核心",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(18, 5))

        ctk.CTkLabel(
            frame,
            text="默认【新建一个服务器】并装上核心；"
                 "要给已有服务器换核心，就在下面把目标服务器选成它",
            font=ctk.CTkFont(size=13), text_color="gray"
        ).pack(pady=(0, 12))

        # v3.5.17：目标服务器。默认"新建"，绝不悄悄覆盖当前核心。
        trow = ctk.CTkFrame(frame, fg_color="transparent")
        trow.pack(pady=(0, 6))

        ctk.CTkLabel(trow, text="目标服务器:",
                     font=ctk.CTkFont(size=15)).pack(side="left", padx=5)
        self.core_target = ctk.CTkOptionMenu(
            trow, values=self._core_target_values(), width=250, height=38,
            font=ctk.CTkFont(size=14),
            command=lambda v: self._on_core_target_change()
        )
        self.core_target.set(CORE_TARGET_NEW)
        want = getattr(self, "_want_core_target", None)
        if want and want in list_servers():
            self.core_target.set(want)      # 刚新建的服务器，别又建一个
        self.core_target.pack(side="left", padx=5)
        self.lbl_core_target_hint = ctk.CTkLabel(
            trow, text="", font=ctk.CTkFont(size=12), text_color="gray",
            anchor="w")
        self.lbl_core_target_hint.pack(side="left", padx=14)

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(pady=12)

        ctk.CTkLabel(row, text="核心类型:",
                     font=ctk.CTkFont(size=15)).pack(side="left", padx=5)
        self.core_type = ctk.CTkOptionMenu(
            row, values=list(CORE_DISPLAY.keys()),
            width=180, height=38, font=ctk.CTkFont(size=14),
            command=lambda v: self._refresh_version_list()
        )
        self.core_type.set("Paper (推荐)")
        self.core_type.pack(side="left", padx=5)

        ctk.CTkLabel(row, text="游戏版本:",
                     font=ctk.CTkFont(size=15)).pack(side="left", padx=(25, 5))
        self.core_version = ctk.CTkOptionMenu(
            row, values=["加载中..."], width=160, height=38,
            font=ctk.CTkFont(size=14)
        )
        self.core_version.pack(side="left", padx=5)

        self.btn_download = ctk.CTkButton(
            row, text="⬇ 下载",
            width=120, height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#3498db", hover_color="#2980b9",
            command=self._download_core
        )
        self.btn_download.pack(side="left", padx=25)
        ctk.CTkButton(row, text="🔄 检查核心更新", width=160, height=42,
                      fg_color="#f39c12", hover_color="#d68910",
                      command=self._check_core_update).pack(side="left", padx=4)
        self._on_core_target_change()      # 按钮文字跟着目标服务器变

        self.lbl_download_status = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=14)
        )
        self.lbl_download_status.pack(pady=15)

        self.download_progress = ctk.CTkProgressBar(frame, width=650, height=14)
        self.download_progress.pack(pady=10)
        self.download_progress.set(0)

        info = ctk.CTkTextbox(frame, width=880, height=250, wrap="word",
                              font=ctk.CTkFont(size=13))
        info.pack(pady=20, padx=40)
        info.insert("1.0", self._core_info_text())
        info.configure(state="disabled")
        # v3.3：第一次打开这个页面时才去取版本列表（加快启动）
        self.after(200, self._refresh_version_list)

    def _core_info_text(self):
        return (
            "【核心类型说明】\n\n"
            "● Vanilla (官方)\n"
            "    Mojang 官方原版服务端，纯净无修改，性能一般，不支持插件。\n\n"
            "● Paper (推荐)\n"
            "    基于 Spigot 深度优化，性能好，兼容 Bukkit/Spigot/Paper 插件。\n\n"
            "● Purpur\n"
            "    基于 Paper，额外加入大量可配置的游戏特性，兼容 Paper 插件。\n\n"
            "● Fabric\n"
            "    轻量级 Mod 加载器，适合玩模组服，把模组放入 mods/ 文件夹。\n"
            "    注意：Fabric 核心不兼容 Bukkit 系插件。\n\n"
            "【下载完成后】\n"
            "    目标服务器 =「➕ 新建服务器」时（默认），会新建一个服务器并装上核心，\n"
            "    下载完会自动切换过去；回到「🏠 概览」点「一键启动」即可开服。\n\n"
            "【给已有服务器换核心】\n"
            "    在上面「目标服务器」里选中那个服务器，再点下载。\n"
            "    只会覆盖它的 server.jar（旧核心存成 server.jar.bak），\n"
            "    存档 / 插件 / 配置都不受影响。\n"
        )

    # ---------- 插件/模组页 ----------
    def _build_mods_tab(self):
        frame = self.tab_mods

        ctk.CTkLabel(frame, text="插件 / 模组 / 数据包下载",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 5))

        tip = ("数据来源：Modrinth｜留空搜索 = 热门推荐｜点击任意项目 = 查看历史版本"
               "｜数据包装到 world/datapacks/")
        ctk.CTkLabel(frame, text=tip,
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 12))

        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=8)

        self.modrinth_type = ctk.CTkSegmentedButton(
            top, values=["插件 (Plugins)", "模组 (Mods)", "数据包 (Datapacks)"],
            font=ctk.CTkFont(size=14),
            command=lambda v: self._search_modrinth(page=0)
        )
        self.modrinth_type.set("插件 (Plugins)")
        self.modrinth_type.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(
            top,
            placeholder_text="搜索名称，例如 EssentialsX、Sodium、Better Nether",
            width=420, height=38, font=ctk.CTkFont(size=14)
        )
        self.search_entry.pack(side="left", padx=15)
        self.search_entry.bind("<Return>",
                               lambda e: self._search_modrinth(page=0))

        ctk.CTkButton(
            top, text="🔍 搜索", width=110, height=38,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._search_modrinth(page=0)
        ).pack(side="left", padx=5)

        # v3.3：筛选栏
        filt = ctk.CTkFrame(frame, fg_color="transparent")
        filt.pack(fill="x", padx=30, pady=(0, 2))
        ctk.CTkLabel(filt, text="游戏版本",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 4))
        self.filter_version = ctk.CTkEntry(filt, width=100, height=30,
                                           placeholder_text="如 1.21.8")
        self.filter_version.pack(side="left", padx=2)
        ctk.CTkLabel(filt, text="加载器",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(10, 4))
        self.filter_loader = ctk.CTkOptionMenu(
            filt, width=110, height=30,
            values=["自动", "paper", "purpur", "spigot", "bukkit", "folia",
                    "fabric", "forge", "neoforge"],
            command=lambda v: self._search_modrinth(page=0))
        self.filter_loader.set("自动")
        self.filter_loader.pack(side="left", padx=2)
        # v3.5（⑱）：插件来源（Modrinth 收录最全 / Hangar 是 Paper 官方站）
        ctk.CTkLabel(filt, text="来源",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(10, 4))
        self.source_menu = ctk.CTkOptionMenu(
            filt, width=160, height=30,
            values=["Modrinth", "Hangar（Paper 官方）"],
            command=lambda v: self._search_modrinth(page=0))
        self.source_menu.set("Modrinth")
        self.source_menu.pack(side="left", padx=2)
        ctk.CTkLabel(filt, text="排序",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(10, 4))
        self.filter_sort = ctk.CTkOptionMenu(
            filt, width=120, height=30,
            values=["下载量", "最近更新", "最新发布", "相关度"],
            command=lambda v: self._search_modrinth(page=0))
        self.filter_sort.set("下载量")
        self.filter_sort.pack(side="left", padx=2)
        self.filter_adapt = ctk.CTkSwitch(
            filt, text="只看适配当前核心", font=ctk.CTkFont(size=13),
            command=lambda: self._search_modrinth(page=0))
        self.filter_adapt.select()
        self.filter_adapt.pack(side="left", padx=12)

        self.search_status = ctk.CTkLabel(
            frame, text="正在加载热门列表...",
            font=ctk.CTkFont(size=13), text_color="gray"
        )
        self.search_status.pack(pady=6)

        # ---- 翻页栏 ----
        # v3.5.6：翻页栏要先占位（side="bottom"），列表再吃剩下的空间。
        # 以前是"列表先 expand、翻页栏后 pack"，窗口一矮翻页栏就被挤成一条缝，
        # 按钮只露一小截（用户截图里那条半截灰条就是这个）。
        page_row = ctk.CTkFrame(frame, fg_color="transparent")
        page_row.pack(side="bottom", fill="x", padx=30, pady=(2, 10))

        self.btn_prev = ctk.CTkButton(
            page_row, text="◀ 上一页", width=100, height=32,
            font=ctk.CTkFont(size=13),
            fg_color="#4a4a4a", hover_color="#5a5a5a",
            state="disabled",
            command=lambda: self._search_modrinth(
                page=self.current_page - 1)
        )
        self.btn_prev.pack(side="left", padx=5)

        self.lbl_page = ctk.CTkLabel(
            page_row, text="第 1 / 1 页",
            font=ctk.CTkFont(size=13), text_color="#cccccc"
        )
        self.lbl_page.pack(side="left", padx=15)

        self.btn_next = ctk.CTkButton(
            page_row, text="下一页 ▶", width=100, height=32,
            font=ctk.CTkFont(size=13),
            fg_color="#4a4a4a", hover_color="#5a5a5a",
            state="disabled",
            command=lambda: self._search_modrinth(
                page=self.current_page + 1)
        )
        self.btn_next.pack(side="left", padx=5)

        self.lbl_total = ctk.CTkLabel(
            page_row, text="",
            font=ctk.CTkFont(size=12), text_color="#888888"
        )
        self.lbl_total.pack(side="right", padx=10)

        # 列表最后放：翻页栏已经占好位了，列表只吃剩下的高度
        self.results_frame = ctk.CTkScrollableFrame(frame, width=920, height=390)
        self.results_frame.pack(padx=30, pady=(8, 4), fill="both", expand=True)
        self._fast_scroll(self.results_frame)

        # v3.3：这个页面第一次打开时才请求 Modrinth（加快启动）
        self.after(200, lambda: self._search_modrinth(page=0))

    # ---------- 配置页 ----------
    def _build_config_tab(self):
        frame = self.tab_config

        ctk.CTkLabel(frame, text="server.properties 完整配置",
                     font=ctk.CTkFont(size=20,
                                       weight="bold")).pack(pady=(14, 4))
        self.lbl_cfg_hint = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_cfg_hint.pack(pady=(0, 4))

        self.cfg_scroll = ctk.CTkScrollableFrame(frame, width=880, height=430)
        self.cfg_scroll.pack(padx=20, pady=5, fill="both", expand=True)
        self._fast_scroll(self.cfg_scroll)

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=10)
        ctk.CTkButton(btn_row, text="从文件读取", width=150,
                      command=self._load_properties).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="💾 保存配置", width=180,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._save_properties).pack(side="left", padx=8)

        self.prop_widgets = {}
        self._rebuild_config_fields()
        self._load_properties(silent=True)   # v3.3：打开配置页时自动读当前值

    def _rebuild_config_fields(self):
        """按当前服务端版本重建属性控件（v3.3：随游戏版本变动）。"""
        if not hasattr(self, "cfg_scroll"):
            return
        for w in self.cfg_scroll.winfo_children():
            w.destroy()
        self.prop_widgets = {}
        version = self.launcher_state.get("version") or ""
        try:
            extra = list(get_properties().keys())
        except Exception:
            extra = []
        rows = catalog_for_version(version, extra)
        last_cat = None
        for key, label, wtype, default, options, cat in rows:
            if cat != last_cat:
                last_cat = cat
                ctk.CTkLabel(self.cfg_scroll, text=f"— {cat} —",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color="#7fb3ff",
                             anchor="w").pack(fill="x", padx=6,
                                              pady=(10, 2))
            row = ctk.CTkFrame(self.cfg_scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=label, width=230, anchor="w",
                         font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
            if wtype in ("bool", "option"):
                opts = ["true", "false"] if wtype == "bool" else options
                w = ctk.CTkOptionMenu(row, values=opts, width=300)
                w.set(default)
            else:
                w = ctk.CTkEntry(row, width=300)
                w.insert(0, default)
            w.pack(side="left", padx=5)
            self.prop_widgets[key] = w
        if hasattr(self, "lbl_cfg_hint"):
            self.lbl_cfg_hint.configure(
                text=(f"服务端版本 {version}：共 {len(self.prop_widgets)} 项"
                      f"（新版本才有的选项会自动出现，旧的不显示）"
                      if version else
                      f"未检测到服务端版本，先显示全部 {len(self.prop_widgets)} 项"))

    # ---------- 控制台页 ----------
    def _build_console_tab(self):
        frame = self.tab_console

        ctk.CTkLabel(frame, text="服务器控制台",
                     font=ctk.CTkFont(size=20,
                                       weight="bold")).pack(pady=(15, 5))

        # v3.5.6：底部的固定行先占位（side="bottom"，从下往上放），
        # 文本框最后放、吃掉剩下的高度。以前文本框先 expand、下面几行后 pack，
        # 窗口一矮输入行就被挤成一条缝（截图里"输入服务器指令…"那行只露一半）。

        # ---- 最下面：指令输入行 ----
        cmd_row = ctk.CTkFrame(frame, fg_color="transparent")
        cmd_row.pack(side="bottom", fill="x", padx=25, pady=8)

        self.cmd_entry = ctk.CTkEntry(
            cmd_row,
            placeholder_text="输入服务器指令，如 say Hello 或 op Steve",
            height=38, font=ctk.CTkFont(size=14)
        )
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.cmd_entry.bind("<Return>", lambda e: self._send_command())
        # v3.4：边打字边给中文说明（CTkEntry 的 bind 要落到内部 entry 上才生效）
        _hint = lambda e=None: self._show_cmd_hint(self.cmd_entry.get())
        try:
            self.cmd_entry._entry.bind("<KeyRelease>", _hint)
        except Exception:
            try:
                self.cmd_entry.bind("<KeyRelease>", _hint)
            except Exception:
                pass

        ctk.CTkButton(cmd_row, text="发送", width=100, height=38,
                      command=self._send_command).pack(side="right")

        # ---- 诊断结果提示 ----
        self.lbl_diag = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=12), text_color="#f39c12",
            anchor="w", justify="left", wraplength=880)
        self.lbl_diag.pack(side="bottom", fill="x", padx=27, pady=(2, 0))

        # ---- v3.4 ⑮：崩溃诊断按钮 ----
        diag_row = ctk.CTkFrame(frame, fg_color="transparent")
        diag_row.pack(side="bottom", fill="x", padx=25, pady=(6, 0))
        ctk.CTkButton(diag_row, text="🔍 分析日志找原因", width=160, height=30,
                      fg_color="#8e44ad", hover_color="#9b59b6",
                      command=self._analyze_log_ui).pack(side="left", padx=(0, 8))
        ctk.CTkButton(diag_row, text="🌐 上传 mclo.gs 深度分析", width=200,
                      height=30, fg_color="#2980b9", hover_color="#3498db",
                      command=self._upload_log_ui).pack(side="left")
        # v3.5.12：上次启动器被强关后留下的服务端（幽灵进程）→ 一键结束
        ctk.CTkButton(diag_row, text="🧹 结束后台残留服务端", width=190,
                      height=30, fg_color="#7a5a3a", hover_color="#9a6a3a",
                      command=self._gui_kill_orphan_server).pack(
            side="left", padx=(10, 0))
        # v3.5（⑭）：日志中文翻译开关（离线）
        self.sw_translate = ctk.CTkSwitch(diag_row, text="日志中文翻译",
                                          command=self._toggle_translate)
        self.sw_translate.pack(side="left", padx=(14, 0))
        self._translate_logs = bool(self.settings.get("translate_log", True))
        if self._translate_logs:
            self.sw_translate.select()

        # ---- v3.4：指令说明行（选中或打字时实时更新） ----
        self.lbl_cmd_hint = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=12), text_color="#7fb3ff",
            anchor="w", justify="left")
        self.lbl_cmd_hint.pack(side="bottom", fill="x", padx=27, pady=(2, 0))

        # ---- v3.3：常用指令下拉栏（可自行添加，存 console_cmds.json） ----
        quick_row = ctk.CTkFrame(frame, fg_color="transparent")
        quick_row.pack(side="bottom", fill="x", padx=25, pady=(4, 0))
        ctk.CTkLabel(quick_row, text="常用指令",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 8))
        self.cmd_combo = ctk.CTkComboBox(
            quick_row, values=self._cmd_labels(), width=380, height=32,
            font=ctk.CTkFont(size=13), command=self._pick_quick_cmd)
        self.cmd_combo.set("")
        self.cmd_combo.pack(side="left", padx=4)
        ctk.CTkButton(quick_row, text="➕ 收藏当前指令", width=140, height=32,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._add_quick_cmd).pack(side="left", padx=4)
        ctk.CTkButton(quick_row, text="➖ 删除选中", width=110, height=32,
                      fg_color="#4a4a4a", hover_color="#5a5a5a",
                      command=self._del_quick_cmd).pack(side="left", padx=4)

        # 文本框最后放：底部那些行已经占好位了，它只吃剩下的高度
        self.console_box = ctk.CTkTextbox(
            frame, width=920, height=430,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.console_box.pack(padx=25, pady=8, fill="both", expand=True)
        self._append_console("")     # v3.3：把懒加载期间缓存的日志补上

    # ==================== 指定文件夹 / 导入服务器（v3.2） ====================
    def _pick_external_folder(self):
        d = filedialog.askdirectory(
            title="选择一个已有的服务器文件夹（原地使用，不复制、不改动）")
        if d:
            self._import_folder(Path(d), copy_in=False)

    def _import_folder_copy(self):
        d = filedialog.askdirectory(
            title="选择要导入的服务器文件夹（会复制一份到 servers/）")
        if d:
            self._import_folder(Path(d), copy_in=True)

    def _import_folder(self, folder, copy_in):
        folder = Path(folder)
        if not folder.is_dir():
            messagebox.showerror("打不开", f"不是有效文件夹:\n{folder}")
            return
        report = detect_server_folder(folder)
        how = ("导入方式: 复制一份到 servers/（原文件夹保留不动）" if copy_in
               else "导入方式: 原地登记为服务器（不会改动你的任何文件）")
        if not messagebox.askyesno(
                "服务器识别结果",
                f"{format_server_report(report)}\n\n{how}\n\n继续吗？"):
            return

        name = unique_server_name(folder.name)
        tid = self.task_start(f"导入服务器 {name}")   # v3.5（0-10）：进侧边栏
        try:
            if copy_in:
                dst = SERVERS_ROOT / name
                self._set_files_status(f"⏳ 正在复制到 {dst} ...", "#f39c12")
                self.update_idletasks()
                shutil.copytree(folder, dst, dirs_exist_ok=True)
            else:
                dst = folder
            self.task_done(tid, str(Path(dst).name))
        except Exception as e:
            self.task_fail(tid, type(e).__name__)
            messagebox.showerror("导入失败", f"{type(e).__name__}: {e}")
            return

        register_server(name, dst)
        # 把识别到的核心/版本写进该服务器状态，概览页就能直接显示
        try:
            sf = Path(dst) / "launcher_state.json"
            data = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {}
            core = str(report.get("core") or "")
            if core and "/" not in core:
                data["core"] = core
            if report.get("version"):
                data["version"] = report["version"]
            if data:
                sf.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        except Exception:
            pass

        self._refresh_servers_tab()
        self._append_console(f"[启动器] 已登记服务器「{name}」→ {dst}\n")
        if messagebox.askyesno("导入完成",
                               f"「{name}」已加入列表。\n现在切换过去吗？"):
            self._switch_server(name)

    # ==================== 拖拽 / 选择文件导入（v3.2） ====================
    def _setup_dnd(self):
        if not HAS_DND:
            self._append_console(
                "[启动器] ⚠ 未安装 tkinterdnd2，拖拽不可用（可用「📥 选择文件导入」）。\n"
                "[启动器] 想启用拖拽: pip install tkinterdnd2\n")
            if hasattr(self, "lbl_drop_hint"):
                self.lbl_drop_hint.configure(
                    text="⚠ 拖拽需要 tkinterdnd2（pip install tkinterdnd2），"
                         "现在请用「📥 选择文件导入」",
                    text_color="#f39c12")
            return
        try:
            self.TkdndVersion = TkinterDnD._require(self)
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
            self._dnd_ready = True
            self._append_console(
                "[启动器] 拖拽导入已启用：把 jar / zip / 服务器文件夹拖进窗口即可。\n")
        except Exception as e:
            self._append_console(f"[启动器] ⚠ 拖拽初始化失败: {e}\n")

    def _on_drop(self, event):
        try:
            items = self.tk.splitlist(event.data)
        except Exception:
            items = [str(event.data).strip("{}")]
        self._handle_import_paths([Path(i) for i in items])

    def _pick_files_import(self):
        files = filedialog.askopenfilenames(
            title="选择要导入的文件（jar / zip / properties / txt）",
            filetypes=[("可导入文件", "*.jar *.zip *.properties *.txt"),
                       ("所有文件", "*.*")])
        if files:
            self._handle_import_paths([Path(f) for f in files])

    def _handle_import_paths(self, paths):
        for p in paths:
            if p.is_dir():
                if messagebox.askyesno(
                        "这是一个文件夹",
                        f"{p}\n\n要把它作为服务器导入吗？\n（原地登记，不改动文件）"):
                    self._import_folder(p, copy_in=False)
                continue
            self._import_file(p)

    def _import_file(self, p):
        info = classify_file(p)
        kind = info["kind"]

        if kind == "core":
            if messagebox.askyesno(
                    "识别为服务端核心",
                    f"{p.name}\n\n检测: {info['detail']}\n"
                    f"核心: {info.get('core')}   "
                    f"版本: {info.get('version') or '未知'}\n\n"
                    f"设为当前服务器「{CURRENT_SERVER}」的核心吗？\n"
                    f"（复制成 server.jar，原有核心会备份为 .bak）"):
                self._install_core_file(p, info)

        elif kind in ("plugin", "mod"):
            kind_cn = "插件" if kind == "plugin" else "模组"
            target_dir = PLUGINS_DIR if kind == "plugin" else MODS_DIR
            if kind == "mod" and self.launcher_state.get("core") in ("paper",
                                                                     "purpur"):
                if not messagebox.askyesno(
                        "核心可能不匹配",
                        "当前是 Paper/Purpur 服务端，不加载 mods/ 里的模组。\n"
                        "继续吗？"):
                    return
            if messagebox.askyesno(
                    f"识别为{kind_cn}",
                    f"{p.name}\n\n检测: {info['detail']}\n\n"
                    f"复制到 {target_dir.name}/ 吗？"):
                self._copy_into(p, target_dir)

        elif kind == "zip":
            ans = messagebox.askyesnocancel(
                "识别为压缩包",
                f"{p.name}\n\n"
                f"是   = 解压到服务器目录（里面若是 world/ 就相当于还原存档）\n"
                f"否   = 当作存档备份放进 backups/\n"
                f"取消 = 跳过")
            if ans is None:
                return
            if ans:
                self._extract_zip(p, SERVER_DIR)
            else:
                self._copy_into(p, SERVER_DIR / "backups")

        elif kind == "properties":
            if messagebox.askyesno(
                    "识别为 server.properties",
                    f"{p.name}\n\n覆盖当前服务器的 server.properties 吗？\n"
                    f"（原文件会先备份成 server.properties.bak）"):
                try:
                    if PROPERTIES_FILE.exists():
                        shutil.copy2(
                            PROPERTIES_FILE,
                            PROPERTIES_FILE.with_suffix(".properties.bak"))
                    shutil.copy2(p, PROPERTIES_FILE)
                    self._load_properties(silent=True)
                    self._refresh_files_tab()
                    self._set_files_status(f"✅ 已导入并生效: {p.name}")
                except Exception as e:
                    messagebox.showerror("导入失败", f"{type(e).__name__}: {e}")

        elif kind == "text":
            if "eula" in p.name.lower():
                if messagebox.askyesno("识别为 eula.txt",
                                       "复制成服务器的 eula.txt 吗？"):
                    self._copy_into(p, SERVER_DIR, dest_name="eula.txt")
            else:
                messagebox.showinfo(
                    "没认出这是啥",
                    f"{p.name} 既不是 eula.txt 也不是配置文件。\n"
                    f"想手动放的话点「📂 打开服务器文件夹」。")

        elif kind == "unknown_jar":
            ans = messagebox.askyesnocancel(
                "这个 jar 我看不出来是什么",
                f"{p.name}\n\n（里面既没有 plugin.yml 也没有 mods.toml）\n\n"
                f"是   = 当作插件放进 plugins/\n"
                f"否   = 当作模组放进 mods/\n"
                f"取消 = 跳过")
            if ans is None:
                return
            self._copy_into(p, PLUGINS_DIR if ans else MODS_DIR)

        else:
            messagebox.showinfo("暂不支持导入",
                                f"{p.name}\n{info['detail']}\n\n"
                                f"可以点「📂 打开服务器文件夹」手动放进去。")

    def _install_core_file(self, p, info):
        try:
            if SERVER_JAR.exists():
                shutil.copy2(SERVER_JAR, SERVER_JAR.with_suffix(".jar.bak"))
            shutil.copy2(p, SERVER_JAR)
            self.launcher_state["core"] = str(info.get("core") or "vanilla")
            if info.get("version"):
                self.launcher_state["version"] = info["version"]
            self._save_state()
            self._refresh_files_tab()
            self._refresh_servers_tab()
            self._refresh_overview()
            self._set_files_status(f"✅ 核心已导入: {p.name}")
        except Exception as e:
            messagebox.showerror("导入失败", f"{type(e).__name__}: {e}")

    def _copy_into(self, src, target_dir, dest_name=None):
        try:
            Path(target_dir).mkdir(parents=True, exist_ok=True)
            dst = Path(target_dir) / (dest_name or src.name)
            if dst.exists() and not messagebox.askyesno(
                    "文件已存在", f"{dst.name} 已存在，覆盖吗？"):
                return
            shutil.copy2(src, dst)
            self._refresh_files_tab()
            self._set_files_status(f"✅ 已导入 {dst.name} → "
                                   f"{Path(target_dir).name}/")
        except Exception as e:
            messagebox.showerror("导入失败", f"{type(e).__name__}: {e}")

    def _extract_zip(self, src, dest_dir):
        tid = self.task_start(f"解压 {src.name}")      # v3.5（0-10）：进侧边栏

        def task():
            try:
                with zipfile.ZipFile(src) as zf:
                    zf.extractall(dest_dir)
                self.after(0, lambda: self.task_done(tid, Path(dest_dir).name + "/"))
                self.after(0, lambda: self._set_files_status(
                    f"✅ 已解压 {src.name} → {Path(dest_dir).name}/"))
            except Exception as e:
                err = f"❌ 解压失败: {type(e).__name__}: {e}"
                print(err)
                self.after(0, lambda t=type(e).__name__: self.task_fail(tid, t))
                self.after(0, lambda: self._set_files_status(err, "#e74c3c"))
            self.after(0, self._refresh_files_tab)

        threading.Thread(target=task, daemon=True).start()

    def _set_files_status(self, text, color="#2ecc71", echo=True):
        try:
            if hasattr(self, "files_status"):
                self.files_status.configure(text=text, text_color=color)
        except Exception:
            pass
        if echo:
            self._append_console(f"[启动器] {text}\n")

    # ==================== 底部常驻状态栏：CPU / 内存（v3.2） ====================
    def _poll_stats(self):
        cpu = cpu_percent()
        ram = ram_info()
        parts = [f"CPU {cpu:.0f}%" if cpu is not None else "CPU --"]
        if ram:
            used, total, pct = ram
            parts.append(f"内存 {used / 1024 ** 3:.1f}/{total / 1024 ** 3:.1f} GB"
                         f"（{pct:.0f}%）")
        else:
            parts.append("内存 --")
        if self.is_running and self.server_process:
            mb = process_ram_mb(self.server_process.pid)
            if mb:
                # v3.5.11：按量自动换单位（10MB 别再写成 0.01 GB）
                parts.append(f"服务端 {human_size(mb * 1024 * 1024)}")
        try:
            self._set_label(self.lbl_stats, "   |   ".join(parts))
            # v3.2：内存提示实时刷新（原来只在启动时算一次快照）
            if ram and hasattr(self, "lbl_mem_hint"):
                total_gb = max(2, int(round(ram[1] / 1024 ** 3)))
                warn = ram[2] > 80
                self._set_label(
                    self.lbl_mem_hint,
                    (f"{'⚠ ' if warn else ''}物理内存 {total_gb} GB，"
                     f"当前已用 {ram[2]:.0f}%"
                     + (f"，建议最大内存不超过 "
                        f"{max(2, total_gb // 2 - 1)} GB" if warn else "")),
                    "#f39c12" if warn else "#888888")
            phase = getattr(self, "server_phase", "stopped")
            if phase == "starting":
                state_txt, col = f"⏳ 启动中「{CURRENT_SERVER}」", "#f39c12"
            elif self.is_running:
                state_txt, col = f"● 运行中「{CURRENT_SERVER}」", "#2ecc71"
            else:
                state_txt, col = f"○ 未运行「{CURRENT_SERVER}」", "gray"
            self._set_label(self.lbl_server_state, state_txt, col)
        except Exception:
            pass
        # v3.5：不再自己排下一次，统一由 _tick 按 TICK_STATS_MS 调度

    # ==================== 联机助手（v3.2） ====================
    def _build_net_tab(self):
        frame = self.tab_net

        ctk.CTkLabel(frame, text="联机助手",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(14, 2))
        ctk.CTkLabel(frame,
                     text="自动检测地址、放行防火墙端口、给出一句话建议",
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 6))

        bar = ctk.CTkFrame(frame, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=(0, 4))
        ctk.CTkButton(bar, text="🔄 重新检测", width=110, height=34,
                      command=self._refresh_net_tab).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="🔓 一键开放防火墙端口", width=190, height=34,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._open_firewall).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="🔒 关闭该端口规则", width=160, height=34,
                      fg_color="#4a4a4a", hover_color="#5a5a5a",
                      command=self._close_firewall).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="📋 复制连接地址", width=150, height=34,
                      fg_color="#3498db", hover_color="#2980b9",
                      command=self._copy_main_addr).pack(side="left", padx=4)

        self.net_status = ctk.CTkLabel(frame, text="",
                                       font=ctk.CTkFont(size=13),
                                       text_color="#f39c12")
        self.net_status.pack(pady=3)

        self.net_addr_frame = ctk.CTkFrame(frame, corner_radius=12)
        self.net_addr_frame.pack(fill="x", padx=30, pady=4)

        srow = ctk.CTkFrame(frame, fg_color="transparent")
        srow.pack(fill="x", padx=30, pady=(6, 2))
        ctk.CTkLabel(srow, text="server-ip", width=80, anchor="w",
                     font=ctk.CTkFont(size=13)).pack(side="left")
        self.net_server_ip = ctk.CTkEntry(
            srow, width=190, placeholder_text="留空＝监听全部(含IPv6)")
        self.net_server_ip.pack(side="left", padx=6)
        ctk.CTkLabel(srow, text="端口", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(10, 4))
        self.net_port = ctk.CTkEntry(srow, width=80)
        self.net_port.pack(side="left")
        ctk.CTkLabel(srow, text="正版验证", font=ctk.CTkFont(size=13)).pack(
            side="left", padx=(10, 4))
        self.net_online = ctk.CTkOptionMenu(srow, values=["true", "false"],
                                            width=95)
        self.net_online.pack(side="left")
        ctk.CTkButton(srow, text="💾 保存联机设置", width=150, height=32,
                      command=self._save_net_settings).pack(side="left", padx=10)

        self.net_tips = ctk.CTkTextbox(frame, height=180, wrap="word",
                                       font=ctk.CTkFont(size=13))
        self.net_tips.pack(fill="both", expand=True, padx=30, pady=(8, 12))
        # v3.2：延后到主循环开始后再检测。直接在 __init__ 里跑会让工作线程的
        # self.after() 报 “main thread is not in main loop”，页面永远停在“正在检测”。
        self.after(600, self._refresh_net_tab)

    def _refresh_net_tab(self):
        self.net_status.configure(text="⏳ 正在检测网络（要联网查公网 IP）…",
                                  text_color="#f39c12")
        _tid = self.task_start("检查网络与端口")        # v3.4：进侧边栏

        def task():
            try:
                port = int(self._get_port() or 25565)
            except Exception:
                port = 25565
            try:
                info = analyze_network(port)
            except Exception as e:
                err = f"❌ 检测失败: {type(e).__name__}: {e}"
                print(err)
                self.after(0, lambda: self.task_fail(
                    _tid, f"{type(e).__name__}: {e}"))
                self.after(0, lambda: self.net_status.configure(
                    text=err, text_color="#e74c3c"))
                return
            def _ok():
                self.task_done(_tid, "检测完成")
                self._render_net(info)

            self.after(0, _ok)

        threading.Thread(target=task, daemon=True).start()

    def _render_net(self, info):
        for w in self.net_addr_frame.winfo_children():
            w.destroy()
        port = info["port"]

        def addr_row(label, value):
            row = ctk.CTkFrame(self.net_addr_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=3)
            ctk.CTkLabel(row, text=label, width=80, anchor="w",
                         font=ctk.CTkFont(size=13)).pack(side="left")
            ctk.CTkLabel(row, text=value or "（没有）", anchor="w",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=("#2ecc71" if value else "#888888")).pack(
                side="left", padx=6)
            if value:
                ctk.CTkButton(row, text="复制", width=60, height=26,
                              font=ctk.CTkFont(size=12),
                              fg_color="#4a4a4a", hover_color="#5a5a5a",
                              command=lambda v=value:
                              self._copy_text(v)).pack(side="right", padx=6)

        addr_row("内网地址", f"{info['lan']}:{port}" if info["lan"] else None)
        addr_row("公网 IPv4",
                 f"{info['public4']}:{port}" if info["public4"] else None)
        v6 = info["public6"] or (info["local6"][0] if info["local6"] else None)
        addr_row("IPv6", f"[{v6}]:{port}" if v6 else None)
        addr_row("防火墙", "已放行" if info["firewall"] else "未放行")

        self.net_tips.configure(state="normal")
        self.net_tips.delete("1.0", "end")
        marks = {"ok": "✅ ", "warn": "⚠ ", "err": "❌ "}
        for kind, text in info["tips"]:
            self.net_tips.insert("end", marks.get(kind, "• ") + text + "\n")
        self.net_tips.configure(state="disabled")

        props = info["props"]
        self.net_server_ip.delete(0, "end")
        self.net_server_ip.insert(0, props.get("server-ip", ""))
        self.net_port.delete(0, "end")
        self.net_port.insert(0, str(port))
        self.net_online.set(str(props.get("online-mode", "true")).lower())
        self.net_status.configure(
            text=("✅ 检测完成，防火墙已放行" if info["firewall"]
                  else "⚠ 防火墙还没放行，点绿色按钮（会弹一次 UAC 授权框）"),
            text_color=("#2ecc71" if info["firewall"] else "#f39c12"))

    def _copy_text(self, text):
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.net_status.configure(text=f"📋 已复制: {text}",
                                      text_color="#2ecc71")
        except Exception as e:
            self.net_status.configure(text=f"复制失败: {e}",
                                      text_color="#e74c3c")

    def _copy_main_addr(self):
        port = self._get_port()
        pub4 = get_public_ips()[0]
        lan = get_lan_ip()
        addr = (f"{pub4}:{port}" if pub4 else
                (f"{lan}:{port}" if lan else ""))
        if addr:
            self._copy_text(addr)
        else:
            self.net_status.configure(text="没检测到可用地址",
                                      text_color="#f39c12")

    def _open_firewall(self):
        try:
            port = int(self.net_port.get().strip() or self._get_port())
        except Exception:
            port = int(self._get_port() or 25565)
        if firewall_rule_exists(port):
            self.net_status.configure(text=f"端口 {port} 已经在防火墙放行了",
                                      text_color="#2ecc71")
            return
        ok, out = firewall_open_port(port)
        if ok:
            self.net_status.configure(
                text=f"已请求开放端口 {port}：如果弹出 UAC 授权框请点「是」，"
                     f"3 秒后自动复查…", text_color="#f39c12")
            self.after(3500, self._refresh_net_tab)
        else:
            messagebox.showerror(
                "开放端口失败",
                f"{out}\n\n可能你点了「否」，或系统策略不允许。\n"
                f"也可以手动在管理员 CMD 里执行：\n"
                f"netsh advfirewall firewall add rule "
                f"name={FIREWALL_RULE_PREFIX}{port} dir=in action=allow "
                f"protocol=TCP localport={port}")

    def _close_firewall(self):
        try:
            port = int(self.net_port.get().strip() or self._get_port())
        except Exception:
            port = int(self._get_port() or 25565)
        if not messagebox.askyesno("关闭端口规则",
                                   f"删除防火墙里端口 {port} 的放行规则？"):
            return
        ok, out = firewall_close_port(port)
        self.net_status.configure(
            text=("已请求删除规则，3 秒后自动复查…" if ok
                  else f"删除失败: {out}"),
            text_color=("#f39c12" if ok else "#e74c3c"))
        if ok:
            self.after(3500, self._refresh_net_tab)

    def _save_net_settings(self):
        try:
            port = int(self.net_port.get().strip() or 25565)
            if not 1 <= port <= 65535:
                raise ValueError
        except Exception:
            messagebox.showerror("端口不合法", "端口必须是 1~65535 的整数")
            return
        ip = self.net_server_ip.get().strip()
        if ip and not re.match(r"^[0-9a-fA-F:.]+$", ip):
            messagebox.showerror("地址不合法",
                                 "server-ip 只能填 IP 地址，或者留空")
            return
        try:
            set_properties({"server-ip": ip, "server-port": str(port),
                            "online-mode": self.net_online.get()})
            self._load_properties(silent=True)
            self._refresh_files_tab()
            self.net_status.configure(
                text=f"✅ 已保存：server-ip={ip or '(留空=监听全部)'}｜"
                     f"端口={port}｜正版验证={self.net_online.get()}"
                     f"（重启服务器后生效）", text_color="#2ecc71")
            self._append_console(
                f"[启动器] 联机设置已保存：server-ip={ip or '(留空)'}, "
                f"port={port}, online-mode={self.net_online.get()}\n")
        except Exception as e:
            messagebox.showerror("保存失败", f"{type(e).__name__}: {e}")

    # ==================== 一键更新（v3.3） ====================
    def _record_install(self, kind, filename, slug, version_number, version_id):
        """记下“这个 jar 是哪个项目的哪个版本”，之后才能查更新。"""
        try:
            data = load_installed()
            data[filename] = {"project": slug, "kind": kind,
                              "version_number": version_number,
                              "version_id": version_id}
            save_installed(data)
        except Exception as e:
            print(f"[启动器] 记录安装信息失败: {e}")

    def _collect_updates(self):
        """返回 [(kind, 目录, 旧文件, 新版本dict, slug)]。

        没有安装记录的 jar 会用 sha1 去 Modrinth 反查（手动丢进去的也能识别）。
        """
        installed = load_installed()
        game = self.launcher_state.get("version")
        core = self.launcher_state.get("core")
        updates = []
        errs = []
        for kind, d, loader in (
                ("plugins", PLUGINS_DIR,
                 CORE_LOADER_MAP.get(core) if core else None),
                ("mods", MODS_DIR, core)):
            if not d.is_dir():
                continue
            for f in sorted(d.glob("*.jar")):
                rec = installed.get(f.name)
                if not rec or not rec.get("project"):
                    sha = sha1_of(f)
                    if not sha:
                        continue
                    try:
                        info = http_get_json(
                            f"{MODRINTH_API}/version_file/{sha}")
                        rec = {"project": info.get("project_id"),
                               "version_number": info.get("version_number"),
                               "version_id": info.get("id"), "kind": kind}
                        installed[f.name] = rec
                    except Exception:
                        continue
                try:
                    versions = modrinth_versions(rec["project"])
                    newest = pick_newest_version(versions, game, loader)
                except Exception as e:
                    errs.append(f"{f.name}: {type(e).__name__} {e}")
                    print(f"[启动器] 查 {f.name} 的更新失败: {e}")
                    continue
                if newest and newest.get("id") != rec.get("version_id"):
                    updates.append((kind, d, f, newest, rec["project"]))
        save_installed(installed)
        self._update_errors = errs      # v3.3：失败不再静默，界面会提示
        return updates

    def _apply_one_update(self, kind, d, old, newest, slug):
        files = newest.get("files", [])
        primary = next((x for x in files if x.get("primary")),
                       files[0] if files else None)
        if not primary:
            raise RuntimeError("该版本没有可下载文件")
        target = d / primary["filename"]
        if old.exists():
            self._save_rollback(kind, old, target.name)   # v3.5（⑪）：留一份旧的
        http_download(primary["url"], target)
        if target.name != old.name and old.exists():
            old.unlink()
        inst = load_installed()
        inst.pop(old.name, None)
        inst[target.name] = {"project": slug, "kind": kind,
                             "version_number": newest.get("version_number"),
                             "version_id": newest.get("id")}
        save_installed(inst)
        return target.name

    def _check_updates_ui(self, silent=False):
        self._set_files_status("⏳ 正在检查插件/模组更新…", "#f39c12")
        _tid = self.task_start("检查插件/模组更新")      # v3.4：进侧边栏

        def task():
            try:
                updates = self._collect_updates()
            except Exception as e:
                err = f"❌ 检查更新失败: {type(e).__name__}: {e}"
                print(err)
                self.after(0, lambda: self.task_fail(
                    _tid, f"{type(e).__name__}: {e}"))
                self.after(0, lambda: self._set_files_status(err, "#e74c3c"))
                return
            errs = getattr(self, "_update_errors", [])
            if not updates:
                if errs:
                    self.after(0, lambda: self._set_files_status(
                        f"⚠ 没有发现更新，但有 {len(errs)} 个文件没查成功"
                        f"（见控制台）", "#f39c12"))
                    self.after(0, lambda: self._append_console(
                        "[启动器] 以下文件检查更新失败:\n  "
                        + "\n  ".join(errs) + "\n"))
                    self.after(0, lambda: self.task_fail(
                        _tid, f"{len(errs)} 个文件没查成功"))
                    return
                self.after(0, lambda: self.task_done(_tid, "已是最新"))
                self.after(0, lambda: self._set_files_status(
                    "✅ 插件/模组都是最新版本", "#2ecc71"))
                if not silent:
                    self.after(0, lambda: messagebox.showinfo(
                        "检查更新", "插件和模组都已经是最新的 ✅"))
                return
            lines = [f"· {f.name}  →  {v.get('version_number')}"
                     for _, _, f, v, _ in updates]
            msg = (f"发现 {len(updates)} 个可以更新：\n\n" + "\n".join(lines)
                   + "\n\n现在全部更新吗？\n（旧文件会被新版替换）")
            self.after(0, lambda: self.task_done(
                _tid, f"发现 {len(updates)} 个可更新"))
            self.after(0, lambda: self._confirm_updates(updates, msg))

        threading.Thread(target=task, daemon=True).start()

    def _confirm_updates(self, updates, msg):
        if not messagebox.askyesno("发现更新", msg):
            self._set_files_status(f"有 {len(updates)} 个更新未安装", "#f39c12")
            return
        self._set_files_status(f"⏳ 正在更新 {len(updates)} 个文件…", "#f39c12")
        _tid = self.task_start(f"更新 {len(updates)} 个插件/模组")

        def task():
            ok = fail = 0
            for kind, d, old, newest, slug in updates:
                try:
                    self.task_update(
                        _tid, f"{ok + fail + 1}/{len(updates)} {old.name}",
                        (ok + fail) / max(1, len(updates)))
                    self._apply_one_update(kind, d, old, newest, slug)
                    ok += 1
                except Exception as e:
                    fail += 1
                    print(f"[启动器] 更新 {old.name} 失败: {e}")
            if fail:
                self.after(0, lambda: self.task_fail(
                    _tid, f"成功 {ok}，失败 {fail}"))
            else:
                self.after(0, lambda: self.task_done(
                    _tid, f"全部成功（{ok} 个）"))
            self.after(0, lambda: self._set_files_status(
                f"✅ 更新完成：成功 {ok} 个" + (f"，失败 {fail} 个" if fail else ""),
                "#2ecc71" if not fail else "#f39c12"))
            self.after(0, self._refresh_files_tab)

        threading.Thread(target=task, daemon=True).start()

    def _auto_update(self):
        """切到该服务器时，按它自己的自动更新开关静默升级。"""
        st = self.launcher_state.get("auto_update", {}) or {}
        if not (st.get("plugins") or st.get("mods") or st.get("core")):
            return
        tid = self.task_start("自动更新插件/模组/核心")   # v3.5（0-10）：进侧边栏

        def task():
            n = 0
            try:
                if st.get("core"):
                    self._auto_update_core()
                try:
                    updates = self._collect_updates()
                except Exception:
                    updates = []
                picked = [u for u in updates
                          if (u[0] == "plugins" and st.get("plugins"))
                          or (u[0] == "mods" and st.get("mods"))]
                if not picked:
                    self.after(0, lambda: self.task_done(tid, "没有可更新的"))
                    return
                self.after(0, lambda: self._append_console(
                    f"[启动器] 自动更新：发现 {len(picked)} 个新版本，开始升级…\n"))
                for kind, d, old, newest, slug in picked:
                    try:
                        name = self._apply_one_update(kind, d, old, newest, slug)
                        n += 1
                        self.after(0, lambda nm=name: self._append_console(
                            f"[启动器] 已自动更新: {nm}\n"))
                    except Exception as e:
                        print(f"[启动器] 自动更新 {old.name} 失败: {e}")
                self.after(0, lambda k=n: self.task_done(tid, f"更新了 {k} 个"))
            except Exception as e:
                self.after(0, lambda x=str(e): self.task_fail(tid, x[:60]))
            self.after(0, self._refresh_files_tab)

        threading.Thread(target=task, daemon=True).start()

    # ==================== 常用指令收藏 + 中文说明（v3.4） ====================
    def _cmd_labels(self):
        """下拉框显示成「指令  —  中文说明」，选的时候再还原成纯指令。"""
        out = []
        for c in self.console_cmds:
            d = describe_command(c)
            base = c.strip()
            out.append(f"{base}   —   {d[0]}" if d else base)
        return out or [""]

    def _cmd_from_label(self, label):
        """从下拉框文本还原成真实指令。"""
        return (label or "").split("   —   ")[0].strip()

    def _show_cmd_hint(self, cmd):
        try:
            d = describe_command(cmd)
            if d:
                self.lbl_cmd_hint.configure(text=f"💡 {d[0]}　｜　用法：{d[1]}")
            else:
                self.lbl_cmd_hint.configure(text="")
        except Exception:
            pass

    def _pick_quick_cmd(self, value):
        """从下拉栏选一条 -> 只把指令填进输入框（说明放在下面的提示行）。"""
        base = self._cmd_from_label(value)
        raw = next((c for c in self.console_cmds if c.strip() == base), base)
        try:
            self.cmd_entry.delete(0, "end")
            self.cmd_entry.insert(0, raw)
            self.cmd_entry.focus_set()
        except Exception:
            pass
        self._show_cmd_hint(base)

    def _add_quick_cmd(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            messagebox.showinfo("提示", "先在下面输入框里写一条指令，再点收藏")
            return
        if cmd not in self.console_cmds:
            self.console_cmds.append(cmd)
            save_console_cmds(self.console_cmds)
            try:
                self.cmd_combo.configure(values=self._cmd_labels())
            except Exception:
                pass
            d = describe_command(cmd)
            self._append_console(
                f"[启动器] 已收藏指令: {cmd}"
                + (f"（{d[0]}）\n" if d else "\n"))
        self._show_cmd_hint(cmd)

    def _del_quick_cmd(self):
        raw = (self.cmd_combo.get() or "").strip()
        base = self._cmd_from_label(raw)
        if base in self.console_cmds:
            self.console_cmds.remove(base)
        elif raw in self.console_cmds:
            self.console_cmds.remove(raw)
        else:
            return
        save_console_cmds(self.console_cmds)
        try:
            self.cmd_combo.configure(values=self._cmd_labels())
            self.cmd_combo.set("")
        except Exception:
            pass
        self.lbl_cmd_hint.configure(text="")
        self._append_console(f"[启动器] 已移除收藏: {base}\n")

    # ==================== 导出 MOD 包（v3.3） ====================
    def _export_mods(self):
        tid = self.task_start("导出 MOD 包")          # v3.5（0-10）：进侧边栏

        def task():
            try:
                out, msg = export_mods_zip(SERVER_DIR, CURRENT_SERVER)
                if out is None:
                    self.after(0, lambda: self.task_fail(tid, msg[:40]))
                    self.after(0, lambda: self._set_files_status(
                        f"⚠ {msg}", "#f39c12"))
                else:
                    self.after(0, lambda n=out.name: self.task_done(tid, n))
                    self.after(0, lambda: self._set_files_status(
                        f"✅ 已导出 {out.name}（{msg}）→ exports/"))
                    self.after(0, lambda: open_in_explorer(EXPORTS_DIR))
            except Exception as e:
                err = f"❌ 导出失败: {type(e).__name__}: {e}"
                print(err)
                self.after(0, lambda t=type(e).__name__: self.task_fail(tid, t))
                self.after(0, lambda: self._set_files_status(err, "#e74c3c"))
            self.after(0, self._refresh_files_tab)

        threading.Thread(target=task, daemon=True).start()

    # ==================== 设置页：启动器 / 服务器（v3.3） ====================
    # ==================== v3.5（⑳）彩色花样文字生成器 ====================
    def _build_coltext_tab(self):
        f = self.tab_coltext
        ctk.CTkLabel(
            f, anchor="w", font=ctk.CTkFont(size=13),
            text="打字时用 & 加代码（例：&a你好 &l加粗）—— 也可以点下面的色块插入；预览是实时的。"
        ).pack(fill="x", padx=12, pady=(10, 6))

        row = ctk.CTkFrame(f, fg_color="transparent")
        row.pack(fill="x", padx=12)
        self.ct_entry = ctk.CTkEntry(row, placeholder_text="&a你好 &c世界 &l加粗")
        self.ct_entry.pack(side="left", fill="x", expand=True)
        self.ct_entry.bind("<KeyRelease>", lambda e: self._refresh_coltext())
        ctk.CTkButton(row, text="示例", width=56, height=28,
                      command=self._demo_coltext).pack(side="left", padx=(6, 0))
        ctk.CTkButton(row, text="清空", width=56, height=28,
                      command=self._clear_coltext).pack(side="left", padx=(6, 0))

        pal = ctk.CTkFrame(f, fg_color="transparent")
        pal.pack(fill="x", padx=12, pady=(8, 0))
        for code, name, hexv, _j in MC_COLORS:
            ctk.CTkButton(
                pal, text=name, width=42, height=26, border_width=1,
                fg_color=hexv, hover_color=hexv,
                text_color=("#111111" if code in "7fedba" else "#FFFFFF"),
                command=lambda c=code: self._insert_coltext("&" + c)
            ).pack(side="left", padx=2)
        for code, name, _j in MC_FORMATS:
            ctk.CTkButton(
                pal, text=name, width=54, height=26,
                command=lambda c=code: self._insert_coltext("&" + c)
            ).pack(side="left", padx=2)
        ctk.CTkButton(pal, text="重置", width=48, height=26,
                      command=lambda: self._insert_coltext("&r")).pack(side="left", padx=2)

        pv = ctk.CTkFrame(f, fg_color="transparent")
        pv.pack(fill="x", padx=12, pady=(8, 0))
        ctk.CTkLabel(pv, text="预览：", font=ctk.CTkFont(size=12)).pack(
            side="left", anchor="n", pady=2)
        self.ct_preview = tkinter.Text(
            pv, height=3, wrap="word", bd=0, highlightthickness=1,
            highlightbackground="#444444", bg="#1f1f1f", fg="#dddddd",
            font=("Microsoft YaHei", 13))
        self.ct_preview.pack(side="left", fill="x", expand=True)
        self.ct_preview.configure(state="disabled")
        self.ct_tags = set()
        self.ct_fonts = {}

        outs = ctk.CTkFrame(f, fg_color="transparent")
        outs.pack(fill="both", expand=True, padx=12, pady=(8, 10))
        outs.grid_columnconfigure(0, weight=1)
        outs.grid_columnconfigure(1, weight=1)
        self.ct_out_section = self._ct_out_box(outs, 0, 0, "§ 码（进游戏 / 写配置）")
        self.ct_out_amp = self._ct_out_box(outs, 0, 1, "& 码（发帖 / 交流）")
        self.ct_out_tellraw = self._ct_out_box(outs, 1, 0, "/tellraw 的 JSON")
        self.ct_out_motd = self._ct_out_box(outs, 1, 1, "MOTD（单行）")
        self._refresh_coltext()

    def _ct_out_box(self, parent, r, c, title):
        cell = ctk.CTkFrame(parent, fg_color="transparent")
        cell.grid(row=r, column=c, sticky="nsew", padx=6, pady=4)
        head = ctk.CTkFrame(cell, fg_color="transparent")
        head.pack(fill="x")
        ctk.CTkLabel(head, text=title, anchor="w",
                     font=ctk.CTkFont(size=12)).pack(side="left")
        box = ctk.CTkTextbox(cell, height=84,
                             font=ctk.CTkFont(family="Consolas", size=12))
        box.pack(fill="both", expand=True)
        box.configure(state="disabled")
        ctk.CTkButton(head, text="复制", width=48, height=22,
                      command=lambda: self._copy_ct_box(box)).pack(side="right")
        return box

    def _ct_set(self, box, text):
        try:
            box.configure(state="normal")
            box.delete("1.0", "end")
            box.insert("1.0", text)
            box.configure(state="disabled")
        except Exception:
            pass

    def _copy_ct_box(self, box):
        try:
            self.clipboard_clear()
            self.clipboard_append(box.get("1.0", "end-1c"))
        except Exception:
            pass

    def _ct_font_for(self, fmts):
        key = tuple(sorted(fmts))
        fnt = self.ct_fonts.get(key)
        if fnt is None:
            fnt = tkinter.font.Font(
                family="Microsoft YaHei", size=13,
                weight="bold" if "l" in fmts else "normal",
                slant="italic" if "o" in fmts else "roman",
                underline=1 if "n" in fmts else 0,
                overstrike=1 if "m" in fmts else 0)
            self.ct_fonts[key] = fnt
        return fnt

    def _insert_coltext(self, code):
        try:
            self.ct_entry.insert(self.ct_entry.index("insert"), code)
            self.ct_entry.focus_set()
        except Exception:
            pass
        self._refresh_coltext()

    def _clear_coltext(self):
        try:
            self.ct_entry.delete(0, "end")
        except Exception:
            pass
        self._refresh_coltext()

    def _demo_coltext(self):
        try:
            self.ct_entry.delete(0, "end")
            self.ct_entry.insert(0, MC_DEMO_TEXT)
        except Exception:
            pass
        self._refresh_coltext()

    def _refresh_coltext(self, _event=None):
        try:
            text = self.ct_entry.get()
        except Exception:
            return
        try:
            self.ct_preview.configure(state="normal")
            self.ct_preview.delete("1.0", "end")
            for seg, color, fmts in mc_preview_runs(text):
                tag = "ct_%s_%s" % (color or "x", "".join(sorted(fmts)) or "x")
                if tag not in self.ct_tags:
                    cfg = {"font": self._ct_font_for(fmts)}
                    if color:
                        cfg["foreground"] = color
                    self.ct_preview.tag_configure(tag, **cfg)
                    self.ct_tags.add(tag)
                self.ct_preview.insert("end", seg, tag)
            self.ct_preview.configure(state="disabled")
        except Exception:
            pass
        self._ct_set(self.ct_out_section, mc_section(text))
        self._ct_set(self.ct_out_amp, mc_amp(text))
        self._ct_set(self.ct_out_tellraw, mc_tellraw(text))
        self._ct_set(self.ct_out_motd, mc_motd(text))

    def _browse_java_path(self):
        """v3.5.3：【浏览…】直接选 java.exe，不用手打路径。

        默认从当前填的路径（或它所在目录）开始翻，省得每次从 C 盘根目录找。
        取消就什么都不改。
        """
        try:
            cur = self.set_java.get().strip().strip('"')
        except Exception:
            cur = ""
        init = ""
        if cur and cur.lower() not in ("java", "javaw", "java.exe"):
            try:
                p = Path(cur)
                init = str(p if p.is_dir() else p.parent)
            except Exception:
                init = ""
        try:
            picked = filedialog.askopenfilename(
                title="选择 java.exe（在 JDK/JRE 的 bin 目录里）",
                initialdir=init or str(BASE_DIR),
                filetypes=[("Java 可执行文件", "java.exe javaw.exe"),
                           ("可执行文件", "*.exe"),
                           ("所有文件", "*.*")])
        except Exception:
            picked = ""
        if not picked:
            return
        try:
            self.set_java.delete(0, "end")
            self.set_java.insert(0, str(picked).strip().strip('"'))
        except Exception:
            pass

    def _build_settings_tab(self):
        frame = self.tab_settings
        ctk.CTkLabel(frame, text="设置",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(12, 2))
        ctk.CTkLabel(frame, text="左边是启动器全局设置，右边是当前服务器的设置",
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 4))

        cols = ctk.CTkFrame(frame, fg_color="transparent")
        cols.pack(fill="both", expand=True, padx=20, pady=4)
        left = ctk.CTkScrollableFrame(cols, width=440, height=430,
                                      label_text="启动器设置（全局）")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = ctk.CTkScrollableFrame(
            cols, width=440, height=430,
            label_text=f"服务器设置（{CURRENT_SERVER}）")
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self._fast_scroll(left)
        self._fast_scroll(right)

        def row(parent, text, factory):
            r = ctk.CTkFrame(parent, fg_color="transparent")
            r.pack(fill="x", pady=6)
            ctk.CTkLabel(r, text=text, width=150, anchor="w",
                         font=ctk.CTkFont(size=13)).pack(side="left")
            w = factory(r)
            w.pack(side="left", fill="x", expand=True, padx=6)
            return w

        s = self.settings
        # v3.5.3：Java 路径这一行加了【浏览…】按钮，不用手打路径
        _jrow_path = ctk.CTkFrame(left, fg_color="transparent")
        _jrow_path.pack(fill="x", pady=6)
        ctk.CTkLabel(_jrow_path, text="Java 路径", width=150, anchor="w",
                     font=ctk.CTkFont(size=13)).pack(side="left")
        self.set_java = ctk.CTkEntry(_jrow_path, height=32)
        self.set_java.pack(side="left", fill="x", expand=True, padx=6)
        self.set_java.insert(0, s.get("java_path", "java"))
        self.btn_browse_java = ctk.CTkButton(
            _jrow_path, text="📂 浏览…", width=88, height=32,
            fg_color="#3a7bd5", hover_color="#2f66b3",
            command=self._browse_java_path)
        self.btn_browse_java.pack(side="left")

        # v3.4：Java 一键安装
        ctk.CTkLabel(left, text="— Java 运行时 —",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#7fb3ff").pack(pady=(12, 2))
        self.lbl_java_rec = ctk.CTkLabel(
            left, text=self._java_recommend_text(),
            font=ctk.CTkFont(size=12), text_color="#f39c12",
            justify="left", wraplength=390)
        self.lbl_java_rec.pack(pady=2)
        _jrow = ctk.CTkFrame(left, fg_color="transparent")
        _jrow.pack(fill="x", pady=4)
        self.java_choice = ctk.CTkOptionMenu(
            _jrow, width=170,
            values=[f"Java {v}"
                    + ("（无法一键安装）" if v in JAVA_NO_INSTALL_REASON else "")
                    for v in JAVA_CHOICES])
        _rec = recommended_java(self.launcher_state.get("version", ""))[1]
        self.java_choice.set(f"Java {_rec or JAVA_CHOICES[-1]}"
                             + ("（无法一键安装）"
                                if (_rec or JAVA_CHOICES[-1])
                                in JAVA_NO_INSTALL_REASON else ""))
        self.java_choice.pack(side="left", padx=4)
        _btn_java = ctk.CTkButton(_jrow, text="⬇ 一键下载安装", width=150,
                                  height=30, fg_color="#2ecc71",
                                  hover_color="#27ae60",
                                  command=self._on_install_java_click)
        _btn_java.pack(side="left", padx=4)
        # v3.5：鼠标停上去就说清楚"这个版本能不能一键装、为什么"
        self._tip(self.java_choice, self._java_choice_tip)
        self._tip(_btn_java, self._java_choice_tip)
        self.lbl_java_cfg_status = ctk.CTkLabel(
            left, text="", font=ctk.CTkFont(size=12), text_color="#2ecc71",
            justify="left", wraplength=390)
        self.lbl_java_cfg_status.pack(pady=2)
        _javas = installed_javas()
        if _javas:
            ctk.CTkLabel(left, text="已装： " + "、".join(n for n, _ in _javas),
                         font=ctk.CTkFont(size=11), text_color="#888888",
                         wraplength=390, justify="left").pack(pady=(0, 4))
        self.set_jvm = row(left, "附加 JVM 参数",
                           lambda p: ctk.CTkEntry(
                               p, height=32,
                               placeholder_text="如 -XX:+UseG1GC -XX:+ParallelRefProcEnabled"))
        self.set_jvm.insert(0, s.get("jvm_args", ""))
        self.set_appearance = row(left, "外观",
                                  lambda p: ctk.CTkOptionMenu(
                                      p, values=["dark", "light", "system"],
                                      width=130))
        self.set_appearance.set(s.get("appearance", "dark"))

        # v3.5（⑨）：主题系统 —— 配色 + 字号/控件缩放（重启生效）
        self.set_ui_theme = row(
            left, "配色主题",
            lambda p: ctk.CTkOptionMenu(p, width=140, values=list(UI_THEMES)))
        self.set_ui_theme.set(UI_THEME_LABELS.get(s.get("ui_theme", "blue"),
                                                 "蓝（默认）"))
        self.set_ui_scale = row(
            left, "界面缩放",
            lambda p: ctk.CTkOptionMenu(p, width=100, values=list(UI_SCALES)))
        self.set_ui_scale.set(ui_scale_label(s.get("ui_scale", 1.0)))
        ctk.CTkLabel(left, text="（配色和缩放的改动要重启启动器才完全生效）",
                     font=ctk.CTkFont(size=11), text_color="#888888",
                     wraplength=390, justify="left").pack(pady=(0, 4))
        # v3.5（⑰）：过渡动画开关
        self.set_animations = row(left, "过渡动画",
                                  lambda p: ctk.CTkSwitch(p, text=""))
        if s.get("animations", True):
            self.set_animations.select()
        ctk.CTkLabel(left, text="（开窗淡入 + 后台任务栏收放；嫌晃眼就关掉）",
                     font=ctk.CTkFont(size=11), text_color="#888888",
                     wraplength=390, justify="left").pack(pady=(0, 4))
        self.set_auto_check = row(left, "启动时检查更新",
                                  lambda p: ctk.CTkSwitch(p, text=""))
        if s.get("auto_check_update", True):
            self.set_auto_check.select()

        # v3.5（⑪）：定时自动备份
        ctk.CTkLabel(left, text="— 自动备份 —",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#7fb3ff").pack(pady=(12, 2))
        self.set_backup_every = row(
            left, "备份间隔",
            lambda p: ctk.CTkOptionMenu(p, width=140,
                                        values=list(BACKUP_MINUTES)))
        self.set_backup_every.set(
            BACKUP_LABELS.get(int(s.get("auto_backup_min", 0) or 0), "关闭"))
        self.set_backup_keep = row(
            left, "保留份数",
            lambda p: ctk.CTkOptionMenu(p, width=100,
                                        values=["3", "5", "10", "20"]))
        self.set_backup_keep.set(str(s.get("auto_backup_keep", 5)))
        ctk.CTkLabel(left, text="开着服务器也会自动备份（存档边写边读，"
                                "极小概率不一致）；只备份 world/",
                     font=ctk.CTkFont(size=11), text_color="#888888",
                     wraplength=390, justify="left").pack(pady=(0, 4))

        # v3.5（⑧）：离线手册（Git / GitHub 教学）
        ctk.CTkButton(left, text="📖 打开离线手册（Git / GitHub 教学）",
                      width=300, height=34, fg_color="#8e44ad",
                      hover_color="#7d3c98",
                      command=self._open_manual).pack(pady=(8, 4))
        self.lbl_set_mem = ctk.CTkLabel(
            left, text=self._mem_hint_text(), font=ctk.CTkFont(size=12),
            text_color="#888888", justify="left")
        self.lbl_set_mem.pack(pady=(6, 0))
        ctk.CTkButton(left, text="💾 保存启动器设置", height=36,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._save_launcher_settings_ui).pack(pady=10)

        st = self.launcher_state.get("auto_update", {}) or {}
        self.srv_auto_plugin = row(right, "自动更新插件",
                                   lambda p: ctk.CTkSwitch(p, text=""))
        self.srv_auto_mod = row(right, "自动更新模组",
                                lambda p: ctk.CTkSwitch(p, text=""))
        self.srv_auto_core = row(right, "自动更新核心",
                                 lambda p: ctk.CTkSwitch(p, text=""))
        for w, k in ((self.srv_auto_plugin, "plugins"),
                     (self.srv_auto_mod, "mods"),
                     (self.srv_auto_core, "core")):
            if st.get(k):
                w.select()
        steps = max(1, self.mem_max_limit - 1)
        self.srv_min_mem = row(right, "该服最小内存(GB)",
                               lambda p: ctk.CTkSlider(
                                   p, from_=1, to=self.mem_max_limit,
                                   number_of_steps=steps))
        self.srv_max_mem = row(right, "该服最大内存(GB)",
                               lambda p: ctk.CTkSlider(
                                   p, from_=1, to=self.mem_max_limit,
                                   number_of_steps=steps))
        self.srv_min_mem.set(int(self.launcher_state.get(
            "min_mem", self.settings.get("default_min_mem", 2))))
        self.srv_max_mem.set(int(self.launcher_state.get(
            "max_mem", self.settings.get("default_max_mem", 4))))
        self.srv_jvm = row(right, "该服 JVM 参数",
                           lambda p: ctk.CTkEntry(
                               p, height=32,
                               placeholder_text="留空＝用启动器设置里的"))
        self.srv_jvm.insert(0, self.launcher_state.get("jvm_args", ""))

        # v3.5（③）：崩溃自动重启 + 定时重启
        ctk.CTkLabel(right, text="— 自动重启 —",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#7fb3ff").pack(pady=(12, 2))
        sc = self.launcher_state.get("schedule", {}) or {}
        self.srv_crash_restart = row(right, "崩溃后自动重启",
                                     lambda p: ctk.CTkSwitch(p, text=""))
        if sc.get("crash_restart"):
            self.srv_crash_restart.select()
        self.srv_crash_limit = row(
            right, "10 分钟内最多重启",
            lambda p: ctk.CTkOptionMenu(p, width=100, values=CRASH_LIMITS))
        self.srv_crash_limit.set(str(sc.get("crash_limit", 3)))
        self.srv_restart_mode = row(
            right, "定时重启",
            lambda p: ctk.CTkOptionMenu(p, width=160,
                                        values=list(RESTART_MODES)))
        self.srv_restart_mode.set(
            RESTART_MODE_LABELS.get(str(sc.get("restart_mode", "off")), "关闭"))
        ctk.CTkLabel(right, text="定时重启会先在游戏里广播 60/30/10 秒提示，"
                                 "停服 15 秒后自动开回来",
                     font=ctk.CTkFont(size=11), text_color="#888888",
                     wraplength=390, justify="left").pack(pady=(0, 4))
        ctk.CTkLabel(
            right,
            text=("说明：\n"
                  "· 自动更新会在「切换到该服务器」时自动检查并升级\n"
                  "· 该服内存/参数留空则用左边的全局设置\n"
                  "· 概览页那两个内存滑块和这里是同一份数值"),
            font=ctk.CTkFont(size=12), text_color="#888888",
            justify="left").pack(pady=6)
        ctk.CTkButton(right, text="💾 保存服务器设置", height=36,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._save_server_settings_ui).pack(pady=10)

        self.lbl_settings_status = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=13), text_color="#2ecc71")
        self.lbl_settings_status.pack(pady=(0, 6))

    def _install_java(self, feature_version):
        """一键下载安装 Adoptium JRE，装好后自动设为当前 Java。"""
        tid = self.task_start(f"安装 Java {feature_version}")
        try:
            self.lbl_java_cfg_status.configure(
                text=f"⏳ 正在查询 Java {feature_version} 下载地址…",
                text_color="#f39c12")
        except Exception:
            pass

        def task():
            try:
                info = java_download_info(feature_version)
                JAVA_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
                dest_dir = JAVA_RUNTIME_DIR / f"jre-{feature_version}"
                zip_path = JAVA_RUNTIME_DIR / info["name"]
                size_mb = (info.get("size") or 0) / 1048576
                self.task_update(
                    tid, f"下载 {info['name']}（{size_mb:.0f} MB）", 0.0)

                def on_progress(done, total):
                    pct = done / total if total else 0
                    self.task_update(
                        tid, f"{done / 1048576:.1f} / {total / 1048576:.1f} MB",
                        pct)

                # v3.5.7：官方 GitHub 在慢网下 38KB/s 且一卡就超时 → 先挑最快的源
                # （国内镜像 640KB/s），下完用 Adoptium 给的 sha256 校验，失败自动续传重试。
                urls = list(info.get("mirrors") or []) + [info["url"]]
                self.task_update(tid, "挑选最快的下载源…", None)
                src = pick_fast_url(urls) or info["url"]
                try:
                    host = urllib.parse.urlparse(src).netloc
                except Exception:
                    host = "?"
                self.task_update(
                    tid, f"下载 {info['name']}（{size_mb:.0f} MB，来源 {host}）",
                    0.0)
                http_download_verified(src, zip_path, on_progress,
                                       checksum=info.get("checksum"),
                                       cancel_check=lambda: self._task_cancel_check(tid))
                self.task_update(tid, "解压中…", None)
                exe = extract_jre(zip_path, dest_dir)
                try:
                    zip_path.unlink()
                except Exception:
                    pass

                self.settings["java_path"] = str(exe)
                save_launcher_settings(self.settings)
                self.launcher_state["java_path"] = str(exe)
                self._save_state()
                self.after(0, self._auto_check_java)
                self.task_done(tid, f"Java {info['version']} → {dest_dir.name}")
                self.after(0, lambda e=exe: self.lbl_java_cfg_status.configure(
                    text=f"✅ 已安装并设为当前 Java：{e}", text_color="#2ecc71"))
                self.after(0, self._refresh_overview)
            except TaskCancelled:
                return                      # 用户点了 ✕，别报错
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                print(f"[启动器] 安装 Java 失败: {err}")
                self.task_fail(tid, err)
                self.after(0, lambda t=err: self.lbl_java_cfg_status.configure(
                    text=f"❌ 安装失败：{t}", text_color="#e74c3c"))

        threading.Thread(target=task, daemon=True).start()

    # ==================== v3.5：鼠标悬停提示 ====================
    def _tip(self, widget, text, delay=350):
        """给控件挂悬停提示。text 可以是字符串，也可以是个函数（悬停时才取）。"""
        def on_enter(_e=None):
            self._tip_cancel()
            try:
                self._tip_job = self.after(delay, lambda: self._show_tip(text))
            except Exception:
                pass

        def on_leave(_e=None):
            self._tip_cancel()
            self._hide_tip()

        try:
            widget.bind("<Enter>", on_enter, add="+")
            widget.bind("<Leave>", on_leave, add="+")
        except Exception as e:
            print(f"[启动器] 挂悬停提示失败: {e}")

    def _tip_cancel(self):
        job = getattr(self, "_tip_job", None)
        if job is not None:
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._tip_job = None

    def _show_tip(self, text, x=None, y=None):
        """显示悬停提示（一个无边框小窗，跟着鼠标）。"""
        self._tip_job = None
        if callable(text):
            try:
                text = text()
            except Exception as e:
                text = f"（提示取不到: {e}）"
        self._hide_tip()
        try:
            win = ctk.CTkToplevel(self)
            win.overrideredirect(True)
            try:
                win.attributes("-topmost", True)
            except Exception:
                pass
            ctk.CTkLabel(win, text=str(text), justify="left",
                         font=ctk.CTkFont(size=12), fg_color="#2b2b2b",
                         text_color="#f1f1f1", corner_radius=6,
                         wraplength=430).pack(padx=12, pady=8)
            if x is None:
                x = self.winfo_pointerx() + 16
                y = self.winfo_pointery() + 20
            win.geometry(f"+{int(x)}+{int(y)}")
            self._tip_win = win
            return win
        except Exception as e:
            print(f"[启动器] 提示窗失败: {e}")
            return None

    def _hide_tip(self):
        win = getattr(self, "_tip_win", None)
        self._tip_win = None
        if win is not None:
            try:
                win.destroy()
            except Exception:
                pass

    def _java_recommend_text(self):
        """设置页里那行“推荐哪个 Java”。"""
        core = self.launcher_state.get("core")
        ver = self.launcher_state.get("version")
        if not ver:
            return "装好服务端核心后，这里会显示推荐版本"
        need, install = recommended_java(ver)
        cur = getattr(self, "java_major", None)
        txt = f"服务端 {core or ''} {ver} → 推荐 Java {need}"
        if need in JAVA_NO_INSTALL_REASON:
            txt += f"（Java {need} 要自己手动装，本站不提供下载）"
        elif install and install != need:
            txt += f"（本站提供 Java {install}）"
        if cur:
            txt += (f"\n当前 Java {cur}：" +
                    ("✅ 够用" if cur >= need else "⚠ 偏低，建议装上面推荐的"))
        return txt

    def _java_choice_version(self):
        """从下拉框文字里取出 Java 大版本号（"Java 16（无法一键安装）" → 16）。"""
        m = re.search(r"Java\s*(\d+)", self.java_choice.get() or "")
        return int(m.group(1)) if m else None

    def _java_choice_tip(self):
        """鼠标悬停在下拉框/安装按钮上时显示的原因。"""
        v = self._java_choice_version()
        if v is None:
            return "选一个 Java 版本"
        reason = JAVA_NO_INSTALL_REASON.get(v)
        if reason:
            return f"❌ Java {v} 无法一键安装\n{reason}"
        return (f"✅ Java {v} 可以一键下载安装"
                f"（Adoptium 官方 JRE，装到 runtime/ 并自动设为当前 Java）")

    def _on_install_java_click(self):
        """从下拉框里取出版本号再安装（值可能带「（无法一键安装）」后缀）。"""
        ver = self._java_choice_version()
        if ver is None:
            messagebox.showerror("无法安装", "没能从下拉框里认出 Java 版本号")
            return
        reason = JAVA_NO_INSTALL_REASON.get(ver)
        if reason:
            self._show_tip(reason)          # 顺手把原因浮出来，别让人找不到
            messagebox.showinfo(f"Java {ver} 没法一键安装", reason)
            return
        try:
            self._install_java(ver)
        except Exception as e:
            messagebox.showerror("无法安装", f"{type(e).__name__}: {e}")

    def _mem_hint_text(self):
        ram = ram_info()
        if not ram:
            return ""
        used, total, pct = ram
        total_gb = max(2, int(round(total / 1024 ** 3)))
        warn = pct > 80
        return (("⚠ " if warn else "") + f"物理内存 {total_gb} GB，当前已用 {pct:.0f}%"
                + (f"，建议最大内存不超过 {max(2, total_gb // 2 - 1)} GB"
                   if warn else ""))

    def _save_launcher_settings_ui(self):
        self.settings.update({
            "java_path": self.set_java.get().strip() or "java",
            "jvm_args": self.set_jvm.get().strip(),
            "appearance": self.set_appearance.get(),
            "auto_check_update": bool(self.set_auto_check.get()),
            "auto_backup_min": BACKUP_MINUTES.get(
                self.set_backup_every.get(), 0),
            "auto_backup_keep": int(self.set_backup_keep.get() or 5),
            "ui_theme": UI_THEMES.get(self.set_ui_theme.get(), "blue"),
            "ui_scale": UI_SCALES.get(self.set_ui_scale.get(), 1.0),
            "animations": bool(self.set_animations.get()),
        })
        save_launcher_settings(self.settings)
        self._last_auto_backup = time.monotonic()   # 从"现在"开始算下一轮
        try:
            ctk.set_appearance_mode(self.settings["appearance"])
        except Exception:
            pass
        every = int(self.settings.get("auto_backup_min", 0) or 0)
        tip = ("✅ 启动器设置已保存（配色/缩放要重启启动器才生效）" if not every else
               f"✅ 已保存（每 {every} 分钟自动备份世界，"
               f"留 {self.settings.get('auto_backup_keep')} 份；"
               f"配色/缩放重启生效）")
        self.lbl_settings_status.configure(text=tip, text_color="#2ecc71")

    def _save_server_settings_ui(self):
        st = self.launcher_state.setdefault("auto_update", {})
        st["plugins"] = bool(self.srv_auto_plugin.get())
        st["mods"] = bool(self.srv_auto_mod.get())
        st["core"] = bool(self.srv_auto_core.get())
        self.launcher_state["min_mem"] = int(round(float(self.srv_min_mem.get())))
        self.launcher_state["max_mem"] = int(round(float(self.srv_max_mem.get())))
        self.launcher_state["jvm_args"] = self.srv_jvm.get().strip()
        sc = self.launcher_state.setdefault("schedule", {})   # v3.5（③）
        sc["crash_restart"] = bool(self.srv_crash_restart.get())
        try:
            sc["crash_limit"] = int(self.srv_crash_limit.get() or 3)
        except Exception:
            sc["crash_limit"] = 3
        sc["restart_mode"] = RESTART_MODES.get(self.srv_restart_mode.get(), "off")
        self._last_restart_at = time.monotonic()   # 定时重启从"现在"开始算
        self._save_state()
        try:
            self.min_mem.set(self.launcher_state["min_mem"])
            self._on_min_mem(self.min_mem.get())
            self.max_mem.set(self.launcher_state["max_mem"])
            self._on_max_mem(self.max_mem.get())
        except Exception:
            pass
        self.lbl_settings_status.configure(
            text=f"✅ 「{CURRENT_SERVER}」的设置已保存（内存 {self.launcher_state['min_mem']}"
                 f"~{self.launcher_state['max_mem']}G，自动更新 "
                 f"插件={'开' if st['plugins'] else '关'} "
                 f"模组={'开' if st['mods'] else '关'} "
                 f"核心={'开' if st['core'] else '关'}）",
            text_color="#2ecc71")

    # ==================== 后台任务侧边栏（v3.4） ====================
    # ==================== v3.5（⑰）过渡动画 ====================
    def _animations_on(self):
        try:
            return bool(self.settings.get("animations", True))
        except Exception:
            return True

    def _fade_in(self, steps=8, ms=18):
        """开窗口时淡入（alpha 0 → 1）。关掉动画就什么都不做。"""
        if not self._animations_on():
            try:
                self.attributes("-alpha", 1.0)
            except Exception:
                pass
            return
        try:
            self.attributes("-alpha", 0.0)
        except Exception:
            return

        def step(i=1):
            try:
                self.attributes("-alpha", min(1.0, i / float(steps)))
            except Exception:
                return
            if i < steps:
                self.after(ms, lambda: step(i + 1))

        step()
        # 兜底：不管中途出什么事，最后一定要完全显示出来（别把窗口留在半透明）
        self.after(steps * ms + 120,
                   lambda: self.attributes("-alpha", 1.0))

    def _set_panel_width(self, w):
        """侧栏宽度一次设置。

        - configure(width=w)：让 CTk 内部按新宽度重画（圆角/底色/子控件重排）
        - place_configure(width=缩放后像素)：浮层的真实几何由 place 说了算
          （CTk 的 place() 不收 width 参数，所以这里直接调 tkinter 的 place_configure，
           缩放自己算，免得改 UI 缩放后宽度对不上）
        """
        try:
            self.task_panel.configure(width=w)
            self.task_panel.place_configure(
                width=self.task_panel._apply_widget_scaling(w))
        except Exception:
            pass
        self._task_panel_w = w

    def _anim_width(self, target, steps=10, ms=16, done=None):
        """把右侧任务栏的宽度平滑地变到 target。

        v3.5.2：侧栏改成覆盖式布局后，宽度动画**只影响侧栏自己的子树**，
        不再牵动标签页/内容区重排（v3.5 老实现单帧要 135~282ms → 8 帧卡成 0.8s 且撕裂；
        现在单帧只有几毫秒），所以中间帧又加回来了。

        注意：CTkFrame.cget("width") 拿到的不是"刚设进去的那个值"，
        所以这里自己记一份当前宽度（_task_panel_w），别依赖 cget。
        """
        job = getattr(self, "_anim_job", None)
        if job is not None:
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._anim_job = None
        start = int(getattr(self, "_task_panel_w", target))
        if not self._animations_on() or start == target:
            self._set_panel_width(target)
            if done is not None:
                try:
                    done()
                except Exception:
                    pass
            return
        nsteps = max(1, int(steps))

        def step(i=1):
            self._anim_job = None
            w = int(round(start + (target - start) * i / nsteps))
            self._set_panel_width(w)
            if i < nsteps:
                self._anim_job = self.after(ms, lambda: step(i + 1))
            else:
                self._set_panel_width(target)
                if done is not None:
                    try:
                        done()
                    except Exception:
                        pass

        step()

    def _build_task_panel(self):
        # v3.5.2：覆盖式侧栏。
        #  - task_slot：永远 104px 的占位槽（宽度从不变化 → 标签页宽度恒定、不重排）
        #  - task_panel：真正显示的侧栏，用 place 浮在最右边，展开时 104 → 250 盖住右边一部分
        # 这样折叠/展开只影响侧栏自己的子树，不再牵动整个窗口重排（老实现的卡顿和撕裂都来自这里）。
        self.task_slot = ctk.CTkFrame(self.content_wrap, width=104,
                                      corner_radius=0, fg_color="transparent")
        self.task_slot.pack(side="right", fill="y")
        self.task_slot.pack_propagate(False)

        self.task_panel = ctk.CTkFrame(self.content_wrap, width=250, corner_radius=0)
        # 注意：CTk 的 place() 不收 width，浮层的宽度只能用 tkinter 的 place_configure 给
        # （宽度由 _set_panel_width 统一维护；这里先按 250 放好）。
        self.task_panel.place_configure(
            relx=1.0, x=0, y=0, relheight=1.0, anchor="ne",
            width=self.task_panel._apply_widget_scaling(250))
        self.task_panel.lift()
        self._task_panel_w = 250        # v3.5（⑰）：自己记当前宽度，动画要用

        head = ctk.CTkFrame(self.task_panel, fg_color="transparent")
        head.pack(fill="x", padx=10, pady=(10, 6))
        self.lbl_task_head = ctk.CTkLabel(
            head, text="📋 后台任务", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_task_head.pack(side="left")
        self.btn_task_toggle = ctk.CTkButton(
            head, text="▶", width=30, height=24, font=ctk.CTkFont(size=12),
            fg_color="#4a4a4a", hover_color="#5a5a5a",
            command=self._toggle_task_panel)
        self.btn_task_toggle.pack(side="right")

        self.task_body = ctk.CTkScrollableFrame(self.task_panel, width=230,
                                                height=560)
        self.task_body.pack(fill="both", expand=True, padx=6, pady=(0, 10))
        self._fast_scroll(self.task_body)
        self._refresh_task_panel()

    def _toggle_task_panel(self, force_collapse=None):
        collapsed = (not self._task_collapsed if force_collapse is None
                     else bool(force_collapse))
        self._task_collapsed = collapsed
        try:
            if collapsed:
                self.btn_task_toggle.configure(text="◀")
                # v3.5.2：动画只动"空壳"（先把任务内容摘掉），
                # 这样每帧只是侧栏自己变窄，内容区一点不重排 → 顺滑。
                self.task_body.pack_forget()
                self._anim_width(104)
            else:
                self.btn_task_toggle.configure(text="▶")
                # 先让空壳从 104 滑到 250，滑完再把任务内容挂回去（内容只在最后一帧重排一次）
                self._anim_width(250, done=lambda: self.task_body.pack(
                    fill="both", expand=True, padx=6, pady=(0, 10)))
        except Exception:
            pass

    def task_start(self, title, detail="", progress=None):
        """登记一个后台任务并显示到侧边栏，返回任务 id。"""
        self._task_seq = getattr(self, "_task_seq", 0) + 1
        tid = self._task_seq
        if not hasattr(self, "tasks"):
            self.tasks = {}
        self.tasks[tid] = {"title": title, "detail": detail,
                           "progress": progress, "state": "running"}
        # v3.5.7：每个任务一个取消开关，任务卡上的 ✕ 就是给它置位
        if not hasattr(self, "_task_cancel_events"):
            self._task_cancel_events = {}
        try:
            self._task_cancel_events[tid] = threading.Event()
        except Exception:
            pass
        if getattr(self, "_task_collapsed", False):
            self._toggle_task_panel(False)      # 有活干就自动展开
        self._refresh_task_panel()
        return tid

    def _task_cancel_check(self, tid):
        """给下载/安装线程用的取消询问函数（v3.5.7）。"""
        ev = (getattr(self, "_task_cancel_events", {}) or {}).get(tid)
        return bool(ev is not None and ev.is_set())

    def task_cancel(self, tid):
        """用户点任务卡上的「✕」：立刻标记取消，正在跑的下载会在下个检查点停。"""
        t = getattr(self, "tasks", {}).get(tid)
        if not t or t.get("state") != "running":
            return
        ev = (getattr(self, "_task_cancel_events", {}) or {}).get(tid)
        if ev is not None:
            try:
                ev.set()
            except Exception:
                pass
        t["state"] = "cancelled"
        t["detail"] = "已取消"
        t["progress"] = 0.0
        self._schedule_task_refresh()
        self.after(5000, lambda: self._drop_task(tid))

    def task_update(self, tid, detail=None, progress=None):
        t = getattr(self, "tasks", {}).get(tid)
        if not t:
            return
        if t.get("state") == "cancelled":     # 已取消就别再被进度覆盖了
            return
        if detail is not None:
            t["detail"] = detail
        if progress is not None:
            t["progress"] = progress
        self._schedule_task_refresh()

    def task_done(self, tid, detail="完成"):
        t = getattr(self, "tasks", {}).get(tid)
        if not t:
            return
        t["state"] = "done"
        t["detail"] = detail
        t["progress"] = 1.0
        self._schedule_task_refresh()
        self.after(6000, lambda: self._drop_task(tid))     # 6 秒后自动清掉

    def task_fail(self, tid, detail="失败"):
        t = getattr(self, "tasks", {}).get(tid)
        if not t:
            return
        if t.get("state") == "cancelled":      # 用户主动取消的，别再标成失败
            return
        t["state"] = "failed"
        t["detail"] = detail
        t["progress"] = None
        self._schedule_task_refresh()
        self.after(20000, lambda: self._drop_task(tid))    # 失败留久一点

    def _drop_task(self, tid):
        try:
            (getattr(self, "tasks", {}) or {}).pop(tid, None)
            (getattr(self, "_task_cancel_events", {}) or {}).pop(tid, None)
            if not self.tasks:
                self._toggle_task_panel(True)     # 没任务了就收起来
        except Exception:
            pass
        self._refresh_task_panel()

    def _schedule_task_refresh(self):
        if getattr(self, "_task_refresh_pending", False):
            return
        self._task_refresh_pending = True
        self.after(250, self._refresh_task_panel_now)

    def _refresh_task_panel_now(self):
        self._task_refresh_pending = False
        self._refresh_task_panel()

    def _refresh_task_panel(self):
        """v3.5.4：改成"原地更新"，不再每次把整块内容删了重建。

        原因：下载核心/插件时进度几十毫秒就来一次，250ms 一次的"全销毁+全重建"
        会让侧边栏一闪一闪（控件被反复销毁新建）。
        现在只做三件事：
          ① 任务没了才销毁对应那一行；
          ② 标题/详情/进度条数值用 configure 原地改（值没变就不动）；
          ③ 转圈模式只在"转圈↔百分比"切换时才 start/stop（否则每 250ms 重启动画，也闪）。
        """
        if not hasattr(self, "task_body"):
            return
        try:
            tasks = getattr(self, "tasks", {}) or {}
            rows = getattr(self, "_task_rows", None)
            if rows is None:
                rows = self._task_rows = {}

            running = sum(1 for t in tasks.values() if t["state"] == "running")
            head_text = (f"📋 任务 {running} 进行中" if running
                         else ("📋 后台任务" if not tasks else "📋 任务 已完成"))
            if getattr(self, "_task_head_text", None) != head_text:
                self._task_head_text = head_text
                self.lbl_task_head.configure(text=head_text)

            # ① 已经不存在的任务：销毁那一行
            for tid in list(rows):
                if tid not in tasks:
                    try:
                        rows[tid]["row"].destroy()
                    except Exception:
                        pass
                    rows.pop(tid, None)

            if not tasks:
                if getattr(self, "_task_empty_lbl", None) is None:
                    self._task_empty_lbl = ctk.CTkLabel(
                        self.task_body, text="（当前没有后台任务）",
                        font=ctk.CTkFont(size=12), text_color="#888888")
                    self._task_empty_lbl.pack(pady=16)
                return
            if getattr(self, "_task_empty_lbl", None) is not None:
                try:
                    self._task_empty_lbl.destroy()
                except Exception:
                    pass
                self._task_empty_lbl = None

            icons = {"running": "⏳", "done": "✅", "failed": "❌",
                     "cancelled": "🚫"}
            for tid in sorted(tasks, reverse=True):
                t = tasks[tid]
                rec = rows.get(tid)
                if rec is None:
                    rec = self._make_task_row(tid, t, icons)   # 只有新任务才建行
                    rows[tid] = rec
                    # 新的排最上面（插在"当前最上面那行"前面；
                    # 注意要用 pack_slaves 的显示顺序，winfo_children 是创建顺序，不一样）
                    kids = [w for w in self.task_body.pack_slaves()
                            if w is not rec["row"]]
                    try:
                        if kids:
                            rec["row"].pack(fill="x", padx=2, pady=3,
                                            before=kids[0])
                        else:
                            rec["row"].pack(fill="x", padx=2, pady=3)
                    except Exception:
                        rec["row"].pack(fill="x", padx=2, pady=3)
                self._update_task_row(rec, t, icons)
        except Exception as e:
            print(f"[任务] 侧边栏刷新失败: {e}")

    def _make_task_row(self, tid, t, icons):
        """建一行任务卡（只在任务第一次出现时调用）。

        v3.5.7：标题右边加「✕」——点它取消这个任务（下载会在下个检查点停下）。
        """
        row = ctk.CTkFrame(self.task_body, corner_radius=8)
        head = ctk.CTkFrame(row, fg_color="transparent")
        head.pack(fill="x", padx=8, pady=(6, 0))
        lbl_title = ctk.CTkLabel(
            head, text=f"{icons.get(t['state'], '•')} {t['title']}",
            font=ctk.CTkFont(size=12, weight="bold"), anchor="w",
            wraplength=168, justify="left")
        lbl_title.pack(side="left", fill="x", expand=True)
        btn_cancel = ctk.CTkButton(
            head, text="✕", width=22, height=20, corner_radius=6,
            font=ctk.CTkFont(size=12),
            fg_color="#5a3a3a", hover_color="#b03a3a", text_color="#ffb3b3",
            command=lambda: self.task_cancel(tid))
        btn_cancel.pack(side="right", padx=(4, 0))
        lbl_detail = ctk.CTkLabel(
            row, text=t.get("detail") or "", font=ctk.CTkFont(size=11),
            text_color="#a0a0a0", anchor="w", wraplength=190, justify="left")
        detail_visible = bool(t.get("detail"))
        if detail_visible:
            lbl_detail.pack(fill="x", padx=8)
        bar = ctk.CTkProgressBar(row, height=6)
        bar.pack(fill="x", padx=8, pady=(3, 8))
        return {"row": row, "title": lbl_title, "detail": lbl_detail,
                "detail_visible": detail_visible, "bar": bar,
                "cancel": btn_cancel, "cancel_visible": True,
                "title_text": None, "detail_text": None,
                "bar_mode": None, "bar_val": None}

    def _update_task_row(self, rec, t, icons):
        """原地更新一行（值没变就不碰控件，避免无谓重画）。"""
        title = f"{icons.get(t['state'], '•')} {t['title']}"
        if rec["title_text"] != title:
            rec["title_text"] = title
            rec["title"].configure(text=title)

        # ✕ 只在"还在跑"的时候有用，结束后藏掉
        want_cancel = (t["state"] == "running")
        if rec.get("cancel_visible") != want_cancel:
            rec["cancel_visible"] = want_cancel
            try:
                if want_cancel:
                    rec["cancel"].pack(side="right", padx=(4, 0))
                else:
                    rec["cancel"].pack_forget()
            except Exception:
                pass

        detail = t.get("detail") or ""
        if detail:
            if rec["detail_text"] != detail:
                rec["detail_text"] = detail
                rec["detail"].configure(text=detail)
            if not rec["detail_visible"]:
                rec["detail_visible"] = True
                rec["detail"].pack(fill="x", padx=8)
        elif rec["detail_visible"]:
            rec["detail_visible"] = False
            rec["detail"].pack_forget()

        want_ind = (t.get("progress") is None and t["state"] == "running")
        want_mode = "indeterminate" if want_ind else "determinate"
        bar = rec["bar"]
        if rec["bar_mode"] != want_mode:
            try:
                bar.configure(mode=want_mode)
                if want_ind:
                    bar.start()
                else:
                    bar.stop()
            except Exception:
                pass
            rec["bar_mode"] = want_mode

        if not want_ind:
            val = max(0.0, min(1.0, float(t.get("progress") or 0.0)))
            if rec["bar_val"] != val:
                rec["bar_val"] = val
                try:
                    bar.set(val)
                except Exception:
                    pass

    # ==================== 通用：标题 / 滚动加速 ====================
    def _update_title(self):
        self.title(f"Minecraft 一键开服启动器 v{APP_VERSION} — "
                   f"当前服务器: {CURRENT_SERVER}")

    def _fast_scroll(self, scrollable, px_per_unit=2):
        """v3.1：每单位 2 像素。滚动距离现在交给上面的“平滑滚动”动画控制，
        这里只需要一个足够细的粒度，让动画能走出小步。"""
        try:
            scrollable._parent_canvas.configure(yscrollincrement=px_per_unit)
        except Exception:
            pass

    # ==================== 封面线程池（v3.0） ====================
    def _start_img_workers(self):
        """v3.4：封面改成 2 个低优先级线程 + 可视优先 + 节流，不再跟界面抢资源。"""
        if self._img_workers_started:
            return
        self._img_workers_started = True
        self._img_queue = queue.Queue()
        self._img_pending = getattr(self, "_img_pending", [])
        self._img_gen = getattr(self, "_img_gen", 0)
        self._img_quiet_until = getattr(
            self, "_img_quiet_until", time.time() + IMG_QUIET_SECONDS)
        for _ in range(IMG_WORKERS):
            threading.Thread(target=self._img_worker, daemon=True).start()
        self.after(400, self._pump_images)

    def _img_worker(self):
        # 把线程优先级降到 BELOW_NORMAL，别和界面抢 CPU 时间片
        try:
            ctypes.windll.kernel32.SetThreadPriority(
                ctypes.windll.kernel32.GetCurrentThread(), -1)
        except Exception:
            pass
        while True:
            label, url, name, size, gen = self._img_queue.get()
            try:
                # 启动静默期：先让界面把该画的画完
                while time.time() < getattr(self, "_img_quiet_until", 0):
                    time.sleep(0.2)
                if gen != getattr(self, "_img_gen", 0):
                    continue                       # 已经翻页了，这张不用下了
                key = (url, size)
                thumb = THUMB_CACHE.get(key)
                if thumb is None:
                    img = load_image(url)
                    if img is None:
                        continue
                    thumb = img.copy()
                    thumb.thumbnail((size, size), Image.BILINEAR)  # 比 LANCZOS 快得多
                    cache_put(THUMB_CACHE, key, thumb)
                self.after(0, lambda l=label, t=thumb, s=size:
                           self._apply_thumb(l, t, s))
            except Exception as ex:
                print(f"[封面] ❌ 处理失败 {name}: {ex}")
            time.sleep(IMG_THROTTLE_SECONDS)       # v3.4：每张之间节流

    def _is_visible(self, widget):
        """控件当前是否在可视区域内（可视优先加载用）。"""
        try:
            # 往上找该控件所属的可滚动画布（结果列表 / 版本弹窗各有一个）
            w, canvas = widget, None
            for _ in range(6):
                w = getattr(w, "master", None)
                if w is None:
                    break
                canvas = getattr(w, "_parent_canvas", None)
                if canvas is not None:
                    break
            if canvas is None:
                return True
            cy0 = canvas.winfo_rooty()
            cy1 = cy0 + canvas.winfo_height()
            wy0 = widget.winfo_rooty()
            return (wy0 + widget.winfo_height()) > cy0 and wy0 < cy1
        except Exception:
            return True

    def _pump_images(self):
        """把“已经滚到可见”的封面排进加载队列（每次最多 IMG_PUMP_MAX 张）。"""
        try:
            pending = getattr(self, "_img_pending", None)
            if pending:
                still, queued = [], 0
                for item in pending:
                    label = item[0]
                    try:
                        alive = label.winfo_exists()
                    except Exception:
                        alive = False
                    if not alive:
                        continue
                    if queued < IMG_PUMP_MAX and self._is_visible(label):
                        self._img_queue.put(item)
                        queued += 1
                    else:
                        still.append(item)
                self._img_pending = still
            if getattr(self, "_img_pending", None):
                self.after(400, self._pump_images)
        except Exception:
            pass

    def _apply_thumb(self, label, thumb, size):
        try:
            if not label.winfo_exists():     # 翻页后旧控件已销毁，别再动它
                return
            ctk_img = ctk.CTkImage(light_image=thumb, dark_image=thumb,
                                   size=(size, size))
            label.configure(image=ctk_img, text="", fg_color="transparent")
            label._ctk_image_ref = ctk_img
        except Exception as ex:
            print(f"[封面] ❌ 应用到 UI 失败: {ex}")

    # ==================== 多服务器管理（v3.0） ====================
    def _server_state_summary(self, name):
        """读指定服务器的 launcher_state.json，返回 'Paper 1.21.8' 这样的描述。"""
        base = server_path(name)
        try:
            data = json.loads(
                (base / "launcher_state.json").read_text(encoding="utf-8"))
            core = (data.get("core") or "").capitalize()
            ver = data.get("version") or ""
            if core and ver:
                return f"{core} {ver}"
        except Exception:
            pass
        return "已装核心(版本未知)" if (base / "server.jar").exists() else "未安装核心"

    def _build_servers_tab(self):
        frame = self.tab_servers

        ctk.CTkLabel(frame, text="服务器管理",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(16, 4))
        self.lbl_server_path = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_server_path.pack(pady=(0, 8))

        bar = ctk.CTkFrame(frame, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=(0, 6))
        ctk.CTkButton(bar, text="＋ 新建空服务器", width=150, height=36,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._new_server).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="📂 指定文件夹为服务器", width=190, height=36,
                      fg_color="#3498db", hover_color="#2980b9",
                      command=self._pick_external_folder).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="📦 导入（复制进来）", width=170, height=36,
                      fg_color="#9b59b6", hover_color="#8e44ad",
                      command=self._import_folder_copy).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="🔄 刷新", width=80, height=36,
                      command=self._refresh_servers_tab).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="📂 servers 目录", width=150, height=36,
                      command=lambda: open_in_explorer(
                          SERVERS_ROOT)).pack(side="left", padx=4)

        self.server_list_frame = ctk.CTkScrollableFrame(frame, width=920,
                                                        height=300)
        self.server_list_frame.pack(padx=30, pady=6, fill="both", expand=True)
        self._fast_scroll(self.server_list_frame)

        ctk.CTkLabel(frame, text="回收站（删除的服务器先放这里，可以恢复）",
                     font=ctk.CTkFont(size=12), text_color="gray").pack(
            anchor="w", padx=36, pady=(6, 0))
        self.trash_frame = ctk.CTkScrollableFrame(frame, width=920, height=100)
        self.trash_frame.pack(padx=30, pady=(2, 12), fill="both")
        self._fast_scroll(self.trash_frame)

        self._refresh_servers_tab()

    def _refresh_servers_tab(self):
        for w in self.server_list_frame.winfo_children():
            w.destroy()
        for w in self.trash_frame.winfo_children():
            w.destroy()

        self.lbl_server_path.configure(text=f"所有服务器存放于: {SERVERS_ROOT}")

        names = list_servers()
        if not names:
            ctk.CTkLabel(self.server_list_frame, text="还没有服务器，点上面「新建服务器」",
                         text_color="gray").pack(pady=20)

        for name in names:
            active = (name == CURRENT_SERVER)
            row = ctk.CTkFrame(self.server_list_frame, corner_radius=10)
            row.pack(fill="x", padx=6, pady=5)

            title = (f"{'✅ ' if active else ''}{name}"
                     + ("   📁外部目录" if is_external_server(name) else ""))
            ctk.CTkLabel(row, text=title,
                         font=ctk.CTkFont(size=15, weight="bold"),
                         anchor="w").pack(side="left", padx=(14, 10), pady=12)
            ctk.CTkLabel(row, text=self._server_state_summary(name),
                         font=ctk.CTkFont(size=12),
                         text_color="#bbbbbb").pack(side="left", padx=6)
            if active and self.is_running:
                ctk.CTkLabel(row, text="● 运行中",
                             font=ctk.CTkFont(size=12),
                             text_color="#2ecc71").pack(side="left", padx=10)

            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.pack(side="right", padx=12)
            if active:
                ctk.CTkButton(btns, text="✓ 当前使用", width=100, height=32,
                              state="disabled").pack(side="left", padx=3)
            else:
                ctk.CTkButton(btns, text="切换到它", width=100, height=32,
                              fg_color="#3498db", hover_color="#2980b9",
                              command=lambda n=name:
                              self._switch_server(n)).pack(side="left", padx=3)
            ctk.CTkButton(btns, text="删除", width=70, height=32,
                          fg_color="#e74c3c", hover_color="#c0392b",
                          command=lambda n=name:
                          self._delete_server(n)).pack(side="left", padx=3)
            ctk.CTkButton(btns, text="重命名", width=80, height=32,
                          fg_color="#4a4a4a", hover_color="#5a5a5a",
                          command=lambda n=name:
                          self._rename_server(n)).pack(side="left", padx=3)
            ctk.CTkButton(btns, text="打开文件夹", width=100, height=32,
                          fg_color="#4a4a4a", hover_color="#5a5a5a",
                          command=lambda n=name: open_in_explorer(
                              server_path(n))).pack(side="left", padx=3)

        # ---- 回收站 ----
        TRASH_ROOT.mkdir(exist_ok=True)
        trashed = sorted([p for p in TRASH_ROOT.iterdir() if p.is_dir()],
                         reverse=True)
        if not trashed:
            ctk.CTkLabel(self.trash_frame, text="（空）", text_color="#888888",
                         font=ctk.CTkFont(size=12)).pack(pady=8)
        for p in trashed:
            row = ctk.CTkFrame(self.trash_frame, corner_radius=8)
            row.pack(fill="x", padx=4, pady=3)
            ctk.CTkLabel(row, text=p.name, font=ctk.CTkFont(size=12),
                         anchor="w").pack(side="left", padx=10, pady=6)
            ctk.CTkButton(row, text="彻底删除", width=90, height=28,
                          fg_color="#e74c3c", hover_color="#c0392b",
                          command=lambda q=p:
                          self._purge_trash(q)).pack(side="right", padx=8, pady=4)
            ctk.CTkButton(row, text="恢复", width=70, height=28,
                          fg_color="#2ecc71", hover_color="#27ae60",
                          command=lambda q=p:
                          self._restore_trash(q)).pack(side="right", padx=4, pady=4)

        # v3.5.17：服务器列表变了，「📥 下载核心」页的目标服务器下拉框跟着刷新
        self._refresh_core_targets()

    def _valid_server_name(self, name):
        if not name:
            return "名称不能为空"
        if re.search(r'[\\/:*?"<>|]', name):
            return '名称不能包含 \\ / : * ? " < > | 这些字符'
        if name.startswith("."):
            return "名称不能以点开头"
        return None

    def _new_server(self):
        dialog = ctk.CTkInputDialog(text="新服务器名称（会作为文件夹名）:",
                                    title="新建服务器")
        name = (dialog.get_input() or "").strip()
        err = self._valid_server_name(name)
        if name == "":
            return
        if err:
            messagebox.showerror("名称不合法", err)
            return
        target = SERVERS_ROOT / name
        if target.exists():
            messagebox.showerror("已存在", f"「{name}」已经存在了")
            return
        try:
            (target / "plugins").mkdir(parents=True, exist_ok=True)
            (target / "mods").mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("失败", f"创建失败: {e}")
            return
        register_server(name, target)
        self._refresh_servers_tab()
        if messagebox.askyesno("新建成功",
                               f"「{name}」创建好了。\n现在切换到它并去下载核心吗？"):
            self._switch_server(name)
            self.tabview.set("📥 下载核心")
            # v3.5.17：下载页的目标服务器直接选成这个新服务器，别再新建一个
            self._select_core_target(name)

    def _switch_server(self, name):
        if self.is_running:
            messagebox.showwarning("请先停止", "有服务器正在运行，请先停止再切换。")
            return
        if name == CURRENT_SERVER or not server_path(name).exists():
            return
        activate_server(name)
        save_index({"current": name})
        self.launcher_state = self._load_state()
        self.online_players.clear()
        self._update_title()
        if hasattr(self, "console_box"):
            self.console_box.configure(state="normal")
            self.console_box.delete("1.0", "end")
            self.console_box.configure(state="disabled")
        self._rebuild_config_fields()      # v3.3：属性表跟着服务端版本走
        self._load_properties(silent=True)
        self._refresh_servers_tab()
        self._refresh_files_tab()
        self._refresh_overview()
        self._append_console(
            f"[启动器] 已切换到服务器「{name}」\n[启动器] 目录: {SERVER_DIR}\n\n")
        if hasattr(self, "search_entry"):
            self._search_modrinth(page=0)
        self.after(900, self._auto_update)     # v3.3：按该服的开关自动更新

    def _rename_server(self, name):
        if self.is_running and name == CURRENT_SERVER:
            messagebox.showwarning("请先停止", "该服务器正在运行，请先停止。")
            return
        dialog = ctk.CTkInputDialog(text=f"把「{name}」改名为:", title="重命名")
        new = (dialog.get_input() or "").strip()
        if not new or new == name:
            return
        err = self._valid_server_name(new)
        if err:
            messagebox.showerror("名称不合法", err)
            return
        if new in SERVER_PATHS:
            messagebox.showerror("已存在", f"「{new}」已经存在了")
            return
        try:
            if is_external_server(name):
                # 外部目录只改“在启动器里的名字”，绝不动你的文件夹
                old_path = server_path(name)
                unregister_server(name)
                register_server(new, old_path)
            else:
                (SERVERS_ROOT / name).rename(SERVERS_ROOT / new)
                unregister_server(name)
                register_server(new, SERVERS_ROOT / new)
        except Exception as e:
            messagebox.showerror("失败", f"重命名失败: {e}")
            return
        if name == CURRENT_SERVER:
            activate_server(new)
            save_index({"current": new})
            self._update_title()
        self._refresh_servers_tab()

    def _delete_server(self, name):
        if self.is_running and name == CURRENT_SERVER:
            messagebox.showwarning("请先停止", "该服务器正在运行，请先停止。")
            return
        ext = is_external_server(name)
        path = server_path(name)
        if ext:
            if not messagebox.askyesno(
                    "从列表移除",
                    f"「{name}」是你指定的外部文件夹:\n{path}\n\n"
                    f"只会把它从启动器列表里移除，\n"
                    f"不会删除任何文件。继续吗？"):
                return
            unregister_server(name)
        else:
            size = human_size(dir_size(path))
            if not messagebox.askyesno(
                    "删除服务器",
                    f"确定删除「{name}」吗？\n占用空间: {size}\n\n"
                    f"（会先移到回收站 .trash，可以恢复）"):
                return
            TRASH_ROOT.mkdir(exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            try:
                shutil.move(str(path), str(TRASH_ROOT / f"{name}_{stamp}"))
            except Exception as e:
                messagebox.showerror("失败", f"删除失败: {e}")
                return
            unregister_server(name)

        if name == CURRENT_SERVER:
            rest = list_servers()
            if not rest:
                d = SERVERS_ROOT / "默认服务器"
                d.mkdir(parents=True, exist_ok=True)
                register_server("默认服务器", d)
                rest = ["默认服务器"]
            activate_server(rest[0])
            save_index({"current": rest[0]})
            self.launcher_state = self._load_state()
            self._update_title()
        self._refresh_servers_tab()
        self._refresh_files_tab()
        self._refresh_overview()

    def _restore_trash(self, path):
        name = path.name.rsplit("_", 2)[0] or "恢复的服务器"
        dst = SERVERS_ROOT / name
        i = 1
        while dst.exists():
            dst = SERVERS_ROOT / f"{name}_{i}"
            i += 1
        try:
            shutil.move(str(path), str(dst))
        except Exception as e:
            messagebox.showerror("失败", f"恢复失败: {e}")
            return
        register_server(dst.name, dst)
        self._refresh_servers_tab()

    def _purge_trash(self, path):
        if not messagebox.askyesno("彻底删除",
                                   f"永久删除「{path.name}」？\n此操作不可恢复！"):
            return
        try:
            shutil.rmtree(path)
        except Exception as e:
            messagebox.showerror("失败", f"删除失败: {e}")
        self._refresh_servers_tab()

    # ==================== 文件管理（v3.0） ====================
    def _build_files_tab(self):
        frame = self.tab_files

        ctk.CTkLabel(frame, text="文件管理",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(16, 4))
        self.lbl_files_hint = ctk.CTkLabel(
            frame, text="", font=ctk.CTkFont(size=12), text_color="gray")
        self.lbl_files_hint.pack(pady=(0, 8))

        bar = ctk.CTkFrame(frame, fg_color="transparent")
        bar.pack(fill="x", padx=30, pady=(0, 4))
        ctk.CTkButton(bar, text="📂 打开服务器文件夹", width=180, height=36,
                      command=lambda: open_in_explorer(
                          SERVER_DIR)).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="🔄 刷新", width=100, height=36,
                      command=self._refresh_files_tab).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="💾 备份存档 (world)", width=180, height=36,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=self._backup_world).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="🗑 删除核心 (server.jar)", width=200, height=36,
                      fg_color="#e74c3c", hover_color="#c0392b",
                      command=self._delete_core).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="📥 选择文件导入", width=150, height=36,
                      fg_color="#9b59b6", hover_color="#8e44ad",
                      command=self._pick_files_import).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="📦 导出 MOD 包", width=140, height=36,
                      fg_color="#f39c12", hover_color="#d68910",
                      command=self._export_mods).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="🔄 检查更新", width=120, height=36,
                      fg_color="#3498db", hover_color="#2980b9",
                      command=lambda: self._check_updates_ui()).pack(
            side="left", padx=4)

        self.lbl_drop_hint = ctk.CTkLabel(
            frame,
            text="💡 也可以把 jar / zip / 整个服务器文件夹 直接拖进窗口导入",
            font=ctk.CTkFont(size=12), text_color="#9b59b6")
        self.lbl_drop_hint.pack(pady=(2, 0))

        self.files_status = ctk.CTkLabel(frame, text="",
                                         font=ctk.CTkFont(size=13),
                                         text_color="#f39c12")
        self.files_status.pack(pady=4)

        # v3.5（⑫）：完整文件浏览器 —— 目录导航条
        nav = ctk.CTkFrame(frame, fg_color="transparent")
        nav.pack(fill="x", padx=30, pady=(4, 2))
        ctk.CTkButton(nav, text="⬆ 上一级", width=90, height=32,
                      command=self._files_up).pack(side="left", padx=4)
        ctk.CTkButton(nav, text="🏠 服务器根目录", width=130, height=32,
                      command=self._files_root).pack(side="left", padx=4)
        self.lbl_files_path = ctk.CTkLabel(
            nav, text="", anchor="w", font=ctk.CTkFont(size=12),
            text_color="#3498db")
        self.lbl_files_path.pack(side="left", padx=10)
        # v3.5（⑤）：世界存档入口（网上找 + 导入 zip）
        ctk.CTkButton(nav, text="🌍 找世界存档", width=120, height=32,
                      command=self._open_world_sites).pack(side="left", padx=4)
        ctk.CTkButton(nav, text="📦 导入存档 zip", width=130, height=32,
                      fg_color="#16a085", hover_color="#138d75",
                      command=self._import_world_zip).pack(side="left", padx=4)
        ctk.CTkButton(nav, text="🎒 玩家背包（只读）", width=150, height=32,
                      fg_color="#2c3e50", hover_color="#34495e",
                      command=self._open_player_inventory).pack(side="left",
                                                               padx=4)
        self.files_cwd = SERVER_DIR

        self.files_frame = ctk.CTkScrollableFrame(frame, width=920, height=420)
        self.files_frame.pack(padx=30, pady=(2, 12), fill="both", expand=True)
        self._fast_scroll(self.files_frame)

        self._refresh_files_tab()

    def _files_section(self, title, items, allow_delete=True,
                       allow_restore=False):
        head = ctk.CTkFrame(self.files_frame, fg_color="transparent")
        head.pack(fill="x", padx=6, pady=(10, 2))
        ctk.CTkLabel(head, text=f"{title}（{len(items)}）",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     anchor="w").pack(side="left", padx=6)
        if not items:
            ctk.CTkLabel(self.files_frame, text="    （空）",
                         font=ctk.CTkFont(size=12), text_color="#888888",
                         anchor="w").pack(fill="x", padx=18)
            return
        for path, display, size in items:
            row = ctk.CTkFrame(self.files_frame, corner_radius=8)
            row.pack(fill="x", padx=6, pady=3)
            ctk.CTkLabel(row, text=display, font=ctk.CTkFont(size=13),
                         anchor="w").pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(row, text=human_size(size), font=ctk.CTkFont(size=12),
                         text_color="#999999").pack(side="left", padx=8)
            if allow_delete:
                ctk.CTkButton(row, text="删除", width=70, height=30,
                              fg_color="#e74c3c", hover_color="#c0392b",
                              command=lambda p=path:
                              self._delete_file(p)).pack(side="right",
                                                         padx=10, pady=5)
            if allow_restore:
                ctk.CTkButton(row, text="恢复", width=70, height=30,
                              fg_color="#3498db", hover_color="#2980b9",
                              command=lambda p=path:
                              self._restore_backup(p)).pack(side="right",
                                                            padx=4, pady=5)

    def _refresh_files_tab(self):
        if not hasattr(self, "files_frame"):
            return
        for w in self.files_frame.winfo_children():
            w.destroy()
        self.lbl_files_hint.configure(
            text=f"当前服务器「{CURRENT_SERVER}」→ {SERVER_DIR}")

        self._files_section(
            "核心 server.jar",
            [(SERVER_JAR, SERVER_JAR.name, SERVER_JAR.stat().st_size)]
            if SERVER_JAR.exists() else [])

        for d, label in ((PLUGINS_DIR, "插件 plugins/"),
                         (MODS_DIR, "模组 mods/")):
            files = sorted([p for p in d.glob("*") if p.is_file()]) \
                if d.exists() else []
            self._files_section(label,
                                [(p, p.name, p.stat().st_size) for p in files])

        world = SERVER_DIR / "world"
        self._files_section("存档 world/",
                            [(world, "world/", dir_size(world))]
                            if world.exists() else [],
                            allow_delete=False)

        backups_dir = SERVER_DIR / "backups"
        backups = sorted([p for p in backups_dir.glob("*.zip")],
                         reverse=True) if backups_dir.exists() else []
        self._files_section("存档备份 backups/",
                            [(p, p.name, p.stat().st_size) for p in backups],
                            allow_delete=True, allow_restore=True)

        # v3.5（⑪）：更新时留下的旧版本，可以一键回滚
        r_idx = self._rollback_index()
        if r_idx:
            rhead = ctk.CTkFrame(self.files_frame, fg_color="transparent")
            rhead.pack(fill="x", padx=6, pady=(10, 2))
            ctk.CTkLabel(rhead, text=f"⏪ 可回滚的旧版本（{len(r_idx)}）",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         anchor="w").pack(side="left", padx=6)
            for ent in r_idx[:20]:
                row = ctk.CTkFrame(self.files_frame, corner_radius=8)
                row.pack(fill="x", padx=6, pady=3)
                ctk.CTkLabel(row,
                             text=f"{ent.get('at', '')}  {ent.get('old', '')}",
                             font=ctk.CTkFont(size=13), anchor="w").pack(
                    side="left", padx=12, pady=8)
                ctk.CTkLabel(row, text=human_size(ent.get("size", 0)),
                             font=ctk.CTkFont(size=12),
                             text_color="#999999").pack(side="left", padx=8)
                ctk.CTkButton(row, text="回滚", width=70, height=30,
                              fg_color="#8e44ad", hover_color="#7d3c98",
                              command=lambda e=ent: self._rollback_plugin(e)
                              ).pack(side="right", padx=10, pady=5)

        self.files_status.configure(
            text=f"该服务器共占用 {human_size(dir_size(SERVER_DIR))}",
            text_color="#2ecc71")

        exports = sorted(EXPORTS_DIR.glob("*.zip"),
                         reverse=True) if EXPORTS_DIR.exists() else []
        self._files_section("导出的 MOD 包 exports/",
                            [(p, p.name, p.stat().st_size) for p in exports])

        # v3.5（⑫）：最后接上"整个服务器目录"的完整文件浏览器
        self.files_browser = ctk.CTkFrame(self.files_frame, fg_color="transparent")
        self.files_browser.pack(fill="x")
        self._refresh_file_browser()

    # ==================== v3.5（⑫）全文件浏览器 ====================
    def _files_up(self):
        cur = Path(self.files_cwd)
        try:
            if cur.resolve() != SERVER_DIR.resolve():
                self.files_cwd = cur.parent
        except Exception:
            self.files_cwd = SERVER_DIR
        self._refresh_files_tab()

    def _files_root(self):
        self.files_cwd = SERVER_DIR
        self._refresh_files_tab()

    def _files_enter(self, path):
        if path.is_dir():
            self.files_cwd = path
            self._refresh_files_tab()

    def _files_open(self, path):
        """用系统默认程序打开（.txt 记事本 / .png 看图 / .jar 什么都不干）。"""
        try:
            os.startfile(str(path))
        except Exception as e:
            messagebox.showerror("打开失败", f"{path.name}: {e}")

    def _files_locate(self, path):
        """在资源管理器里选中这个文件。"""
        try:
            subprocess.Popen(["explorer", "/select," + str(path)])
        except Exception as e:
            messagebox.showerror("定位失败", str(e))

    def _files_rename(self, path):
        dialog = ctk.CTkInputDialog(text=f"把「{path.name}」改名为:", title="重命名")
        new = (dialog.get_input() or "").strip()
        if not new or new == path.name:
            return
        if any(c in new for c in '\\/:*?"<>|'):
            messagebox.showwarning("名字不合法", '文件名里不能有 \\ / : * ? " < > |')
            return
        dst = path.parent / new
        if dst.exists():
            messagebox.showwarning("已存在", f"{new} 已经存在了")
            return
        try:
            path.rename(dst)
            self.files_status.configure(text=f"✏ 已改名为 {new}", text_color="#2ecc71")
        except Exception as e:
            messagebox.showerror("重命名失败", str(e))
        self._refresh_files_tab()

    def _files_delete(self, path):
        """浏览器里的删除：只挪进 .trash，不真删，随时能从资源管理器找回来。"""
        if self.is_running and Path(path) == SERVER_JAR:
            messagebox.showwarning("请先停止", "服务器正在运行，无法删除核心。")
            return
        try:
            if Path(path).resolve() == SERVER_DIR.resolve():
                return
        except Exception:
            return
        is_dir = path.is_dir()
        try:
            size = human_size(dir_size(path) if is_dir else path.stat().st_size)
        except Exception:
            size = "?"
        if not messagebox.askyesno(
                "移到回收站",
                f"把 {path.name}（{size}）移到 .trash 吗？\n"
                f"（不会真的删掉，之后能在资源管理器里找回来）"):
            return
        try:
            trash = SERVER_DIR / ".trash"
            trash.mkdir(exist_ok=True)
            dst = trash / (datetime.now().strftime("%Y%m%d_%H%M%S_") + path.name)
            shutil.move(str(path), str(dst))
            self.files_status.configure(text=f"🗑 {path.name} 已移进 .trash",
                                        text_color="#f39c12")
        except Exception as e:
            messagebox.showerror("移动失败", str(e))
        self._refresh_files_tab()

    def _refresh_file_browser(self):
        frame = getattr(self, "files_browser", None)
        if frame is None:
            return
        # 上一次还没建完就被刷新了 → 先把那条分块任务取消，免得重复建行
        job = getattr(self, "_row_job", None)
        if job is not None:
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._row_job = None
        for w in frame.winfo_children():
            w.destroy()
        # 换服务器/被删掉的目录 → 自动退回服务器根目录（绝不停在别人家的目录里）
        try:
            cwd = Path(self.files_cwd).resolve()
            root = SERVER_DIR.resolve()
            if cwd != root and root not in cwd.parents:
                self.files_cwd = SERVER_DIR
            if not Path(self.files_cwd).is_dir():
                self.files_cwd = SERVER_DIR
        except Exception:
            self.files_cwd = SERVER_DIR
        if hasattr(self, "lbl_files_path"):
            self.lbl_files_path.configure(text=str(self.files_cwd))
        try:
            entries = sorted(Path(self.files_cwd).iterdir(),
                             key=lambda p: (not p.is_dir(), p.name.lower()))
        except Exception as e:
            ctk.CTkLabel(frame, text=f"读不了这个目录: {e}",
                         text_color="#e74c3c").pack(anchor="w", padx=8)
            return
        ctk.CTkLabel(frame, text=f"📁 整个服务器目录（{len(entries)} 项）",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     anchor="w").pack(fill="x", padx=6, pady=(10, 2))
        ctk.CTkLabel(frame, text="    双击不了就点按钮：文件夹「进入」、文本「打开」、"
                                 "删掉的会进 .trash",
                     font=ctk.CTkFont(size=11), text_color="#888888",
                     anchor="w").pack(fill="x", padx=8, pady=(0, 2))
        if not entries:
            ctk.CTkLabel(frame, text="    （空）", font=ctk.CTkFont(size=12),
                         text_color="#888888", anchor="w").pack(fill="x", padx=18)
            return
        rows = entries[:400]
        # v3.5（0-8）：目录里东西多的时候，一次性建几百行会让窗口"假死"。
        # 现在分块建：每帧最多 BROWSER_CHUNK 行，建完一帧就还给事件循环，
        # 用户这时候还能滚动/点按钮；进度用一行小字显示。
        hint = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=11),
                            text_color="#888888", anchor="w")
        state = {"todo": rows, "done": 0}
        if len(rows) > BROWSER_CHUNK:
            hint.configure(text=f"⏳ 正在列出 0/{len(rows)}…")
            hint.pack(fill="x", padx=18)

        def build_chunk():
            self._row_job = None
            if not frame.winfo_exists():
                return                      # 页面被重建了，别往死控件里画
            batch = state["todo"][:BROWSER_CHUNK]
            state["todo"] = state["todo"][BROWSER_CHUNK:]
            for p in batch:
                self._add_browser_row(frame, p)
            state["done"] += len(batch)
            if state["todo"]:
                try:
                    hint.configure(
                        text=f"⏳ 正在列出 {state['done']}/{len(rows)}…")
                except Exception:
                    pass
                self._row_job = self.after(BROWSER_CHUNK_MS, build_chunk)
                return
            try:
                hint.destroy()
            except Exception:
                pass
            if len(entries) > 400:
                ctk.CTkLabel(frame,
                             text=f"    （只列出前 400 项，实际 {len(entries)} 项）",
                             font=ctk.CTkFont(size=11), text_color="#f39c12",
                             anchor="w").pack(fill="x", padx=18)

        build_chunk()

    def _add_browser_row(self, frame, p):
        """文件浏览器里的一行（①图标+名字 ②大小/时间 ③操作按钮）。"""
        isdir = p.is_dir()
        row = ctk.CTkFrame(frame, corner_radius=8)
        row.pack(fill="x", padx=6, pady=2)
        ctk.CTkLabel(row, text=("📁 " if isdir else "📄 ") + p.name
                     + ("/" if isdir else ""),
                     font=ctk.CTkFont(size=13), anchor="w").pack(
            side="left", padx=12, pady=6)
        try:
            size = dir_size(p) if isdir else p.stat().st_size
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%m-%d %H:%M")
        except Exception:
            size, mtime = 0, ""
        ctk.CTkLabel(row, text=f"{human_size(size)}   {mtime}",
                     font=ctk.CTkFont(size=11),
                     text_color="#999999").pack(side="left", padx=8)
        ctk.CTkButton(row, text="删除", width=56, height=26,
                      fg_color="#e74c3c", hover_color="#c0392b",
                      command=lambda q=p: self._files_delete(q)).pack(
            side="right", padx=4, pady=4)
        ctk.CTkButton(row, text="重命名", width=68, height=26,
                      command=lambda q=p: self._files_rename(q)).pack(
            side="right", padx=2)
        ctk.CTkButton(row, text="定位", width=56, height=26,
                      command=lambda q=p: self._files_locate(q)).pack(
            side="right", padx=2)
        if isdir:
            ctk.CTkButton(row, text="进入", width=56, height=26,
                          fg_color="#3498db", hover_color="#2980b9",
                          command=lambda q=p: self._files_enter(q)).pack(
                side="right", padx=2)
        else:
            ctk.CTkButton(row, text="打开", width=56, height=26,
                          fg_color="#2ecc71", hover_color="#27ae60",
                          command=lambda q=p: self._files_open(q)).pack(
                side="right", padx=2)
            if p.suffix.lower() in EDITABLE_EXTS:
                ctk.CTkButton(row, text="编辑", width=56, height=26,
                              fg_color="#9b59b6", hover_color="#8e44ad",
                              command=lambda q=p: self._open_text_editor(q)
                              ).pack(side="right", padx=2)
        return row

    # ==================== v3.5（⑬）内置配置文件编辑器 ====================
    def _text_kind(self, path):
        n = str(path).lower()
        if n.endswith((".yml", ".yaml")):
            return "yaml"
        if n.endswith(".properties"):
            return "props"
        if n.endswith(".json"):
            return "json"
        return "text"

    def _yaml_load(self, text):
        """校验 YAML 语法。pyyaml 是函数内延迟导入的（不拖慢启动）。"""
        try:
            import yaml
        except Exception:
            return "MISSING", None
        try:
            return "OK", yaml.safe_load(text)
        except Exception as e:
            return "ERR", str(e)

    def _validate_text(self, path, text):
        """返回 (能不能保存, 给人看的提示)。YAML/JSON 坏了就坚决不写盘。"""
        kind = self._text_kind(path)
        if kind == "yaml":
            st, info = self._yaml_load(text)
            if st == "MISSING":
                return True, ("⚠ 没装 pyyaml，跳过 YAML 校验"
                              "（点旁边按钮可装）")
            if st == "ERR":
                return False, f"❌ YAML 有错，没保存：{info}"
            return True, "✅ YAML 语法没问题"
        if kind == "json":
            try:
                json.loads(text)
                return True, "✅ JSON 语法没问题"
            except Exception as e:
                return False, f"❌ JSON 有错，没保存：{e}"
        if kind == "props":
            bad = []
            for i, line in enumerate(text.splitlines(), 1):
                s = line.strip()
                if not s or s.startswith(("#", "!")):
                    continue
                if "=" not in s and ":" not in s:
                    bad.append(i)
            if bad:
                return True, (f"⚠ 第 {bad[:5]} 行不是 key=value，"
                              f"Minecraft 可能读不到这一行")
            return True, "✅ properties 格式看起来没问题"
        return True, ""

    def _edit_note(self, msg, color="#2ecc71"):
        try:
            self._edit_status.configure(text=msg, text_color=color)
        except Exception:
            pass

    def _open_text_editor(self, path):
        path = Path(path)
        try:
            if path.stat().st_size > EDIT_MAX_BYTES:
                messagebox.showinfo(
                    "文件太大", "这个文件超过 2 MB，用系统自带编辑器打开吧。")
                self._files_open(path)
                return None
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            messagebox.showerror("打不开", f"{path.name}: {e}")
            return None
        win = ctk.CTkToplevel(self)
        win.title(f"编辑 - {path.name}")
        win.geometry("920x640")
        try:
            win.transient(self)
        except Exception:
            pass
        self._edit_win, self._edit_path, self._edit_orig = win, path, text
        head = ctk.CTkFrame(win, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(10, 2))
        ctk.CTkLabel(head, text=str(path), anchor="w",
                     font=ctk.CTkFont(size=12),
                     text_color="#3498db").pack(side="left")
        self._edit_status = ctk.CTkLabel(head, text="", font=ctk.CTkFont(size=12))
        self._edit_status.pack(side="right", padx=8)
        self._edit_box = ctk.CTkTextbox(win, font=ctk.CTkFont(family="Consolas",
                                                              size=13))
        self._edit_box.pack(fill="both", expand=True, padx=12, pady=4)
        self._edit_box.insert("1.0", text)
        self._edit_box.bind("<KeyRelease>", lambda e: self._edit_touch())
        bar = ctk.CTkFrame(win, fg_color="transparent")
        bar.pack(fill="x", padx=12, pady=(4, 12))
        ctk.CTkButton(bar, text="✅ 校验", width=90,
                      command=self._check_text_editor).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="💾 保存", width=110, fg_color="#2ecc71",
                      hover_color="#27ae60",
                      command=self._save_text_editor).pack(side="left", padx=4)
        ctk.CTkButton(bar, text="↩ 还原", width=90,
                      command=self._reload_text_editor).pack(side="left", padx=4)
        if self._text_kind(path) == "yaml" and self._yaml_load("")[0] == "MISSING":
            ctk.CTkButton(bar, text="⬇ 装 pyyaml（校验用）", width=170,
                          fg_color="#f39c12", hover_color="#d68910",
                          command=lambda: self._install_pkg("pyyaml")).pack(
                side="left", padx=4)
        ctk.CTkLabel(bar, text="保存时会自动留一份 .bak_时间戳",
                     font=ctk.CTkFont(size=11),
                     text_color="#888888").pack(side="right", padx=8)
        ctk.CTkButton(bar, text="❌ 关闭", width=90, fg_color="#7f8c8d",
                      hover_color="#616a6b",
                      command=lambda: win.destroy()).pack(side="right", padx=4)
        self._edit_touch()
        return win

    def _edit_touch(self):
        try:
            t = self._edit_box.get("1.0", "end-1c")
            self._edit_note(
                f"{t.count(chr(10)) + 1} 行 / {len(t)} 字符（还没保存）",
                "#f39c12")
        except Exception:
            pass

    def _check_text_editor(self):
        try:
            ok, msg = self._validate_text(
                self._edit_path, self._edit_box.get("1.0", "end-1c"))
            self._edit_note(msg, "#2ecc71" if ok else "#e74c3c")
            return ok
        except Exception as e:
            self._edit_note(str(e), "#e74c3c")
            return False

    def _save_text_editor(self):
        try:
            t = self._edit_box.get("1.0", "end-1c")
        except Exception:
            return False
        ok, msg = self._validate_text(self._edit_path, t)
        if not ok:
            self._edit_note(msg, "#e74c3c")
            return False
        try:
            p = Path(self._edit_path)
            if self._edit_orig is not None and self._edit_orig != t:
                bak = p.with_name(
                    p.name + datetime.now().strftime(".bak_%Y%m%d_%H%M%S"))
                try:
                    bak.write_text(self._edit_orig, encoding="utf-8")
                except Exception:
                    pass
            p.write_text(t, encoding="utf-8")
            self._edit_orig = t
            self._edit_note("✅ 已保存" + ("" if msg.startswith("✅") else f"（{msg}）"))
            self._set_files_status(f"💾 已保存 {p.name}（旧版留了 .bak）", "#2ecc71")
            self._refresh_files_tab()
            return True
        except Exception as e:
            self._edit_note(f"❌ 保存失败: {e}", "#e74c3c")
            return False

    def _reload_text_editor(self):
        try:
            t = Path(self._edit_path).read_text(encoding="utf-8", errors="replace")
            self._edit_box.delete("1.0", "end")
            self._edit_box.insert("1.0", t)
            self._edit_orig = t
            self._edit_note("↩ 已重新读盘", "#3498db")
        except Exception as e:
            self._edit_note(str(e), "#e74c3c")

    def _install_pkg(self, pkg):
        """后台 pip 安装（给编辑器校验用的 pyyaml 之类）。"""
        tid = self.task_start(f"安装 {pkg}")
        exe = sys.executable.replace("pythonw.exe", "python.exe")

        def task():
            try:
                r = subprocess.run([exe, "-m", "pip", "install", pkg],
                                   capture_output=True, text=True, timeout=600,
                                   **hidden_console_kwargs())
                ok = r.returncode == 0
                self.after(0, lambda: self.task_done(
                    tid, "装好了" if ok else "失败"))
                self.after(0, lambda: self._edit_note(
                    f"✅ {pkg} 装好了，再点「校验」" if ok else f"❌ {pkg} 装失败",
                    "#2ecc71" if ok else "#e74c3c"))
            except Exception as e:
                self.after(0, lambda: self.task_fail(tid, str(e)))

        threading.Thread(target=task, daemon=True).start()

    def _delete_file(self, path):
        if self.is_running and path == SERVER_JAR:
            messagebox.showwarning("请先停止", "服务器正在运行，无法删除核心。")
            return
        is_dir = path.is_dir()
        size = human_size(dir_size(path) if is_dir else path.stat().st_size)
        if not messagebox.askyesno("删除", f"确定删除 {path.name}（{size}）？"):
            return
        try:
            if is_dir:
                shutil.rmtree(path)
            else:
                path.unlink()
        except Exception as e:
            messagebox.showerror("失败", f"删除失败: {e}")
        self._refresh_files_tab()

    def _delete_core(self):
        if not SERVER_JAR.exists():
            messagebox.showinfo("提示", "当前还没有 server.jar")
            return
        if self.is_running:
            messagebox.showwarning("请先停止", "服务器正在运行，无法删除核心。")
            return
        size = human_size(SERVER_JAR.stat().st_size)
        if not messagebox.askyesno(
                "删除核心",
                f"删除 server.jar（{size}）？\n"
                f"插件、模组和存档都不会被删，之后可以重新下载核心。"):
            return
        try:
            SERVER_JAR.unlink()
        except Exception as e:
            messagebox.showerror("失败", f"删除失败: {e}")
        self._refresh_files_tab()

    def _backup_world(self):
        world = SERVER_DIR / "world"
        if not world.exists():
            messagebox.showinfo(
                "提示", "还没有 world 存档目录。\n先启动一次服务器，它才会生成。")
            return
        if self.is_running:
            messagebox.showwarning("请先停止", "服务器正在运行，请先停止再备份。")
            return
        self._backup_busy = True
        tid = self.task_start("备份世界存档")     # v3.5（⑪）：进侧边栏
        threading.Thread(target=self._do_world_backup,
                         args=(tid,), daemon=True).start()

    # ==================== v3.5（⑪）定时自动备份 ====================
    def _do_world_backup(self, tid=None):
        """真正干活的备份（手动和自动都走这里）。自动备份允许服务器在跑。"""
        backups_dir = SERVER_DIR / "backups"
        world = SERVER_DIR / "world"
        try:
            keep = int(self.settings.get("auto_backup_keep", 5) or 5)
        except Exception:
            keep = 5
        msg = ""
        err = ""
        try:
            backups_dir.mkdir(exist_ok=True)
            dst = backups_dir / datetime.now().strftime("world_%Y%m%d_%H%M%S.zip")
            count = 0
            with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
                for p in world.rglob("*"):
                    if p.is_file():
                        zf.write(p, p.relative_to(SERVER_DIR))
                        count += 1
            self._prune_backups(keep)
            msg = (f"✅ 备份完成: {dst.name}｜{count} 个文件｜"
                   f"{human_size(dst.stat().st_size)}")
            done_name = dst.name
        except Exception as e:
            err = f"❌ 备份失败: [{type(e).__name__}] {e}"
            print(err)
        finally:
            self._backup_busy = False
        if tid is not None:
            if err:
                self.after(0, lambda: self.task_fail(tid, err[:60]))
            else:
                self.after(0, lambda: self.task_done(tid, done_name))
        if msg:
            self.after(0, lambda: self._set_files_status(msg, "#2ecc71"))
        if err:
            self.after(0, lambda: self._set_files_status(err, "#e74c3c"))
        self.after(0, self._refresh_files_tab)

    def _prune_backups(self, keep):
        """只留最新的 keep 份 world_*.zip。"""
        try:
            keep = max(1, int(keep))
            zips = sorted((SERVER_DIR / "backups").glob("world_*.zip"),
                          reverse=True)
            for p in zips[keep:]:
                p.unlink()
        except Exception as e:
            print(f"[启动器] 清理旧备份失败: {e}")

    def _auto_backup_tick(self):
        """统一心跳里的自动备份检查：到点就丢后台备份，不挡界面。"""
        try:
            every = int(self.settings.get("auto_backup_min", 0) or 0)
        except Exception:
            every = 0
        if every <= 0 or getattr(self, "_backup_busy", False):
            return
        now = time.monotonic()
        last = getattr(self, "_last_auto_backup", 0.0)
        if last and now - last < every * 60:
            return
        self._last_auto_backup = now
        if not (SERVER_DIR / "world").exists():
            return
        self._backup_busy = True
        tid = self.task_start(f"自动备份世界（每 {every} 分钟）")
        threading.Thread(target=self._do_world_backup,
                         args=(tid,), daemon=True).start()

    # ==================== v3.5（⑪）插件 / 模组版本回滚 ====================
    def _rollback_dir(self):
        return SERVER_DIR / "backups" / "rollback"

    def _rollback_index_path(self):
        return self._rollback_dir() / "index.json"

    def _rollback_index(self):
        p = self._rollback_index_path()
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
            except Exception:
                pass
        return []

    def _save_rollback(self, kind, old_path, new_name):
        """更新前把旧 jar 存一份，并记下它从哪来（回滚用）。后台线程里调用。"""
        try:
            if not old_path.exists():
                return
            d = self._rollback_dir()
            d.mkdir(parents=True, exist_ok=True)
            at = datetime.now().strftime("%Y%m%d_%H%M%S")
            stored = d / f"{kind}_{at}_{old_path.name}"
            shutil.copy2(old_path, stored)
            idx = self._rollback_index()
            idx.insert(0, {"at": at, "kind": kind, "old": old_path.name,
                           "new": new_name, "file": stored.name,
                           "size": stored.stat().st_size})
            self._rollback_index_path().write_text(
                json.dumps(idx[:40], ensure_ascii=False, indent=2),
                encoding="utf-8")
        except Exception as e:
            print(f"[启动器] 存旧版本失败: {e}")

    def _rollback_plugin(self, ent):
        """把存的旧版本拷回 plugins/ 或 mods/。"""
        stored = self._rollback_dir() / str(ent.get("file", ""))
        if not stored.exists():
            messagebox.showwarning("找不到文件", f"旧版本文件已经不在了：\n{stored}")
            return
        kind = str(ent.get("kind", "mods"))
        target_dir = PLUGINS_DIR if kind.startswith("plugin") else MODS_DIR
        old_name = str(ent.get("old") or stored.name)
        if not messagebox.askyesno(
                "回滚版本",
                f"把 {old_name} 恢复到 {target_dir.name}/ 吗？\n"
                f"（现在的新版本 {ent.get('new')} 会被删掉）"):
            return
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(stored, target_dir / old_name)
            new_name = str(ent.get("new") or "")
            if new_name and new_name != old_name:
                np = target_dir / new_name
                if np.exists():
                    np.unlink()
            try:
                inst = load_installed()
                inst.pop(new_name, None)
                save_installed(inst)
            except Exception:
                pass
            self._set_files_status(
                f"⏪ 已回滚到 {old_name}（版本记录下次检查更新会重新识别）",
                "#2ecc71")
        except Exception as e:
            messagebox.showerror("回滚失败", str(e))
        self._refresh_files_tab()

    def _restore_backup(self, zip_path):
        if self.is_running:
            messagebox.showwarning("请先停止", "服务器正在运行，请先停止再恢复。")
            return
        if not messagebox.askyesno(
                "恢复存档",
                f"用「{zip_path.name}」覆盖当前 world 存档？\n"
                f"当前 world 会被替换掉！"):
            return
        tid = self.task_start(f"恢复存档 {zip_path.name}")   # v3.5（0-10）

        def task():
            try:
                world = SERVER_DIR / "world"
                if world.exists():
                    shutil.rmtree(world)
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(SERVER_DIR)
                self.after(0, lambda: self.task_done(tid, zip_path.name))
                msg = f"✅ 已恢复存档: {zip_path.name}"
                self.after(0, lambda: self.files_status.configure(
                    text=msg, text_color="#2ecc71"))
            except Exception as e:
                err = f"❌ 恢复失败: [{type(e).__name__}] {e}"
                print(err)
                self.after(0, lambda t=type(e).__name__: self.task_fail(tid, t))
                self.after(0, lambda: self.files_status.configure(
                    text=err, text_color="#e74c3c"))
            self.after(0, self._refresh_files_tab)

        threading.Thread(target=task, daemon=True).start()

    # ==================== 概览刷新 ====================
    def _refresh_overview(self):
        core = self.launcher_state.get("core")
        version = self.launcher_state.get("version")
        phase = getattr(self, "server_phase", "stopped")

        if core and version:
            self._set_label(self.lbl_core, f"核心: {core.capitalize()}")
            self._set_label(self.lbl_version, f"版本: {version}")
            if phase == "starting":
                self._set_label(
                    self.lbl_hint,
                    "⏳ 正在启动，首次启动要生成世界（约 30~90 秒），请稍候…",
                    "#f39c12")
            elif phase == "running":
                self._set_label(self.lbl_hint, "✅ 服务端已就绪，可以进游戏了",
                                "#2ecc71")
            else:
                self._set_label(self.lbl_hint, "")
        else:
            self._set_label(self.lbl_core, "核心: 未安装")
            self._set_label(self.lbl_version, "版本: -")
            self._set_label(
                self.lbl_hint,
                "💡 还没安装服务端核心，请到「📥 下载核心」页面下载",
                "#f39c12")

        # v3.4：顶部“推荐 Java 版本”横幅
        try:
            _need, _ = recommended_java(version or "")
            _cur = getattr(self, "java_major", None)
            if _need:
                if _cur and _cur >= _need:
                    self._set_label(
                        self.lbl_java_banner,
                        f"推荐 Java 版本：{_need}（当前 Java {_cur} ✅）",
                        "#2ecc71")
                elif _cur:
                    self._set_label(
                        self.lbl_java_banner,
                        f"推荐 Java 版本：{_need}"
                        f"（当前 Java {_cur} ⚠ 偏低，去「🔧 设置」一键装）",
                        "#f39c12")
                else:
                    self._set_label(self.lbl_java_banner,
                                    f"推荐 Java 版本：{_need}", "#f39c12")
            else:
                self._set_label(self.lbl_java_banner, "")
        except Exception:
            pass

        self._set_label(self.lbl_port, f"端口: {self._get_port()}")
        self._set_label(self.lbl_players,
                        f"在线玩家: {len(self.online_players)}")

        if phase == "starting":
            self._set_label(self.lbl_status, "⏳ 启动中…", "#f39c12")
        elif self.is_running:
            self._set_label(self.lbl_status, "● 服务器运行中", "#2ecc71")
        else:
            self._set_label(self.lbl_status, "● 未运行", "gray")

        # v3.5：不再自己排下一次，统一由 _tick 按 TICK_OVERVIEW_MS 调度

    def _get_port(self):
        # v3.5：按 (路径, 修改时间, 大小) 缓存。以前概览每 1.5 秒读一次 properties 文件，
        # 空转时纯属白读盘。文件改了（改端口/换服务器）就自动重读。
        try:
            st = PROPERTIES_FILE.stat()
            key = (str(PROPERTIES_FILE), st.st_mtime_ns, st.st_size)
        except Exception:
            key = None
        if key is not None and getattr(self, "_port_key", None) == key:
            return self._port_val
        port = "25565"
        try:
            for line in PROPERTIES_FILE.read_text(
                    encoding="utf-8").splitlines():
                if line.strip().startswith("server-port="):
                    port = line.split("=", 1)[1].strip()
                    break
        except Exception:
            pass
        if key is not None:
            self._port_key, self._port_val = key, port
        return port

    # ==================== Java 检测 ====================
    def _auto_check_java(self):
        threading.Thread(target=self._check_java, daemon=True).start()

    @staticmethod
    def required_java_for(version):
        """该游戏版本需要哪个 Java（统一走模块级 recommended_java，避免两份表不一致）。"""
        return recommended_java(version)[0]

    def _check_java(self):
        try:
            # v3.2：超时从 10s 放宽到 30s——机器负载高时 java -version 也可能要十几秒
            # v3.3：java 路径可以在「🔧 设置」里改
            java_exe = (self.launcher_state.get("java_path")
                        or self.settings.get("java_path") or "java")
            out = subprocess.check_output(
                [java_exe, "-version"], stderr=subprocess.STDOUT, timeout=30,
                **hidden_console_kwargs()
            ).decode(errors="ignore")
            m = re.search(r'version "(\d+)(?:\.(\d+))?', out)
            if m:
                major = int(m.group(1))
                if major == 1:
                    major = int(m.group(2)) if m.group(2) else 0
                self.java_major = major
                txt = f"Java: 已安装 (Java {major})"
                self.after(0, lambda t=txt: self.lbl_java.configure(
                    text=t, text_color="#2ecc71"))
            else:
                self.after(0, lambda: self.lbl_java.configure(
                    text="Java: 已安装（版本未知）", text_color="orange"))
        except subprocess.TimeoutExpired:
            self.java_major = None
            self.after(0, lambda: self.lbl_java.configure(
                text="Java: 检测超时（系统太忙），点右边「重新检测」再试一次",
                text_color="#f39c12"))
        except FileNotFoundError:
            self.java_major = None
            self.after(0, lambda: self.lbl_java.configure(
                text="Java: ❌ 未检测到 Java（1.20.5+ 需要 Java 21）",
                text_color="#e74c3c"))
        except Exception as e:
            err = f"Java: 检测失败 [{type(e).__name__}] {e}"
            self.after(0, lambda t=err: self.lbl_java.configure(
                text=t, text_color="orange"))

    # ==================== 版本列表刷新 ====================
    def _refresh_version_list(self):
        display = self.core_type.get()
        core = CORE_DISPLAY[display]
        self.core_version.configure(values=["加载中..."])
        self.core_version.set("加载中...")
        self._set_download_status(f"⏳ 正在获取 {display} 的版本列表...",
                                  "#f39c12")

        def task():
            try:
                if core == "vanilla":
                    versions = fetch_vanilla_versions()
                elif core == "paper":
                    versions = fetch_paper_versions()
                elif core == "purpur":
                    versions = fetch_purpur_versions()
                elif core == "fabric":
                    versions = fetch_fabric_versions()
                else:
                    versions = []

                # v2.9：放宽截断，否则 1.13 及更早的版本在界面上选不到
                versions = [str(v) for v in versions][:200]

                def apply():
                    if versions:
                        self.core_version.configure(values=versions)
                        self.core_version.set(versions[0])
                        self._set_download_status(
                            f"✅ 已加载 {len(versions)} 个版本，可直接下载",
                            "#2ecc71")
                    else:
                        self.core_version.configure(values=["无可用版本"])
                        self.core_version.set("无可用版本")
                        self._set_download_status("⚠ 该核心没有可用版本",
                                                  "#f39c12")

                self.after(0, apply)
            except Exception as e:
                err_text = (f"❌ 版本列表获取失败: "
                            f"[{type(e).__name__}] {e}")
                print(err_text)
                self.after(0, lambda t=err_text: self._set_download_status(
                    t, "#e74c3c"))
                self.after(0, lambda: self.core_version.configure(
                    values=["获取失败"]))
                self.after(0, lambda: self.core_version.set("获取失败"))

        threading.Thread(target=task, daemon=True).start()

    # ==================== 下载核心 ====================
    def _download_core(self):
        display = self.core_type.get()
        core = CORE_DISPLAY[display]
        version = self.core_version.get()

        if version in ("加载中...", "获取失败", "无可用版本", ""):
            messagebox.showwarning("提示", "请等待版本列表加载完成")
            return

        # v3.5.17：默认新建服务器；只有明确选中已有服务器，才会覆盖它的核心
        sel = self.core_target.get()
        is_new = (sel == CORE_TARGET_NEW)
        if is_new:
            target_name = unique_server_name(f"{core}-{version}")
            target_dir = SERVERS_ROOT / target_name
        else:
            target_name = sel
            target_dir = server_path(sel)
            if not target_dir.exists():
                messagebox.showerror(
                    "找不到服务器", f"「{sel}」的目录不存在了:\n{target_dir}")
                return
            if (target_dir / "server.jar").exists():
                state = self._read_server_state(target_dir)
                old = (f"{state.get('core') or '未知核心'} "
                       f"{state.get('version') or ''}").strip()
                now = "（这是当前服务器）" if sel == CURRENT_SERVER else ""
                if not messagebox.askyesno(
                        "确认换核心",
                        f"把「{sel}」的核心换成 {core} {version}？{now}\n\n"
                        f"现在的核心: {old}\n"
                        f"会覆盖它的 server.jar，旧核心存成 server.jar.bak；\n"
                        f"存档 / 插件 / 配置都不受影响。\n\n继续吗？"):
                    return

        self.btn_download.configure(state="disabled", text="下载中")
        self.download_progress.set(0)
        self._set_download_status(
            (f"正在为新服务器「{target_name}」解析下载地址..."
             if is_new else f"正在为「{target_name}」解析下载地址..."),
            "#f39c12")
        _tid = self.task_start(f"下载核心 {core} {version}")   # v3.4：进侧边栏

        def task():
            try:
                if core == "vanilla":
                    url = get_vanilla_url(version)
                elif core == "paper":
                    url = get_paper_url(version)
                elif core == "purpur":
                    url = get_purpur_url(version)
                elif core == "fabric":
                    url = get_fabric_url(version)
                else:
                    raise RuntimeError("未知核心类型")

                # 新服务器：先建目录并登记，失败了也能在列表里看到它（下次续传）
                if is_new:
                    (target_dir / "plugins").mkdir(parents=True, exist_ok=True)
                    (target_dir / "mods").mkdir(parents=True, exist_ok=True)
                    register_server(target_name, target_dir)
                    self.after(0, self._refresh_servers_tab)

                self._set_download_status(
                    f"正在下载 {core} {version} → 「{target_name}」...",
                    "#f39c12")

                jar = target_dir / "server.jar"
                tmp = target_dir / "server.jar.tmp"

                # v3.1：换了核心/版本/目标就不能拿旧的半成品续传，否则会拼坏 jar
                dl_key = f"{target_name}|{core}-{version}"
                if getattr(self, "_dl_key", None) != dl_key and tmp.exists():
                    try:
                        tmp.unlink()
                    except OSError:
                        pass
                self._dl_key = dl_key

                def on_progress(done, total):
                    pct = done / total if total else 0
                    mb_done = done / 1024 / 1024
                    mb_total = total / 1024 / 1024
                    self.task_update(_tid, f"{mb_done:.1f} / {mb_total:.1f} MB",
                                     pct)
                    self.after(0,
                               lambda p=pct: self.download_progress.set(p))
                    self._set_download_status(
                        f"下载中... {mb_done:.1f} / {mb_total:.1f} MB "
                        f"({pct * 100:.1f}%)", "#f39c12"
                    )

                http_download(url, tmp, on_progress,
                              cancel_check=lambda: self._task_cancel_check(_tid))

                # 换核心是用户明确选的：旧核心留个 .bak，比直接删稳
                if jar.exists():
                    try:
                        jar.replace(jar.with_name(jar.name + ".bak"))
                    except OSError:
                        pass
                tmp.replace(jar)

                self._write_server_state(target_dir, core, version)
                try:
                    is_current = (Path(target_dir).resolve()
                                  == Path(SERVER_DIR).resolve())
                except Exception:
                    is_current = False
                if is_current:
                    self.launcher_state.update({"core": core,
                                                "version": version})
                    self._save_state()

                self.after(0, self._refresh_files_tab)
                self.after(0, self._refresh_servers_tab)
                self.after(0, lambda: self.download_progress.set(1.0))

                def finish():
                    self.task_done(_tid, f"{core} {version} 下载完成")
                    if is_new:
                        if self.is_running:
                            self._set_download_status(
                                f"✅ 新服务器「{target_name}」已装好 "
                                f"{core} {version}；服务器正在运行，"
                                f"停服后去「🖥 服务器」页切过去", "#2ecc71")
                        else:
                            self._switch_server(target_name)
                            self._set_download_status(
                                f"✅ 新服务器「{target_name}」已建好并装上 "
                                f"{core} {version}，已自动切换过去，"
                                f"回概览即可启动", "#2ecc71")
                    else:
                        self._refresh_overview()
                        self._set_download_status(
                            f"✅ 「{target_name}」的核心已换成 {core} {version}"
                            f"（旧核心存为 server.jar.bak）", "#2ecc71")

                self.after(0, finish)
            except TaskCancelled:
                # 新建的服务器如果取消下载：别留个空壳在列表里
                if is_new:
                    def cleanup():
                        try:
                            if not (target_dir / "server.jar").exists():
                                unregister_server(target_name)
                                for sub in ("plugins", "mods"):
                                    try:
                                        (target_dir / sub).rmdir()
                                    except OSError:
                                        pass
                                try:
                                    (target_dir / "server.jar.tmp").unlink()
                                except OSError:
                                    pass
                                try:
                                    target_dir.rmdir()
                                except OSError:
                                    pass
                                self._refresh_servers_tab()
                                self._set_download_status(
                                    "已取消：新服务器没有留下", "#f39c12")
                        except Exception:
                            pass
                    self.after(0, cleanup)
                return                      # 用户点了 ✕，不算失败
            except Exception as e:
                err_text = f"❌ 下载失败: [{type(e).__name__}] {e}"
                print(err_text)
                self.task_fail(_tid, f"{type(e).__name__}: {e}")
                self._set_download_status(err_text, "#e74c3c")
                # v3.1：失败必须到处都看得见——控制台 + 弹窗。
                self.after(0, lambda t=err_text: self._append_console(
                    f"\n[启动器] {t}\n"
                    f"[启动器] 再点一次下载会从断点继续，不用重下。\n"))
                self.after(0, lambda t=err_text: messagebox.showerror(
                    "核心下载失败", f"{t}\n\n再点一次下载会断点续传。"))
            finally:
                def restore():
                    self.btn_download.configure(state="normal")
                    self._on_core_target_change()
                self.after(0, restore)

        threading.Thread(target=task, daemon=True).start()

    # ==================== 核心一键更新（v3.3） ====================
    def _check_core_update(self):
        # v3.5.17：检查/更新也认「目标服务器」，不是永远对着当前服务器
        sel = self.core_target.get()
        if sel == CORE_TARGET_NEW:
            messagebox.showinfo(
                "提示", "「新建服务器」还没有旧核心可更新。\n"
                        "先选一个已有服务器，或直接点下载新建一个。")
            return
        target_name = sel
        target_dir = server_path(target_name)
        target_jar = target_dir / "server.jar"
        state = self._read_server_state(target_dir)
        core = state.get("core")
        version = state.get("version")
        if not core or not version or not target_jar.exists():
            messagebox.showinfo(
                "提示", f"「{target_name}」还没装核心，先在下面下载一个吧")
            return
        self._set_download_status("⏳ 正在比对核心版本…", "#f39c12")
        tid = self.task_start(f"检查「{target_name}」核心更新")

        def task():
            try:
                st = core_update_status(core, version, target_jar)
            except Exception as e:
                err = f"❌ 检查核心更新失败: {type(e).__name__}: {e}"
                print(err)
                self.after(0, lambda t=type(e).__name__: self.task_fail(tid, t))
                self.after(0, lambda: self._set_download_status(
                    err, "#e74c3c"))
                return
            self.after(0, lambda s=st: self.task_done(
                tid, "已是最新" if s.get("up_to_date") else "发现新构建"))

            def show():
                head = (f"目标服务器: {target_name}\n"
                        f"当前核心: {core} {version}\n"
                        f"远端最新: {st['note']}\n\n")
                if st["up_to_date"]:
                    self._set_download_status("✅ 核心已是最新构建", "#2ecc71")
                    messagebox.showinfo("核心更新", head + "已经是最新构建 ✅")
                    return
                if st["local_hash"] and st["hash"]:
                    detail = (f"本地 {st['algo']}: {st['local_hash'][:16]}…\n"
                              f"远端 {st['algo']}: {str(st['hash'])[:16]}…\n"
                              f"→ 远端有更新的构建")
                else:
                    detail = "该核心没提供校验值，无法比对，将直接重新下载最新构建"
                if messagebox.askyesno(
                        "发现核心更新",
                        head + detail + "\n\n现在更新吗？\n"
                        "（下载最新构建覆盖它的 server.jar；"
                        "存档/插件/配置都不受影响，旧核心会存成 server.jar.bak）"):
                    self._do_core_update(st["url"], core, version, target_name)

            self.after(0, show)

        threading.Thread(target=task, daemon=True).start()

    def _do_core_update(self, url, core, version, target_name=None):
        target_name = target_name or CURRENT_SERVER
        target_dir = server_path(target_name)
        target_jar = target_dir / "server.jar"
        self.btn_download.configure(state="disabled")
        self.download_progress.set(0)
        self._set_download_status(
            f"正在为「{target_name}」下载 {core} {version} 最新构建…",
            "#f39c12")
        _tid = self.task_start(f"更新核心 {core} {version}")   # v3.4：进侧边栏

        def task():
            try:
                tmp = target_jar.with_suffix(".jar.tmp")
                if tmp.exists():
                    tmp.unlink()

                def on_progress(done, total):
                    pct = done / total if total else 0
                    self.task_update(
                        _tid, f"{done / 1048576:.1f} / {total / 1048576:.1f} MB",
                        pct)
                    self.after(0, lambda p=pct: self.download_progress.set(p))
                    self._set_download_status(
                        f"更新核心中… {done / 1048576:.1f}/"
                        f"{total / 1048576:.1f} MB ({pct * 100:.1f}%)",
                        "#f39c12")

                http_download(url, tmp, on_progress,
                              cancel_check=lambda: self._task_cancel_check(_tid))
                target_jar.replace(target_jar.with_name(
                    target_jar.name + ".bak"))
                tmp.replace(target_jar)
                self._write_server_state(target_dir, core, version)
                self.task_done(_tid, f"「{target_name}」核心已更新到最新构建")
                self._set_download_status(
                    f"✅ 「{target_name}」的核心已更新到最新构建"
                    f"（旧核心存为 server.jar.bak）", "#2ecc71")
                self.after(0, self._refresh_files_tab)
            except TaskCancelled:
                return                      # 用户点了 ✕，不算失败
            except Exception as e:
                err = f"❌ 核心更新失败: [{type(e).__name__}] {e}"
                print(err)
                self.task_fail(_tid, f"{type(e).__name__}: {e}")
                self._set_download_status(err, "#e74c3c")
                self.after(0, lambda t=err: messagebox.showerror(
                    "核心更新失败", f"{t}\n\n可以重试，会从断点继续。"))
            finally:
                def restore():
                    self.btn_download.configure(state="normal")
                    self._on_core_target_change()
                self.after(0, restore)

        threading.Thread(target=task, daemon=True).start()

    def _auto_update_core(self):
        core = self.launcher_state.get("core")
        version = self.launcher_state.get("version")
        if not core or not version or not SERVER_JAR.exists():
            return
        try:
            st = core_update_status(core, version, SERVER_JAR)
            if st["up_to_date"] or not st.get("url"):
                return
            self.after(0, lambda: self._append_console(
                f"[启动器] 自动更新核心：{st['note']}\n"))
            tmp = SERVER_JAR.with_suffix(".jar.tmp")
            if tmp.exists():
                tmp.unlink()
            http_download(st["url"], tmp)
            SERVER_JAR.replace(SERVER_JAR.with_suffix(".jar.bak"))
            tmp.replace(SERVER_JAR)
            self.after(0, lambda: self._append_console(
                "[启动器] 核心已自动更新到最新构建\n"))
            self.after(0, self._refresh_files_tab)
        except Exception as e:
            print(f"[启动器] 自动更新核心失败: {e}")

    def _set_download_status(self, text, color):
        self.after(0, lambda t=text, c=color:
                   self.lbl_download_status.configure(text=t, text_color=c))

    # ==================== 翻页按钮状态 ====================
    def _update_pagination_buttons(self, loading=False):
        def ui():
            if loading:
                self.btn_prev.configure(state="disabled")
                self.btn_next.configure(state="disabled")
                self.lbl_page.configure(text="加载中...")
                return

            max_offset = MODRINTH_MAX_OFFSET
            if self.total_hits <= 0:
                total_pages = 1
            else:
                total_pages = (self.total_hits + PAGE_SIZE - 1) // PAGE_SIZE
                max_page_by_offset = max_offset // PAGE_SIZE
                total_pages = min(total_pages, max_page_by_offset)

            total_pages = max(1, total_pages)

            self.lbl_page.configure(
                text=f"第 {self.current_page + 1} / {total_pages} 页"
            )

            if self.current_page <= 0:
                self.btn_prev.configure(state="disabled")
            else:
                self.btn_prev.configure(state="normal")

            if self.current_page >= total_pages - 1:
                self.btn_next.configure(state="disabled")
            else:
                self.btn_next.configure(state="normal")

            if self.total_hits > 0:
                self.lbl_total.configure(
                    text=f"共 {self.total_hits} 条结果")
            else:
                self.lbl_total.configure(text="")

        self.after(0, ui)

    # ==================== Modrinth 搜索 / 热门列表 ====================
    def _search_modrinth(self, page=0):
        if not hasattr(self, "search_entry"):
            return                     # v3.3：该页还没建（懒加载）
        query = self.search_entry.get().strip()
        _sel = self.modrinth_type.get()
        if "数据包" in _sel:
            project_type, is_plugin = "datapack", False
        elif "插件" in _sel:
            project_type, is_plugin = "plugin", True
        else:
            project_type, is_plugin = "mod", False
        kind_cn = {"plugin": "插件", "mod": "模组",
                   "datapack": "数据包"}[project_type]

        # v3.5（⑱）：切到 Hangar 就整个交给 Hangar 那条路（只有插件）
        _src = (self.source_menu.get()
                if hasattr(self, "source_menu") else "Modrinth")
        if str(_src).startswith("Hangar") and project_type == "plugin":
            return self._search_hangar(page)

        if query != self.last_query or \
                project_type != self.last_project_type:
            page = 0
            self.last_query = query
            self.last_project_type = project_type

        if page < 0:
            page = 0

        self.current_page = page

        if query:
            self._set_search_status(f"🔍 正在搜索「{query}」...", "#f39c12")
        else:
            self._set_search_status(f"⏳ 正在加载热门{kind_cn}...", "#f39c12")

        # v3.4：翻页/重新搜索 → 作废旧代号的封面任务，别让旧图继续下完
        self._img_gen = getattr(self, "_img_gen", 0) + 1
        self._img_pending = []
        _q = getattr(self, "_img_queue", None)
        if _q is not None:
            try:
                while True:
                    _q.get_nowait()
            except Exception:
                pass
        for w in self.results_frame.winfo_children():
            w.destroy()

        self._update_pagination_buttons(loading=True)

        server_version = self.launcher_state.get("version")
        core = self.launcher_state.get("core")
        loader = CORE_LOADER_MAP.get(core) if is_plugin else core

        # v3.3：筛选条件（版本 / 加载器 / 排序 / 只看适配）
        f_ver = f_loader = None
        index = "downloads"
        try:
            if self.filter_adapt.get():
                f_ver = self.filter_version.get().strip() or server_version
                f_loader = (None if self.filter_loader.get() == "自动"
                            else self.filter_loader.get()) or loader
            else:
                f_ver = self.filter_version.get().strip() or None
                f_loader = (None if self.filter_loader.get() == "自动"
                            else self.filter_loader.get())
            index = {"下载量": "downloads", "最近更新": "updated",
                     "最新发布": "newest",
                     "相关度": "relevance"}.get(self.filter_sort.get(),
                                                "downloads")
        except Exception:
            f_ver, f_loader, index = server_version, loader, "downloads"

        if project_type == "datapack":
            f_loader = None      # v3.5（⑤）：数据包没有"加载器"这一说

        def task():
            try:
                strict = [[f"project_type:{project_type}"]]
                if f_loader:
                    strict.append([f"categories:{f_loader}"])
                if f_ver:
                    strict.append([f"versions:{f_ver}"])
                candidates = []
                if len(strict) > 1:
                    candidates.append(strict)          # 版本+加载器都卡
                if f_loader:
                    candidates.append([[f"project_type:{project_type}"],
                                       [f"categories:{f_loader}"]])
                elif f_ver:
                    candidates.append([[f"project_type:{project_type}"],
                                       [f"versions:{f_ver}"]])
                candidates.append([[f"project_type:{project_type}"]])
                candidates.append(None)

                offset = page * PAGE_SIZE
                hits = []
                total_hits = 0
                used_facets_desc = ""

                for i, facets in enumerate(candidates):
                    params = {
                        "limit": PAGE_SIZE,
                        "offset": offset,
                        "index": index,
                    }
                    if facets:
                        params["facets"] = json.dumps(facets)
                    if query:
                        params["query"] = query

                    url = (f"{MODRINTH_API}/search?"
                           + urllib.parse.urlencode(params))
                    data = http_get_json(url)
                    hits = data.get("hits", [])
                    total_hits = data.get("total_hits", len(hits))

                    if hits:
                        descs = ["严格", "宽松", "无过滤"]
                        used_facets_desc = (
                            descs[i] if i < len(descs)
                            else f"级别{i + 1}"
                        )
                        break

                if not hits and page > 0:
                    max_page = max(
                        0, (total_hits + PAGE_SIZE - 1) // PAGE_SIZE - 1)
                    if max_page < page:
                        self.after(
                            0,
                            lambda: self._search_modrinth(page=max_page)
                        )
                        return

                def render():
                    self.total_hits = total_hits

                    if not hits:
                        self._set_search_status(
                            "没有找到相关结果", "#f39c12")
                        self._update_pagination_buttons()
                        return

                    label = "搜索结果" if query else "热门推荐"
                    extra = (f"｜匹配：{used_facets_desc}"
                             if used_facets_desc else "")
                    self._set_search_status(
                        f"✅ {label}｜第 {page + 1} 页｜共 {total_hits} 条"
                        + extra,
                        "#2ecc71"
                    )
                    for project in hits:
                        self._add_result_row(project, project_type)

                    self._update_pagination_buttons()

                    try:
                        self.results_frame._parent_canvas.yview_moveto(0)
                    except Exception:
                        pass

                self.after(0, render)

            except Exception as e:
                err_text = f"❌ 加载失败: [{type(e).__name__}] {e}"
                print(err_text)
                self.after(0, lambda t=err_text:
                           self._set_search_status(t, "#e74c3c"))
                self.after(0, lambda: self._update_pagination_buttons())

        threading.Thread(target=task, daemon=True).start()

    def _set_search_status(self, text, color):
        self.after(0, lambda t=text, c=color:
                   self.search_status.configure(text=t, text_color=c))

    # ==================== 工具：头像 & 封面 ====================
    def _make_avatar(self, label, name, slug, size):
        initial = (name[:1] or "?").upper()
        # v2.9 修复：hash() 每次运行都不同（PYTHONHASHSEED 随机），头像颜色会乱变
        seed = sum((i + 1) * ord(ch) for i, ch in enumerate(slug or name))
        bg = AVATAR_PALETTE[seed % len(AVATAR_PALETTE)]
        font_size = max(14, int(size * 0.42))
        label.configure(
            text=initial,
            font=ctk.CTkFont(size=font_size, weight="bold"),
            fg_color=bg, corner_radius=int(size * 0.18),
            text_color="white", width=size, height=size
        )

    def _try_apply_image(self, label, url, name, size):
        if not url or not HAS_PIL:
            return
        self._start_img_workers()
        item = (label, url, name, size, getattr(self, "_img_gen", 0))
        if self._is_visible(label):
            self._img_queue.put(item)
        else:
            self._img_pending.append(item)      # v3.4：滚到可见再加载，不抢资源

    def _add_result_row(self, project, project_type):
        # v3.0：行内控件扁平化——去掉两层嵌套 CTkFrame，改用 grid 直接排布。
        # Tk 控件数大幅下降，滚动时每帧的重绘量随之下降。
        row = ctk.CTkFrame(self.results_frame, corner_radius=10)
        row.pack(fill="x", padx=6, pady=5)
        row.grid_columnconfigure(1, weight=1)

        title = project.get("title", "Unknown")
        slug = project.get("slug") or project.get("project_id") or title

        icon_label = ctk.CTkLabel(row, text="", width=64, height=64)
        icon_label.grid(row=0, column=0, rowspan=3, padx=(14, 12), pady=10,
                        sticky="n")
        self._make_avatar(icon_label, title, slug, 64)
        self._try_apply_image(icon_label, project.get("icon_url"),
                              title, 64)

        title_label = ctk.CTkLabel(
            row, text=title,
            font=ctk.CTkFont(size=15, weight="bold"), anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="ew", pady=(10, 0))

        desc = project.get("description", "")[:130]
        desc_label = ctk.CTkLabel(
            row, text=desc, font=ctk.CTkFont(size=12),
            text_color="#bbbbbb", anchor="w",
            wraplength=560, justify="left"
        )
        desc_label.grid(row=1, column=1, sticky="ew", pady=2)

        downloads = project.get("downloads", 0)
        versions = project.get("versions", [])
        ver_str = versions[-1] if versions else "-"
        meta_label = ctk.CTkLabel(
            row,
            text=f"⬇ {downloads:,}    最新版本: {ver_str}",
            font=ctk.CTkFont(size=11), text_color="#888888", anchor="w"
        )
        meta_label.grid(row=2, column=1, sticky="ew", pady=(0, 10))

        ctk.CTkButton(
            row, text="⚡ 快速安装", width=110, height=34,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2ecc71", hover_color="#27ae60",
            command=lambda p=project, t=project_type:
                self._install_project(p, t)
        ).grid(row=0, column=2, padx=(10, 14), pady=(10, 2))

        ctk.CTkButton(
            row, text="📋 选择版本", width=110, height=34,
            font=ctk.CTkFont(size=13),
            fg_color="#3498db", hover_color="#2980b9",
            command=lambda p=project, t=project_type:
                self._open_version_dialog(p, t)
        ).grid(row=1, column=2, padx=(10, 14), pady=(2, 10))

        callback = lambda p=project, t=project_type: self._open_version_dialog(p, t)
        for w in (row, icon_label, title_label, desc_label, meta_label):
            w.bind("<Button-1>", lambda e, cb=callback: cb())

    # ==================== 版本选择对话框 ====================
    def _open_version_dialog(self, project, project_type):
        slug = project.get("slug") or project.get("project_id")
        title = project.get("title", slug)
        kind = {"plugin": "插件", "mod": "模组",
                "datapack": "数据包"}.get(project_type, "模组")

        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{title} - 选择版本")
        dialog.geometry("880x660")
        dialog.transient(self)
        dialog.after(120, dialog.lift)
        dialog.after(200, dialog.focus_force)

        header = ctk.CTkFrame(dialog, fg_color="transparent")
        header.pack(fill="x", padx=22, pady=(20, 10))

        dialog_icon = ctk.CTkLabel(header, text="", width=84, height=84)
        dialog_icon.pack(side="left", padx=(0, 18))

        self._make_avatar(dialog_icon, title, slug or title, 84)
        self._try_apply_image(dialog_icon, project.get("icon_url"),
                              title, 84)

        info = ctk.CTkFrame(header, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(info, text=title,
                     font=ctk.CTkFont(size=20, weight="bold"),
                     anchor="w").pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=(f"类型: {kind}    "
                  f"下载总量: {project.get('downloads', 0):,}"),
            font=ctk.CTkFont(size=12), text_color="#a0a0a0",
            anchor="w"
        ).pack(anchor="w", pady=2)

        desc = project.get("description", "")
        ctk.CTkLabel(info, text=desc, font=ctk.CTkFont(size=12),
                     text_color="#bbbbbb", anchor="w",
                     wraplength=620,
                     justify="left").pack(anchor="w", pady=(4, 0))

        status_lbl = ctk.CTkLabel(
            dialog, text="⏳ 正在加载版本列表...",
            font=ctk.CTkFont(size=13), text_color="#f39c12"
        )
        status_lbl.pack(pady=8)

        scroll = ctk.CTkScrollableFrame(dialog, width=820, height=440)
        scroll.pack(padx=20, pady=8, fill="both", expand=True)
        self._fast_scroll(scroll)

        def task():
            try:
                versions = http_get_json(
                    f"{MODRINTH_API}/project/{slug}/version")
                if not versions:
                    self.after(0, lambda: status_lbl.configure(
                        text="❌ 该项目没有可用版本",
                        text_color="#e74c3c"))
                    return

                type_order = {"release": 0, "beta": 1, "alpha": 2}

                def sort_key(v):
                    return (
                        type_order.get(
                            v.get("version_type", "release"), 9),
                        -self._date_to_int(v.get("date_published", ""))
                    )

                versions_sorted = sorted(versions, key=sort_key)

                def render():
                    status_lbl.configure(
                        text=(f"✅ 共 {len(versions_sorted)} 个版本，"
                              f"选择合适的一项下载"),
                        text_color="#2ecc71"
                    )
                    for v in versions_sorted[:60]:
                        self._add_version_row(
                            scroll, v, project_type, status_lbl, slug)

                self.after(0, render)
            except Exception as e:
                err = f"❌ 加载失败: [{type(e).__name__}] {e}"
                print(err)
                self.after(0, lambda: status_lbl.configure(
                    text=err, text_color="#e74c3c"))

        threading.Thread(target=task, daemon=True).start()

    def _date_to_int(self, date_str):
        try:
            return int(re.sub(r"\D", "", date_str)[:14] or "0")
        except Exception:
            return 0

    def _add_version_row(self, parent, ver, project_type, status_lbl,
                         slug=None):
        # v3.0：和搜索结果行一样做扁平化——去掉 left / title_row 两层嵌套 CTkFrame。
        # 版本列表最多 60 行，控件少了滚动才不卡。
        row = ctk.CTkFrame(parent, corner_radius=8)
        row.pack(fill="x", padx=4, pady=3)
        row.grid_columnconfigure(2, weight=1)

        ver_num = ver.get("version_number", "?")
        vtype = ver.get("version_type", "release")
        type_color = {
            "release": "#2ecc71",
            "beta": "#f39c12",
            "alpha": "#e74c3c"
        }.get(vtype, "#888888")

        ctk.CTkLabel(row, text=ver_num,
                     font=ctk.CTkFont(size=14,
                                       weight="bold")).grid(
            row=0, column=0, sticky="w", padx=(12, 4), pady=(8, 0))
        ctk.CTkLabel(row, text=f"[{vtype}]",
                     font=ctk.CTkFont(size=11),
                     text_color=type_color).grid(
            row=0, column=1, sticky="w", padx=(0, 8), pady=(8, 0))

        game_vers = ", ".join(ver.get("game_versions", [])[:8])
        loaders = ", ".join(ver.get("loaders", []))
        date = ver.get("date_published", "")[:10]
        ctk.CTkLabel(
            row,
            text=(f"游戏版本: {game_vers}    "
                  f"加载器: {loaders}    发布: {date}"),
            font=ctk.CTkFont(size=11), text_color="#999999", anchor="w"
        ).grid(row=1, column=0, columnspan=3, sticky="ew",
               padx=(12, 6), pady=(2, 8))

        files = ver.get("files", [])
        if not files:
            ctk.CTkLabel(row, text="无文件",
                         text_color="gray").grid(row=0, column=3, rowspan=2,
                                                 padx=14)
            return

        primary = next(
            (f for f in files if f.get("primary")), files[0])

        def do_download(p=primary):
            tid = self.task_start(f"下载 {p['filename']}")   # v3.4：进侧边栏
            try:
                target_dir, dir_label = self._target_dir_for(project_type)
                if project_type == "datapack" and not self._datapack_ready():
                    self.task_fail(tid, "还没有 world 存档")
                    self.after(0, lambda: status_lbl.configure(
                        text="⚠ 还没有 world 存档，先启动一次服务器",
                        text_color="#f39c12"))
                    return
                target_dir.mkdir(parents=True, exist_ok=True)
                target = target_dir / p["filename"]

                self.after(0, lambda: status_lbl.configure(
                    text=f"⏳ 正在下载 {p['filename']} ...",
                    text_color="#f39c12"))

                http_download(p["url"], target,
                              cancel_check=lambda: self._task_cancel_check(tid))

                self._record_install(target_dir.name, p["filename"], slug,
                                     ver.get("version_number"), ver.get("id"))
                self.task_done(tid, f"{p['filename']} → {dir_label}/")
                self.after(0, self._refresh_files_tab)
                self.after(0, lambda: status_lbl.configure(
                    text=(f"✅ {p['filename']} "
                          f"已安装到 {dir_label}/"),
                    text_color="#2ecc71"))
            except TaskCancelled:
                return                      # 用户点了 ✕
            except Exception as e:
                err = f"❌ 下载失败: [{type(e).__name__}] {e}"
                print(err)
                self.task_fail(tid, f"{type(e).__name__}: {e}")
                self.after(0, lambda: status_lbl.configure(
                    text=err, text_color="#e74c3c"))

        ctk.CTkButton(
            row, text="⬇ 下载", width=90, height=34,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3498db", hover_color="#2980b9",
            command=lambda: threading.Thread(
                target=do_download, daemon=True).start()
        ).grid(row=0, column=3, rowspan=2, padx=14)

    # ==================== 快速安装 ====================
    # ==================== v3.5（⑤）世界存档入口 ====================
    WORLD_SITES = (
        ("Planet Minecraft（存档最多，英文）",
         "https://www.planetminecraft.com/projects/?project_categories=worlds"),
        ("CurseForge 世界（英文）",
         "https://www.curseforge.com/minecraft/worlds"),
        ("MC 百科 · 地图分享（中文）",
         "https://www.mcmod.cn/class/?mcmod_category=map"),
    )

    def _open_url(self, url):
        try:
            os.startfile(url)          # Windows：交给默认浏览器
        except Exception:
            try:
                import webbrowser
                webbrowser.open(url)
            except Exception as e:
                print(f"[启动器] 打开网址失败: {e}")

    def _open_world_sites(self):
        """网上下载存档的地方（下载完回来点「导入存档 zip」）。"""
        win = ctk.CTkToplevel(self)
        win.title("去哪里找世界存档")
        win.geometry("660x320")
        try:
            win.transient(self)
        except Exception:
            pass
        ctk.CTkLabel(
            win, anchor="w", justify="left", wraplength=620,
            font=ctk.CTkFont(size=13),
            text=("在下面任意一个站里下载一个存档 zip → 回到文件页点「📦 导入存档 zip」。\n"
                  "⚠ 存档要和你服务端版本接近：太新的存档，旧版本服务端打不开。")
        ).pack(fill="x", padx=16, pady=(14, 8))
        for name, url in self.WORLD_SITES:
            ctk.CTkButton(win, text=f"🌍 {name}", width=580, height=34,
                          command=lambda u=url: self._open_url(u)).pack(pady=4)
        ctk.CTkButton(win, text="关闭", width=90, fg_color="#7f8c8d",
                      hover_color="#616a6b",
                      command=win.destroy).pack(pady=(10, 12))
        return win

    def _import_world_zip(self):
        """把下载来的存档 zip 导入成这个服务器的 world/（旧的挪进 .trash）。"""
        p = filedialog.askopenfilename(title="选一个存档压缩包（.zip）",
                                       filetypes=[("zip 压缩包", "*.zip")])
        if not p:
            return
        src = Path(p)
        has_world = (SERVER_DIR / "world").exists()
        if not messagebox.askyesno(
                "导入存档",
                f"要把「{src.name}」作为这个世界存档的 world/ 吗？\n"
                + ("（当前 world/ 会先挪进 .trash，不真删）\n" if has_world else "")
                + "导入完请重启服务器，让它加载新世界。"):
            return
        tid = self.task_start(f"导入存档 {src.name}")

        def task():
            tmp = SERVER_DIR / "_world_import_tmp"
            msg = ""
            try:
                shutil.rmtree(tmp, ignore_errors=True)
                with zipfile.ZipFile(src) as zf:
                    zf.extractall(tmp)
                level = next((q for q in Path(tmp).rglob("level.dat")), None)
                if level is None:
                    raise RuntimeError("这个 zip 里没有 level.dat，不像存档")
                srcdir = level.parent
                world = SERVER_DIR / "world"
                if world.exists():
                    trash = SERVER_DIR / ".trash"
                    trash.mkdir(exist_ok=True)
                    shutil.move(
                        str(world),
                        str(trash / (datetime.now().strftime("%Y%m%d_%H%M%S_")
                                     + "world")))
                if srcdir == tmp:
                    shutil.move(str(tmp), str(world))
                else:
                    shutil.move(str(srcdir), str(world))
                msg = f"✅ 已导入存档 {src.name} → world/"
                self.after(0, lambda: self.task_done(tid, src.name))
            except Exception as e:
                msg = f"❌ 导入存档失败: {type(e).__name__}: {e}"
                print(msg)
                self.after(0, lambda t=type(e).__name__: self.task_fail(tid, t))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            self.after(0, lambda mm=msg: self._set_files_status(
                mm, "#2ecc71" if not mm.startswith("❌") else "#e74c3c"))
            self.after(0, self._refresh_files_tab)

        threading.Thread(target=task, daemon=True).start()

    # ==================== v3.5（⑲）玩家背包（只读） ====================
    # ==================== v3.5（⑱）Hangar 插件源 ====================
    def _search_hangar(self, page=0):
        """在 Hangar 搜插件（结果用 _add_hangar_row 画）。"""
        if not hasattr(self, "search_entry"):
            return
        query = self.search_entry.get().strip()
        self.last_query = query
        self.last_project_type = "hangar"
        self.current_page = max(0, int(page))
        self._set_search_status(
            (f"🔍 正在 Hangar 搜「{query}」..." if query
             else "⏳ 正在加载 Hangar 热门插件..."), "#f39c12")
        for w in self.results_frame.winfo_children():
            w.destroy()
        self._update_pagination_buttons(loading=True)

        def task():
            try:
                items, total = hangar_search(
                    query, HANGAR_PAGE, self.current_page * HANGAR_PAGE)
            except Exception as e:
                msg = f"❌ Hangar 搜索失败: {type(e).__name__}: {e}"
                print(msg)
                self.after(0, lambda: self._set_search_status(msg, "#e74c3c"))
                self.after(0, lambda: self._update_pagination_buttons())
                return
            self.total_hits = total
            for p in items:
                self.after(0, lambda pp=p: self._add_hangar_row(pp))
            self.after(0, lambda: self._set_search_status(
                f"✅ Hangar 找到 {total} 个插件（第 {self.current_page + 1} 页）",
                "#2ecc71"))
            self.after(0, lambda: self._update_pagination_buttons())

        threading.Thread(target=task, daemon=True).start()

    def _add_hangar_row(self, p):
        row = ctk.CTkFrame(self.results_frame, corner_radius=10)
        row.pack(fill="x", pady=4, padx=2)
        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=12, pady=8)
        ctk.CTkLabel(left, text=p.get("title", "?"),
                     font=ctk.CTkFont(size=15, weight="bold"),
                     anchor="w").pack(fill="x")
        desc = (p.get("description") or "（没有简介）")[:120]
        ctk.CTkLabel(left, text=desc, font=ctk.CTkFont(size=12),
                     text_color="#999999", anchor="w", wraplength=560,
                     justify="left").pack(fill="x")
        ctk.CTkLabel(left, text=f"⬇ {int(p.get('downloads') or 0):,}"
                                f"　·　来源 Hangar（Paper 官方）",
                     font=ctk.CTkFont(size=11), text_color="#7fb3ff",
                     anchor="w").pack(fill="x")
        ctk.CTkButton(row, text="⬇ 快速安装", width=110, height=32,
                      fg_color="#2ecc71", hover_color="#27ae60",
                      command=lambda pp=p: self._install_hangar(pp)).pack(
            side="right", padx=8)
        ctk.CTkButton(row, text="🌐 页面", width=80, height=32,
                      fg_color="#4a4a4a", hover_color="#5a5a5a",
                      command=lambda pp=p: self._open_url(
                          "https://hangar.papermc.io/" + pp.get("slug", ""))
                      ).pack(side="right", padx=2)

    def _install_hangar(self, p):
        """装一个 Hangar 插件：自动挑适配版本 → plugins/。"""
        core = self.launcher_state.get("core")
        if core in ("vanilla", "fabric"):
            if not messagebox.askyesno(
                    "核心不匹配",
                    f"「{p.get('title')}」是 Paper/Purpur 插件，"
                    f"装到 {core} 上不会生效。\n仍然安装吗？"):
                return
        owner, _, slug = str(p.get("slug", "")).partition("/")
        if not owner or not slug:
            messagebox.showerror("装不了", "这个项目的地址不完整")
            return
        tid = self.task_start(f"安装 {p.get('title')}（Hangar）")
        self._set_search_status(
            f"⏳ 正在挑 {p.get('title')} 的适配版本...", "#f39c12")

        def task():
            try:
                ver = hangar_pick_version(
                    owner, slug, self.launcher_state.get("version"))
                if ver is None:
                    self.after(0, lambda: self.task_fail(tid, "没有适配版本"))
                    self.after(0, lambda: self._set_search_status(
                        f"❌ {p.get('title')} 没有适配当前版本的构建",
                        "#e74c3c"))
                    return
                PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
                target = PLUGINS_DIR / ver["filename"]
                if target.exists():
                    self._save_rollback("plugins", target, ver["filename"])
                http_download(ver["url"], target,
                              cancel_check=lambda: self._task_cancel_check(tid))
                self._record_install("plugins", ver["filename"], slug,
                                     ver.get("version"), None)
                self.task_done(tid, f"{ver['filename']} → plugins/")
                self.after(0, self._refresh_files_tab)
                self.after(0, lambda vv=ver: self._set_search_status(
                    f"✅ {vv['filename']}（{vv.get('channel')} "
                    f"{vv.get('version')}）已装到 plugins/", "#2ecc71"))
            except TaskCancelled:
                return                      # 用户点了 ✕
            except Exception as e:
                msg = f"❌ 安装失败: {type(e).__name__}: {e}"
                print(msg)
                self.after(0, lambda t=type(e).__name__:
                           self.task_fail(tid, t))
                self.after(0, lambda: self._set_search_status(msg, "#e74c3c"))

        threading.Thread(target=task, daemon=True).start()

    def _open_player_inventory(self):
        """打开"玩家背包（只读）"窗口。"""
        if nbtlib_module() is None:
            if messagebox.askyesno(
                    "需要一个小库",
                    "看玩家背包要解析存档（NBT 格式），需要一个 100KB 的库 nbtlib。\n"
                    "现在装吗？（只在校验/查看时用，不影响启动速度）"):
                self._install_pkg("nbtlib")
            return
        if not (SERVER_DIR / "world").exists():
            messagebox.showinfo(
                "还没有世界",
                "服务器还没生成世界（先「一键启动」一次），没有玩家数据可看。")
            return
        win = ctk.CTkToplevel(self)
        win.title("玩家背包（只读）")
        win.geometry("780x620")
        try:
            win.transient(self)
        except Exception:
            pass
        head = ctk.CTkFrame(win, fg_color="transparent")
        head.pack(fill="x", padx=14, pady=(12, 4))
        ctk.CTkLabel(head, text="玩家", font=ctk.CTkFont(size=13)).pack(
            side="left")
        names = player_cache()
        uuids = []
        try:
            uuids = sorted(p.stem for p in playerdata_dir().glob("*.dat"))
        except Exception:
            pass
        choices = []
        for nm, uu in sorted(names.items()):
            choices.append(f"{nm} ({uu[:8]}…)")
            self._inv_map = getattr(self, "_inv_map", {})
            self._inv_map[f"{nm} ({uu[:8]}…)"] = uu
        # v3.5.16：存档文件名是带短横线的 uuid，usercache 里常是去掉短横线的，
        # 比较前统一归一化，否则已经认识的人会被再列一遍成"未知玩家"
        norm_names = {str(u).replace("-", "").lower() for u in names.values()}
        for uu in uuids:
            if str(uu).replace("-", "").lower() not in norm_names:
                label = f"（未知玩家）{uu[:8]}…"
                choices.append(label)
                self._inv_map = getattr(self, "_inv_map", {})
                self._inv_map[label] = uu
        self.lbl_inv_hint = ctk.CTkLabel(
            head, text="", font=ctk.CTkFont(size=12), text_color="#888888")
        self.lbl_inv_hint.pack(side="right")
        if not choices:
            choices = ["（没有玩家数据）"]
        self.inv_choice = ctk.CTkOptionMenu(
            head, width=220, values=choices, command=self._render_player_inv)
        self.inv_choice.set(choices[0])
        self.inv_choice.pack(side="left", padx=8)
        ctk.CTkButton(head, text="刷新", width=70,
                      command=lambda: self._render_player_inv(
                          self.inv_choice.get())).pack(side="left", padx=4)
        ctk.CTkLabel(
            win, anchor="w", justify="left", wraplength=740,
            font=ctk.CTkFont(size=12), text_color="#f39c12",
            text="⚠ 只读：这里只是读存档给你看，绝不改任何东西（改背包请用游戏里的指令）。"
        ).pack(fill="x", padx=16, pady=(0, 4))
        self.inv_box = ctk.CTkTextbox(
            win, font=ctk.CTkFont(family="Consolas", size=13))
        self.inv_box.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self._render_player_inv(choices[0])
        return win

    def _render_player_inv(self, label):
        uu = getattr(self, "_inv_map", {}).get(label)
        if not uu:
            self._set_inv_text("（没有玩家数据。让玩家先进一次服务器，"
                               "或者这个服务器还没生成世界）")
            return
        inv, ender, note = read_player_inventory(uu)
        if inv is None:
            self._set_inv_text(f"⚠ {note}")
            return
        lines = []
        if not inv:
            lines.append("背包是空的。")
        for it in inv:
            extra = ("　" + "、".join(it["extra"])) if it["extra"] else ""
            lines.append(f"{slot_label(it['slot']):<10} {it['display']} ×{it['count']}"
                         f"　（{it['id']}）{extra}")
        lines.append("")
        lines.append(f"—— 末影箱（{len(ender)} 件）——")
        for it in ender:
            lines.append(f"第 {it['slot'] + 1} 格　{it['display']} ×{it['count']}"
                         f"　（{it['id']}）")
        self._set_inv_text("\n".join(lines))
        if hasattr(self, "lbl_inv_hint"):
            self.lbl_inv_hint.configure(
                text=f"共 {len(inv)} 件物品（只读）", text_color="#2ecc71")

    def _set_inv_text(self, text):
        try:
            self.inv_box.configure(state="normal")
            self.inv_box.delete("1.0", "end")
            self.inv_box.insert("1.0", text)
            self.inv_box.configure(state="disabled")
        except Exception:
            pass

    def _target_dir_for(self, project_type):
        """插件 / 模组 / 数据包 分别装到哪 → (目录, 给用户看的名字)。"""
        if project_type == "plugin":
            return PLUGINS_DIR, "plugins"
        if project_type == "datapack":
            return datapacks_dir(), "world/datapacks"
        return MODS_DIR, "mods"

    def _datapack_ready(self):
        """数据包是跟着世界存档走的：还没有 world 就先让用户启动一次。"""
        if (SERVER_DIR / "world").exists():
            return True
        messagebox.showinfo(
            "还没有世界存档",
            "数据包是放在世界存档（world/）里的。\n\n"
            "请先回「🏠 概览」点一次「一键启动」，让服务器生成 world/，\n"
            "然后再来装数据包（生成的 world 里会自动带上 datapacks/ 目录）。")
        return False

    def _install_project(self, project, project_type):
        """快速安装前的“常识检查”（v3.1 新增）。

        以前没有这些检查，而 _do_install_project 在缺少核心信息时会把所有版本
        都当候选，于是把 NeoForge 的构建装进了 Paper 的 plugins/ 目录
        （用户实际遇到：plugins/Chunky-NeoForge-1.5.4.jar）。
        """
        core = self.launcher_state.get("core")
        version = self.launcher_state.get("version")
        title = project.get("title", "该项目")

        if not core or not version:
            if not messagebox.askyesno(
                    "还没装核心",
                    f"这个服务器还没下载服务端核心，无法判断「{title}」\n"
                    f"该装哪个版本（Paper 插件？Fabric 模组？）。\n\n"
                    f"建议先去「📥 下载核心」装好核心。\n\n"
                    f"仍然随便挑一个版本安装吗？"):
                self.tabview.set("📥 下载核心")
                return
        else:
            if project_type == "datapack" and not self._datapack_ready():
                return
            if project_type == "plugin" and core in ("vanilla", "fabric"):
                why = ("Fabric 服务端不加载 plugins/ 里的 Bukkit 系插件。"
                       if core == "fabric" else
                       "原版(Vanilla)服务端不支持插件，装了也不会生效。")
                if not messagebox.askyesno(
                        "核心不匹配",
                        f"「{title}」是 Paper/Purpur（Bukkit 系）插件。\n\n"
                        f"{why}\n\n仍然安装吗？"):
                    return
            if project_type == "mod" and core in ("paper", "purpur"):
                if not messagebox.askyesno(
                        "核心不匹配",
                        f"Paper/Purpur 服务端不加载 mods/ 里的模组\n"
                        f"（模组是给 Fabric/Forge 用的）。\n\n"
                        f"仍然安装吗？"):
                    return

        threading.Thread(
            target=self._do_install_project,
            args=(project, project_type),
            daemon=True
        ).start()

    def _do_install_project(self, project, project_type):
        tid = None
        try:
            slug = project.get("slug") or project.get("project_id")
            title = project.get("title", slug)
            tid = self.task_start(f"安装 {title}")     # v3.4：进侧边栏
            self._set_search_status(
                f"⏳ 正在为 {title} 挑选最佳版本...", "#f39c12")

            versions = http_get_json(
                f"{MODRINTH_API}/project/{slug}/version")
            if not versions:
                self._set_search_status("❌ 该项目没有可用版本",
                                        "#e74c3c")
                return

            server_version = self.launcher_state.get("version")
            core = self.launcher_state.get("core")
            if project_type == "datapack":
                loader = None          # v3.5（⑤）：数据包只按游戏版本卡
            else:
                loader = (CORE_LOADER_MAP.get(core)
                          if project_type == "plugin" else core)

            candidates = []
            for v in versions:
                if server_version and \
                        server_version not in v.get("game_versions", []):
                    continue
                if loader and loader not in v.get("loaders", []):
                    continue
                candidates.append(v)

            if not candidates:
                # v3.1：只放宽“游戏版本”，绝不放宽加载器。
                # 以前这里放宽成“任意版本”，结果把 NeoForge 的包装进了 Paper 的 plugins/。
                if loader:
                    candidates = [v for v in versions
                                  if loader in v.get("loaders", [])]

            if not candidates:
                if server_version or loader:
                    self._set_search_status(
                        f"❌ {title} 没有适配 "
                        f"{(core or '').capitalize()} {server_version or ''} 的版本，"
                        f"可以点「📋 选择版本」自己挑一个", "#e74c3c")
                    return
                candidates = versions

            release_first = sorted(
                candidates,
                key=lambda v: (
                    0 if v.get("version_type") == "release" else 1)
            )
            ver = release_first[0]

            files = ver.get("files", [])
            if not files:
                self._set_search_status("❌ 该版本没有文件", "#e74c3c")
                return

            primary = next(
                (f for f in files if f.get("primary")), files[0])

            target_dir, dir_label = self._target_dir_for(project_type)
            if project_type == "datapack" and not self._datapack_ready():
                self._set_search_status(
                    "⚠ 还没有 world 存档，先在概览页启动一次服务器",
                    "#f39c12")
                return
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / primary["filename"]

            self._set_search_status(
                f"⏳ 正在下载 {primary['filename']} "
                f"({ver.get('version_number', '?')})...",
                "#f39c12")

            http_download(primary["url"], target,
                          cancel_check=(lambda: self._task_cancel_check(tid))
                          if tid else None)

            self._record_install(target_dir.name, primary["filename"], slug,
                                 ver.get("version_number"), ver.get("id"))
            if tid:
                self.task_done(tid, f"{primary['filename']} → {dir_label}/")
            self.after(0, self._refresh_files_tab)
            self._set_search_status(
                f"✅ {primary['filename']} "
                f"已安装到 {dir_label}/",
                "#2ecc71"
            )
        except TaskCancelled:
            return                      # 用户点了 ✕
        except Exception as e:
            err_text = f"❌ 安装失败: [{type(e).__name__}] {e}"
            print(err_text)
            if tid:
                self.task_fail(tid, f"{type(e).__name__}: {e}")
            self._set_search_status(err_text, "#e74c3c")

    # ==================== EULA / properties ====================
    def _accept_eula(self):
        SERVER_DIR.mkdir(exist_ok=True)
        EULA_FILE.write_text(
            "#By changing the setting below to TRUE you are indicating "
            "your agreement to our EULA "
            "(https://aka.ms/MinecraftEULA).\n"
            "eula=true\n",
            encoding="utf-8"
        )

    def _save_properties(self):
        # v3.3：配置页没建过就没有可保存的控件，直接跳过
        if not hasattr(self, "prop_widgets"):
            return
        SERVER_DIR.mkdir(exist_ok=True)

        existing_lines = []
        if PROPERTIES_FILE.exists():
            existing_lines = PROPERTIES_FILE.read_text(
                encoding="utf-8").splitlines(keepends=True)

        new_values = {}
        for key, widget in self.prop_widgets.items():
            if isinstance(widget, ctk.CTkEntry):
                new_values[key] = widget.get().strip()
            else:
                new_values[key] = widget.get()

        updated = set()
        out = []
        for line in existing_lines:
            s = line.strip()
            if s.startswith("#") or "=" not in s:
                out.append(line)
                continue
            k = s.split("=", 1)[0].strip()
            if k in new_values:
                out.append(f"{k}={new_values[k]}\n")
                updated.add(k)
            else:
                out.append(line)

        for k, v in new_values.items():
            if k not in updated:
                out.append(f"{k}={v}\n")

        PROPERTIES_FILE.write_text("".join(out), encoding="utf-8")

    def _load_properties(self, silent=False):
        # v3.3：配置页是懒加载的，没建过就别动
        if not hasattr(self, "prop_widgets"):
            return
        if not PROPERTIES_FILE.exists():
            if not silent:
                messagebox.showinfo(
                    "提示", "server.properties 尚未生成，请先启动一次服务器。")
            return
        props = {}
        for line in PROPERTIES_FILE.read_text(
                encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#") or "=" not in s:
                continue
            k, v = s.split("=", 1)
            props[k.strip()] = v.strip()

        for key, widget in self.prop_widgets.items():
            if key in props:
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                    widget.insert(0, props[key])
                else:
                    widget.set(props[key])
        if not silent:
            messagebox.showinfo("成功", "已读取当前配置文件。")

    # ==================== 启动 / 停止 ====================
    def _start_server(self):
        if self.is_running:
            return

        # v3.5.12：上次启动器被关/被杀后留下的服务端还占着端口 → 先处理它
        ghost = self._detect_orphan_server()
        if ghost:
            if messagebox.askyesno(
                    "检测到后台还有服务端在跑",
                    f"上次启动器关掉后，服务端（PID {ghost}）还在后台跑着。\n"
                    f"启动器接管不了它，端口也一直被它占着。\n\n"
                    f"要结束它再重新启动吗？\n"
                    f"（强制结束可能丢掉最近几分钟没保存的存档）"):
                if not self._kill_orphan_server(ghost):
                    return
            else:
                return

        if not SERVER_JAR.exists():
            if messagebox.askyesno(
                    "未安装核心",
                    "还没下载服务端核心。\n现在跳转到下载页面吗？"):
                self.tabview.set("📥 下载核心")
            return

        # v2.9：不再替用户静默同意 EULA，首次启动先确认一次
        if not getattr(self, "_eula_confirmed", False):
            if not messagebox.askyesno(
                    "同意 Minecraft EULA",
                    "启动服务器需要同意 Mojang 最终用户许可协议：\n"
                    "https://aka.ms/MinecraftEULA\n\n是否同意并继续？"):
                return
            self._eula_confirmed = True

        self._accept_eula()
        self._save_properties()

        try:
            min_gb = int(round(float(self.min_mem.get())))
            max_gb = int(round(float(self.max_mem.get())))
        except Exception:
            messagebox.showerror("错误", "内存设置读取失败")
            return

        if min_gb <= 0 or max_gb <= 0:
            messagebox.showerror("错误", "内存必须大于 0 GB")
            return
        if min_gb > max_gb:
            messagebox.showerror(
                "错误", f"最小内存（{min_gb}G）不能大于最大内存（{max_gb}G）")
            return

        # v2.9：按所选版本检查 Java（1.20.5+ 需要 21，1.16 及更早需要 8）
        need_java = self.required_java_for(
            self.launcher_state.get("version", ""))
        java_major = getattr(self, "java_major", None)
        if need_java and java_major and java_major < need_java:
            # v3.4：改成“先劝、但允许硬闯”，并直接把一键安装指给他
            if not messagebox.askyesno(
                    "Java 版本过低",
                    f"这个服务端需要 Java {need_java} 或更高，\n"
                    f"当前用的是 Java {java_major} —— 大概率会直接退出：\n"
                    f"“requires running the server with Java "
                    f"{need_java} or above”\n\n"
                    f"到「🔧 设置 → Java 运行时」点「⬇ 一键下载安装」"
                    f"就能装好 Java {need_java}（装完自动切换）。\n\n"
                    f"仍然要尝试启动吗？"):
                return

        # v3.0：老版本 + 新 Java 也是常见坑（例如 1.16.5 配 Java 24，必崩）
        if need_java == 8 and java_major and java_major >= 17:
            if not messagebox.askyesno(
                    "Java 版本可能过高",
                    f"该版本官方要求 Java 8，但你装的是 Java {java_major}，"
                    f"服务端很可能起不来。\n\n"
                    f"建议改选 1.17 以上的游戏版本，或另外装一个 Java 8。\n\n"
                    f"仍然尝试启动吗？"):
                return

        # v3.0：启动前先查端口占用，给一句人话，而不是让服务端抛一大堆异常
        try:
            import socket as _socket
            with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as _s:
                _s.settimeout(0.4)
                port_busy = (_s.connect_ex(
                    ("127.0.0.1", int(self._get_port()))) == 0)
        except Exception:
            port_busy = False
        if port_busy:
            if not messagebox.askyesno(
                    "端口已被占用",
                    f"端口 {self._get_port()} 已经被别的程序占用。\n"
                    f"最常见的原因：已经有一个服务器在运行。\n\n"
                    f"仍然尝试启动吗？"):
                return

        # v3.3：Java 路径 / JVM 参数 / 内存都听设置的
        java_exe = (self.launcher_state.get("java_path")
                    or self.settings.get("java_path") or "java")
        extra_args = (self.launcher_state.get("jvm_args")
                      or self.settings.get("jvm_args") or "").split()
        self.launcher_state["min_mem"] = min_gb
        self.launcher_state["max_mem"] = max_gb
        self._save_state()
        cmd = [java_exe,
               # v2.9：强制 UTF-8 输出，避免中文日志乱码（Java 19+ 生效）
               "-Dfile.encoding=UTF-8",
               "-Dstdout.encoding=UTF-8",
               "-Dstderr.encoding=UTF-8",
               f"-Xms{min_gb}G", f"-Xmx{max_gb}G"]
        cmd += extra_args
        cmd += ["-jar", "server.jar", "nogui"]

        # v3.2：立即给出“正在启动”的可见反馈，别让人以为点不动
        self.server_phase = "starting"
        try:
            self.lbl_status.configure(text="⏳ 启动中…", text_color="#f39c12")
            self.lbl_hint.configure(
                text="⏳ 正在启动，首次启动要生成世界（约 30~90 秒），请稍候…",
                text_color="#f39c12")
            self.tabview.set("💻 控制台")     # 立刻跳过去，能看见日志在滚
        except Exception:
            pass

        self._append_console(f"\n[启动器] 正在启动服务器...\n")
        self._append_console(f"[启动器] 命令: {' '.join(cmd)}\n\n")
        self._append_console(
            "[启动器] 服务器在后台运行，不会再弹黑窗口打扰你。\n"
            "[启动器] 日志就在这一页；要停服点「■ 关闭服务器」，别直接关启动器。\n\n")

        try:
            self.server_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                cwd=str(SERVER_DIR), bufsize=1,
                **hidden_console_kwargs()      # v3.5.8：别弹黑窗口
            )
            self.is_running = True
            self.online_players.clear()
            self._update_buttons()
            # v3.5.12：记下 PID —— 万一启动器被强关，下次启动能发现这个"幽灵服务端"
            try:
                self.launcher_state["server_pid"] = int(self.server_process.pid)
                self._save_state()
                self._orphan_server_pid = 0
            except Exception:
                pass

            threading.Thread(target=self._read_output,
                             args=(self.server_process,),
                             daemon=True).start()
        except FileNotFoundError:
            messagebox.showerror(
                "错误", "未找到 java 命令，请先安装 Java 17+")
        except Exception as e:
            messagebox.showerror(
                "错误", f"启动失败: [{type(e).__name__}] {e}")

    def _read_output(self, proc):
        try:
            for line in iter(proc.stdout.readline, ""):
                # v3.5.15：翻译/玩家解析/阶段判断都在这条工作线程里做掉，
                # 主线程只负责把已经拼好的文本一次性插进控制台（拖窗口才不卡）
                self.log_queue.put(self._prepare_log_text(line))
            proc.stdout.close()
        except Exception:
            pass
        self.log_queue.put(None)

    def _prepare_log_text(self, raw):
        """工作线程里把一行原始日志加工成"可直接显示"的文本（含 ↳ 中文）。"""
        line = strip_ansi(raw)
        out = line
        try:
            self._parse_players(line)
        except Exception:
            pass
        try:
            low = line.lower()
            extra = []
            if getattr(self, "server_phase", "") == "starting":
                if re.search(r"Done \([\d.]+s\)!", line):
                    self.server_phase = "running"
                    extra.append("[启动器] ✅ 服务端已就绪，可以进游戏了。\n")
                elif "unsupported class file major version" in low:
                    self.server_phase = "stopped"
                    extra.append(
                        "[启动器] ⚠ Java 版本不匹配（Unsupported class file "
                        "major version），换个 Java 版本再试。\n")
                elif "you need to agree to the eula" in low:
                    self.server_phase = "stopped"
                    extra.append(
                        "[启动器] ⚠ 服务端要求同意 EULA，"
                        "请到「📁 文件」里检查 eula.txt。\n")
            if getattr(self, "_translate_logs", False):
                out = self._with_translations(line)
            if extra:
                sep = "" if out.endswith("\n") else "\n"
                out = out + sep + "".join(extra)
        except Exception:
            pass
        return out

    def _poll_log_queue(self, budget_ms=4.0):
        """把**已经加工好**的日志文本搬进控制台（v3.5.15）。

        翻译/玩家解析/阶段判断都在工作线程 `_read_output` 里做掉了，
        主线程这里只剩"攒一批、一次性 insert"，单次通常几毫秒。
        """
        t0 = time.perf_counter()
        chunks = []
        while True:
            if chunks and (time.perf_counter() - t0) * 1000.0 > budget_ms:
                break
            try:
                text = self.log_queue.get_nowait()
            except queue.Empty:
                break
            if text is None:
                continue
            chunks.append(text)
            if len(chunks) >= 400:
                break
        if chunks:
            self._append_console_raw("".join(chunks))
        # v3.5：不再自己排下一次，统一由 _tick 调度（忙 100ms / 闲 500ms）

    def _parse_players(self, line):
        m = re.search(r"\]: (\w+) joined the game", line)
        if m:
            name = m.group(1)
            self.online_players.add(name)
            if not hasattr(self, "online_since"):
                self.online_since = {}
            self.online_since[name] = datetime.now()      # v3.5（③）
            return
        m = re.search(r"\]: (\w+) left the game", line)
        if m:
            name = m.group(1)
            self.online_players.discard(name)
            if not hasattr(self, "last_seen"):
                self.last_seen = {}
            self.last_seen[name] = datetime.now()
            if hasattr(self, "online_since"):
                self.online_since.pop(name, None)

    # ==================== v3.5（③）玩家列表 ====================
    def _player_table(self):
        """返回 (在线名字列表, {名字: uuid} 来过的人)。在线靠日志，来过靠 usercache。"""
        online = sorted(self.online_players)
        cache = player_cache()
        ever = dict(cache)
        try:
            ever_norm = {str(v).replace("-", "").lower()
                         for v in ever.values()}
            for p in playerdata_dir().glob("*.dat"):
                uu = p.stem.lower()
                if uu.replace("-", "").lower() not in ever_norm:
                    ever.setdefault(f"（未知玩家）{uu[:8]}", uu)
        except Exception:
            pass
        return online, ever

    def _server_cmd(self, cmd, need_ask=None):
        """往服务端控制台发一条指令（等于自己手动在控制台敲）。不需要 RCON。"""
        if not self.is_running or not self.server_process:
            messagebox.showinfo("服务器没在跑", "这个操作要服务器开着才行。")
            return False
        self._say_to_server(cmd)
        self._append_console(f"[启动器] 已发送指令: {cmd}\n")
        return True

    def _kick_player(self, name):
        if not messagebox.askyesno("踢出玩家", f"把「{name}」踢下线吗？"):
            return
        self._server_cmd(f"kick {name} 被管理员请出服务器")

    def _op_player(self, name):
        if not messagebox.askyesno(
                "设为管理员",
                f"把「{name}」设为管理员（OP）吗？\n（等于在控制台敲 op {name}）"):
            return
        self._server_cmd(f"op {name}")

    def _open_players_window(self):
        """玩家名单：在线靠日志认，来过的靠 usercache；能踢人 / 给 OP / 看背包。"""
        win = ctk.CTkToplevel(self)
        win.title("玩家列表")
        win.geometry("660x560")
        try:
            win.transient(self)
        except Exception:
            pass
        online, ever = self._player_table()
        head = ctk.CTkFrame(win, fg_color="transparent")
        head.pack(fill="x", padx=14, pady=(12, 4))
        self.lbl_players_head = ctk.CTkLabel(
            head, anchor="w", font=ctk.CTkFont(size=14, weight="bold"),
            text=f"在线 {len(online)} 人　·　来过 {len(ever)} 人")
        self.lbl_players_head.pack(side="left")
        ctk.CTkButton(head, text="刷新", width=70,
                      command=lambda: (win.destroy(),
                                       self._open_players_window())
                      ).pack(side="right")
        ctk.CTkLabel(
            win, anchor="w", justify="left", wraplength=620,
            font=ctk.CTkFont(size=12), text_color="#f39c12",
            text="操作是往服务端控制台发指令（不需要 RCON）：踢人 / 给 OP / 看背包（只读）。"
        ).pack(fill="x", padx=16, pady=(0, 4))
        body = ctk.CTkScrollableFrame(win, width=600, height=420)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 12))
        self._fast_scroll(body)

        def section(title):
            ctk.CTkLabel(body, text=title, anchor="w",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#7fb3ff").pack(fill="x", padx=6, pady=(8, 2))

        section(f"🟢 在线（{len(online)}）")
        if not online:
            ctk.CTkLabel(body, text="    （现在没人）", anchor="w",
                         text_color="#888888").pack(fill="x", padx=16)
        for name in online:
            since = getattr(self, "online_since", {}).get(name)
            dur = ""
            if since:
                mins = int((datetime.now() - since).total_seconds() // 60)
                dur = f"（已在线 {mins} 分钟）"
            row = ctk.CTkFrame(body, corner_radius=8)
            row.pack(fill="x", padx=6, pady=2)
            ctk.CTkLabel(row, text=f"{name} {dur}", anchor="w",
                         font=ctk.CTkFont(size=13)).pack(side="left", padx=12,
                                                          pady=6)
            uu = ever.get(name)
            if uu:
                ctk.CTkButton(row, text="🎒 背包", width=80, height=26,
                              fg_color="#2c3e50", hover_color="#34495e",
                              command=lambda n=name, u=uu: self._view_inv_of(n, u)
                              ).pack(side="right", padx=4)
            ctk.CTkButton(row, text="👑 给 OP", width=90, height=26,
                          fg_color="#8e44ad", hover_color="#7d3c98",
                          command=lambda n=name: self._op_player(n)).pack(
                side="right", padx=4)
            ctk.CTkButton(row, text="👢 踢出", width=80, height=26,
                          fg_color="#e74c3c", hover_color="#c0392b",
                          command=lambda n=name: self._kick_player(n)).pack(
                side="right", padx=4)

        section(f"📜 来过的人（{len(ever)}）")
        if not ever:
            ctk.CTkLabel(body, text="    （还没有玩家来过）", anchor="w",
                         text_color="#888888").pack(fill="x", padx=16)
        for name, uu in sorted(ever.items()):
            if name in online:
                continue
            row = ctk.CTkFrame(body, corner_radius=8)
            row.pack(fill="x", padx=6, pady=2)
            seen = getattr(self, "last_seen", {}).get(name)
            tail = f"　（最后下线 {seen.strftime('%m-%d %H:%M')}）" if seen else ""
            ctk.CTkLabel(row, text=f"{name}{tail}", anchor="w",
                         font=ctk.CTkFont(size=13)).pack(side="left", padx=12,
                                                          pady=6)
            ctk.CTkButton(row, text="🎒 背包", width=80, height=26,
                          fg_color="#2c3e50", hover_color="#34495e",
                          command=lambda n=name, u=uu: self._view_inv_of(n, u)
                          ).pack(side="right", padx=4)
        return win

    def _view_inv_of(self, name, uuid):
        """从玩家列表直接跳去看这个人的背包（只读）。"""
        win = self._open_player_inventory()
        if win is None:
            return
        try:
            for lab, uu in getattr(self, "_inv_map", {}).items():
                if uu == uuid:
                    self.inv_choice.set(lab)
                    self._render_player_inv(lab)
                    break
        except Exception:
            pass

    # ==================== v3.5（⑭）日志离线中文翻译 ====================
    def _with_translations(self, text):
        """在每行日志下面插一行「↳ 中文」；翻不出来就只留原行。"""
        out = []
        for line in str(text).splitlines():
            out.append(line)
            tr = translate_log_line(line)
            if tr:
                out.append("        ↳ " + tr)
        tail = "\n" if str(text).endswith("\n") else ""
        return "\n".join(out) + tail

    # ==================== v3.5（⑧）离线手册 ====================
    def _open_manual(self):
        p = write_manual()
        if p is None:
            messagebox.showerror("打不开手册", "写手册文件失败了（详见控制台）")
            return
        try:
            os.startfile(str(p))
        except Exception:
            messagebox.showinfo(
                "手册已生成",
                f"手册已经生成好了：\n{p}\n\n用浏览器打开它就行（不用联网）")

    def _toggle_translate(self):
        self._translate_logs = bool(self.sw_translate.get())
        self.settings["translate_log"] = self._translate_logs
        try:
            save_launcher_settings(self.settings)
        except Exception:
            pass
        self._append_console(
            f"[启动器] 日志中文翻译已"
            f"{'打开' if self._translate_logs else '关闭'}"
            f"（离线词库，不联网）\n")

    def _append_console(self, text):
        text = strip_ansi(text)            # v3.5.9：颜色控制符别进控制台
        if getattr(self, "_translate_logs", False):
            text = self._with_translations(text)
        self._append_console_raw(text)

    def _append_console_raw(self, text):
        """不翻译、直接写进控制台（批量搬运日志时用，v3.5.15）。"""
        # v3.3：控制台页是懒加载的。还没建就先缓存，等页面建好一次性补上，
        # 否则 __init__ 里的日志（拖拽初始化、Pillow 提示）会直接把程序搞崩。
        box = getattr(self, "console_box", None)
        if box is None:
            backlog = getattr(self, "_console_backlog", None)
            if backlog is None:
                backlog = self._console_backlog = []
            if len(backlog) < 2000:
                backlog.append(text)
            return
        backlog = getattr(self, "_console_backlog", None)
        if backlog:
            self._console_backlog = []
            text = "".join(backlog) + text
        try:
            box.configure(state="normal")
            box.insert("end", text)
            box.see("end")
            box.configure(state="disabled")
        except Exception:
            pass

    def _stop_server(self):
        if not self.server_process or not self.is_running:
            return
        self._user_stopping = True      # v3.4：自己停的不算崩溃，别触发诊断弹窗

        # v3.0：5 秒内再点一次「停止」＝ 强制结束。
        # 以前如果服务端卡在存档/卡死，stop 指令发出去就没下文了，界面会一直卡在“运行中”。
        last = getattr(self, "_stop_at", None)
        if last is not None and (datetime.now() - last).total_seconds() < 5:
            self._append_console("[启动器] 强制结束服务器进程...\n")
            try:
                self.server_process.kill()
            except Exception as e:
                self._append_console(f"[启动器] 强制结束失败: {e}\n")
            self._stop_at = None
            return

        self._stop_at = datetime.now()
        self._append_console(
            "\n[启动器] 正在发送 stop 指令...\n"
            "[启动器] 如果 5 秒后还没停，就再点一次「停止」强制结束。\n")
        try:
            self.server_process.stdin.write("stop\n")
            self.server_process.stdin.flush()
        except Exception:
            try:
                self.server_process.kill()
            except Exception:
                pass

    # ==================== v3.5（③）崩溃自动重启 + 定时重启 ====================
    def _sched(self):
        """当前服务器的计划任务设置（跟着服务器走，存在 launcher_state）。"""
        return self.launcher_state.setdefault("schedule", {})

    def _maybe_auto_restart(self, ret):
        """异常退出后按设置自动重启。10 分钟内最多重试 crash_limit 次，防死循环。"""
        cfg = self._sched()
        if not cfg.get("crash_restart"):
            return
        now = time.monotonic()
        tries = [t for t in getattr(self, "_restart_times", []) if now - t < 600]
        tries.append(now)
        self._restart_times = tries
        try:
            limit = int(cfg.get("crash_limit", 3) or 3)
        except Exception:
            limit = 3
        if len(tries) > limit:
            self._append_console(
                f"\n[启动器] ⚠ 10 分钟内已经自动重启过 {limit} 次，这次不重启了"
                f"（怕一直崩溃重启死循环）。把原因修好再手动启动。\n")
            self._diagnose_and_report(
                self._server_log_tail(),
                f"反复崩溃（{limit} 次），已停止自动重启")
            return
        try:
            delay = max(3, int(cfg.get("crash_delay", 10) or 10))
        except Exception:
            delay = 10
        tid = self.task_start(f"崩溃自动重启（第 {len(tries)}/{limit} 次）")
        self._restart_task_id = tid
        self._append_console(
            f"[启动器] 🔁 服务器崩了，{delay} 秒后自动重启"
            f"（第 {len(tries)}/{limit} 次，返回码 {ret}）\n")
        self._restart_job = self.after(delay * 1000, self._do_auto_restart)

    def _do_auto_restart(self):
        self._restart_job = None
        tid = getattr(self, "_restart_task_id", None)
        try:
            self._start_server()
            if tid is not None:
                self.task_done(tid, "已重新启动")
        except Exception as e:
            print(f"[启动器] 自动重启失败: {e}")
            if tid is not None:
                self.task_fail(tid, str(e))

    def _sched_restart_tick(self):
        """定时重启：距上次重启够久、而且服务器在跑，就安排一次重启。"""
        cfg = self._sched()
        hours = {"6h": 6, "12h": 12, "24h": 24}.get(
            str(cfg.get("restart_mode", "off")), 0)
        if hours <= 0 or not self.is_running:
            return
        if getattr(self, "_sched_restart_busy", False):
            return
        last = getattr(self, "_last_restart_at", None)
        now = time.monotonic()
        if last is None:
            self._last_restart_at = now       # 从这次开服开始算
            return
        if now - last < hours * 3600:
            return
        self._last_restart_at = now
        self._begin_sched_restart()

    def _begin_sched_restart(self):
        """先广播，再停服，停完自动开回来。"""
        if not self.is_running:
            return
        self._sched_restart_busy = True
        tid = self.task_start("定时重启服务器")
        self._sched_tid = tid
        self._append_console(
            "\n[启动器] ⏰ 到点了：60 秒后重启服务器（游戏里也会广播提示）\n")
        for left, msg in ((60, "say [启动器] 60 秒后重启服务器，请找安全的地方下线"),
                          (30, "say [启动器] 30 秒后重启"),
                          (10, "say [启动器] 10 秒后重启")):
            self.after((60 - left) * 1000,
                       lambda m=msg: self._say_to_server(m))
        self.after(61000, self._do_sched_restart)

    def _say_to_server(self, cmd):
        """往服务端 stdin 写一条命令（广播用）。"""
        try:
            if self.server_process and self.server_process.stdin:
                self.server_process.stdin.write(cmd + "\n")
                self.server_process.stdin.flush()
                self._append_console(f"[启动器] 已广播: {cmd}\n")
        except Exception as e:
            print(f"[启动器] 广播失败: {e}")

    def _do_sched_restart(self):
        tid = getattr(self, "_sched_tid", None)
        was = self.is_running
        try:
            self._stop_server()
        except Exception as e:
            print(f"[启动器] 定时重启停止失败: {e}")
        if was:
            self.after(15000, lambda: self._restart_after_sched(tid))
        else:
            self._sched_restart_busy = False
            if tid is not None:
                self.task_fail(tid, "服务器当时没在跑")

    def _restart_after_sched(self, tid=None):
        try:
            self._start_server()
            if tid is not None:
                self.task_done(tid, "已重启完成")
        except Exception as e:
            print(f"[启动器] 定时重启失败: {e}")
            if tid is not None:
                self.task_fail(tid, str(e))
        finally:
            self._sched_restart_busy = False

    def _poll_process(self):
        if self.is_running and self.server_process:
            ret = self.server_process.poll()
            if ret is None:
                self._user_stopping = False      # 真的在跑 → 清掉“用户主动停”标记
            if ret is not None:
                self.is_running = False
                self.server_process = None
                self.server_phase = "stopped"
                self.online_players.clear()
                try:
                    self.launcher_state.pop("server_pid", None)   # v3.5.12
                    self._save_state()
                except Exception:
                    pass
                self._append_console(
                    f"\n[启动器] 服务器进程已退出 (返回码 {ret})\n")
                # v3.4 ⑮：异常退出 → 自动扫日志，用人话报原因
                if ret not in (0, None) and not getattr(self, "_user_stopping",
                                                        False):
                    self._diagnose_and_report(
                        self._server_log_tail(),
                        f"服务器异常退出（返回码 {ret}）")
                    self._maybe_auto_restart(ret)      # v3.5（③）
                self._update_buttons()
        # v3.5：不再自己排下一次，统一由 _tick 按 TICK_PROC_MS 调度

    # ==================== 崩溃诊断（v3.4 ⑮） ====================
    def _server_log_tail(self, limit=60000):
        """取最近的日志：优先 logs/latest.log，没有再退回控制台缓冲。"""
        text = ""
        try:
            log = SERVER_DIR / "logs" / "latest.log"
            if log.exists():
                text = log.read_text(encoding="utf-8", errors="replace")
        except Exception:
            text = ""
        text = strip_ansi(text)            # v3.5.9：诊断/上传日志前也要剥颜色码
        if not text.strip():
            try:
                text = self.console_box.get("1.0", "end")
            except Exception:
                text = ""
        return text[-limit:]

    def _format_findings(self, findings, suspects, key=""):
        """把诊断结果排成人话（v3.5.10：先给"关键报错"原文，再给结论和怎么改）。"""
        lines = []
        if key:
            lines.append(f"  关键报错：{key}")
        for f in findings:
            lines.append(f"  [{f['sev']}] {f['why']}")
            lines.append(f"        → {f['fix']}")
        if suspects:
            lines.append("  可疑组件（栈里出现的 jar）：" + "、".join(suspects))
        elif findings:
            lines.append("  可疑组件：无 —— 报错出在服务端/Paper 内部，"
                         "不是你装的插件或模组引起的")
        return "\n".join(lines)

    def _diagnose_and_report(self, text, reason, popup=True):
        """扫日志 → 控制台输出 + 弹窗给结论。"""
        findings = analyze_log(text, limit=5)
        suspects = suspect_components(text)
        key = key_error_line(text)
        if not findings:
            if popup:
                messagebox.showinfo(
                    "崩溃诊断",
                    "没看出已知的报错模式。\n\n"
                    "可以点「🌐 上传 mclo.gs 深度分析」，让在线分析器再看一遍。")
            return []
        body = (f"\n[诊断] {reason}\n"
                + self._format_findings(findings, suspects, key=key) + "\n")
        self._append_console(body)
        if popup:
            parts = []
            if key:
                parts.append("关键报错：\n" + key)
            for f in findings[:3]:
                parts.append(f"[{f['sev']}] {f['why']}\n→ {f['fix']}")
            if suspects:
                parts.append("可疑组件：" + "、".join(suspects))
            elif len(findings) == 1:
                parts.append("可疑组件：无（服务端内部问题，不用去翻插件）")
            messagebox.showwarning("崩溃诊断", "\n\n".join(parts))
        return findings

    def _analyze_log_ui(self):
        """手动点「分析日志找原因」。"""
        text = self._server_log_tail()
        findings = analyze_log(text, limit=8)
        suspects = suspect_components(text)
        key = key_error_line(text)
        if not findings:
            self.lbl_diag.configure(
                text="没看出明显问题。可上传 mclo.gs 深度分析。",
                text_color="#2ecc71")
            self._append_console("[诊断] 没在日志里看到已知的报错模式。\n")
            return
        self._append_console(
            f"\n[诊断] 共发现 {len(findings)} 条线索：\n"
            + self._format_findings(findings, suspects, key=key) + "\n")
        self.lbl_diag.configure(
            text=f"发现 {len(findings)} 条线索：" +
                 "；".join(f["why"][:22] for f in findings[:3]),
            text_color="#f39c12")
        msg = "\n\n".join(f"[{f['sev']}] {f['why']}\n→ {f['fix']}"
                          for f in findings[:5])
        if suspects:
            msg += "\n\n可疑组件：" + "、".join(suspects)
        messagebox.showwarning("日志分析结果", msg)

    def _upload_log_ui(self):
        """上传到 mclo.gs（第三方）做深度分析。"""
        if not messagebox.askyesno(
                "上传到 mclo.gs",
                "会把当前日志内容发到第三方网站 mclo.gs（Aternos 运营，"
                "专门做 Minecraft 日志分析）。\n\n"
                "日志里可能含服务器描述、玩家名等信息。要继续吗？"):
            return
        text = self._server_log_tail()
        if not text.strip():
            messagebox.showinfo("上传", "没有可上传的日志内容")
            return
        tid = self.task_start("上传日志到 mclo.gs")
        self.lbl_diag.configure(text="⏳ 正在上传…", text_color="#f39c12")

        def task():
            try:
                url = upload_log_to_mclogs(text)
                self.task_done(tid, url)
                self.after(0, lambda u=url: self.lbl_diag.configure(
                    text=f"✅ 已上传：{u}", text_color="#2ecc71"))
                self.after(0, lambda u=url: self._append_console(
                    f"[诊断] 日志已上传：{u}\n"))
                try:
                    self.clipboard_clear()
                    self.clipboard_append(url)
                except Exception:
                    pass
                self.after(0, lambda u=url: messagebox.askyesno(
                    "上传成功",
                    f"日志已上传（链接已复制到剪贴板）：\n{u}\n\n"
                    f"现在用浏览器打开看分析结果吗？") and
                    __import__("webbrowser").open(u))
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                self.task_fail(tid, err)
                self.after(0, lambda t=err: self.lbl_diag.configure(
                    text=f"❌ 上传失败：{t}", text_color="#e74c3c"))

        threading.Thread(target=task, daemon=True).start()

    def _update_buttons(self):
        if self.is_running:
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="normal")
        else:
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="disabled")

    def _send_command(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        if not self.is_running or not self.server_process:
            # v3.0：以前这里静默 return，用户敲了指令没反应会以为程序坏了
            self._append_console("[启动器] 服务器没有在运行，指令未发送。\n")
            self.cmd_entry.delete(0, "end")
            return
        try:
            self.server_process.stdin.write(cmd + "\n")
            self.server_process.stdin.flush()
            self._append_console(f"\n> {cmd}\n")
            self.cmd_entry.delete(0, "end")
        except Exception as e:
            self._append_console(
                f"[启动器] 发送失败: [{type(e).__name__}] {e}\n")


# ==================== 入口 ====================
if __name__ == "__main__":
    # v3.0：先开窗，再在后台检查/安装 Pillow。
    # 以前是 ensure_pillow() 先同步跑，没装 Pillow 时会“没有任何窗口”地静默装好几分钟，
    # 双击运行的人只会以为程序卡死了。
    app = LauncherApp()
    threading.Thread(target=ensure_pillow, daemon=True).start()
    app.mainloop()