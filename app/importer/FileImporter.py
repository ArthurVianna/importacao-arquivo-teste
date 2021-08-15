from app.utils.exceptions import ValidationError
from fastapi import File

d = [
    "cpf",
    "private",
    "incomplete",
    "last_order_date",
    "avg_ticket",
    "last_ticket",
    "most_frequent_store_cnpj",
    "last_store_cnpj"
]
class FileImporter():

    @staticmethod
    def file_import(file : File, separator: str = None, row_validator_method = None):
        head = None
        line_number = 0
        list_valid_dict = []
        list_invalid_dict = []
        for line in file.file:
            row_dict = {}
            line_number += 1
            line = line.decode("UTF-8").split(separator)
            #line = str(line).replace("/r/n","")
            if not head:
                head = line
                continue

            for i, value in enumerate(line):
                value = str(value).lower()
                if value != "null":
                    row_dict[d[i]] = value
            
            try:
                if row_validator_method:
                    row_dict = row_validator_method(row_dict)
                list_valid_dict.append(row_dict)
            except ValidationError as ex:
                list_invalid_dict.append(
                    {
                        "error": str(ex),
                        "file_line_number": line_number,
                        "dict":row_dict
                    }
                )
            
        
        return list_valid_dict, list_invalid_dict