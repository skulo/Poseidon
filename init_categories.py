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
    {"id": "3", "name": "Matematikai alapok", "parent_id": "1"},
    {"id": "50", "name": "Számítógépes rendszerek", "parent_id": "1"},
    {"id": "5", "name": "Analízis 1", "parent_id": "2"},
    {"id": "6", "name": "Webfejlesztés", "parent_id": "2"},
    {"id": "14", "name": "Webprogramozás", "parent_id": "7"},
    {"id": "15", "name": "Programozási alapismeretek", "parent_id": "1"},
    {"id": "16", "name": "Imperatív programozás", "parent_id": "1"},
    {"id": "17", "name": "Programozási nyelvek", "parent_id": "2"},
    {"id": "18", "name": "Objektumelvű programozás", "parent_id": "2"},
    {"id": "19", "name": "Diszkrét matematika 1", "parent_id": "2"},
    {"id": "20", "name": "Alogritmusok és adatszerkezetek 1", "parent_id": "2"},
    {"id": "21", "name": "Alogritmusok és adatszerkezetek 2", "parent_id": "7"},
    {"id": "21", "name": "Alogritmusok és adatszerkezetek 2", "parent_id": "7"},
    {"id": "22", "name": "Analízis 2", "parent_id": "7"},
    {"id": "23", "name": "Programozási technológia", "parent_id": "7"},
    {"id": "24", "name": "Diszkrét modellek", "parent_id": "7"},
    {"id": "25", "name": "Eseményvezérelt alkalmazások", "parent_id": "7"},
    {"id": "26", "name": "Adatbázisok 1", "parent_id": "9"},
    {"id": "27", "name": "Szoftvertechnológia", "parent_id": "9"},
    {"id": "28", "name": "Számelításelmélet 1", "parent_id": "9"},
    {"id": "29", "name": "Operációs rendszerek", "parent_id": "9"},
    {"id": "30", "name": "Numerikus módszerek", "parent_id": "9"},
    {"id": "36", "name": "Szakdolgozat", "parent_id": "13"},
    {"id": "37", "name": "Szerveroldali webprogramozás", "parent_id": "10"},
    {"id": "38", "name": "Kliensoldali webprogramozás", "parent_id": "10"},
    {"id": "39", "name": "Számítógépes grafika", "parent_id": "10"},
    {"id": "40", "name": "Python", "parent_id": "10"},
    {"id": "41", "name": "Az informatika története", "parent_id": "10"},
    {"id": "41", "name": "Az informatika története", "parent_id": "10"},
    {"id": "42", "name": "Cisco", "parent_id": "10"},
    {"id": "43", "name": "Logika", "parent_id": "10"},
    {"id": "44", "name": "Programozáselmélet", "parent_id": "10"},
    {"id": "45", "name": "C++", "parent_id": "10"},
    {"id": "46", "name": "Big Data", "parent_id": "10"},
    {"id": "100", "name": "ELTE IK BSC", "parent_id": None},
    {"id": "1", "name": "1. félév", "parent_id": "100"},
    {"id": "2", "name": "2. félév", "parent_id": "100"},
    {"id": "7", "name": "3. félév", "parent_id": "100"},
    {"id": "9", "name": "4. félév", "parent_id": "100"},
    {"id": "11", "name": "5. félév", "parent_id": "100"},
    {"id": "13", "name": "6. félév", "parent_id": "100"},
    {"id": "10", "name": "Kötelezően választható tárgyak", "parent_id": "100"},
    {"id": "4", "name": "Funkcionális programozás", "parent_id": "1"},
    {"id": "31", "name": "Adatbázisok 2", "parent_id": "11"},
    {"id": "32", "name": "Számításelmélet 2", "parent_id": "11"},
    {"id": "33", "name": "Telekommunikációs hálózatok", "parent_id": "11"},
    {"id": "34", "name": "Konkrurens programozás", "parent_id": "11"},
    {"id": "35", "name": "Mesterséges intelligencia", "parent_id": "11"},
    {"id": "12", "name": "Valószínűségszámítás és statisztika", "parent_id": "11"},
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
