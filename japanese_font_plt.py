"""
このモジュールをimportするだけで、matplotlib系の出力に日本語フォントが使えるようになります。
使用するフォント名は、環境に合わせて変更してください。
注意1:
    seaborn等、matplotlibの見た目を上書きするモジュールをimportする場合は、
    その後の行でこのモジュールをimportしてください。
    例）
    import seaborn as sns
    import japanese_font_plt   # seabornの後の行でimport
注意2:
    うまく表示されない場合は、フォントキャッシュの削除を試してみてください。
    手順)
    1.フォントキャッシュの場所を確認
        import matplotlib
        print(matplotlib.get_cachedir())
        -> /home/(ユーザー名)/.cache/matplotlib/*.cache  # 環境に依存します
    2.フォントキャッシュを削除
        rm /home/(ユーザー名)tk/.cache/matplotlib/*.cache
注意3:
    指定すべきフォント名が分からない場合は、こちらを参考に。
    for font in fonts:
        print(str(font), '\t', fm.FontProperties(fname=font).get_name())
"""

from matplotlib import rcParams
rcParams['font.sans-serif'] = 'Source Han Code JP'
rcParams['font.weight'] = 'regular'
# rcParams['axes.titlesize'] = 15
# rcParams['xtick.labelsize'] = 12
# rcParams['ytick.labelsize'] = 12
