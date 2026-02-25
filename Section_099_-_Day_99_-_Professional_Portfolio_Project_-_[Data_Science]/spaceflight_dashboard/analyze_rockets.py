import pandas as pd

def get_rocket_stats():
    df = pd.read_csv('data/rockets.csv')
    stats = {
        'total': len(df),
        'by_agency': df['agency'].value_counts().to_dict()
    }
    return stats