class OrderBook:
    def __init__(self, current_price):
        self.bids = [] # Buy orders
        self.asks = [] # Sell orders
        self.last_price = current_price

    def add_order(self, order):
        # order = {id, type: 'BUY'/'SELL', price, amount}
        if order['type'] == 'BUY':
            self.bids.append(order)
        else:
            self.asks.append(order)

    def match(self):
        # Sort: High bids first, Low asks first
        self.bids.sort(key=lambda x: x['price'], reverse=True)
        self.asks.sort(key=lambda x: x['price'])

        matched_volume = 0
        
        # Simple MVP Matching Logic:
        # If highest bid >= lowest ask, we have a trade.
        # For this simulation, we just take the mid-point as the clearing price.
        if self.bids and self.asks:
            best_bid = self.bids[0]['price']
            best_ask = self.asks[0]['price']

            if best_bid >= best_ask:
                clearing_price = (best_bid + best_ask) / 2
                self.last_price = clearing_price
                matched_volume = min(len(self.bids), len(self.asks)) # Mock volume
        
        return self.last_price, matched_volume
