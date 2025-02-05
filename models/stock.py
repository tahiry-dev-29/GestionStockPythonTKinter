from database.db_config import DbConnection

# Classe pour gérer les mouvements de stock

class Stock:
    def __init__(self):
        self.db = DbConnection()

    def add_stock_movement(self, product_id, quantity, movement_type, date=None):
        query = """INSERT INTO stock_movements 
                  (product_id, quantity, movement_type, movement_date) 
                  VALUES (%s, %s, %s, COALESCE(%s, NOW()))"""
        return self.db.execute(query, (product_id, quantity, movement_type, date))

    def get_stock_movements(self, product_id=None):
        query = """SELECT sm.*, p.name as product_name 
                  FROM stock_movements sm 
                  JOIN products p ON sm.product_id = p.id"""
        params = None
        
        if product_id:
            query += " WHERE product_id = %s"
            params = (product_id,)
            
        query += " ORDER BY movement_date DESC"
        return self.db.fetch_all(query, params)

    def get_current_stock(self, product_id):
        query = """SELECT SUM(
                    CASE 
                        WHEN movement_type = 'IN' THEN quantity 
                        ELSE -quantity 
                    END
                  ) as current_stock 
                  FROM stock_movements 
                  WHERE product_id = %s"""
        result = self.db.fetch_one(query, (product_id,))
        return result['current_stock'] if result['current_stock'] else 0