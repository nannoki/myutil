
import numpy as np
import pandas as pd


def show_dfsize(df, unit=2):
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
    float
        unitに応じたデータフレームのサイズ
    """

    unit_dict = {1: 'KB',
                 2: 'MB',
                 3: 'GB'}
    assert unit in unit_dict.keys(), 'unitは1(KB), 2(MB), 3(GB)のいずれか'
    mem = df.memory_usage(index=True).sum() / 1024 ** unit
    print('{:.4f} {}'.format(mem, unit_dict[unit]))

    return mem


def cast_smaller_dtype(df):
    """
    データフレームの各カラムの型を最適化して、省メモリ化する。
    整数はデータの値は変わらないが、小数は倍精度(float64)から単精度(float32)に変わる。

    Parameters
    ----------
    df: pd.DataFrame
        メモリを縮小させたいデータフレーム

    Returns
    -------
    なし。渡されたデータフレーム自体を更新する。

    """

    def _show_info(df1, msg):
        """
        情報表示用のヘルパー関数
        """
        print('-' * 30, msg, '-' * 30)
        show_dfsize(df1)
        print()
        print(df1.info())
        print(df1.memory_usage())
    
    _show_info(df, 'Before')
    
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
    
