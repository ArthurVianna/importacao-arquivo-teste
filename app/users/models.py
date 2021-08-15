import re
from decimal import Decimal
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Numeric, Date
from sqlalchemy.sql.expression import null


from app.core.database import Base
from app.utils.exceptions import ValidationError

class User(Base):
    __tablename__ = "user"


    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String, nullable=False, unique=True)
    private = Column(Boolean, default=False, nullable=False)
    incomplete = Column(Boolean, default=False, nullable=False)
    last_order_date = Column(Date, nullable=True)
    avg_ticket = Column(Numeric, nullable=True)
    last_ticket = Column(Numeric, nullable=True)
    most_frequent_store_cnpj = Column(String, nullable=True)
    last_store_cnpj = Column(String, nullable=True)

    