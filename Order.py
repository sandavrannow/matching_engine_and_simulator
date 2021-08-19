class Order:
    def __init__(self, order_id, stock_id, user_id, price, quantity, order_type ) :
        self.order_id = order_id
        self.stock_id = stock_id
        self.user_id = user_id
        self.price = price
        self.quantity = quantity
        self.order_type = order_type

    def get_order_id(self):
        return self.order_id

    def get_user_id(self):
        return self.user_id


    def get_stock_id(self):
        return self.stock_id

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_order_type(self):
        return self.order_type

    def get_total_order_price( self ) :
        return self.price * self.quantity

    def __lt__( self , other ) :
        if self.get_price() < other.get_price() :
            return True
        else :
            return False

    def __gt__( self , other ) :
        if self.get_price() > other.get_price() :
            return True
        else :
            return False

