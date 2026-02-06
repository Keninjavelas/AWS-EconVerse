import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Your actual live API
API_URL = "https://rpb9ezyy63.execute-api.us-east-1.amazonaws.com/state"

print(f"🔌 Connecting to EconVerse at: {API_URL}")
try:
    response = requests.get(API_URL)
    data = response.json()
    
    print("✅ Data received. Processing...")

    # Extract Data
    ticks = data['feed']
    timestamps = []
    prices = []

    for tick in ticks:
        # Convert ISO timestamp to readable time
        dt = datetime.fromisoformat(tick['Timestamp'])
        timestamps.append(dt.strftime("%H:%M"))
        # Ensure price is a float
        prices.append(float(tick['Price']))

    # Reverse so oldest is on the left
    timestamps.reverse()
    prices.reverse()

    # Draw the Graph
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, prices, marker='o', linestyle='-', color='#007acc', linewidth=2)
    
    plt.title(f"EconVerse Live Asset Tracking: {ticks[0]['PK']}", fontsize=14)
    plt.xlabel("Simulation Time (UTC)", fontsize=12)
    plt.ylabel("Price (USD)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save it
    filename = "econverse_status.png"
    plt.savefig(filename)
    print(f"🎉 Success! Chart saved as '{filename}'. Open it to see your economy.")

except Exception as e:
    print(f"❌ Error: {e}")
