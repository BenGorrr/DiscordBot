from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from models import *

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def recreate_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_class(code, name=" ", class_link=" "):
    new_class = Classes(
        course_code = code,
        course_name = name,
        link = class_link
    )
    s.add(new_class)
    s.commit()

def get_class(name):
    c = s.query(Classes).filter_by(course_name=name).all()
    return c

def get_class_byid(id):
    c = s.query(Classes).get(id)
    return c

def get_class_bycode(code):
    c = s.query(Classes).filter_by(course_code=code).all()
    return c

def get_all_class():
    c = s.query(Classes).all()
    return c

def delete_class_byid(id):
    s.delete(get_class_byid(id))
    s.commit()

def update_classLink_byid(id, new_link):
    c = get_class_byid(id)
    c.link = new_link
    s.commit()

def update_classLink_bycode(code, new_link):
    c = get_class_bycode(code)
    c.link = new_link
    s.commit()

def update_classCode_byid(id, new_code):
    c = get_class_byid(id)
    c.course_code = new_code
    s.commit()

def update_classCode_bycode(code, new_code):
    c = get_class_bycode(code)
    c.course_code = new_code
    s.commit()

def update_className_byid(id, new_name):
    c = get_class_byid(id)
    c.course_name = new_name
    s.commit()

def update_classCode_bycode(code, new_name):
    c = get_class_bycode(code)
    c.course_name = new_name
    s.commit()

if __name__ == '__main__':
    # recreate_db()
    # add_class("AACS2034", "FCN")
    # add_class("AACS2284", "OS")
    # add_class("AAMS3163", "Algebra")
    # delete_class_byid(1)
    #update_classLink_byid(1, r'https://meet.google.com/xby-eben-awt?authuser=0')
    # c = get_class_byid(1)
    # print(c.course_code)
    # update_className_byid(2, "Operating System")
    # get_all_class()
    # s.close()
