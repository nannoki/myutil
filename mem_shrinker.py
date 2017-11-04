import sys

import numpy as np
import pandas as pd


def show_object_size(threshold, unit=2):
    """
    生きている全部の変数のサイズを表示する

    Parameters
    ----------
    threshold : int, float
        表示するサイズの下限しきい値。
        unitに応じた値にすること。
    unit : int
        表示するサイズの単位
        1: KB
        2: MB
        3: GB
    ex.
        100MB超の変数をGB単位で表示したい場合
        threshold=0.1, unit=3

    Returns
    -------
        なし
    """
    disp_unit = {1: 'KB', 2: 'MB', 3: 'GB'}
    threshold = threshold * 1024 ** unit
    # 処理中に変数が変動しないように固定
    globals_copy = globals().copy()
    for object_name in globals_copy.keys():
        size = sys.getsizeof(eval(object_name))
        if size > threshold:
            print('{:<15}{:.3f} {}'.format(object_name, size / 1024 ** unit, disp_unit[unit]))


def get_df_size(df, unit=2):
    """
    データフレームのサイズを返す

    Parameters
    ----------
    df : pd.DataFrame
    unit : int
        1: KB
        2: MB
        3: GB

    Returns
    -------
    (float) unitに応じたデータフレームのサイズ
    """

    unit_dict = {1: 'KB',
                 2: 'MB',
                 3: 'GB'}
    assert unit in unit_dict.keys(), 'unitは1(KB), 2(MB), 3(GB)のいずれか'
    mem = df.memory_usage(index=True).sum() / 1024 ** unit
    print('{:.4f} {}'.format(mem, unit_dict[unit]))

    return mem


def df_cast_smaller_dtype(df0, *, inplace=True):
    """
    データフレームの各カラムの型を最適化して、省メモリ化する。
    整数はデータの値は変わらないが、小数は倍精度(float64)から単精度(float32)に変わる。

    Parameters
    ----------
    df0: pd.DataFrame
        メモリを縮小させたいデータフレーム
    inplace: bool
        True: 引数のデータフレームを直接更新する。戻り値なし。
        False: 引数のデータフレームの更新はせず、コピーした更新済みデータフレームを返す。【注意】コピーした分のメモリが増える。

    Returns
    -------
        inplace=Trueの時: なし。渡されたデータフレーム自体を更新する。
        inplace=Falseの時: 更新済みデータフレームを返す。
    """

    def _show_info(df, msg):
        """
        情報表示用のヘルパー関数
        """
        print('-' * 30, msg, '-' * 30)
        get_df_size(df)
        print()
        print(df.info())
        print(df.memory_usage())

    _show_info(df0, 'Before')

    if inplace:
        # 参照代入。引数のデータフレームを直接更新する。
        df = df0
    else:
        # コピー。メモリが増える。
        print('【注意】 "inplace=False"が設定されています。処理過程でdfのコピーを作成する為、その分メモリを消費します。')
        df = df0.copy()


    print('-' * 30, 'Cast DF', '-' * 30)
    # int
    int_cols = df.select_dtypes(include=['int']).columns.tolist()
    for col in int_cols:
        if ((np.max(df[col]) <= 127) and(np.min(df[col] >= -128))):
            print('cast {} : {} -> {}'.format(col, df[col].dtype, 'np.int8'))
            df[col] = df[col].astype(np.int8)
        elif ((np.max(df[col]) <= 32767) and(np.min(df[col] >= -32768))):
            print('cast {} : {} -> {}'.format(col, df[col].dtype, 'np.int16'))
            df[col] = df[col].astype(np.int16)
        elif ((np.max(df[col]) <= 2147483647) and(np.min(df[col] >= -2147483648))):
            df[col] = df[col].astype(np.int32)
        else:
            df[col] = df[col].astype(np.int64)

    # float
    float_cols = df.select_dtypes(include=['float']).columns.tolist()
    for col in float_cols:
        df[col] = df[col].astype(np.float32)

    _show_info(df, 'After')

    print('-' * 65)

    if not inplace:
        return df
