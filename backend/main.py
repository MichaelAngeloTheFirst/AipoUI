import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from DBBroker import DBBroker, Person, IdentityCard
from document_extraction_from_image import extract_document_from_image
from ocr import extract_form_values
from face_recognition_module import FaceRecognitionModule

app = FastAPI()
load_dotenv()

db_broker = DBBroker()

@app.get("/recreate-db")
def recreate_db():
    db_broker.recreate_db()
    return {"message": "Database recreated"}


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

    #     print(buffer.name)
    face_vector = str(FaceRecognitionModule.image_to_vector(file.filename))
    person, passport_check, identity_check = db_broker.find_person_documents(face_vector)
    
    if person:
        data = {
            "first_name": person.firstname,
            "last_name": person.lastname,
            "dateofbirth": person.dateofbirth,
            "nationality": person.nationality,
            "sex": person.sex,
            "passportnumber": person.passport.number if passport_check else "No passport",
            "identitynumber": person.identity_card.number if identity_check else "No identity"
        }
        # print("HELLLOOOOOO")
        return JSONResponse(content=data)
    
    data = extract_form_values(file.filename)


    mapping = {
        'IMIONA / GIVEN NAMES': 'firstname',
        'NAZWISKO / SURNAME': 'lastname',
        'DATA URODZENIA / DATE OF BIRTH': 'dateofbirth',
        'OBYWATELSTWO / NATIONALITY': 'nationality',
        'PLEC/SEX': 'sex'
    }

    person = Person()

    for key, value in data.items():
        if key in mapping:
            setattr(person, mapping[key], value)

   
    if data.get("TYP") == 'Dowod':
        _ = db_broker.add_identity_to_person(face_vector, data.get("NUMER DOWODU OSOBISTEGO/ IDENTITY CARD NUMBER"), data.get("TERMIN WAZNOSCI / EXPIRY DATE"), person)


    # data="HEHE YOU MORON I DON'T WORK :D"

    return JSONResponse(content=data)