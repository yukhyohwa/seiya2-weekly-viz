# processors.py
import pandas as pd
from .. import config

def process_kpi_channel_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process KPI CHANNEL data, ranking and grouping channels by WAU."""
    df_recent = df[df['weekid'] > (max(df['weekid']) - 6)].copy()
    
    # Rank affcode by sum of WAU
    rkdk_channel = df_recent.groupby('affcode')['wau'].sum().reset_index()
    rkdk_channel = rkdk_channel.sort_values(by='wau', ascending=False)
    rkdk_channel['row_number'] = rkdk_channel['wau'].rank(ascending=False, method='first')
    
    # Merge ranking information
    df_merged = pd.merge(df_recent, rkdk_channel[['affcode', 'row_number']], how='left', on='affcode')
    
    # Group low-ranking channels as 'others'
    df_merged.loc[df_merged["row_number"] > 9, "affcode"] = 'others'
    
    # Re-aggregate by week, md, and affcode
    df_processed = df_merged.groupby(['week', 'md', 'affcode']).agg({'wau': "sum", 'wnu': "sum"}).reset_index()
    return df_processed

def process_cur_spend_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process currency consumption data, ranking and grouping consumption activities."""
    df['date'] = pd.to_datetime(df.day, format='%Y%m%d')
    df_recent = df[df['date'].isin(pd.date_range(df['date'].max() - pd.to_timedelta(90, unit="D"), df['date'].max()))].copy()

    # Rank consumption activities (a_typ)
    rkdc_spend = df_recent.groupby('a_typ')['totaldiamond'].sum().reset_index()
    rkdc_spend = rkdc_spend.sort_values(by='totaldiamond', ascending=False).reset_index(drop=True)
    rkdc_spend['row_number'] = rkdc_spend['totaldiamond'].rank(ascending=False, method='first')

    df_merged = pd.merge(df_recent, rkdc_spend[['a_typ', 'row_number']], how='left', on='a_typ')
    
    # Group low-ranking activities as 'others'
    df_merged.loc[df_merged["row_number"] >= 10, 'a_typ'] = 'others'
    
    # Calculate net consumption and re-aggregate
    if 'backdiamond' in df_merged.columns:
        df_merged['totaldiamond'] = df_merged['totaldiamond'] - df_merged['backdiamond']
    
    df_processed = df_merged.groupby(['day', 'date', 'a_typ']).agg({'totaldiamond': "sum", 'paiddiamond': "sum"}).reset_index()
    
    return df_processed

def process_activity_data(df: pd.DataFrame, date_col='day', date_format='%Y%m%d') -> pd.DataFrame:
    """Generic activity data processing, adding ranking and mapping VIP types."""
    df['date'] = pd.to_datetime(df[date_col], format=date_format)
    df_sorted = df.sort_values(by='date', ascending=False)
    df_sorted['row_number'] = df_sorted['date'].rank(ascending=False, method='dense')
    
    df_filtered = df_sorted[df_sorted['zonetype'] != 'Potential Internal User'].copy()
    
    # Use mappings from config
    df_filtered['viptype_code'] = df_filtered['viptype'].map(config.VIP_TYPE_MAPPING)
    
    return df_filtered
