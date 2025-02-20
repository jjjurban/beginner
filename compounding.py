try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as e:
    print(f"Error: {e}")
    print("Please install required libraries:")
    print("Run 'pip install matplotlib numpy' in your terminal")
    exit()

def compound_interest(principal, rate, time, compounds_per_year):
    """Calculate compound interest and return list of yearly values"""
    amounts = []
    for t in range(time + 1):
        amount = principal * (1 + rate/compounds_per_year)**(compounds_per_year * t)
        amounts.append(amount)
    return amounts

# Parameters
initial_investment = 1000  # Starting amount in dollars
annual_rate = 0.08        # 8% annual interest rate
years = 30               # Time period in years
compounds = 12           # Monthly compounding

# Calculate compound interest
time_points = list(range(years + 1))
compound_values = compound_interest(initial_investment, annual_rate, years, compounds)

# Calculate simple interest for comparison
simple_values = [initial_investment + (initial_investment * annual_rate * t) for t in time_points]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(time_points, compound_values, 'b-', label='Compound Interest (8% monthly)')
plt.plot(time_points, simple_values, 'r--', label='Simple Interest (8%)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.title('Compound Interest vs Simple Interest Growth\nStarting with $1000')
plt.xlabel('Years')
plt.ylabel('Amount ($)')
plt.legend()
plt.xticks(range(0, years + 1, 5))

# Add some key data points as text
final_compound = compound_values[-1]
final_simple = simple_values[-1]
plt.text(years, final_compound, f'${final_compound:.2f}', 
         verticalalignment='bottom', horizontalalignment='right')
plt.text(years, final_simple, f'${final_simple:.2f}', 
         verticalalignment='top', horizontalalignment='right')

plt.show()

# Print some key statistics
print(f"Initial Investment: ${initial_investment:.2f}")
print(f"After {years} years with compound interest: ${final_compound:.2f}")
print(f"After {years} years with simple interest: ${final_simple:.2f}")
print(f"Extra earnings from compounding: ${(final_compound - final_simple):.2f}")