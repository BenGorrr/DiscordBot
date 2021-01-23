from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import *
from models import *

engine = create_engine(conn, pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def recreate_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_class(s, code, name=" ", class_link=" ", class_type=" "):
    class_links = {"link_L":" ", "link_T":" ", "link_P":" "}
    if class_type.lower() == "l":
        class_links["link_L"] = class_link
    elif class_type.lower() == "t":
        class_links["link_T"] = class_link
    elif class_type.lower() == "p":
        class_links["link_P"] = class_link

    print(class_links)
    new_class = Classes(
        course_code = code,
        course_name = name,
        link_L = class_links["link_L"],
        link_T = class_links["link_T"],
        link_P = class_links["link_P"]
    )
    s.add(new_class)
    return 1

def get_class(s, name):
    c = s.query(Classes).filter_by(course_name=name).all()
    return c

def get_class_byid(s, id):
    c = s.query(Classes).get(id)
    return c

def get_class_bycode(s, code):
    c = s.query(Classes).filter_by(course_code=code).first()
    return c

def get_all_class(s):
    c = s.query(Classes).all()
    return c

def delete_class_byid(s, id):
    s.delete(get_class_byid(s, id))

def delete_class_bycode(s, code):
    c = get_class_bycode(s, code)
    if c != None:
        s.delete(c)
        return 1
    else:
        print("Class not found")
        return 0

def update_classLink_byid(s, id, new_link):
    c = get_class_byid(s, id)
    c.link = new_link

def update_classLink_bycode(s, code, new_link, class_type):
    c = get_class_bycode(s, code)
    print(c)
    if c != None:
        print(c)
        if class_type.lower() == "l":
            print("Class = L")
            c.link_L = new_link
        elif class_type.lower() == "t":
            print("Class = T")
            c.link_T = new_link
        elif class_type.lower() == "p":
            print("Class = P")
            c.link_P = new_link
        print(c)
        return 1
    else:
        print("Class not found")
        return 0

def update_classCode_byid(s, id, new_code):
    c = get_class_byid(s, id)
    c.course_code = new_code

def update_classCode_bycode(s, code, new_code):
    c = get_class_bycode(s, code)
    c.course_code = new_code

def update_className_byid(s, id, new_name):
    c = get_class_byid(s, id)
    c.course_name = new_name

def update_classCode_bycode(s, code, new_name):
    c = get_class_bycode(s, code)
    c.course_name = new_name

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
    pass
