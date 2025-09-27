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
        'rok': 'year',
        'měsíc': 'month',
        'stav_cizineckého_prukazu': 'residence_status',
        'státní_příslušnost': 'country',
        'počet_bodů': 'points'
    })

    # Handle possible encoding issues (replace non-UTF chars if needed)
    df = df.astype(str).replace('nan', None)

    # Convert numeric
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['month'] = pd.to_numeric(df['month'], errors='coerce')
    df['points'] = pd.to_numeric(df['points'], errors='coerce')

    # Drop invalid rows
    df = df.dropna(subset=['country', 'points'])

    # Aggregate: total points by country
    summary = df.groupby('country')['points'].sum().reset_index()
    summary = summary.rename(columns={'points': 'total_points'})
    summary = summary.sort_values('total_points', ascending=False)

    return summary.to_dict(orient='records')