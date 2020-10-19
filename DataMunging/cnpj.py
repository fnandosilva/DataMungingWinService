class Cnpj:

    """This is the class made to validate Cnpj document.
       There is a method that validad the object passed through
       this class. 
    """

    def __init__(self, document):
        document = str(document)
        if self.cnpj_is_valid(document):
            self.cnpj = document
        else:
            raise ValueError("invalid CNPJ number!")

    def cpf_is_valid(self, document):
        if len(document) == 14:
            return True
        else:
            return False
