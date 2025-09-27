import pandas as pd
from src.transform import transform_data

def test_transform_returns_list_of_dicts():
    # Mock data
    mock_df = pd.DataFrame({
        'year': [2025, 2025],
        'month': [6, 6],
        'stav_cizineckého_prukazu': ['povolen', 'povolen'],
        'státní_příslušnost': ['Polsko', 'Německo'],
        'počet_bodů': [10, 20]
    })
    result = transform_data(mock_df)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]['country'] == 'Německo'  # sorted by points desc
    assert result[0]['total_points'] == 20