# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['professional_ui_robust.py'],
    pathex=[],
    binaries=[],
    datas=[('plugins', 'plugins'), ('core', 'core'), ('config', 'config'), ('models', 'models'), ('utils', 'utils'), ('frontend', 'frontend'), ('threat_intel', 'threat_intel')],
    hiddenimports=['core', 'core.engine', 'core.plugin_manager', 'core.plugin_registry', 'core.event_bus', 'core.interfaces', 'core.base_plugin'],
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
    name='professional_ui_robust_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
