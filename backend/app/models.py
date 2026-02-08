from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(32), index=True, nullable=False)
    name = Column(String(128), nullable=False)
    units = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
