# processors.py
import pandas as pd
import config

def process_kpi_channel_data(df: pd.DataFrame) -> pd.DataFrame:
    """处理KPI CHANNEL数据，按wau对渠道进行排名和分组。"""
    df_recent = df[df['weekid'] > (max(df['weekid']) - 6)].copy()
    
    # 按wau总和对affcode进行排名
    rkdk_channel = df_recent.groupby('affcode')['wau'].sum().reset_index()
    rkdk_channel = rkdk_channel.sort_values(by='wau', ascending=False)
    rkdk_channel['row_number'] = rkdk_channel['wau'].rank(ascending=False, method='first')
    
    # 合并排名信息
    df_merged = pd.merge(df_recent, rkdk_channel[['affcode', 'row_number']], how='left', on='affcode')
    
    # 将排名低的渠道分组为'others'
    df_merged.loc[df_merged["row_number"] > 9, "affcode"] = 'others'
    
    # 按周、md和affcode重新聚合
    df_processed = df_merged.groupby(['week', 'md', 'affcode']).agg({'wau': "sum", 'wnu': "sum"}).reset_index()
    return df_processed

def process_cur_spend_data(df: pd.DataFrame) -> pd.DataFrame:
    """处理货币消耗数据，对消耗活动进行排名和分组。"""
    df['date'] = pd.to_datetime(df.day, format='%Y%m%d')
    df_recent = df[df['date'].isin(pd.date_range(df['date'].max() - pd.to_timedelta(90, unit="D"), df['date'].max()))].copy()

    # 对消耗活动(a_typ)进行排名
    rkdc_spend = df_recent.groupby('a_typ')['totaldiamond'].sum().reset_index()
    rkdc_spend = rkdc_spend.sort_values(by='totaldiamond', ascending=False).reset_index(drop=True)
    rkdc_spend['row_number'] = rkdc_spend['totaldiamond'].rank(ascending=False, method='first')

    df_merged = pd.merge(df_recent, rkdc_spend[['a_typ', 'row_number']], how='left', on='a_typ')
    
    # 将排名低的活动分组为'其他活动'
    df_merged.loc[df_merged["row_number"] >= 10, 'a_typ'] = '其他活动'
    
    # 计算净消耗并重新聚合
    if 'backdiamond' in df_merged.columns:
        df_merged['totaldiamond'] = df_merged['totaldiamond'] - df_merged['backdiamond']
    
    df_processed = df_merged.groupby(['day', 'date', 'a_typ']).agg({'totaldiamond': "sum", 'paiddiamond': "sum"}).reset_index()
    
    return df_processed

def process_activity_data(df: pd.DataFrame, date_col='day', date_format='%Y%m%d') -> pd.DataFrame:
    """通用活动数据处理，添加排名和映射VIP类型。"""
    df['date'] = pd.to_datetime(df[date_col], format=date_format)
    df_sorted = df.sort_values(by='date', ascending=False)
    df_sorted['row_number'] = df_sorted['date'].rank(ascending=False, method='dense')
    
    df_filtered = df_sorted[df_sorted['zonetype'] != '疑似内网用户'].copy()
    
    # 使用config中的映射
    df_filtered['viptype_code'] = df_filtered['viptype'].map(config.VIP_TYPE_MAPPING)
    
    return df_filtered
