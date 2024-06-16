from fastapi import FastAPI
from dotenv import load_dotenv

from DBBroker import DBBroker, Person
from ocr import extract_form_values

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

@app.get("/test2")
def extract_data():
    # Ścieżka do obrazu dowodu osobistego lub paszportu
    image_path = 'ex1.jpg'
    
    # Wywołanie funkcji i wyświetlenie wyników
    data = extract_form_values(image_path)
    
    return data
