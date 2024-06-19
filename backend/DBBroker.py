import os

from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from face_recognition_module import FaceRecognitionModule

Base = declarative_base()
class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    dateofbirth = Column(String)
    nationality = Column(String)
    sex = Column(String)
    identity_card_id = Column(Integer, ForeignKey('identity_card.id'))
    passport_id = Column(Integer, ForeignKey('passport.id'))
    image_vector = Column(String) # todo: investigate how to store image vector

    identity_card = relationship("IdentityCard", back_populates="person")
    passport = relationship("Passport", back_populates="person")
        

class IdentityCard(Base):
    __tablename__ = 'identity_card'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    expiry_date = Column(String)

    person = relationship("Person", back_populates="identity_card")

class Passport(Base):
    __tablename__ = 'passport'

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)

    person = relationship("Person", back_populates="passport")

# todo: create tables for other documents

class DBBroker:
    def __init__(self):
        db_url = os.getenv('DATABASE_URL')
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session = self.SessionLocal()
    
    def add_passport_to_person(self, image_vector: str, passport_number: str, new_person: Person) -> Passport:
        person_id_to_image = self.session.query(Person.id, Person.image_vector).all()

        person = None
        for person_id, image in person_id_to_image:
            if FaceRecognitionModule.compare_vectors(image, image_vector): #image == image_vector: # todo: implement image comparison
                person = self.session.query(Person).filter(Person.id == person_id).first()
                break

        if person:
            new_passport = Passport(number=passport_number)
            person.passport = new_passport
            self.session.commit()

            return new_passport
        else:
            new_passport = Passport(number=passport_number)
            new_person.image_vector = image_vector
            new_person.passport = new_passport
            self.session.add(new_person)
            self.session.commit()

    def add_identity_to_person(self, image_vector: str, identity_number: str, expiry_date: str, new_person: Person) -> Passport:
        person_id_to_image = self.session.query(Person.id, Person.image_vector).all()
        # print(image_vector)
        person = None
        for person_id, image in person_id_to_image:
            # print(image)
            if FaceRecognitionModule.compare_vectors(image_vector, image): #image == image_vector: # todo: implement image comparison
                person = self.session.query(Person).filter(Person.id == person_id).first()
                break

        if person:
            new_identity_card = IdentityCard(number=identity_number)
            person.identity_card = new_identity_card
            self.session.commit()

            return new_identity_card
        else:
            new_identity_card = IdentityCard(number=identity_number, expiry_date=expiry_date)
            new_person.image_vector = image_vector
            new_person.identity_card = new_identity_card
            self.session.add(new_person)
            self.session.commit()

    def find_person_documents(self, image_vector: str):
        person_id_to_image = self.session.query(Person.id, Person.image_vector).all()
        # print(image_vector)
        person = None
        for person_id, image in person_id_to_image:
            # print(image)
            if FaceRecognitionModule.compare_vectors(image, image_vector): #image == image_vector: # todo: implement image comparison
                person = self.session.query(Person).filter(Person.id == person_id).first()
                break

        if person:
            check_passport = person.passport != None
            check_identity = person.identity_card != None

            return person, check_passport, check_identity
        else:
            return None, None, None

    def recreate_db(self):
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    