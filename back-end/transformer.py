from lark import Transformer, Token
from symbol_table import SymbolTable
from error_handler import *
from flask_socketio import emit
from threading import Event


class CSharpTransformer(Transformer):

    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.input_value = None
        self.input_event = Event()

    def var_decl(self, items):
        # print(items)
        if len(items) == 3:

            data_type = items[0]
            identifier = items[1]
            value = items[2]

            if data_type.children[0].value == "int":
                if type(value) in [int, float]:
                    value = int(value)
                else:
                    raise ValueError(f"Valore non valido per la variabile {identifier} tipo int: '{value}'")
            elif data_type.children[0].value == "string":
                value = str(value).strip('"')
            elif data_type.children[0].value == "bool":
                if isinstance(value, bool):
                    value = value
                else:
                    raise ValueError(f"Valore non valido per la variabile {identifier} tipo bool: '{value}'")

            self.symbol_table.define(identifier, data_type, value)

        elif len(items) == 2:
            data_type = items[0]
            identifier = items[1]

            self.symbol_table.define(identifier, data_type)

    def var_assignment(self, items):
        # print(items)
        identifier = items[0]

        if identifier not in self.symbol_table.symbols:
            raise SymbolNotFoundError(identifier)

        value = items[1]

        expected_type = self.symbol_table.get_type(identifier)
        e_type = expected_type.children[0].value

        if e_type == "int":
            if type(value) in [int, float]:
                value = int(value)
            else:
                raise ValueError(f"Valore non valido per la variabile {identifier} tipo int: '{value}'")
        elif e_type == "string":
            value = str(value).strip('"')
        elif e_type == "bool":
            if isinstance(value, bool):
                value = value
            else:
                raise ValueError(f"Valore non valido per la variabile {identifier} tipo bool: '{value}'")

        self.symbol_table.set_value(identifier, value)

    @staticmethod
    def output_statement(items):
        if not items:
            emit('output', {'output': ' '})
            # print('')
        else:
            emit('output', {'output': items[0]})
            # print(items[0])

    @staticmethod
    def bool_expr(items):
        return items[0]

    @staticmethod
    def bool_term(items):
        return items[0]

    @staticmethod
    def expr(items):
        return items[0]

    @staticmethod
    def term(items):
        return items[0]

    def factor(self, items):
        if items[0].type == 'NUMBER':
            return int(items[0].value)
        elif items[0].type == 'STRING':
            return str(items[0].value.strip('"'))  # Remove quotes
        elif items[0].type == 'IDENTIFIER':
            # print("valore= ", self.symbol_table.get_value(expr_tree))
            return self.symbol_table.get_value(items[0].value)
        return items[0]

    @staticmethod
    def add(items):
        operation = 'addition'
        try:
            if type(items[0]) in [int, float] and type(items[1]) in [int, float] or type(items[0]) == type(items[1]):
                return items[0] + items[1]
            elif type(items[0]) in [int, float, list] and type(items[1]) == str:
                return str(items[0]) + items[1]
            elif type(items[0]) == str and type(items[1]) in [int, float, list]:
                return items[0] + str(items[1])
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def sub(items):
        operation = "subtraction"
        try:
            op_type(items, operation)
            return items[0] - items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def mul(items):
        operation = "multiplication"
        try:
            op_type(items, operation)
            return items[0] * items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def div(items):
        operation = "division"
        try:
            op_type(items, operation)
            if type(items[0]) == int:
                return items[0] // items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def mod(items):
        operation = "module"
        try:
            op_type(items, operation)
            return items[0] % items[1]
        except UnsupportedOperationType:
            raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

    @staticmethod
    def eq(items):
        return items[0] == items[1]

    @staticmethod
    def neq(items):
        return items[0] != items[1]

    @staticmethod
    def lt(items):
        return items[0] < items[1]

    @staticmethod
    def gt(items):
        return items[0] > items[1]

    @staticmethod
    def le(items):
        return items[0] <= items[1]

    @staticmethod
    def ge(items):
        return items[0] >= items[1]

    @staticmethod
    def lor(items):
        return items[0] or items[1]

    @staticmethod
    def land(items):
        return items[0] and items[1]

    @staticmethod
    def lnot(items):
        return not items[0]

    @staticmethod
    def false(items):
        return False

    @staticmethod
    def true(items):
        return True

    def set_input_value(self, input_value):
        self.input_value = input_value
        self.input_event.set()

    def input_statement(self, items):
        print("items: ", items)
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
