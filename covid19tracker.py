import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load COVID-19 dataset (replace with your actual data path)
try:
    df = pd.read_csv('covid_global_data.csv', parse_dates=['Date'])
    print("Data loaded successfully!")
    print(f"Total records: {len(df)}")
except FileNotFoundError:
    print("Error: Data file not found. Using sample data instead.")
    # Sample data fallback
    data = {
        'Date': pd.date_range(start='2023-01-01', periods=30),
        'Country': ['USA']*15 + ['India']*15,
        'Confirmed': list(range(100, 115)) + list(range(50, 65)),
        'Deaths': list(range(1, 16)) + list(range(1, 16)),
        'Recovered': list(range(80, 95)) + list(range(40, 55))
    }
    df = pd.DataFrame(data)

# Data Cleaning
df.fillna(0, inplace=True)
df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

# Analysis Functions
def get_latest_stats():
    latest_date = df['Date'].max()
    return df[df['Date'] == latest_date]

def country_trend(country):
    return df[df['Country'] == country].sort_values('Date')

# Visualization Functions
def plot_global_trend():
    plt.figure(figsize=(12, 6))
    global_trend = df.groupby('Date').sum()
    sns.lineplot(data=global_trend, x='Date', y='Confirmed', label='Confirmed')
    sns.lineplot(data=global_trend, x='Date', y='Deaths', label='Deaths')
    sns.lineplot(data=global_trend, x='Date', y='Recovered', label='Recovered')
    plt.title('Global COVID-19 Trends')
    plt.ylabel('Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('global_trend.png')
    plt.show()

def plot_country_comparison():
    latest = get_latest_stats()
    top_countries = latest.nlargest(10, 'Confirmed')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_countries, x='Country', y='Confirmed')
    plt.title('Top 10 Countries by Confirmed Cases')
    plt.ylabel('Confirmed Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('country_comparison.png')
    plt.show()

# Interactive Menu
def main_menu():
    while True:
        print("\nCOVID-19 Data Tracker")
        print("1. Show global trends")
        print("2. Compare countries")
        print("3. View country-specific data")
        print("4. Export current data")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            plot_global_trend()
        elif choice == '2':
            plot_country_comparison()
        elif choice == '3':
            country = input("Enter country name: ")
            if country in df['Country'].unique():
                print(country_trend(country).tail())
            else:
                print("Country not found in dataset")
        elif choice == '4':
            df.to_csv('covid_processed_data.csv', index=False)
            print("Data exported to covid_processed_data.csv")
        elif choice == '5':
            print("Stay safe! Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    print("COVID-19 GLOBAL DATA TRACKER")
    print(f"Data from {df['Date'].min().date()} to {df['Date'].max().date()}")
    main_menu()