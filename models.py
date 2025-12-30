from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker


db_url = "sqlite:///database.db"

Base = declarative_base()
engine = create_engine(db_url)
# session = sessionmaker(bind=engine)
# session = session()
Session = sessionmaker(bind=engine)
session = Session()

class RegisterApp(Base):
    __tablename__ = "users_app"

    id = Column(Integer, primary_key=True)
    username = Column(String(50),unique=True,nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

    def __repr__(self):
        return f"this is the username which I want to registered {self.username}"


Base.metadata.create_all(engine)  



