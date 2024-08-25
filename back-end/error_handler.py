class CsharpInterpreterError(Exception):
    pass

class SymbolNotFoundError(CsharpInterpreterError):
    def __init__(self, identifier):
        super().__init__(f"Error: Variable '{identifier}' not found.")

class SymbolRedefinitionError(CsharpInterpreterError):
    def __init__(self, identifier):
        super().__init__(f"Error: Variable '{identifier}' already defined.")

class TypeMismatchError(CsharpInterpreterError):
    def __init__(self, expected, got):
        super().__init__(f"Error: Wrong type. Expected '{expected}', obtained '{got}'.")


class CsharpSyntaxError(SyntaxError):
    def __str__(self):
        context, line, column = self.args
        return '%s at line %s, column %s.\n\n%s' % (self.label, context, line, column)

class UnmatchedParenthesisError(CsharpSyntaxError):
    pass

class MissingOpeningBracketError(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing ('

    def __str__(self):
        context, line, column = self.args
        error_pointer = ' ' * (column - 2) + '^'
        return '%s at line %s, column %s.\n\n%s\n%s' % (self.label, line, column, context, error_pointer)

class MissingClosingBracketError(UnmatchedParenthesisError):
    label = 'Syntax Error: Missing )'

    def __str__(self):
        context, line, column = self.args
        error_pointer = ' ' * (column - 2) + '^'
        return '%s at line %s, column %s.\n\n%s\n%s' % (self.label, line, column, context, error_pointer)

class MissingEqual(CsharpSyntaxError):
    label = 'Syntax Error: Missing ='

    def __str__(self):
        context, line, column = self.args
        error_pointer = ' ' * (column - 2) + '^'
        return '%s at line %s, column %s.\n\n%s\n%s' % (self.label, line, column, context, error_pointer)

class MissingSemicolon(CsharpSyntaxError):
    label = 'Syntax Error: Missing ;'

    def __str__(self):
        context, line, column = self.args
        error_pointer = ' ' * (column - 2) + '^'
        return '%s at line %s, column %s.\n\n%s\n%s' % (self.label, line, column, context, error_pointer)

class CsharpSemanticError(Exception):
    pass

class UnsupportedOperationType(CsharpSemanticError):
    def __init__(self, type1, type2, operation):
        super().__init__(f"Semantic Error: The operation '{operation}' is not supported by type '{type1.__name__}' and '{type2.__name__}'.")

class  IndexOut(CsharpSemanticError):
    def __init__(self, length, position):
        super().__init__(f"Semantic Error, index out of range: Tried to access position {position}, but the valid range is 0 to {length - 1}.")


def op_type(items, operation):
    if type(items[0]) != type(items[1]):
        raise UnsupportedOperationType(type1=type(items[0]), type2=type(items[1]), operation=operation)

def check_array_type(array_type, expected_type):
    if type(array_type) != type(expected_type):
        raise TypeMismatchError(expected_type, array_type)


def type_in_array(array_type, array_content):
    if array_type == 'string':
        for item in array_content:
            if not item.startswith('"') and not item.endswith('"'):
                raise TypeError(
                    f"Invalid value for string array. Check element at position:  {array_content.index(item)}")
    elif array_type == 'int':
        for item in array_content:
            try:
                int(item)
            except ValueError:
                raise TypeError(
                    f"Invalid value for array of integers. Check element at position: {array_content.index(item)}")


def length_array(array_max_length, array_content):
    if array_max_length != len(array_content):
        raise Exception(
            f"It expected initialization of arrays of length {array_max_length}, and not length {len(array_content)}.")


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass