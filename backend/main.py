import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
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

@app.post("/photo_data")
async def extract_data(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    data = extract_form_values(file.filename)
    
    return JSONResponse(content=data)