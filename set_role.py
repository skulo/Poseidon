import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category  
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv
load_dotenv()

DATABASE_NUMBER = os.getenv("DATABASE_NUMBER", "")  

DATABASE_URL = f"postgresql://postgres:postgres@localhost:{DATABASE_NUMBER}/poseidon"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

from models import User

db = SessionLocal()

email = input("Add meg a tesztelni kívánt felhasználó email-címét: ")
new_role = input("Add meg az új szerepkört (user / moderator / admin): ")

user = db.query(User).filter(User.email == email).first()
if user:
    user.role = new_role
    db.commit()
    print(f"{email} szerepköre módosítva: {new_role}")
else:
    print("Nincs ilyen felhasználó!")

db.close()
