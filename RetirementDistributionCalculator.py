import numpy as np

def calculate_sustainable_distribution(
    starting_balance: float, 
    years: int, 
    annual_return: float, 
    inflation_rate: float
) -> float:
    """
    Calculate a sustainable annual distribution amount that maintains purchasing power
    over a specified number of years, considering investment returns and inflation.
    
    Args:
        starting_balance (float): Initial investment amount
        years (int): Number of years for distribution
        annual_return (float): Expected annual investment return (as decimal)
        inflation_rate (float): Expected annual inflation rate (as decimal)
    
    Returns:
        float: Initial annual distribution amount that can be sustained
    """
    # Validate inputs
    if starting_balance <= 0 or years <= 0:
        raise ValueError("Starting balance and years must be positive")
    
    # Calculate real return (inflation-adjusted return)
    real_return = (1 + annual_return) / (1 + inflation_rate) - 1
    
    # If real return is negative or zero, distribution is not sustainable
    if real_return <= 0:
        return 0
    
    # Calculate sustainable distribution factor using present value of an annuity formula
    # Adjusted to account for inflation-linked withdrawals
    numerator = real_return
    denominator = 1 - (1 / ((1 + real_return) ** years))
    
    sustainable_distribution = starting_balance * (numerator / denominator)
    
    return sustainable_distribution

# Example usage and demonstration
def demonstrate_sustainability():
    # Scenario parameters
    starting_balance = 1798000  # $2,212,000 starting balance
    years = 50  # 50 years of distribution
    annual_return = 0.06  # 5% expected annual return
    inflation_rate = 0.03  # 3% expected inflation

    # Calculate sustainable distribution
    annual_distribution = calculate_sustainable_distribution(
        starting_balance, years, annual_return, inflation_rate
    )
    
    print(f"Starting Balance: ${starting_balance:,.2f}")
    print(f"Years of Distribution: {years}")
    print(f"Expected Annual Return: {annual_return:.2%}")
    print(f"Expected Inflation Rate: {inflation_rate:.2%}")
    print(f"Sustainable Annual Distribution: ${annual_distribution:,.2f}")
    
    # Verify sustainability with a simulation
    def simulate_distribution():
        balance = starting_balance
        for year in range(years):
            # Grow balance
            balance *= (1 + annual_return)
            
            # Subtract inflation-adjusted distribution
            distribution = annual_distribution * ((1 + inflation_rate) ** year)
            balance -= distribution
            
            # Check if balance becomes negative
            if balance < 0:
                return False, year
        
        return True, years

    sustainable, final_year = simulate_distribution()
    print(f"Distribution Sustainable: {sustainable}")
    print(f"Final Year of Distribution: {final_year}")

# Run the demonstration
demonstrate_sustainability()