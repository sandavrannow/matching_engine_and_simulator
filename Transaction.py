class Transaction :
    def __init__( self , transaction_id , stock_id , buyer_id , seller_id , price , quantity ) :
        self.transaction_id = transaction_id
        self.stock_id = stock_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.price = price
        self.quantity = quantity

    def get_transaction_id( self ) :
        return self.transaction_id

    def get_stock_id( self ) :
        return self.stock_id


    def get_buyer_id( self ) :
        return self.buyer_id

    def get_seller_id( self ) :
        return self.seller_id

    def get_price( self ) :
        return self.price

    def get_quantity( self ) :
        return self.quantity

    def get_total_transaction_price( self ) :
        return self.price * self.quantity
