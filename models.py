from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Date,Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    Custom = "custom"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    surname = Column(String,index=True)
    dateofbirth = Column(Date,index=True)
    gender = Column(Enum(Gender),index=True)
    email = Column(String, index=True)
    password = Column(String)
    # items = relationship("Item", back_populates="owner")