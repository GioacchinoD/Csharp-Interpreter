from lark.visitors import Interpreter


class CsharpInterpreter(Interpreter):

    def __init__(self, csharp_transformer):
        self.csharp_transformer = csharp_transformer

    def start(self, tree):
        return self.visit_children(tree)

    def var_decl(self, tree):
        return self.csharp_transformer.transform(tree)

    def var_assignment(self, tree):
        return self.csharp_transformer.transform(tree)

    def output_statement(self, tree):
        return self.csharp_transformer.transform(tree)

    def add(self, tree):
        return self.csharp_transformer.transform(tree)

    def sub(self, tree):
        return self.csharp_transformer.transform(tree)

    def mul(self, tree):
        return self.csharp_transformer.transform(tree)

    def div(self, tree):
        return self.csharp_transformer.transform(tree)

    def mod(self, tree):
        return self.csharp_transformer.transform(tree)

    def if_statement(self, tree):
        # Ottieni la condizione
        condition = self.csharp_transformer.transform(tree.children[0])

        if condition:

            for statement in tree.children[1].children:
                self.visit(statement)

        elif len(tree.children) > 2:
            # Visita il blocco "else", se esiste
            # print("condizione falsa")
            self.if_statement(tree.children[2])

    def while_statement(self, tree):
        condition = self.csharp_transformer.transform(tree.children[0])
        while condition:
            for statement in tree.children[1].children:
                self.visit(statement)

            condition = self.csharp_transformer.transform(tree.children[0])

    def eq(self, tree):
        return self.csharp_transformer.transform(tree)

    def neq(self, tree):
        return self.csharp_transformer.transform(tree)

    def lt(self, tree):
        return self.csharp_transformer.transform(tree)

    def gt(self, tree):
        return self.csharp_transformer.transform(tree)

    def le(self, tree):
        return self.csharp_transformer.transform(tree)

    def ge(self, tree):
        return self.csharp_transformer.transform(tree)

    def bool_expr(self, tree):
        return self.csharp_transformer.transform(tree)

    def lor(self, tree):
        return self.csharp_transformer.transform(tree)

    def land(self, tree):
        return self.csharp_transformer.transform(tree)

    def lnot(self, tree):
        return self.csharp_transformer.transform(tree)

    def false(self, tree):
        return self.csharp_transformer.transform(tree)

    def true(self, tree):
        return self.csharp_transformer.transform(tree)

    def input_statement(self, tree):
        return self.csharp_transformer.transform(tree)
