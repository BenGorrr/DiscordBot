from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from models import *

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session() #create session object

def recreate_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_class(name, class_link=""):
    new_class = Classes(
        course_name = name,
        link = class_link
    )
    s.add(new_class)
    s.commit()

add_class("FCN")


s.close()
