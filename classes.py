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

def add_class(s, code, name=" "):
    new_class = Classes(
        course_code = code,
        course_name = name
    )
    s.add(new_class)
    return 1

def get_all_class(s):
    c = s.query(Classes).all()
    return c

def get_class_byname(s, name):
    c = s.query(Classes).filter_by(course_name=name).first()
    return c

def get_class_byid(s, id):
    c = s.query(Classes).get(id)
    return c

def get_class_bycode(s, code):
    c = s.query(Classes).filter_by(course_code=code).first()
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

def update_classCode_byid(s, id, new_code):
    c = get_class_byid(s, id)
    c.course_code = new_code

def update_classCode_bycode(s, code, new_code):
    c = get_class_bycode(s, code)
    c.course_code = new_code

def update_className_byid(s, id, new_name):
    c = get_class_byid(s, id)
    c.course_name = new_name

def update_className_bycode(s, code, new_name):
    c = get_class_bycode(s, code)
    c.course_name = new_name

def new_add(s):
    new_class = Classes(course_code="Acas", course_name="course name")
    new_link = Links(url_name="Tuto", url="meetlinkhere")
    new_class.urls.append(new_link)
    s.add(new_class)

def add_link_byid(s, course_id, url_name, url):
    c = get_class_byid(s, course_id)
    new_link = Links(url_name=url_name, url=url)
    c.urls.append(new_link)

def add_link_bycode(s, course_code, url_name, url):
    c = get_class_bycode(s, course_code)
    if c != None:
        new_link = Links(url_name=url_name, url=url)
        c.urls.append(new_link)
        return 1
    else:
        print("Class not found")
        return 0

def get_all_links_in_course(s, course_code):
    return get_class_bycode(s, course_code).urls

def update_link(s, course_code, url_name, new_link):
    urls = get_all_links_in_course(s, course_code)
    for l in urls:
        if l.url_name == url_name:
            l.url = new_link
            return 1
    return 0


def update_link_name(s, course_code, url_name, new_name):
    urls = get_all_links_in_course(s, course_code)
    for l in urls:
        if l.url_name == url_name:
            l.url_name = new_name
            break

def delete_link(s, course_code, url_name):
    urls = get_all_links_in_course(s, course_code)
    for l in urls:
        if l.url_name == url_name:
            s.delete(l)
            return 1
    return 0

def delete_all_links_in_course(s, course_code):
    urls = get_all_links_in_course(s, course_code)
    for l in urls:
        s.delete(l)

if __name__ == '__main__':
    # add_class("AACS2034", "FCN")
    # add_class("AACS2284", "OS")
    # add_class("AAMS3163", "Algebra")
    # delete_class_byid(1)
    #update_classLink_byid(1, r'https://meet.google.com/xby-eben-awt?authuser=0')
    # c = get_class_byid(1)
    # print(c.course_code)
    # update_className_byid(2, "Operating System")
    #recreate_db()
    s = Session()
    #delete_link(s, "course name", "Tuto")
    #delete_class_byid(s, 1)
    #new_add(s)
    #update_link(s, "Tuto", "new link")
    #add_link_byid(s, 1, "Lec", "lec link")
    #s.commit()
    print(get_all_class(s))
    s.close()
    #pass
