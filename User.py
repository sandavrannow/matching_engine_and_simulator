class User :
    def __init__( self , user_id , cash_left , stock_amount_hash_map ) :
        self.user_id = user_id
        self.cash_left = cash_left
        self.stock_amount_hash_map = stock_amount_hash_map

    def get_user_id( self ) :
        return self.user_id

    def get_cash_left( self ) :
        return self.cash_left

    def get_user_stock_amount( self , stock_id ) :
        return self.stock_amount_hash_map[ stock_id ]


    def can_user_buy( self , cash_required ) :
        amount_left = self.get_cash_left()
        if amount_left >= cash_required :
            return True
        else :
            return False

    def can_user_sell( self , stock_id , quantity ) :
        amount_left = self.get_user_stock_amount( stock_id )
        if amount_left >= quantity :
            return True
        else :
            return False

