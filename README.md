# myutil
## 自作モジュール

### add_sys_path
任意の場所にあるモジュールのディレクトリパスを、sys.pathに追加する

### japanese_font_plt
matplotlib系のグラフで、日本語フォトを表示できるようにする。
このモジュールをimportするだけで良い。

### post2slack
Slackに投稿

### text_proc
形態素解析をして、指定の品詞を抽出して分かち書きファイルを出力する。半角全角変換も可能。

### df_mem_shrinker
pandas.DataFrameを投入すると、カラムの型をデータに合わせて最適化して、メモリサイズを縮小する。
他、一定サイズを超えるオブジェクトの一覧を表示する関数等。
【注意】精度を縮小した後に、精度を超える更新・代入を実行しても、エラーにならずに不正な値になってしまうので注意すること。
