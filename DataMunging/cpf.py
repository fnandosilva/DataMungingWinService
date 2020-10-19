class Cpf:
    """ This is the class made to validate CPF document.
        There is a method that validad the object passed through
        this class. 
    """
    def __init__(self, document):
        document = str(document)
        if self.cpf_is_valid(document):
            self.cpf = document
        else:
            raise ValueError("Invalid CPF number!")

    def cpf_is_valid(self, document):
        if len(document) == 11:
            return True
        else:
            return False
