def calculate_roi(initial_investment, current_balance):
    # ROI = Return on Investment logic
    profit = current_balance - initial_investment
    performance = (profit / initial_investment) * 100
    return f"Profit: ${profit} | Performance: {performance}%"

# Example: Starting with $1000 and reaching target
print(calculate_roi(1000, 2500))