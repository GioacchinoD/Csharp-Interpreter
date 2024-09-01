class SymbolTable:

    def __init__(self):
        # Utilizza un dizionario per memorizzare il nome delle variabili e i suoi dettagli (tipo di dato e valore)
        self.symbols = {}

    def define(self, identifier, symbol_type, value=None):
        """
        Permette di aggiungere un simbolo alla tabella symbols
        :param identifier: Indica il nome della variabile
        :param symbol_type: Indica il tipo della variabile
        :param value: Indica il valore della variabile
        """
        if identifier in self.symbols:
            raise Exception(f"Error: the variable '{identifier}' is already defined.")
        self.symbols[identifier] = {'type': symbol_type, 'value': value}

    def set_value(self, identifier, value):
        """
        Permette di assegnare/aggiornare il valore di una variabile esistente
        :param identifier: Indica il nome della variabile
        :param value: Indica il nuovo valore della variabile
        """
        if identifier not in self.symbols:
            raise Exception(f"Error: The variable '{identifier}' was not defined.")
        self.symbols[identifier]['value'] = value

    def get_value(self, identifier):
        """
        Permette di recuperare il valore di una variabile esistente
        :param identifier: Indica il nome della variabile di cui recuperare il valore
        :return: Restituisce il valore associato alla variabile nella tabella symbols
        """
        if identifier not in self.symbols:
            raise Exception(f"Error: The variable '{identifier}' was not defined.")
        if self.symbols[identifier]['value'] is None:
            raise Exception(f"Error: The variable '{identifier}' does not have a valid value.")
        return self.symbols[identifier]['value']

    def get_type(self, identifier):
        """
        Permette di recuperare il tipo di una variabile esistente
        :param identifier: Indica il nome della variabile di cui recuperare il tipo
        :return: Restituisce il tipo associato alla variabile nella tabella symbols
        """
        if identifier not in self.symbols:
            raise Exception(f"Error: The variable '{identifier}' was not defined.")
        return self.symbols[identifier]['type']

    def method_define(self, identifier, attributes):
        """
        Permette di aggiungere un metodo alla tabella symbols
        :param identifier: Indica il nome del metodo da aggiungere alla tabella symbols
        :param attributes: Dizionario che indica tutti gli attributi del metodo
        """
        if identifier in self.symbols:
            raise Exception(f"Error: The method '{identifier}' is already defined.")
        self.symbols[identifier] = attributes

    def get_method_attribute(self, identifier):
        """
        Permette di recuperare il dizionario degli attributi di un metodo presente nella tabella symbols
        :param identifier: Indica il nome del metodo di cui recuperare gli attributi
        :return: Restituisce il dizionario degli attributi associato al metodo.
        """
        if identifier not in self.symbols:
            raise Exception(f"Error: The method '{identifier}' was not defined.")
        return self.symbols[identifier]