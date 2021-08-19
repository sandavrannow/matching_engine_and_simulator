from Engine import Engine

print( "This is an order matching simulator, you need to provide some details about what you want to simulate " )
print( "We will be asking you some questions about the desired simulation type and then perform the simulation " )

trading_engine = Engine()
user_amount = int( input( "User Amount : " ) )
unique_stock_amount = int( input( "Unique Stock Amount : " ) )
cash_per_user = int( input( "Cash Per User : " ) )

stock_amount_per_user = int( input( "Stock Amount Per User : " ) )
required_quantity_of_orders = int( input( "Required Quantity Of Orders : " ) )
price_range_from = int( input( "Price Range From : " ) )


price_range_to = int( input( "Price Range To : " ) )
quantity_range_from = int( input( "Quantity Range From : " ) )


quantity_range_to = int( input( "Quantity Range To : " ) )
trading_engine.run_simulation(user_amount, unique_stock_amount, cash_per_user, stock_amount_per_user, required_quantity_of_orders, price_range_from, price_range_to, quantity_range_from, quantity_range_to)  # ( self , user_amount , unique_stock_amount , cash_per_user , stock_amount_per_user , required_quantity_of_orders , price_range_from , price_range_to , quantity_range_from , quantity_range_to )
