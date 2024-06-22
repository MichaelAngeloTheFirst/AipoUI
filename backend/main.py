import shutil
from fuzzywuzzy import process
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from DBBroker import DBBroker, Person, IdentityCard, Passport
from document_extraction_from_image import extract_document_from_image
from ocr import extract_form_values
from face_recognition_module import FaceRecognitionModule

app = FastAPI()
load_dotenv()

db_broker = DBBroker()


# functions for matching ocr strings
def normalize_key(key):
    key = key.strip()
    return key

def get_standard_key(key, key_map, standard_keys):
    normalized_key = normalize_key(key)
    return get_closest_key(normalized_key, standard_keys)

def get_closest_key(key, keys):
    closest_key, score = process.extractOne(key, keys)

    # if its more than 60% similar return the closest key -> value is adjustable if someone wants to test it
    return closest_key if score > 60 else key

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

    face_vector = str(FaceRecognitionModule.image_to_vector(file.filename))
    person, passport_check, identity_check = db_broker.find_person_documents(face_vector)
    

    all_keys = {
        'IMIONA/GIVEN NAMES': 'IMIONA/GIVEN NAMES',
        'IMIONA / GIVEN NAMES': 'IMIONA/GIVEN NAMES',
        'IMIONA/ GIVEN NAMES': 'IMIONA/GIVEN NAMES',
        '2 IMIONA/GIVEN NAMES': 'IMIONA/GIVEN NAMES',
        'NAZWISKO/SURNAME': 'NAZWISKO/SURNAME',
        'NAZWISKO / SURNAME': 'NAZWISKO/SURNAME',
        '1 NAZWISKO/SURNAME': 'NAZWISKO/SURNAME',
        'I NAZWISKO/SURNAME': 'NAZWISKO/SURNAME',
        'NUMER PESEL/PERSONAL ID No': 'NUMER PESEL/PERSONAL ID No', 
        'NUMER PESEL / PERSONAL ID No': 'NUMER PESEL/PERSONAL ID No', 
        'NUMER PESEL/ PERSONAL ID No': 'NUMER PESEL/PERSONAL ID No', 
        '6 NUMER PESEL/PERSONAL ID No.': 'NUMER PESEL/PERSONAL ID No', 
        'DATA URODZENIA/DATE OF BIRTH': 'DATA URODZENIA/DATE OF BIRTH',
        'DATA URODZENIA / DATE OF BIRTH': 'DATA URODZENIA/DATE OF BIRTH',
        'DATA URODZENIA/ DATE OF BIRTH': 'DATA URODZENIA/DATE OF BIRTH',
        '3 DATA URODZENIA/DATE OF BIRTH': 'DATA URODZENIA/DATE OF BIRTH',
        'MIEJSCE URODZENIA/PLACE OF BIRTH': 'MIEJSCE URODZENIA/PLACE OF BIRTH',
        'MIEJSCE URODZENIA / PLACE OF BIRTH': 'MIEJSCE URODZENIA/PLACE OF BIRTH',
        'MIEJSCE URODZENIA/ PLACE OF BIRTH': 'MIEJSCE URODZENIA/PLACE OF BIRTH',
        '4 MIEJSCE URODZENIA/PLACE OF BIRTH': 'MIEJSCE URODZENIA/PLACE OF BIRTH',
        'OBYWATELSTWO/NATIONALITY': 'OBYWATELSTWO/NATIONALITY',
        'OBYWATELSTWO / NATIONALITY': 'OBYWATELSTWO/NATIONALITY',
        'OBYWATELSTWO/ NATIONALITY': 'OBYWATELSTWO/NATIONALITY',
        '5 OBYWATELSTWO/NATIONALITY': 'OBYWATELSTWO/NATIONALITY',
        'PLEC/SEX': 'PLEC/SEX',
        'PLEC / SEX': 'PLEC/SEX',
        'PLEC/ SEX': 'PLEC/SEX',
        '8 PLEC/SEX': 'PLEC/SEX',
        'PODPIS POSIADACZA/HOLDER\'S SIGNATURE': 'PODPIS POSIADACZA/HOLDER\'S SIGNATURE',
        'PODPIS POSIADACZA / HOLDER\'S SIGNATURE': 'PODPIS POSIADACZA/HOLDER\'S SIGNATURE',
        '11 PODPIS POSIADACZA/HOLDER\'S SIGNATURE': 'PODPIS POSIADACZA/HOLDER\'S SIGNATURE',
        'PODPIS POSIADACZA/HOLDER\'S SIGNATU': 'PODPIS POSIADACZA/HOLDER\'S SIGNATURE',
        'NUMER DOWODU OSOBISTEGO/IDENTITY CARD NUMBER': 'NUMER DOWODU OSOBISTEGO/IDENTITY CARD NUMBER',
        'NUMER DOWODU OSOBISTEGO / IDENTITY CARD NUMBER': 'NUMER DOWODU OSOBISTEGO/IDENTITY CARD NUMBER',
        'NUMER DOWODU OSOBISTEGO/ IDENTITY CARD NUMBER': 'NUMER DOWODU OSOBISTEGO/IDENTITY CARD NUMBER',
        'NUMER DOWDU OSOBISTEGO/IDENTITY CARD NUMBE': 'NUMER DOWODU OSOBISTEGO/IDENTITY CARD NUMBER',
        'TERMIN WAZNOSCI/EXPIRY DATE': 'TERMIN WAZNOSCI/EXPIRY DATE',
        'TERMIN WAZNOSCI / EXPIRY DATE': 'TERMIN WAZNOSCI/EXPIRY DATE',
        'TERMIN WAZNOSCI/ EXPIRY DATE': 'TERMIN WAZNOSCI/EXPIRY DATE',
        'EXPIRY DATE': 'TERMIN WAZNOSCI/EXPIRY DATE',
        'TERMI WAZNOSCI/EXPIRY DAT': 'TERMIN WAZNOSCI/EXPIRY DATE',
        'NUMER PASZPORTU/PASSPORT No':'NUMER PASZPORTU/PASSPORT No',
        'NUMER PASZPORTU / PASSPORT No':'NUMER PASZPORTU/PASSPORT No',
        'NUMER PASZPORTU/ PASSPORT No':'NUMER PASZPORTU/PASSPORT No',
        'NUMER PASZPORTU/PASSPOR ':'NUMER PASZPORTU/PASSPORT No',
        'ORGAN WYDAJACY/AUTHORITY': 'ORGAN WYDAJACY/AUTHORITY',
        'ORGAN WYDAJACY / AUTHORITY': 'ORGAN WYDAJACY/AUTHORITY',
        'ORGAN WYDAJACY/ AUTHORITY': 'ORGAN WYDAJACY/AUTHORITY',
        '10. ORGAN WYDAJACY/AUTHORITY': 'ORGAN WYDAJACY/AUTHORITY',
        '10.': 'ORGAN WYDAJACY/AUTHORITY',
        'DATA WAZNOSCI/DATE OF EXPIRY': 'DATA WAZNOSCI/DATE OF EXPIRY',
        'DATA WAZNOSCI / DATE OF EXPIRY': 'DATA WAZNOSCI/DATE OF EXPIRY',
        'DATA WAZNOSCI/ DATE OF EXPIRY': 'DATA WAZNOSCI/DATE OF EXPIRY',
        '9 DATA WAZNOSCI/DATE OF EXPIRY': 'DATA WAZNOSCI/DATE OF EXPIRY',
        'DATA WYDANIA/DATE OF ISSUE': 'DATA WYDANIA/DATE OF ISSUE',
        'DATA WYDANIA / DATE OF ISSUE': 'DATA WYDANIA/DATE OF ISSUE',
        'DATA WYDANIA/ DATE OF ISSUE': 'DATA WYDANIA/DATE OF ISSUE',
        '7 DATA WYDANIA/DATE OF ISSUE': 'DATA WYDANIA/DATE OF ISSUE',
        'KOD/CODE': 'KOD/CODE',
        'KOD / CODE': 'KOD/CODE',
        'KOD/ CODE': 'KOD/CODE',
        'KOD/COD': 'KOD/CODE',
        'TYP/TYPE': 'TYP/TYPE',
        'TYP / TYPE': 'TYP/TYPE',
        'TYP/ TYPE': 'TYP/TYPE',
        'TYP/TYP': 'TYP/TYPE',
    }

    person_mapping = {
        'IMIONA/GIVEN NAMES': 'firstname',
        'NAZWISKO/SURNAME': 'lastname',
        'NUMER PESEL/PERSONAL ID No': 'pesel', 
        'DATA URODZENIA/DATE OF BIRTH': 'dateofbirth',
        'MIEJSCE URODZENIA/PLACE OF BIRTH': 'placeofbirth',
        'OBYWATELSTWO/NATIONALITY': 'nationality',
        'PLEC/SEX': 'sex',
        'PODPIS POSIADACZA/HOLDER\'S SIGNATURE': 'signature'
    }

    identity_mapping = {
        'NUMER DOWODU OSOBISTEGO/IDENTITY CARD NUMBER': 'number',
        'TERMIN WAZNOSCI/EXPIRY DATE': 'expiry_date'
    }

    passport_mapping = {
        'NUMER PASZPORTU/PASSPORT No':'number',
        'ORGAN WYDAJACY/AUTHORITY': 'issued_by',
        'DATA WAZNOSCI/DATE OF EXPIRY': 'date_expires',
        'DATA WYDANIA/DATE OF ISSUE': 'date_issued',
        'KOD/CODE': 'code',
        'TYP/TYPE': 'type'
    }

    if person:
        print("hello person")

        passport, identity_card = {}, {}


        if passport_check:
            passport = {
                "number": person.passport.number,
                "type": person.passport.type,
                "date_issued": person.passport.date_issued,
                "date_expires": person.passport.date_expires,
                "issued_by": person.passport.issued_by,
                "code": person.passport.code
            }

        if identity_check:
            identity_card = {
                "number": person.identity_card.number,
                "date_expires": person.identity_card.date_expires,
            }

        data = {
            "first_name": person.firstname,
            "last_name": person.lastname,
            "pesel": person.pesel,
            "place_of_birth": person.placeofbirth,
            "date_of_birth": person.dateofbirth,
            "nationality": person.nationality,
            "sex": person.sex,
            "signature": person.signature,
            "passport": passport,
            "identitynumber": identity_card,
        }
        
        if not passport_check:
            data = extract_form_values(file.filename)

            if data.get("TYP") == 'PASZPORT':
                new_passport = Passport()

                for key, value in data.items():
                    read_key = get_standard_key(key, all_keys, list(all_keys.values()))
                    if read_key in person_mapping:
                        setattr(person, person_mapping[read_key], value)
                    if read_key in passport_mapping:
                        setattr(new_passport, passport_mapping[read_key], value)


                # new_person.image_vector = person.image_vector
                
                _ = db_broker.add_passport_to_person(face_vector, new_passport, person)


                passport = {
                    "number": new_passport.number,
                    "type": new_passport.type,
                    "date_issued": new_passport.date_issued,
                    "date_expires": new_passport.date_expires,
                    "issued_by": new_passport.issued_by,
                    "code": new_passport.code
                }

                data = {
                    "first_name": person.firstname,
                    "last_name": person.lastname,
                    "pesel": person.pesel,
                    "place_of_birth": person.placeofbirth,
                    "date_of_birth": person.dateofbirth,
                    "nationality": person.nationality,
                    "sex": person.sex,
                    "signature": person.signature,
                    "passport": passport,
                    "identitynumber": identity_card
                }

                print("hi passport")
        
        if not identity_check:
            data = extract_form_values(file.filename)

            if data.get("TYP") == 'DOWOD':
                new_identity = IdentityCard()

                for key, value in data.items():
                    read_key = get_standard_key(key, all_keys, list(all_keys.values()))
                    if read_key in person_mapping:
                        setattr(person, person_mapping[read_key], value)
                    if read_key in identity_mapping:
                        setattr(new_identity, identity_mapping[read_key], value)


                # new_person.image_vector = person.image_vector

                _ = db_broker.add_identity_to_person(face_vector, new_identity, person)

                identity_card = {
                    "number": new_identity.number,
                    "date_expires": new_identity.date_expires,
                }

                data = {
                    "first_name": person.firstname,
                    "last_name": person.lastname,
                    "pesel": person.pesel,
                    "place_of_birth": person.placeofbirth,
                    "date_of_birth": person.dateofbirth,
                    "nationality": person.nationality,
                    "sex": person.sex,
                    "signature": person.signature,
                    "passport": passport,
                    "identitynumber": identity_card
                }

                print("hi identity")

        print("hi database")
        return JSONResponse(content=data)
    else:
        data = extract_form_values(file.filename)

        person = Person()

        if data.get("TYP") == 'DOWOD':
            identity = IdentityCard()

            for key, value in data.items():
                read_key = get_standard_key(key, all_keys, list(all_keys.values()))
                if read_key in person_mapping:
                    setattr(person, person_mapping[read_key], value)
                if read_key in identity_mapping:
                    setattr(identity, identity_mapping[read_key], value)

            _ = db_broker.add_identity_to_person(face_vector, identity, person)
        else:
            passport = Passport()
            print(data)

            for key, value in data.items():
                read_key = get_standard_key(key, all_keys, list(all_keys.values()))
                print(read_key)
                if read_key in person_mapping:
                    setattr(person, person_mapping[read_key], value)
                if read_key in passport_mapping:
                    setattr(passport, passport_mapping[read_key], value)
            
            _ = db_broker.add_passport_to_person(face_vector, passport, person)

        print("hi default")
        return JSONResponse(content=data)