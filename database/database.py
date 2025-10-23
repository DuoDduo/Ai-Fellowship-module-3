# database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pymysql.constants import CLIENT
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Build database connection URL
db_url = (
    f"mysql+pymysql://{os.getenv('dbuser')}:{os.getenv('dbpassword')}"
    f"@{os.getenv('dbhost')}:{os.getenv('dbport')}/{os.getenv('dbname')}"
)

# Create SQLAlchemy engine
engine = create_engine(db_url)

# Create a session
Session = sessionmaker(bind=engine)
db = Session()

# Create tables
create_users = text("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );
""")

create_courses = text("""
    CREATE TABLE IF NOT EXISTS courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        level VARCHAR(100) NOT NULL
    );
""")

create_enrollments = text("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userId INT,
        courseId INT,
        FOREIGN KEY (userId) REFERENCES users(id),
        FOREIGN KEY (courseId) REFERENCES courses(id)
    );
""")

# Execute setup
db.execute(create_users)
db.execute(create_courses)
db.execute(create_enrollments)
db.commit()

print("Tables created successfully")
