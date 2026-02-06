class MacroState:
    def __init__(self):
        self.gdp = 100000.0  # Starting GDP in billions
        self.inflation = 2.0  # Starting inflation rate (%)
    
    def update_gdp(self, growth_rate):
        """Update GDP based on growth rate"""
        self.gdp = self.gdp * (1 + growth_rate)
        return self.gdp
    
    def update_inflation(self, asset_price):
        """Update inflation based on asset price movements (simplified model)"""
        # Simple mock: if BTC price is high, inflation tends to be lower
        if asset_price > 50000:
            self.inflation = 1.5
        elif asset_price > 40000:
            self.inflation = 2.5
        else:
            self.inflation = 4.0
        return self.inflation
