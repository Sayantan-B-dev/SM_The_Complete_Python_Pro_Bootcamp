import pandas as pd

def get_launch_stats():
    df = pd.read_csv('data/launches.csv')
    stats = {
        'total': len(df),
        'by_agency': df['agency'].value_counts().to_dict(),
        'by_status': df['status'].value_counts().to_dict(),
        'by_location': df['location'].value_counts().head(10).to_dict(),
    }
    # extract month from date string
    df['month'] = df['date'].str.extract(r'([A-Z][a-z]+)')  # e.g., "March"
    stats['by_month'] = df['month'].value_counts().to_dict()
    return stats