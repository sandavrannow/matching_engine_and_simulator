import heapq
import random
from User import User
from Order import Order
from Transaction import Transaction

class Engine :
    def __init__( self ) : # SIMULATION DATA ( self , user_amount , unique_stock_amount , cash_per_user , stock_amount_per_user , required_quantity_of_orders , price_range_from , price_range_to , quantity_range_from , quantity_range_to )
        self.user_hash_map_of_users = {}
        self.buy_hash_map_of_heaps = {}
        self.sell_hash_map_of_heaps = {}
        self.user_id_counter = 0
        self.order_id_counter = 0
        self.transaction_id_counter = 0


    def add_user( self , user_amount , cash_left , unique_stock_list , stock_amount_per_user ) :
        for i in range( user_amount ) :
            self.user_id_counter += 1
            stock_amount_hash_map = {}
            for stock_id in unique_stock_list:
                stock_amount_hash_map[stock_id] = stock_amount_per_user
            self.user_hash_map_of_users[ self.user_id_counter ] = User( self.user_id_counter , cash_left , stock_amount_hash_map  )

    def make_hash_map_of_heaps( self , unique_stock_list ) :
        for stock_id in unique_stock_list :
            self.buy_hash_map_of_heaps[ stock_id ] = []
            self.sell_hash_map_of_heaps[ stock_id ] = []

    def make_order_and_transfer( self , stock_id, user_id, price, quantity, order_type ) :
        self.add_order( stock_id, user_id, price, quantity, order_type )
        self.look_for_possible_transaction( stock_id )

    def add_order( self , stock_id, user_id, price, quantity, order_type ) :
        # INTEGERS ARE NOT MUTABLE SO WE CAN ASSIGN THEM DIRECTLY
        self.order_id_counter += 1

        this_order = Order( self.order_id_counter , stock_id , user_id , price , quantity , order_type ) # (self, order_id, stock_id, user_id, price, quantity, order_type )

        if this_order.order_type == "buy" :
            # ADD ORDER TO THE BUY HASH MAP OF HEAPS
            # BECAUSE BUY ORDER HEAPS ARE MAX HEAPS WE SHOULD DO THIS TIMES MINUS ONE TRICK
            print( f" Order Id = { this_order.order_id } < - - > Stock Id = { this_order.stock_id } < - - > User Id = { this_order.user_id } < - - > Price = { this_order.price } < - - > Quantity = { this_order.quantity } < - - > Order Type = { this_order.order_type } " ) # (self, order_id, stock_id, user_id, price, quantity, order_type )
            this_order.price = ( this_order.price * ( - 1 ) )
            heapq.heappush( self.buy_hash_map_of_heaps[ stock_id ] ,  this_order )

        elif this_order.order_type == "sell" :
            # ADD ORDER TO THE SELL HASH MAP OF HEAPS
            print( f" Order Id = { this_order.order_id } < - - > Stock Id = { this_order.stock_id } < - - > User Id = { this_order.user_id } < - - > Price = { this_order.price } < - - > Quantity = { this_order.quantity } < - - > Order Type = { this_order.order_type } " ) # (self, order_id, stock_id, user_id, price, quantity, order_type )
            heapq.heappush( self.sell_hash_map_of_heaps[ stock_id ] , this_order )


    def look_for_possible_transaction( self , stock_id ) :
        if self.is_there_any_buy_orders( stock_id ) == True and self.is_there_any_sell_orders( stock_id ) == True :

            if self.look_largest_buy_order( stock_id ).get_price() * ( - 1 ) >= self.look_smallest_sell_order( stock_id ).get_price() :

                # INSIDE THE HEAP THE BUY ORDER IS NEGATIVE SO MAKE IT BACK TO POSITIVE
                largest_buy = self.get_largest_buy_order( stock_id )
                largest_buy.price = largest_buy.price * ( - 1 )
                smallest_sell = self.get_smallest_sell_order( stock_id )

                # CALCULATE FINAL PRICE
                final_price = self.calculate_final_price( largest_buy , smallest_sell )

                # WE SAVE MANY CODE BY FIRST CHECKING DOES THE USER HAVE THE REQUIREMENTS AND THEN EXECUTING AS OPPOSED TO CHECKING THAT FACT AT THE TIME OF TRANSACTION
                if self.is_buy_possible( largest_buy.user_id , ( final_price * largest_buy.get_quantity() ) ) == False and self.is_sell_possible( smallest_sell.user_id , smallest_sell.stock_id , smallest_sell.get_quantity() ) == False :
                    pass

                elif self.is_buy_possible( largest_buy.user_id , ( final_price * largest_buy.get_quantity() ) ) == False and self.is_sell_possible( smallest_sell.user_id , smallest_sell.stock_id , smallest_sell.get_quantity() ) == True :
                    # ONLY PUSH BACK THE SELL ORDER AND LET THE BUY ORDER DISAPPEAR AS USER DOES NOT HAVE THE REQUIREMENTS

                    self.make_order_and_transfer( stock_id, smallest_sell.get_user_id() , smallest_sell.get_price() , smallest_sell.get_quantity() , "sell" )

                elif self.is_buy_possible( largest_buy.user_id , ( final_price * largest_buy.get_quantity() ) ) == True and self.is_sell_possible( smallest_sell.user_id , smallest_sell.stock_id , smallest_sell.get_quantity() ) == False :
                    # ONLY PUSH BACK THE BUY ORDER AND LET THE SELL ORDER DISAPPEAR AS USER DOES NOT HAVE THE REQUIREMENTS

                    self.make_order_and_transfer( stock_id, largest_buy.get_user_id(), largest_buy.get_price(), largest_buy.get_quantity(), "buy" )

                    # THEY BOTH HAVE THE REQUIREMENTS SO MAKE THE TRANSACTION NOW
                elif self.is_buy_possible( largest_buy.user_id , ( final_price * largest_buy.get_quantity() ) ) == True and self.is_sell_possible( smallest_sell.user_id , smallest_sell.stock_id , smallest_sell.get_quantity() ) == True :

                    # THE ORDER AMOUNTS DO MATCH SO JUST MAKE THE TRANSACTION AND DO NOT PUSH ANY ORDERS BACK
                    if largest_buy.get_quantity() == smallest_sell.get_quantity() :
                        self.transaction_id_counter += 1
                        this_transaction = Transaction( self.transaction_id_counter , stock_id , largest_buy.get_user_id() , smallest_sell.get_user_id() , final_price , largest_buy.get_quantity() ) # ( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity )
                        print( f" Transaction Id = { this_transaction.transaction_id } < - - > Stock Id = { this_transaction.stock_id } < - - > Buyer Id = { this_transaction.buyer_id } < - - > Seller Id = { this_transaction.seller_id } < - - > Price = { this_transaction.price } < - - > Quantity = { this_transaction.quantity } " ) # ( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity )
                        self.make_cash_stock_transfer( this_transaction.get_total_transaction_price() , this_transaction.get_stock_id() , this_transaction.get_quantity() , this_transaction.get_buyer_id() , this_transaction.get_seller_id() ) # ( self , cash_amount , stock_id , stock_amount , buyer_id , seller_id )

                        # MAKE THE TRANSACTION BUT THEN PUSH THE REMAINING QUANTITY OF THE BUY ORDER BACK
                    elif largest_buy.get_quantity() > smallest_sell.get_quantity() :
                        amount_left = largest_buy.get_quantity() - smallest_sell.get_quantity()
                        self.transaction_id_counter += 1
                        this_transaction = Transaction( self.transaction_id_counter, stock_id, largest_buy.get_user_id(), smallest_sell.get_user_id(), final_price, smallest_sell.get_quantity() ) # ( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity )
                        print( f" Transaction Id = { this_transaction.transaction_id } < - - > Stock Id = { this_transaction.stock_id } < - - > Buyer Id = { this_transaction.buyer_id } < - - > Seller Id = { this_transaction.seller_id } < - - > Price = { this_transaction.price } < - - > Quantity = { this_transaction.quantity } " ) # ( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity )
                        self.make_cash_stock_transfer( this_transaction.get_total_transaction_price() , this_transaction.get_stock_id() , this_transaction.get_quantity() , this_transaction.get_buyer_id() , this_transaction.get_seller_id() ) # ( self , cash_amount , stock_id , stock_amount , buyer_id , seller_id )
                        # PUSH THE REMAINING BUY ORDER BACK
                        # RECURSE NOW

                        self.make_order_and_transfer( smallest_sell.stock_id, largest_buy.user_id , largest_buy.price , amount_left , "buy" )

                    # MAKE THE TRANSACTION BUT THEN PUSH THE REMAINING QUANTITY OF THE SELL ORDER BACK
                    elif largest_buy.get_quantity() < smallest_sell.get_quantity() :
                        amount_left = smallest_sell.get_quantity() - largest_buy.get_quantity()


                        self.transaction_id_counter += 1
                        this_transaction = Transaction(self.transaction_id_counter, stock_id, largest_buy.get_user_id(),smallest_sell.get_user_id(), final_price, largest_buy.get_quantity()) # ( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity )
                        print( f" Transaction Id = { this_transaction.transaction_id } < - - > Stock Id = { this_transaction.stock_id } < - - > Buyer Id = { this_transaction.buyer_id } < - - > Seller Id = { this_transaction.seller_id } < - - > Price = { this_transaction.price } < - - > Quantity = { this_transaction.quantity } " ) # ( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity )
                        self.make_cash_stock_transfer( this_transaction.get_total_transaction_price() , this_transaction.get_stock_id() , this_transaction.get_quantity() , this_transaction.get_buyer_id() , this_transaction.get_seller_id() ) # ( self , cash_amount , stock_id , stock_amount , buyer_id , seller_id )
                        # PUSH THE REMAINING SELL ORDER BACK
                        # RECURSE NOW

                        self.make_order_and_transfer( smallest_sell.stock_id , smallest_sell.user_id , smallest_sell.price , amount_left , "sell" )

    def make_cash_stock_transfer( self , cash_amount , stock_id , stock_quantity , buyer_id , seller_id ) : # # ( self , cash_amount , stock_id , stock_amount , buyer_id , seller_id )
        self.increase_user_cash( seller_id , cash_amount ) # ( self , user_id , amount )
        self.decrease_user_cash( buyer_id , cash_amount ) # ( self , user_id , amount )
        self.increase_user_stock( buyer_id , stock_id , stock_quantity ) # ( self , user_id , stock_id , quantity ) POTENTIAL PROBLEM
        self.decrease_user_stock( seller_id , stock_id , stock_quantity ) # ( self , user_id , stock_id , quantity ) POTENTIAL PROBLEM

    def is_there_any_buy_orders( self , stock_id ) :
        if len( self.buy_hash_map_of_heaps[ stock_id ] ) > 0 :
            return True
        else :
            return False

    def is_there_any_sell_orders( self , stock_id ) :
        if len( self.sell_hash_map_of_heaps[ stock_id ] ) > 0 :
            return True
        else :
            return False

    def calculate_final_price( self , buy_order , sell_order ) : # LOOK FOR MUTABILITY
        # ORDER IDS ARE UNIQUE
        # FINAL PRICE IS THE SAME AS THE LAST ORDERS PRICE IN THE TRANSACTION
        if buy_order.get_order_id() < sell_order.get_order_id() :
            return sell_order.get_price()
        elif buy_order.get_order_id() > sell_order.get_order_id() :
            return buy_order.get_price()

    def is_buy_possible( self , user_id , cash_required ) :
        is_possible = self.user_hash_map_of_users[ user_id ].can_user_buy( cash_required )
        return is_possible

    def is_sell_possible( self , user_id , stock_id , amount_required ) :
        is_possible = self.user_hash_map_of_users[ user_id ].can_user_sell( stock_id , amount_required )
        return is_possible



    def look_largest_buy_order( self , stock_id ) :
        return self.buy_hash_map_of_heaps[ stock_id ][ 0 ]

    def look_smallest_sell_order( self , stock_id ) :
        return self.sell_hash_map_of_heaps[ stock_id ][ 0 ]

    def get_largest_buy_order( self , stock_id ) :
        largest_buy_order = heapq.heappop( self.buy_hash_map_of_heaps[ stock_id ] )
        return largest_buy_order

    def get_smallest_sell_order( self , stock_id ) :
        smallest_sell_order = heapq.heappop( self.sell_hash_map_of_heaps[ stock_id ] )
        return smallest_sell_order

    def increase_user_cash( self , user_id , amount ) :
        self.user_hash_map_of_users[ user_id ].cash_left += amount

    def decrease_user_cash( self , user_id , amount ) :
        self.user_hash_map_of_users[ user_id ].cash_left -= amount

    def increase_user_stock( self , user_id , stock_id , quantity ) :
        self.user_hash_map_of_users[ user_id ].stock_amount_hash_map[ stock_id ] += quantity

    def decrease_user_stock( self , user_id , stock_id , quantity ) :
        self.user_hash_map_of_users[ user_id ].stock_amount_hash_map[ stock_id ] -= quantity # TRANSFORMED += TO -=

    def run_simulation( self , user_amount , unique_stock_amount , cash_per_user , stock_amount_per_user , required_quantity_of_orders , price_range_from , price_range_to , quantity_range_from , quantity_range_to ) :
        self.add_user( user_amount , cash_per_user , [ k for k in range( 1 , unique_stock_amount + 1 ) ] , stock_amount_per_user ) # ( self , user_amount , cash_left , unique_stock_list )
        self.make_hash_map_of_heaps( [ k for k in range( 1 , unique_stock_amount + 1 ) ] ) # ( self , unique_stock_list )
        self.print_users()
        self.calculate_cash_in_the_system()
        self.calculate_stock_in_the_system()
        for i in range( required_quantity_of_orders ) :
                random_user = random.randint( 1 , user_amount )
                random_stock = random.randint( 1, unique_stock_amount )
                random_price = random.randint( price_range_from , price_range_to )
                random_quantity = random.randint( quantity_range_from , quantity_range_to )
                random_type = random.randint( 0 , 1 )
                string_type = "buy" if random_type == 0 else "sell"
                self.make_order_and_transfer( random_stock , random_user , random_price , random_quantity , string_type ) # ( self , stock_id, user_id, price, quantity, order_type )
        self.print_users()
        self.calculate_cash_in_the_system()
        self.calculate_stock_in_the_system()

    def print_users( self ) :
        # LOOP USERS SORTED BY USER ID IN AN ASCENDING WAY AND PRINT ALL OF THE POSSESSIONS
        print( "This displays the portfolios of each users as well as cash remaining for each user " )
        for user_key in sorted( self.user_hash_map_of_users.keys() ) :
            user_id = self.user_hash_map_of_users[ user_key ].get_user_id()
            cash_left = self.user_hash_map_of_users[ user_key ].get_cash_left()
            print( f" User Id = { user_id } < - - - - > Cash Left = { cash_left } " )
            for stock_key in sorted( self.user_hash_map_of_users[ user_key ].stock_amount_hash_map.keys() ) :
                print( f" Stock Id = { stock_key } < - - - - > Stock Quantity = { self.user_hash_map_of_users[ user_key ].stock_amount_hash_map[ stock_key ] } " )

    def calculate_cash_in_the_system( self ) :
        total_cash = 0
        for user_key in sorted(self.user_hash_map_of_users.keys()):
            cash_left = self.user_hash_map_of_users[user_key].get_cash_left()
            total_cash += cash_left
        print( f" The amount of cash in the system after the simulation has completed = { total_cash } " )

    def calculate_stock_in_the_system( self ) :
        total_stock = 0
        for user_key in sorted( self.user_hash_map_of_users.keys() ) :
            for stock_key in sorted( self.user_hash_map_of_users[ user_key ].stock_amount_hash_map.keys() ) :
                total_stock += self.user_hash_map_of_users[ user_key ].stock_amount_hash_map[ stock_key ]
        print( f" The amount of stock in the system after the simulation hash completed = { total_stock } " )

