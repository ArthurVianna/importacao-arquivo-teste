from datetime import date
from decimal import Decimal

# pylint might have a problem with this pydantic import
# add this exception in ".pylintrc" so pylint ignores imports from pydantic
# "--extension-pkg-whitelist=pydantic"
from pydantic import BaseModel

class UserBase(BaseModel):
    cpf : str
    private : bool

class UserCreate(UserBase):
    pass

class User(UserBase):

    id : int
    private : bool
    incomplete : bool
    last_order_date : date = None
    avg_ticket : Decimal = None
    last_ticket : Decimal = None
    most_frequent_store_cnpj : str = None
    last_store_cnpj : str = None

    class Config:
        orm_mode = True