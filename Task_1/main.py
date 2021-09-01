import create_data_base

conn = create_data_base.create_connection()
create_data_base.insert_products(conn)