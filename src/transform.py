import pandas as pd
import io
import requests
from pathlib import Path

# Public dataset URL (from md.gov.cz)
DATA_URL = "https://md.gov.cz/MDCR/media/otevrenadata/ostatnidatovesady/Bodovani_ridici_cizinci_202506.csv"

def fetch_data():
    """Fetch CSV data from public URL."""
    response = requests.get(DATA_URL)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text), sep=",")

def transform_data(df=None):
    """
    Transform raw 
    - Rename columns for clarity
    - Add derived fields
    - Return clean JSON-serializable list
    """
    if df is None:
        df = fetch_data()

    # Clean column names (Czech → English-friendly)
    df = df.rename(columns={
        'stav_k_datu': 'year',
        'uzemi_txt': 'area',
        'pocet_bodovanych_ridicu': 'penalty_count',
        'celkovy_pocet_ridicu': 'drivers_count'
    })

    # Handle possible encoding issues (replace non-UTF chars if needed)
    df = df.astype(str).replace('nan', None)

    # Convert numeric
    df['penalty_count'] = pd.to_numeric(df['penalty_count'], errors='coerce')
    df['drivers_count'] = pd.to_numeric(df['drivers_count'], errors='coerce')
    #df['points'] = pd.to_numeric(df['points'], errors='coerce')

    # Drop invalid rows
    df = df.dropna(subset=['area', 'penalty_count'])

    # Aggregate: total points by country
    summary = df.groupby('area')['penalty_count'].sum().reset_index()
    summary = summary.rename(columns={'penalty_count': 'total_points'})
    summary = summary.sort_values('total_points', ascending=False)

    return summary.to_dict(orient='records')