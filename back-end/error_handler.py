class CsharpInterpreterError(Exception):
    pass

class SymbolNotFoundError(CsharpInterpreterError):
    def __init__(self, identifier):
        super().__init__(f"Errore: Variabile '{identifier}' non trovata.")

class SymbolRedefinitionError(CsharpInterpreterError):
    def __init__(self, identifier):
        super().__init__(f"Errore: Variabile '{identifier}' già definita.")

class TypeMismatchError(CsharpInterpreterError):
    def __init__(self, expected, got):
        super().__init__(f"Errore: Tipo errato. Aspettato '{expected}', ottenuto '{got}'.")


class CsharpSyntaxError(SyntaxError):
    def __str__(self):
        context, line, column = self.args
        return '%s at line %s, column %s.\n\n%s' % (self.label, context, line, column)

class UnmatchedParenthesisError(CsharpSyntaxError):
    pass

class MissingOpeningBracketError(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing ('

class MissingClosingBracketError(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing )'

class MissingEqual(CsharpSyntaxError):
    label = 'Syntax Error: Missing ='

class MissingSemicolon(CsharpSyntaxError):
    label = 'Syntax Error: Missing ;'

class CsharpSemanticError(Exception):
    pass

class UnsupportedOperationType(CsharpSemanticError):
    def __init__(self, type1, type2, operation):
        super().__init__(f"The operation '{operation}' is not supported by type '{type1}' and '{type2}'.")


def op_type(items, operation):
    if type(items[0]) != type(items[1]):
        raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)