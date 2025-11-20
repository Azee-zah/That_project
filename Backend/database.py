import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT

load_dotenv()

db_url= f'mysql+pymysql://{os.getenv("db_user")}:{os.getenv("db_password")}@{os.getenv("db_host")}:{os.getenv("db_port")}/{os.getenv("db_name")}'

engine = create_engine(
    db_url,
    connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}
)

session = sessionmaker(bind=engine)
db = session()

create_tables = text("""
    CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR (150) NOT NULL,
        email VARCHAR (150) NOT NULL,
        password VARCHAR (200) NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS activities(
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR (200) NOT NULL,
        priority VARCHAR (150) NOT NULL,
        status VARCHAR (150) NOT NULL,
        due_date DATE,
        userId INT NOT NULL,
        FOREIGN KEY (userId) REFERENCES users(id)           
    );
""")

db.execute(create_tables)
print("Successfully created the to_do table")




