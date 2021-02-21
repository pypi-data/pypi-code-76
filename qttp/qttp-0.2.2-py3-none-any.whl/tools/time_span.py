import pandas as pd

def time_span(df, span="24h", base="9h"):
    df_span = pd.DataFrame()
    df_span['open'] = df['open'].resample(span, offset=base).first()
    df_span['high'] = df['high'].resample(span, offset=base).max()
    df_span['low'] = df['low'].resample(span, offset=base).min()
    df_span['close'] = df['close'].resample(span, offset=base).last()
    df_span['volume'] = df['volume'].resample(span, offset=base).sum()
    return df_span
