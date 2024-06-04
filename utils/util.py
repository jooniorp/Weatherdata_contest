import pandas as pd

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    데이터프레임의 칼럼명에서 접두사를 제거하고, 칼럼명을 매핑에 따라 변경.

    Args:
        df (pd.DataFrame): 원본 데이터프레임

    Returns:
        pd.DataFrame: 칼럼명이 정리된 데이터프레임
    """
    
    mapping = {
    'tm': '날짜', 'hh24': '시간', 'weekday': '요일', 'week_name': '주중_주말', 'sum_qctr': '계약전력합계',
    'n': '공동주택수', 'sum_load': '전력수요_합계', 'n_mean_load': '전력부하량_평균', 'elec': '전력기상지수',
    'num': '격자넘버', 'stn': '지점번호', 'nph_ta': '기온', 'nph_hm': '상대습도', 'nph_ws_10m': '풍속',
    'nph_rn_60m': '강수량', 'nph_ta_chi': '체감온도'
    }

    prefix_to_remove = 'electric_train.'
    
    
    # 접두사 제거
    df.columns = [col.replace(prefix_to_remove, '') for col in df.columns]
    
    # 칼럼명 변경
    df = df.rename(columns=mapping)
    
    return df