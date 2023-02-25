import psycopg2


# 
# conn = psycopg2.connect(
    # host ="postgres://test:lLanLmosmZSJ0B7c8ltpUEVsjwKKik94@dpg-cft38parrk0c8348kc1g-a.ohio-postgres.render.com/users_w7iu",
    # user =  "test",
    # password = "lLanLmosmZSJ0B7c8ltpUEVsjwKKik94",
    # port = "5432",
    # # database = "users_w7iu"
# )
# 
# cursor = conn.cursor()

conn = psycopg2.connect("postgres://test:lLanLmosmZSJ0B7c8ltpUEVsjwKKik94@dpg-cft38parrk0c8348kc1g-a.ohio-postgres.render.com/users_w7iu")


cursor = conn.cursor()
data = cursor.fetchone()

