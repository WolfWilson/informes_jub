# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

datas = [('Source/wolf.png', 'Source'), ('Source/generar.png', 'Source'), ('Source/toexcel2.png', 'Source'), ('Source/graphics.png', 'Source'), ('Source/save.png', 'Source'), ('Modules/styles.py', 'Modules'), ('Modules/database_utils.py', 'Modules'), ('Modules/graficos.py', 'Modules')]
hiddenimports = ['pandas', 'pandas._libs']
datas += collect_data_files('pandas')
hiddenimports += collect_submodules('pandas')


a = Analysis(
    ['informes_v4.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas.tests'],
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
    name='informes_v4',
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
    icon=['wolf.ico'],
)
