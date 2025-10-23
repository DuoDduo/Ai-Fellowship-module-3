# importing module to setup the database
from sqlalchemy import create_engine,text
# importing sessionmaker to ensure we close our connnection after
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# loading environment variables
load_dotenv()

# db_url= dialect+driver://dbuser;dbpassword;dbhost;dbport;dbname

db_url = f"mysql+pymysql://{os.getenv('dbuser')}:{os.getenv('dbpassword')}@{os.getenv('dbhost')}:{os.getenv('dbport')}/{os.getenv('dbname')}"

engine = create_engine(db_url)

# binding our engine to the sessionmake
session = sessionmaker(bind=engine)

db=session()

# running a query to get data from our table
query = text("select * from user")

users = db.execute(query).fetchall()
print(users)
