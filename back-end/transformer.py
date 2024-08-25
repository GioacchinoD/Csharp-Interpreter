from lark import Transformer, Token
from symbol_table import SymbolTable
from error_handler import *
from flask_socketio import emit
from threading import Event


class CSharpTransformer(Transformer):
    """
    Questa classe estende la classe transformer di Lark, che fornisce una comoda interfaccia per elaborare l'albero di
    parse restituito da Lark. Ogni metodo della classe corrisponde a una delle regole della grammatica.
    """

    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.input_value = None  # Variabile utilizzata per memorizzare il valore di input
        self.input_event = Event()  # Evento per sincronizzare l'input

    def var_decl(self, items):
        """
        Gestisce la dichiarazione di una variabile. La variabile può essere dichiarata con o senza
        l'assegnazione di un valore iniziale. Se un valore viene fornito, viene verificato e convertito
        al tipo di dato specificato.

        La dichiarazione può avvenire in due modi principali:
        - int a = 5: Dichiarazione di una variabile con un tipo specifico e un valore iniziale.
        - string s: Dichiarazione di una variabile con un tipo specifico senza valore iniziale.

        :param items: Una lista contenente il tipo di dato, l'identificatore della variabile e, opzionalmente,
                      il valore da assegnare.
        :raises ValueError: Se il valore assegnato non è compatibile con il tipo di dato dichiarato.
        """
        if len(items) == 3: # dichiarazione di una variabile con tre elementi (tipo, identifier, valore)

            data_type = items[0]
            identifier = items[1]
            value = items[2]

            # Conversione del valore in base al tipo di dato
            if data_type.children[0].value == "int":
                if type(value) in [int, float]:
                    value = int(value)
                else:
                    raise ValueError(f"Invalid value for variable {identifier} of type int: '{value}'")
            elif data_type.children[0].value == "string":
                value = str(value).strip('"')
            elif data_type.children[0].value == "bool":
                if isinstance(value, bool):
                    value = value
                else:
                    raise ValueError(f"Invalid value for variable {identifier} of type bool: '{value}'")

            self.symbol_table.define(identifier, data_type, value)

        elif len(items) == 2: # dichiarazione di una variabile con due elementi (tipo, identifier)
            data_type = items[0]
            identifier = items[1]

            self.symbol_table.define(identifier, data_type)

    def var_assignment(self, items):
        """
        Gestisce l'assegnazione di un nuovo valore a una variabile già definita. La variabile può essere aggiornata
        con un valore calcolato attraverso operazioni aritmetiche o con un valore diretto. La funzione verifica
        il tipo di dato della variabile e converte il valore assegnato in base al tipo di dato specificato.

        La variabile può essere assegnata in due modi principali:
        - Attraverso operazioni aritmetiche: Incremento, decremento, somma, sottrazione, moltiplicazione, divisione.
        - Assegnazione diretta di un valore.

        :param items: Una lista contenente l'identificatore della variabile e il valore da assegnare.
                      Il valore può essere una operazione aritmetica o un valore diretto.
        :raises SymbolNotFoundError: Se l'identificatore della variabile non è presente nella tabella dei simboli.
        :raises ValueError: Se il valore assegnato non è compatibile con il tipo di dato della variabile.
        """
        identifier = items[0]

        # Verifica se la variabile indicata esiste nella tabella dei simboli
        if identifier not in self.symbol_table.symbols:
            raise SymbolNotFoundError(identifier)

        # Gestione delle operazioni incrementali e assegnazioni aritmetiche
        if len(items) >= 2 and isinstance(items[1], Token):
            if items[1].type == "INCREASES_BY_ONE":
                pre_val = self.symbol_table.get_value(identifier)
                value = pre_val + 1
            elif items[1].type == "DECREASES_BY_ONE":
                pre_val = self.symbol_table.get_value(identifier)
                value = pre_val - 1
            elif items[1].type == "SUM_AT_VAR":
                value_identifier = self.symbol_table.get_value(identifier)
                value = self.add([value_identifier, items[2]])
            elif items[1].type == "SUB_AT_VAR":
                value_identifier = self.symbol_table.get_value(identifier)
                value = self.sub([value_identifier, items[2]])
            elif items[1].type == "MUL_AT_VAR":
                value_identifier = self.symbol_table.get_value(identifier)
                value = self.mul([value_identifier, items[2]])
            elif items[1].type == "DIV_AT_VAR":
                value_identifier = self.symbol_table.get_value(identifier)
                value = self.div([value_identifier, items[2]])

        else: # Assegnazione diretta di valore
            value = items[1]

            # Controllo del tipo di dato atteso
            expected_type = self.symbol_table.get_type(identifier)
            e_type = expected_type.children[0].value

            # Conversione del valore in base al tipo di dato
            if e_type == "int":
                if type(value) in [int, float]:
                    value = int(value)
                else:
                    raise ValueError(f"Invalid value for variable {identifier} of type int: '{value}'")
            elif e_type == "string":
                value = str(value).strip('"')
            elif e_type == "bool":
                if isinstance(value, bool):
                    value = value
                else:
                    raise ValueError(f"Invalid value for variable {identifier} of type bool: '{value}'")

        self.symbol_table.set_value(identifier, value)

    # Funzioni necessarie a gestire espressioni booleane, termini, etc..

    @staticmethod
    def bool_expr(items):
        """
        Restituisce il risultato di un'espressione booleana.
        :param items: Elementi dell'espressione booleana.
        :return: Risultato dell'espressione booleana.
        """
        return items[0]

    @staticmethod
    def bool_term(items):
        """
        Restituisce il risultato di un termine booleano.
        :param items: Elementi del termine booleano.
        :return: Risultato del termine booleano.
        """
        return items[0]

    @staticmethod
    def expr(items):
        """
        Restituisce il risultato di un'espressione.
        :param items: Elementi dell'espressione.
        :return: Risultato dell'espressione.
        """
        return items[0]

    @staticmethod
    def term(items):
        """
        Restituisce il risultato di un termine.
        :param items: Elementi del termine.
        :return: Risultato del termine.
        """
        return items[0]

    def factor(self, items):
        """
        Gestisce il recupero di un valore (fattore) da un numero, stringa o identificatore.
        :param items: Elementi che rappresentano il fattore.
        :return: Il valore del fattore.
        """
        if items[0].type == 'NUMBER':
            return int(items[0].value)
        elif items[0].type == 'STRING':
            return str(items[0].value.strip('"'))
        elif items[0].type == 'IDENTIFIER':
            return self.symbol_table.get_value(items[0].value)
        return items[0]

    # Operazioni aritmetiche di somma, sottrazione, moltiplicazione e divisione, modulo

    @staticmethod
    def add(items):
        """
        Gestisce l'operazione di somma o la concatenazione di stringhe
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce la somma tra numeri o la concatenazione di stringhe
        """
        operation = 'addition'
        try:
            if type(items[0]) == type(items[1]):
                return items[0] + items[1]
            elif type(items[0]) in [int, list] and type(items[1]) == str:
                return str(items[0]) + items[1]
            elif type(items[0]) == str and type(items[1]) in [int, list]:
                return items[0] + str(items[1])
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def sub(items):
        """
        Gestisce l'operazione di sottrazione
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce il risultato dell'operazione
        """
        operation = "subtraction"
        try:
            op_type(items, operation)
            return items[0] - items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def mul(items):
        """
        Gestisce l'operazione di moltiplicazione
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce il risultato dell'operazione
        """
        operation = "multiplication"
        try:
            op_type(items, operation)
            return items[0] * items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def div(items):
        """
        Gestisce l'operazione di divisione
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce il risultato dell'operazione
        """
        operation = "division"
        try:
            op_type(items, operation)
            if type(items[0]) == int:
                return items[0] // items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def mod(items):
        """
        Gestisce l'operazione di divisione con resto
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce il risultato dell'operazione
        """
        operation = "module"
        try:
            op_type(items, operation)
            return items[0] % items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    # Funzioni per confronti logici e operazioni logiche

    @staticmethod
    def eq(items):
        """
        Verifica l'uguaglianza
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] == items[1]

    @staticmethod
    def neq(items):
        """
        Verifica di diseguaglianza
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] != items[1]

    @staticmethod
    def lt(items):
        """
        Verifica se il primo elemento è minore del secondo
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] < items[1]

    @staticmethod
    def gt(items):
        """
        Verifica se il primo elemento è maggiore del secondo
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] > items[1]

    @staticmethod
    def le(items):
        """
        Verifica se il primo elemento è minore o uguale del secondo
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] <= items[1]

    @staticmethod
    def ge(items):
        """
        Verifica se il primo elemento è maggiore o uguale del secondo
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] >= items[1]

    @staticmethod
    def lor(items):
        """
        Gestisce l'operazione logica OR
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] or items[1]

    @staticmethod
    def land(items):
        """
        Gestisce l'operazione logica AND
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return items[0] and items[1]

    @staticmethod
    def lnot(items):
        """
        Gestisce l'operazione logica NOT
        :param items: Contiene gli elementi da utilizzare per il confronto
        :return: Restituisce True o False in base al risultato dell'operazione di confronto
        """
        return not items[0]

    @staticmethod
    def false(items):
        """
        Restituisce il valore booleano False.
        :param items: Gli elementi associati al valore booleano (non utilizzati).
        :return: False
        """
        return False

    @staticmethod
    def true(items):
        """
        Restituisce il valore booleano True.
        :param items: Gli elementi associati al valore booleano (non utilizzati).
        :return: True
        """
        return True

    # Istruzioni di Input/Output
    def set_input_value(self, input_value):
        """
        Metodo per settare il valore di input dall'esterno.
        :param input_value: Valore di input inserito dall'utente.
        """
        # Imposta il valore dell'input e segnala che è disponibile
        self.input_value = input_value
        self.input_event.set()

    def input_statement(self, items):
        """
        Gestisce la dichiarazione di input, attendendo un valore dall'utente.
        """
        emit('input_required')
        self.input_event.wait()  # Aspetta che l'input venga impostato
        self.input_event.clear()  # Resetta l'evento per eventuali input futuri
        if self.input_value == '':
            emit('error', {'error': 'No input value provided'})
            raise
        else:
            value = self.input_value  # Recupera il valore dell'input
        try:
            value = int(value)
        except ValueError:
            pass
        return value  # Restituisci il valore dell'input

    @staticmethod
    def output_statement(items):
        """
        Gestisce l'istruzione di output, inviando il valore al client.
        :param items: Valore da inviare al client.
        """
        if not items:
            emit('output', {'output': ' '})
        else:
            emit('output', {'output': items[0]})

    # Istruzione di break
    @staticmethod
    def break_statement(items):
        """
        Gestisce l'istruzione 'break' all'interno di un ciclo.
        Lancia un'eccezione BreakException per uscire dal ciclo.
        :param items: Gli elementi associati all'istruzione break (se presenti).
        """
        raise BreakException("break statement")

    # Istruzione continue
    @staticmethod
    def continue_statement(items):
        """
        Gestisce l'istruzione 'continue' all'interno di un ciclo.
        Lancia un'eccezione ContinueException per saltare alla prossima iterazione del ciclo.
        :param items: Gli elementi associati all'istruzione continue (se presenti).
        """
        raise ContinueException("continue statement")

    # Definizione di funzioni per metodi sulle stringhe e per la dichiarazione/assegnazione di array

    def length_statement(self, items):
        """
        Permette di ottenere la lunghezza di una variabile di tipo string, o la lunghezza di un array
        :param items:
        :return: Restituisce la lunghezza di una variabile di tipo string o la lunghezza di un array
        """
        identifier = items[0]
        value = self.symbol_table.get_value(identifier)
        if isinstance(value, str):
            return len(value)
        elif isinstance(value, list):
            return len(value)
        else:
            raise TypeError(f"Cannot get Length of non-string or non-array type for variable {identifier}")

    def access_statement(self, items):
        """
        Permette di ottenere un elemento a una determinata posizione di una stringa o di un array
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce l'elemento alla posizione richiesta
        """
        identifier = items[0]

        if identifier not in self.symbol_table.symbols:
            raise SymbolNotFoundError(identifier)

        position = items[1]
        value = self.symbol_table.get_value(identifier)
        if isinstance(value, str):
            try:
                return value[position]
            except Exception:
                raise IndexOut(length=len(value), position=position)
        elif isinstance(value, list):
            try:
                return value[position]
            except Exception:
                raise IndexOut(length=len(value), position=position)
        else:
            raise TypeError(f"Cannot get element at position {position} for not-string or not-array type for variable {identifier}")

    def to_upper_string(self, items):
        """
        Permette di convertire una stringa in caratteri maiuscoli.
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce una stringa convertita in caratteri maiuscoli.
        """
        identifier = items[0]
        value = self.symbol_table.get_value(identifier)
        if type(value) == str:
            value = value.upper()
            return value
        else:
            raise TypeError(f"Cannot get Upper of non-string type for variable {identifier}")

    def to_lower_string(self, items):
        """
        Permette di convertire una stringa in caratteri minuscoli.
        :param items: Contiene gli elementi da utilizzare per l'operazione
        :return: Restituisce una stringa convertita in caratteri minuscoli.
        """
        identifier = items[0]
        value = self.symbol_table.get_value(identifier)
        if isinstance(value, str):
            return str(value.lower())
        else:
            raise TypeError(f"Cannot get Lower of non-string type for variable {identifier}")


    def array_decl(self, items):
        """
        Gestisce la dichiarazione di un array in vari formati, definendo il tipo di array e il contenuto,
        e memorizzandolo nella symbol table.

        La dichiarazione di array può essere di varie forme, ad esempio:
        - string[] cars                : Dichiarazione di un array vuoto di tipo stringa.
        - string[] cars = {"Volvo", "BMW"}: Dichiarazione e inizializzazione di un array con elementi.
        - string[] cars = new string[] {"Volvo", "BMW"}: Dichiarazione con allocazione di memoria e inizializzazione.
        - string[] cars = new string[4] {"Volvo", "BMW"}: Dichiarazione con dimensione fissa e inizializzazione.

        :param items: Una lista di elementi che rappresentano il tipo di array, l'identificatore,
                      e opzionalmente il contenuto e la lunghezza dell'array.
        """
        array_type = items[0]
        identifier = items[1]

        if len(items) == 2:  # Dichiarazione di un array con due elementi (es. string[] cars)
            self.symbol_table.define(identifier, array_type, value=[])

        elif len(items) == 3:  # Dichiarazione di un array con tre elementi (es. string[] cars = {"Volvo", "BMW", "Ford", "Mazda"})
            array_content = [item.strip() for item in items[2].split(',')]
            type_in_array(array_type.children[0].children[0].value, array_content)

            if array_type.children[0].children[0].value == 'string':
                array_content = [item.strip('"') for item in array_content]
            if array_type.children[0].children[0].value == 'int':
                array_content = [int(item) for item in array_content]

            self.symbol_table.define(identifier, array_type, array_content)

        elif len(items) == 4: # Dichiarazione di un array con quattro elementi (es. string[] cars = new string[] {"Volvo", "BMW", "Ford", "Mazda"})
            if isinstance(items[3], Token):
                if items[3].type == 'ARRAY_CONTENT':
                    array_content = [item.strip() for item in items[3].split(',')]
                    type_in_array(array_type.children[0].children[0].value, array_content)

                    if array_type.children[0].children[0].value == 'string':
                        array_content = [item.strip('"') for item in array_content]
                    if array_type.children[0].children[0].value == 'int':
                        array_content = [int(item) for item in array_content]
                        self.symbol_table.define(identifier, array_type, array_content)
            else:
                self.symbol_table.define(identifier, array_type, value=[])

        elif len(items) == 5: # Dichiarazione di un array con cinque elementi (es. string[] cars = new string[4] {"Volvo", "BMW", "Ford", "Mazda"})
            array_max_length = items[3]
            array_content = [item.strip() for item in items[4].split(',')]
            length_array(array_max_length, array_content)
            type_in_array(array_type.children[0].children[0].value, array_content)

            if array_type.children[0].children[0].value == 'string':
                array_content = [item.strip('"') for item in array_content]
            if array_type.children[0].children[0].value == 'int':
                array_content = [int(item) for item in array_content]

            self.symbol_table.define(identifier, array_type, array_content)

    def array_assignment(self, items):
        """
        Gestisce l'assegnazione del contenuto a un array già definito in precedenza. Verifica che l'array esista
        e che il tipo di dati assegnato sia corretto, quindi aggiorna il contenuto dell'array nella symbol table.

        L'assegnazione può avvenire in due modi principali:
        - cars = new string[] {"Volvo", "BMW", "Ford"}: Assegnazione di un nuovo array con elementi specificati.
        - cars = new string[4] {"Volvo", "BMW", "Ford", "Mazda"}: Assegnazione di un nuovo array con una dimensione massima e elementi specificati.

        :param items: Una lista di elementi che rappresentano l'identificatore dell'array,
                      il tipo previsto e il contenuto da assegnare.
        """
        identifier = items[0]

        if identifier not in self.symbol_table.symbols:
            raise SymbolNotFoundError(identifier)

        array_type = self.symbol_table.get_type(identifier)
        expected_type = items[1]

        check_array_type(array_type.children[0].children[0].value, expected_type.children[0].value)

        if len(items) == 3: # Assegnazione di un array con tre elementi (es. cars = new string[] {"Volvo", "BMW", "Ford"})
            array_content = [item.strip() for item in items[2].split(',')]
            type_in_array(array_type.children[0].children[0].value, array_content)
            if array_type.children[0].children[0].value == 'string':
                array_content = [item.strip('"') for item in array_content]
            if array_type.children[0].children[0].value == 'int':
                array_content = [int(item) for item in array_content]

            self.symbol_table.set_value(identifier, array_content)

        elif len(items) == 4: # Assegnazione di un array con quattro elementi (es. cars = new string[4] {"Volvo", "BMW", "Ford", "Mazda"})
            array_max_length = items[2]
            array_content = [item.strip() for item in items[3].split(',')]
            type_in_array(array_type.children[0].children[0].value, array_content)
            length_array(array_max_length, array_content)
            if array_type.children[0].children[0].value == 'string':
                array_content = [item.strip('"') for item in array_content]
            if array_type.children[0].children[0].value == 'int':
                array_content = [int(item) for item in array_content]

            self.symbol_table.set_value(identifier, array_content)

    # Aggiornamento della variabile di controllo di un ciclo for
    def for_update(self, items):
        """
        Gestisce l'aggiornamento di una variabile all'interno di un ciclo for.
        :param items: Contiene gli elementi necessari per aggiornare una variabile (generalmente un'espressione di assegnazione).
        :return: Restituisce il risultato dell'operazione di assegnazione della variabile.
        """
        return self.var_assignment(items)

    # Clausole presenti in un'istruzione switch
    @staticmethod
    def case_clause(items):
        """
        Rappresenta una clausola 'case' in una struttura di controllo switch-case.
        :param items: Gli elementi associati alla clausola 'case'.
        :return: Restituisce gli elementi della clausola 'case'.
        """
        return items

    @staticmethod
    def default_clause(items):
        """
        Rappresenta una clausola 'default' in una struttura di controllo switch-case.
        :param items: Gli elementi associati alla clausola 'default'.
        :return: Restituisce gli elementi della clausola 'default'.
        """
        return items

    # Istruzione di return
    @staticmethod
    def return_statement(items):
        """
        Gestisce l'operazione di 'return' in una funzione o metodo.
        :param items: Contiene gli elementi da restituire come risultato della funzione.
        :return: Restituisce il primo elemento dell'espressione di ritorno.
        """
        return items[0]