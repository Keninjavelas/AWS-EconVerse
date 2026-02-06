import random

class RetailStrategy:
    def decide(self, market_price, sentiment):
        # Simple Logic: If sentiment is high, Buy. If low, Sell.
        decision = None
        
        if sentiment > 0.7:
            decision = "BUY"
        elif sentiment < 0.3:
            decision = "SELL"
        else:
            # Random noise (Panic selling or FOMO)
            if random.random() > 0.9:
                decision = "BUY"
        
        return decision
