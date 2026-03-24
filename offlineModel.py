import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def generate_lookup_table(input_csv_path, output_csv_path):
    df = pd.read_csv(input_csv_path, parse_dates=['timestamp'])
    
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['hour'] = df['timestamp'].dt.hour
    df['minute'] = df['timestamp'].dt.minute
    
    X = df[['day_of_week', 'hour', 'minute']]
    y = df['qps']
    
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)
    
    lookup_data = []
    days_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    for d in range(7):
        for h in range(24):
            for m in [0, 15, 30, 45]:
                lookup_data.append({'day_num': d, 'hour': h, 'minute': m})
                
    lookup_df = pd.DataFrame(lookup_data)
    predictions = model.predict(lookup_df[['day_num', 'hour', 'minute']])
    
    final_table = []
    for idx, row in lookup_df.iterrows():
        day_name = days_map[row['day_num']]
        timeslot = f"{day_name}-{int(row['hour']):02d}-{int(row['minute']):02d}"
        final_table.append({
            'Timeslot': timeslot,
            'ExpectedLoad': round(predictions[idx], 2)
        })
        
    final_df = pd.DataFrame(final_table)
    final_df.to_csv(output_csv_path, index=False)
    return final_df

if __name__ == "__main__":
    generate_lookup_table('historical_year_traffic.csv', 'scaling_lookup_table.csv')
