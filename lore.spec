# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Lore TUI."""

from PyInstaller.utils.hooks import collect_all, collect_submodules

textual_datas, textual_binaries, textual_hidden = collect_all("textual")
rich_datas, rich_binaries, rich_hidden = collect_all("rich")

a = Analysis(
    ['src/lore/tui.py'],
    pathex=['src'],
    binaries=textual_binaries + rich_binaries,
    datas=textual_datas + rich_datas,
    hiddenimports=textual_hidden
    + rich_hidden
    + collect_submodules("textual.widgets")
    + [
        "textual.widgets._markdown",
        "textual.widgets._markdown_viewer",
        "textual.widgets._tabs",
        "textual.widgets._list_view",
        "textual.widgets._list_item",
        "textual.widgets._static",
        "textual.widgets._label",
        "textual.widgets._header",
        "textual.widgets._footer",
        "textual.widgets._input",
        "textual.widgets._button",
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
    console=True,  # TUI requires a console — windowed (False) leaves stdin=None and crashes win32 driver
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
