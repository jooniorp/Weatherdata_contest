import pandas as pd
import numpy as np

def clean_column_names(df: pd.DataFrame, prefix_to_remove: str='electric_train.') -> pd.DataFrame:
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

    # 접두사 제거
    df.columns = [col.replace(prefix_to_remove, '') for col in df.columns]
    
    # 칼럼명 변경
    df = df.rename(columns=mapping)
    
    return df

def get_rscore(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    실제 값과 예측 값 사이의 피어슨 상관 계수(R-score)를 계산.
    
    이 함수는 두 데이터 집합 간의 선형 상관 관계를 측정하는 피어슨 상관 계수를 계산한다.
    반환되는 값은 -1과 1 사이이며:
     - 1은 완벽한 양의 선형 관계
     - -1은 완벽한 음의 선형 관계
     - 0은 선형 관계가 없음을 나타냄.

    Args:
        y_true (np.ndarray): 실제 값의 배열
        y_pred (np.ndarray): 예측 값의 배열

    Returns:
        float: 'y_true'와 'y_pred' 사이의 피어슨 상관 계수
    """
    return np.corrcoef(y_true, y_pred)[0, 1]

def calculate_power_index(df: pd.DataFrame, year: int, grid_number: int) -> pd.Series:
    """
    특정 연도와 격자넘버에 해당하는 전력기상지수를 계산하는 함수.

    Args:
        df (pd.DataFrame): 입력 데이터프레임
        year (int): 연도
        grid_number (int): 격자넘버

    Returns:
        pd.Series: 계산된 전력기상지수
    """
    # 날짜 칼럼이 datetime 타입인지 확인하고 변환
    if not pd.api.types.is_datetime64_any_dtype(df['날짜']):
        df['날짜'] = pd.to_datetime(df['날짜'])
        
    # 특정 연도와 격자넘버에 대한 마스크 생성
    mask = (df['날짜'].dt.year == year) & (df['격자넘버'] == grid_number)
    
    # 마스크를 사용하여 데이터 필터링
    df_masked = df[mask]
    
    # 전력기상지수 계산
    power_index = (df_masked['전력수요_합계'] / df_masked['전력수요_합계'].mean()) * 100
    
    return power_index