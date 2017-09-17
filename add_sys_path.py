"""
任意のディレクトリにある自作モジュールのインポート出来るように、
モジュールパスをsys.pathに追加する。
sys.pathに追加することは、あまり推奨されない。
ディレクトリ管理が複雑にならないよう、明確なルールのもと使用すること。
単に上位ディレクトリを追加したいだけなら、 `sys.path.append('../../')`等でよい。
"""

import sys
import os

def import_my_module(modulepath):
    if os.path.isabs(modulepath):
        p = os.path.dirname(modulepath)
    else:
        p = os.path.dirname(os.path.realpath(modulepath))

    sys.path.append(p)
    print("Added the module's directory path to 'sys.path' :", p)
