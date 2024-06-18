import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from DBBroker import DBBroker, Person
from document_extraction_from_image import extract_document_from_image
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

    extracted_document = extract_document_from_image(file.filename)

    if extracted_document is not None:
        output_filename = file.filename
        extracted_document.save(output_filename)

    data = extract_form_values(file.filename)
    
    return JSONResponse(content=data)