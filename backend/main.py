from fastapi import FastAPI
from dotenv import load_dotenv

from DBBroker import DBBroker, Person

app = FastAPI()
load_dotenv()

db_broker = DBBroker()


@app.get("/test")
def read_root():
    person = Person()
    person.firstname = "Jan"
    person.lastname = "Kowalski"
    db_broker.add_passport_to_person("123", "111", person)
    return {"message": "chyba działa"}

