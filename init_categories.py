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

raw_categories = [
    {"id": "3", "name": "Matalap", "parent_id": "1"},
    {"id": "5", "name": "Anal 1", "parent_id": "2"},
    {"id": "6", "name": "Webfejl", "parent_id": "2"},
    {"id": "14", "name": "Webprog", "parent_id": "7"},
    {"id": "15", "name": "Progalap", "parent_id": "1"},
    {"id": "16", "name": "Improg", "parent_id": "1"},
    {"id": "17", "name": "Prognyelv", "parent_id": "2"},
    {"id": "18", "name": "Oep", "parent_id": "2"},
    {"id": "19", "name": "Dimat 1", "parent_id": "2"},
    {"id": "20", "name": "Algo 1", "parent_id": "2"},
    {"id": "21", "name": "Algo 2", "parent_id": "7"},
    {"id": "22", "name": "Anal 2", "parent_id": "7"},
    {"id": "23", "name": "Progtech", "parent_id": "7"},
    {"id": "24", "name": "Dimodell", "parent_id": "7"},
    {"id": "25", "name": "Eva", "parent_id": "7"},
    {"id": "26", "name": "Adatb 1", "parent_id": "9"},
    {"id": "27", "name": "Szofttech", "parent_id": "9"},
    {"id": "28", "name": "Számelm 1", "parent_id": "9"},
    {"id": "29", "name": "Oprend", "parent_id": "9"},
    {"id": "30", "name": "Nummod", "parent_id": "9"},
    {"id": "36", "name": "Szakdoga", "parent_id": "13"},
    {"id": "37", "name": "Szerveroldali", "parent_id": "10"},
    {"id": "38", "name": "Kliensoldali", "parent_id": "10"},
    {"id": "39", "name": "Számgraf", "parent_id": "10"},
    {"id": "40", "name": "Python", "parent_id": "10"},
    {"id": "41", "name": "Infotöri", "parent_id": "10"},
    {"id": "42", "name": "Cisco", "parent_id": "10"},
    {"id": "43", "name": "Logika", "parent_id": "10"},
    {"id": "44", "name": "Progelm", "parent_id": "10"},
    {"id": "45", "name": "C++", "parent_id": "10"},
    {"id": "46", "name": "Big Data", "parent_id": "10"},
    {"id": "100", "name": "ELTE IK BSC", "parent_id": None},
    {"id": "1", "name": "1. félév", "parent_id": "100"},
    {"id": "2", "name": "2. félév", "parent_id": "100"},
    {"id": "7", "name": "3. félév", "parent_id": "100"},
    {"id": "9", "name": "4. félév", "parent_id": "100"},
    {"id": "11", "name": "5. félév", "parent_id": "100"},
    {"id": "13", "name": "6. félév", "parent_id": "100"},
    {"id": "10", "name": "Kötválok", "parent_id": "100"},
    {"id": "4", "name": "Funkcprog", "parent_id": "1"},
    {"id": "31", "name": "Adatbázisok 2", "parent_id": "11"},
    {"id": "32", "name": "Számításelmélet 2", "parent_id": "11"},
    {"id": "33", "name": "Telekommunikációs Hálózatok", "parent_id": "11"},
    {"id": "34", "name": "Konkrurens Programozás", "parent_id": "11"},
    {"id": "35", "name": "Mesterséges Intelligencia", "parent_id": "11"},
    {"id": "12", "name": "Valószínűségszámítás és Statisztika", "parent_id": "11"},
]

def populate_categories():
    session = SessionLocal()


    session.query(Category).delete()
    session.commit()

    categories_by_id = {}

    for cat in raw_categories:
        category = Category(id=cat["id"], name=cat["name"], parent_id=cat["parent_id"])
        session.add(category)
        categories_by_id[cat["id"]] = category

    session.commit()

    for cat in raw_categories:
        category = categories_by_id[cat["id"]]
        parent_id = cat["parent_id"]
        if parent_id:
            category.parent = categories_by_id[parent_id]

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_categories()
