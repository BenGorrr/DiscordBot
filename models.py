from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    course_code = Column(String)
    course_name = Column(String)
    link = Column(String)

    def __repr__(self):
        return "<Classes({} course_code='{}', course_name='{}', link='{}')"\
        .format(self.id, self.course_code, self.course_name, self.link)