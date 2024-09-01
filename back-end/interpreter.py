from lark.visitors import Interpreter, Token, Tree
from error_handler import *


class CsharpInterpreter(Interpreter):
    """
    Interprete personalizzato per il linguaggio C# che utilizza la libreria Lark per attraversare e interpretare
    un albero sintattico generato da un parser.
    """

    def __init__(self, csharp_transformer):
        """
        Inizializza l'interprete con un trasformatore C# per manipolare e trasformare gli alberi sintattici.
        :param csharp_transformer: Un'istanza del trasformatore utilizzato per la trasformazione dell'albero sintattico.
        """
        self.csharp_transformer = csharp_transformer

    def start(self, tree):
        """
        Metodo di inizio che visita i figli dell'albero sintattico.
        :param tree: Albero sintattico da visitare.
        :return: Risultato della visita ai figli dell'albero.
        """
        return self.visit_children(tree)

    def var_decl(self, tree):
        """
        Interpreta una dichiarazione di variabile, visitando eventuali chiamate di metodo all'interno.
        :param tree: Albero sintattico della dichiarazione di variabile.
        :return: Albero sintattico trasformato.
        """
        for i in range(len(tree.children)):
            if isinstance(tree.children[i], Tree):
                if tree.children[i].data == 'method_call':
                    tree.children[i] = self.visit(tree.children[i])
        return self.csharp_transformer.transform(tree)

    def var_assignment(self, tree):
        """
        Interpreta un'assegnazione di variabile, visitando eventuali chiamate di metodo all'interno.
        :param tree: Albero sintattico dell'assegnazione di variabile.
        :return: Albero sintattico trasformato.
        """
        for i in range(len(tree.children)):
            if isinstance(tree.children[i], Tree):
                if tree.children[i].data == 'method_call':
                    tree.children[i] = self.visit(tree.children[i])
        return self.csharp_transformer.transform(tree)

    def output_statement(self, tree):
        """
        Interpreta una dichiarazione di output (es. Console.WriteLine()).
        :param tree: Albero sintattico della dichiarazione di output.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def add(self, tree):
        """
        Interpreta un'operazione di addizione.
        :param tree: Albero sintattico dell'operazione di addizione.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def sub(self, tree):
        """
        Interpreta un'operazione di sottrazione.
        :param tree: Albero sintattico dell'operazione di sottrazione.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def mul(self, tree):
        """
        Interpreta un'operazione di moltiplicazione.
        :param tree: Albero sintattico dell'operazione di moltiplicazione.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def div(self, tree):
        """
        Interpreta un'operazione di divisione.
        :param tree: Albero sintattico dell'operazione di divisione.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def mod(self, tree):
        """
        Interpreta un'operazione di divisione con resto (modulo).
        :param tree: Albero sintattico dell'operazione di modulo.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def if_statement(self, tree):
        """
        Interpreta un'istruzione di diramazione di tipo if/if-else.
        :param tree: Albero sintattico della dichiarazione if.
        """
        condition = self.csharp_transformer.transform(tree.children[0])

        if type(condition) != bool and condition is not None:
            raise Exception(f"Semantic Error: Cannot implicitly convert type `{type(condition).__name__}` to `bool`")

        if condition:
            try:
                for statement in tree.children[1].children:
                    self.visit(statement)
            except BreakException:
                raise BreakException
            except ContinueException:
                raise ContinueException
        elif len(tree.children) > 2:
            self.if_statement(tree.children[2])

    def while_statement(self, tree):
        """
        Interpreta un'istruzione di loop di tipo while.
        :param tree: Albero sintattico della dichiarazione while.
        """
        condition = self.csharp_transformer.transform(tree.children[0])

        if type(condition) != bool and condition is not None:
            raise Exception(f"Semantic Error: Cannot implicitly convert type `{type(condition).__name__}` to `bool`")

        while condition:
            try:
                for statement in tree.children[1].children:
                    self.visit(statement)
            except BreakException:
                break
            except ContinueException:
                condition = self.csharp_transformer.transform(tree.children[0])
                continue
            condition = self.csharp_transformer.transform(tree.children[0])

    def switch_statement(self, tree):
        """
        Interpreta un'istruzione di diramazione di tipo switch.
        :param tree: Albero sintattico della dichiarazione switch.
        """
        identifier = tree.children[0]
        if isinstance(identifier, Token):
            identifier_value = self.csharp_transformer.symbol_table.get_value(identifier.value)
        else:
            identifier_value = self.csharp_transformer.transform(identifier)

        matched = False

        for case_clause in tree.children[1:]:
            if case_clause.data == "case_clause":
                case_value = self.csharp_transformer.transform(case_clause.children[0])
                if identifier_value == case_value:
                    matched = True
                    try:
                        for statement in case_clause.children[1:]:
                            self.visit(statement)
                    except BreakException:
                        return

            elif case_clause.data == "default_clause":
                if not matched:
                    try:
                        for statement in case_clause.children:
                            self.visit(statement)
                    except BreakException:
                        return


    def for_statement(self, tree):
        """
        Interpreta un'istruzione di loop di tipo for.
        :param tree: Albero sintattico della dichiarazione for.
        """
        if tree.children[0]:
            self.visit(tree.children[0])

        while True:

            condition = self.csharp_transformer.transform(tree.children[1])

            if not condition:
                break

            try:
                for statement in tree.children[3].children:
                    self.visit(statement)
            except BreakException:
                break
            except ContinueException:
                pass

            if tree.children[2]:
                self.visit(tree.children[2])

    def for_update(self, tree):
        """
        Interpreta un'operazione di aggiornamento all'interno di un ciclo for.
        :param tree: Albero sintattico dell'operazione di aggiornamento del ciclo for.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def eq(self, tree):
        """
        Interpreta un'operazione di uguaglianza.
        :param tree: Albero sintattico dell'operazione di uguaglianza.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def neq(self, tree):
        """
        Interpreta un'operazione di disuguaglianza.
        :param tree: Albero sintattico dell'operazione di disuguaglianza.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def lt(self, tree):
        """
        Interpreta un'operazione di minore.
        :param tree: Albero sintattico dell'operazione di minore.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def gt(self, tree):
        """
        Interpreta un'operazione di maggiore.
        :param tree: Albero sintattico dell'operazione di maggiore.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def le(self, tree):
        """
        Interpreta un'operazione di minore o uguale.
        :param tree: Albero sintattico dell'operazione di minore o uguale.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def ge(self, tree):
        """
        Interpreta un'operazione di maggiore o uguale.
        :param tree: Albero sintattico dell'operazione di maggiore o uguale.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def bool_expr(self, tree):
        """
        Interpreta un'espressione booleana.
        :param tree: Albero sintattico dell'espressione booleana.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def lor(self, tree):
        """
        Interpreta un'operazione di OR logico.
        :param tree: Albero sintattico dell'operazione di OR logico.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def land(self, tree):
        """
        Interpreta un'operazione di AND logico.
        :param tree: Albero sintattico dell'operazione di AND logico.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def lnot(self, tree):
        """
        Interpreta un'operazione di NOT logico.
        :param tree: Albero sintattico dell'operazione di NOT logico.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def false(self, tree):
        """
        Interpreta il valore booleano False.
        :param tree: Albero sintattico del valore False.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def true(self, tree):
        """
        Interpreta il valore booleano True.
        :param tree: Albero sintattico del valore True.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def input_statement(self, tree):
        """
        Interpreta una dichiarazione di input (es. Console.ReadLine()).

        :param tree: Albero sintattico della dichiarazione di input.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def break_statement(self, tree):
        """
        Interpreta una dichiarazione break, interrompendo l'esecuzione del ciclo.
        :param tree: Albero sintattico della dichiarazione break.
        :raise BreakException: Eccezione per interrompere un ciclo.
        """
        raise BreakException()

    def continue_statement(self, tree):
        """
        Interpreta una dichiarazione continue, interrompendo l'iterazione corrente del ciclo e passando alla successiva.
        :param tree: Albero sintattico della dichiarazione continue.
        :raise ContinueException: Eccezione per passare alla successiva iterazione di un ciclo.
        """
        raise ContinueException()

    def length_statement(self, tree):
        """
        Interpreta un'operazione per ottenere la lunghezza di una stringa o un array.
        :param tree: Albero sintattico dell'operazione length.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def to_upper_string(self, tree):
        """
        Interpreta un'operazione per convertire una stringa in maiuscolo.
        :param tree: Albero sintattico dell'operazione toUpperCase.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def to_lower_string(self, tree):
        """
        Interpreta un'operazione per convertire una stringa in minuscolo.
        :param tree: Albero sintattico dell'operazione toUpperCase.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def array_decl(self, tree):
        """
         Interpreta una dichiarazione di array.
         :param tree: Albero sintattico della dichiarazione di array.
         :return: Albero sintattico trasformato.
         """
        return self.csharp_transformer.transform(tree)

    def array_assignment(self, tree):
        """
        Interpreta un'assegnazione per un array.
        :param tree: Albero sintattico dell'assegnazione a un array.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)

    def access_statement(self, tree):
        """
         Interpreta un'operazione di accesso a un elemento di un array o a una stringa.
         :param tree: Albero sintattico dell'operazione di accesso.
         :return: Albero sintattico trasformato.
         """
        return self.csharp_transformer.transform(tree)

    def method_declaration(self, tree):
        """
        Interpreta una dichiarazione di metodo e registra il metodo nella tabella dei simboli.
        :param tree: Albero sintattico della dichiarazione di metodo.
        """
        identifier = None
        method_body = []
        parameter_list = []

        if isinstance(tree.children[0], Token):
            if tree.children[0].type == "IDENTIFIER":
                identifier = tree.children[0]
                for child in tree.children[1:]:
                    if isinstance(child, Tree):
                        if child.data == "statement":
                            method_body.append(child)
                        elif child.data == "parameter_list":
                            parameter_list.extend(child.children)

            self.csharp_transformer.symbol_table.method_define(identifier=identifier,
                                                               attributes={'data_type': None,
                                                                           'parameter_list': parameter_list,
                                                                           'method_body': method_body})

        elif tree.children[0].data == "data_type":
            data_type = tree.children[0]
            identifier = tree.children[1]
            for child in tree.children[2:]:
                if isinstance(child, Tree):
                    if child.data == "statement":
                        method_body.append(child)
                    elif child.data == "parameter_list":
                        parameter_list.extend(child.children)

            self.csharp_transformer.symbol_table.method_define(identifier=identifier,
                                                               attributes={'data_type': data_type,
                                                                           'parameter_list': parameter_list,
                                                                           'method_body': method_body})

    def method_call(self, tree):
        """
        Interpreta una chiamata di metodo, verifica i tipi di argomenti ed esegue il corpo del metodo.
        :param tree: Albero sintattico della chiamata di metodo.
        :return: Risultato dell'esecuzione del metodo.
        :raise TypeError: Se i tipi di argomenti o di ritorno non corrispondono.
        """
        identifier = tree.children[0]


        arguments = self.csharp_transformer.symbol_table.get_method_attribute(identifier)
        data_type = arguments['data_type']
        parameter_list = arguments['parameter_list']
        method_body = arguments['method_body']

        argument_list = []


        if len(tree.children) > 1 and isinstance(tree.children[1], Tree) and tree.children[1].data == 'argument_list':
            for child in tree.children[1].children:
                if isinstance(child, Tree):
                    argument_list.append(self.csharp_transformer.transform(child))

        if len(argument_list) != len(parameter_list) // 2:
            raise TypeError(f"Expected {len(parameter_list) // 2} arguments, got {len(argument_list)}")

        type_map = {
            'string': str,
            'int': int,
            'bool': bool
        }

        for i in range(0, len(parameter_list), 2):
            param_type = parameter_list[i]
            param_name = parameter_list[i + 1]
            argument_value = argument_list[i // 2]

            expected_type = type_map.get(param_type.children[0], None)
            if expected_type is None:
                raise TypeError(f"Unknown parameter type {param_type.children[0]}")

            if not isinstance(argument_value, expected_type):
                raise TypeError(
                    f"Argument {param_name.value} expected type {expected_type.__name__}, got {type(argument_value).__name__}"
                )
            self.csharp_transformer.symbol_table.define(identifier=param_name, symbol_type=param_type, value=argument_value)

        result = None

        for statement in method_body:

            if isinstance(statement.children[0], Tree) and statement.children[0].data == 'return_statement':
                result = self.csharp_transformer.transform(statement.children[0])
                break
            elif isinstance(statement.children[0], Tree):
                result = self.csharp_transformer.transform(statement.children[0])

        if result is not None:
            expected_return_type = type_map.get(data_type.children[0].value, None)
            if expected_return_type is None:
                raise TypeError(f"Unknown return type {data_type.children[0].value}")
            if not isinstance(result, expected_return_type):
                raise TypeError(
                    f"Return value expected type {expected_return_type.__name__}, got {type(result).__name__}"
                )

        return result

    def return_statement(self, tree):
        """
        Interpreta una dichiarazione return all'interno di un metodo.
        :param tree: Albero sintattico della dichiarazione return.
        :return: Albero sintattico trasformato.
        """
        return self.csharp_transformer.transform(tree)
