"""
src/etl.py

Dashboard için temel veri yükleme, temizlik ve aggregate fonksiyonları.
Amaç: notebook'lardan bağımsız, tekrar kullanılabilir fonksiyonlar sunmak.
"""
from typing import Optional
import pandas as pd

def load_csv(path: str, parse_dates: Optional[list] = None) -> pd.DataFrame:
    """CSV dosyasını yükler."""
    if parse_dates:
        return pd.read_csv(path, parse_dates=parse_dates)
    return pd.read_csv(path)

def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Basit temizlik adımları:
    - Tarih parse (varsa)
    - Gereken sütunların varlığını kontrol
    - Negatif/0 quantity filtreleme
    - NaN satırların temizlenmesi
    """
    df = df.copy()
    # Tarih isimleri farklı olabilir; yaygın kolon isimlerini kontrol et
    date_cols = [c for c in ['Date', 'date', 'OrderDate', 'order_date'] if c in df.columns]
    if date_cols:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
        df = df.dropna(subset=[date_cols[0]])
        df = df.rename(columns={date_cols[0]: 'date'})
    # Quantity temizleme
    for qcol in ['Quantity', 'quantity', 'Qty']:
        if qcol in df.columns:
            df = df[df[qcol] > 0]
            df = df.rename(columns={qcol: 'quantity'})
            break
    # Price / Total kolonu normalizasyonu
    for tcol in ['Total', 'total', 'Sales', 'sales', 'Amount', 'amount']:
        if tcol in df.columns:
            df = df.rename(columns={tcol: 'total'})
            break
    # Basit NaN temizliği
    df = df.dropna(subset=['date'], how='any')
    return df

def aggregate_for_dashboard(df: pd.DataFrame, freq: str = 'D') -> pd.DataFrame:
    """Zamansal olarak aggregate edilmiş satış toplamı döner.
    freq: 'D' günlük, 'M' aylık, 'W' haftalık vb.
    """
    df = df.copy()
    if 'date' not in df.columns or 'total' not in df.columns:
        return pd.DataFrame()
    df['date'] = pd.to_datetime(df['date'])
    agg = df.set_index('date').resample(freq)['total'].sum().reset_index()
    agg.columns = ['date', 'total_sales']
    return agg
