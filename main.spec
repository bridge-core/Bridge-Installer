# -*- mode: python ; coding: utf-8 -*-

a = Analysis(['src\\main.py'],
             pathex=['C:\\Users\\Flavia\\PycharmProjects\\Bridge-installer'],
             binaries=[],
             datas=[('icon.png', 'icon.png')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=True)
pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=None)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Bridge. installer',
          debug=False,
          bootloader_ignore_signals=True,
          strip=True,
          upx=True,
          console=True,
          icon='icon.png')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=True,
               upx=True,
               upx_exclude=[],
               name='Bridge. installer')
