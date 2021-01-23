from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    course_code = Column(String)
    course_name = Column(String)
    link_L = Column(String)
    link_T = Column(String)
    link_P = Column(String)

    def __repr__(self):
        return "<Classes({} course_code='{}', course_name='{}', links='{},{},{}')"\
        .format(self.id, self.course_code, self.course_name, self.link_L, self.link_T, self.link_P)
