import time

def fetch_market_data(product_name):
    # Logic to simulate data extraction from global markets
    print(f"Searching for: {product_name}...")
    time.sleep(1) # Simulates network processing
    
    # Professional logic: Returning structured data
    market_results = {
        "Amazon": 450.99,
        "eBay": 445.50,
        "Walmart": 460.00
    }
    return market_results

# Execute analysis
results = fetch_market_data("Enterprise Server")
for store, price in results.items():
    print(f"Store: {store} | Price: ${price}")