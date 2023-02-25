import psycopg2

# establish connection to PostgreSQL server
conn = psycopg2.connect(
    host="dpg-cft38parrk0c8348kc1g-a.ohio-postgres.render.com",
    port="5432",
    database="users_w7iu",
    user="test",
    password="lLanLmosmZSJ0B7c8ltpUEVsjwKKik94"
)

# create cursor
cur = conn.cursor()

# define UserInformation table
cur.execute('''CREATE TABLE IF NOT EXISTS user_information (
               username VARCHAR(50) PRIMARY KEY,
               token VARCHAR(100)
            )''')

# define Friends table
cur.execute('''CREATE TABLE IF NOT EXISTS friends (
                username VARCHAR(50), 
                friend VARCHAR(50),
                PRIMARY KEY (username, friend),
                FOREIGN KEY (username) REFERENCES user_information(username)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )''')

# define Debts table
cur.execute('''CREATE TABLE IF NOT EXISTS debts (
                requester VARCHAR(50),
                requestee VARCHAR(50),
                description VARCHAR(255),
                amount REAL,
                time_requested TIMESTAMP,
                PRIMARY KEY (requester, requestee, description),
                FOREIGN KEY (requester, requestee) REFERENCES friends(username, friend)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )''')

# define Transactions table
cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
                requester VARCHAR(50),
                requestee VARCHAR(50),
                description VARCHAR(255),
                amount REAL,
                time_paid TIMESTAMP,
                PRIMARY KEY (requester, requestee, description),
                FOREIGN KEY (requester, requestee) REFERENCES friends(username, friend)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            ''')

# commit changes and close cursor and connection
conn.commit()
cur.close()
conn.close()
