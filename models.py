from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import relationship

Base = declarative_base()

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    course_code = Column(String)
    course_name = Column(String)
    urls = relationship("Links", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Classes({} course_code='{}', course_name='{}', urls={})>"\
        .format(self.id, self.course_code, self.course_name, self.urls)

class Links(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('classes.id'))
    url_name = Column(String)
    url = Column(String)
    course = relationship("Classes")

    def __repr__(self):
        return "<Links({} course_id='{}', name='{}', url='{}')>"\
        .format(self.id, self.course_id, self.url_name, self.url)

class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    link = Column(String)
