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

    @staticmethod
    def validate_dict(user_dict):
        # CPF validation
        cpf = user_dict.get("cpf", None)
        if cpf:
            user_dict["cpf"] = User._numeric_str_cleaner(cpf)
            User._validate_cpf(user_dict["cpf"])
        else:
            raise ValidationError("CPF is needed to create a User")

        # private validation
        private = user_dict.get("private", None)

        if private:
            user_dict["private"] = False if private in ["n", "no", "f", "false", "off", "0"] else True
        

        # incomplete validation
        incomplete = user_dict.get("incomplete", None)

        if incomplete:
            user_dict["incomplete"] = (incomplete not in ["n", "no", "f", "false", "off", "0"])


        # last_order_date validation
        last_order_date = user_dict.get("last_order_date", None)

        if last_order_date:
            try:
                datetime.strptime(last_order_date, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("Incorrect date")


        # avg_ticket validation
        avg_ticket = user_dict.get("avg_ticket", None)

        if avg_ticket:
            try:
                user_dict["avg_ticket"] = Decimal(avg_ticket.replace(",", "."))
            except ValueError:
                raise ValidationError("Incorrect decimal number")


        # last_ticket validation
        last_ticket = user_dict.get("last_ticket", None)

        if last_ticket:
            try:
                user_dict["last_ticket"] = Decimal(last_ticket.replace(",", "."))
            except ValueError:
                raise ValidationError("Incorrect decimal number")


        # most_frequent_store_cnpj validation
        most_frequent_store_cnpj = user_dict.get("most_frequent_store_cnpj", None)

        if most_frequent_store_cnpj:
            user_dict["most_frequent_store_cnpj"] = User._numeric_str_cleaner(most_frequent_store_cnpj)
            User._validate_cnpj(user_dict["most_frequent_store_cnpj"])
        

        # last_store_cnpj validation
        last_store_cnpj = user_dict.get("last_store_cnpj", None)
        
        if last_store_cnpj:
            user_dict["last_store_cnpj"] = User._numeric_str_cleaner(last_store_cnpj)
            User._validate_cnpj(user_dict["last_store_cnpj"])


        return user_dict

    @staticmethod
    def _numeric_str_cleaner(string: str):
        # Using regex to delete everything that isnt numeric
        return re.sub("[^0-9]", "" ,string)
    
    @staticmethod
    def _validate_cpf(cpf: str):
        if len(cpf) != 11:
            raise ValidationError("CPF needs exactly 11 digits")

        digit_list = [int(d) for d in cpf]
        
        # validate first validator digit
        multiplier_start = 10
        sum_result = 0
        for index, digit in enumerate(digit_list):

            if index < 9:
                sum_result += digit * (multiplier_start - index)

        remainder = ((sum_result * 10) % 11)
        if remainder in [10, 11]:
            remainder = 0
        if remainder != digit_list[9]:
            raise ValidationError("Invalid CPF : " + cpf)
        
        # validate second validator digit
        multiplier_start = 11
        sum_result = 0

        for index, digit in enumerate(digit_list):
            if index < 10:
                sum_result += digit * (multiplier_start - index)

        remainder = ((sum_result * 10) % 11)
        if remainder in [10, 11]:
            remainder = 0

        if remainder != digit_list[10]:
            raise ValidationError("Invalid CPF : " + cpf)
        
        return True

    @staticmethod
    def _validate_cnpj(cnpj: str):
        if len(cnpj) != 14:
            raise ValidationError("CNPJ needs exactly 14 digits")

        digit_list = [int(d) for d in cnpj]
        
        multipliers = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_result = 0
        for index, digit in enumerate(multipliers):
            sum_result += digit * digit_list[index]

        remainder = sum_result % 11

        if remainder < 2:
            valid_digit = 0
        else:
            valid_digit = 11 - remainder

        if valid_digit != digit_list[12]:
            raise ValidationError("Invalid CNPJ : " + cnpj)


        multipliers = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        sum_result = 0
        for index, digit in enumerate(multipliers):
            sum_result += digit * digit_list[index]

        remainder = sum_result % 11

        if remainder < 2:
            valid_digit = 0
        else:
            valid_digit = 11 - remainder

        if valid_digit != digit_list[13]:
            raise ValidationError("Invalid CNPJ : " + cnpj)

        return True

