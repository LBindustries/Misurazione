from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, DateTime, Float, create_engine

engine = create_engine("sqlite:///db.sqlite")
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class Registrazione(Base):
    __tablename__ = "registrazione"
    rid = Column(Integer, primary_key=True)
    orario = Column(DateTime, nullable=False)
    valore = Column(Float, nullable=False)

    def __repr__(self):
        return "<Registrazione {}/{}/{} {}:{} [{}]>".format(self.orario.day,
                                                            self.orario.month,
                                                            self.orario.year,
                                                            self.orario.hour,
                                                            self.orario.minute,
                                                            self.valore)


Base.metadata.create_all()
