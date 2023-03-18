
# the combined activer order book
self.book_of_active_orders = np.zeros((2, 3, 10),dtype=int)
# the first dimention are 
# ask orders - sell ETF orders
# bid orders - buy ETF orders

# the second dimension are
# order id, price, volume

def update_book_of_active_orders(self, placing_order : bool, id : int, cancel : bool = False, buy : bool = True, placing_price : int = 0, placing_volume : int = 0, remaining_volume : int = 0):
        '''
        parameters:
        - placing_order: True if the order is being placed, False if the order is partially filled and needs updating
        - id: the id of the order
        - cancel: True if the order is being cancelled, False if the order is being placed or updated, only used if placing_order is False
        - buy: True if the order is a buy order, False if the order is a sell order, only used if placing_order is True
        - placing_price: the price of the order to be placed, only used if placing_order is True
        - placing_volume: the volume of the order to be placed, only used if placing_order is True
        - remaining_volume: the remaining volume of the order, only used if placing_order is False
        
        '''

        if placing_order:
            num_orders = len(np.argwhere(self.book_of_active_orders[:,0,:] != 0))
            if self.debug_prints:
                if num_orders = 10:
                    print('cant place more orders')
                elif num_orders > 10:
                    print('ERROR: more than 10 orders in the book already')
                 
            if buy:
                layer = 1
            else:
                layer = 0
                
            index = np.argwhere(self.book_of_active_orders[layer,0,:] == 0)[0,0,0]
            self.book_of_active_orders[layer,index,:] = np.array([id,placing_price,placing_volume])
                
        elif cancel or placing_order == False:
            if len(np.argwhere(self.book_of_active_orders[:,0,:] == id)) > 0:
                INDEX = np.argwhere(self.book_of_active_orders[:,0,:] == id)
                self.book_of_active_orders[INDEX[0], 2, INDEX[2]] = remaining_volume
                if remaining_volume == 0:
                    self.book_of_active_orders= np.delete(self.book_of_active_orders,INDEX[2],axis=2)
                    self.book_of_active_orders=np.insert(self.book_of_active_orders,0,np.array([0,0,0]),axis=2)
            else:
                if self.debug_prints == True: print('Order not found in book of orders')