# -*- mode: python ; coding: utf-8 -*-
# 打包命令：pyinstaller wow.spec
# 产物：dist/wow.exe
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]
try:                                   # 拖拽依赖，没装也能打包
    tmp_ret = collect_all('tkinterdnd2')
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]
except Exception:
    pass
# 这两个是函数内延迟导入的，写明白免得打包漏掉
# （nbtlib 会拖上 numpy，exe 会因此变大，但"看玩家背包"在 exe 里要能用）
hiddenimports += ['yaml', 'nbtlib']


a = Analysis(
    ['minecraft-simple-server-launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='minecraft-simple-server-launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
