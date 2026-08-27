# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Lore TUI."""

a = Analysis(
    ['src/lore/tui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        "textual",
        "textual.app",
        "textual.binding",
        "textual.containers",
        "textual.widgets",
        "textual.widgets._markdown",
        "textual.reactive",
        "textual.screen",
        "textual.suggester",
        "textual.events",
        "textual.message",
        "rich",
        "frontmatter",
        "yaml",
        "markdown",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='lore',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # TUI, no console window on Windows
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
