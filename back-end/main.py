import base64
from lark import Lark, UnexpectedInput
from lark.exceptions import UnexpectedEOF, UnexpectedToken
from lark.tree import pydot__tree_to_png
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from transformer import CSharpTransformer
from interpreter import CsharpInterpreter
from error_handler import *

# Carica la grammatica dal file
with open('csharp_grammar.lark', 'r') as file:
    grammar = file.read()

# Crea il parser
parser = Lark(grammar, parser='earley', lexer='basic', start='start')

# Inizializzazione l'app Flask
app = Flask(__name__)

# Abilita il supporto CORS per l'app Flask
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Inizializzazione del server SocketIO con l'app Flask
socketio = SocketIO(app=app, cors_allowed_origins="http://localhost:3000")

# Inizializzazione il trasformatore e l'interprete per il codice C#
csharp_transformer = CSharpTransformer()
csharp_interpreter = CsharpInterpreter(csharp_transformer)


def parse(csharp_code):
    """
    Analizza il codice C# e gestisce gli errori di sintassi. Utilizza un parser per generare l'albero sintattico e
    rileva errori di sintassi comuni, sollevando eccezioni specifiche basate sul tipo di errore riscontrato.

    :param csharp_code: Una stringa che rappresenta il codice C# da analizzare.
    :raises MissingEqual: Se manca un simbolo di uguaglianza ('=') dove è previsto.
    :raises MissingSemicolon: Se manca un punto e virgola (';') dove è previsto.
    :raises MissingClosingBracketError: Se manca una parentesi tonda chiusa (')').
    :raises MissingOpeningBracketError: Se manca una parentesi tonda aperta ('(').
    :raises MissingClosingSquareBracketError: Se manca una parentesi quadra chiusa (']').
    :raises MissingOpeningSquareBracketError: Se manca una parentesi quadra aperta ('[').
    :raises MissingClosingClawBracketError: Se manca una parentesi graffa  chiusa ('}').
    :raises MissingOpeningClawBracketError: Se manca una parentesi graffa aperta ('{').
    :raises CsharpLexicalError: Se non si verifica nessuna delle condizioni precedenti, viene lanciata un eccezione di questo tipo.
    :return: L'albero sintattico generato dal parser se il codice è valido.
    """
    try:
        tree = parser.parse(csharp_code)
        return tree
    except UnexpectedEOF as u:
        # Controllo specifico per le parentesi graffe in caso di fine inattesa
        open_braces = csharp_code.count('{')
        close_braces = csharp_code.count('}')

        # Se ci sono più graffe aperte rispetto a quelle chiuse, manca una graffa chiusa
        if open_braces > close_braces:
            raise MissingClosingClawBracketError(csharp_code.splitlines()[-1], len(csharp_code.splitlines()),
                                                 len(csharp_code.splitlines()[-1]))
    except UnexpectedToken as u:
        error_line = csharp_code.splitlines()[u.line - 1]
        if error_line.strip() == '{':
            error_line = csharp_code.splitlines()[u.line - 2]
            u.line = u.line - 1
            u.column = len(error_line) + 2

        for rule in u.considered_rules:
            expect = rule.expect
            if expect.name == 'RPAR' and csharp_code.count('(') != csharp_code.count(')'):
                raise MissingClosingBracketError(error_line, u.line, u.column)
            elif expect.name == 'LPAR' and csharp_code.count('(') != csharp_code.count(')'):
                raise MissingOpeningBracketError(error_line, u.line, u.column)
            elif expect.name == 'SEMICOLON':
                raise MissingSemicolon(error_line, u.line, u.column)
            elif expect.name == 'EQUAL' and "=" not in error_line:
                raise MissingEqual(error_line, u.line, u.column)
            elif expect.name == 'RSQB' and csharp_code.count('[') != csharp_code.count(']'):
                raise MissingClosingSquareBracketError(error_line, u.line, u.column)
            elif expect.name == 'LSQB' and csharp_code.count('[') != csharp_code.count(']'):
                raise MissingOpeningSquareBracketError(error_line, u.line, u.column)
            elif expect.name == 'RBRACE' and csharp_code.count('{') != csharp_code.count('}'):
                raise MissingClosingClawBracketError(error_line, u.line, u.column)
            elif expect.name == 'LBRACE' and csharp_code.count('{') != csharp_code.count('}'):
                raise MissingOpeningClawBracketError(error_line, u.line, u.column)

        raise CsharpLexicalError(error_line, u.line, u.column)


@socketio.on('run_code')
def run(data):
    """
    Gestisce l'esecuzione del codice C# inviato dal client tramite un evento Socket.IO.
    Pulisce la tabella dei simboli, analizza il codice, esegue l'interprete, e invia indietro risultati o errori.

    :param data: Un dizionario contenente il codice C# da eseguire e informazioni sulla console.
    """

    csharp_transformer.symbol_table.symbols.clear()
    emit('clear')
    code = data.get('code')
    consoleType = data.get('consoleType')
    initial_code = """using System;    
  
class Program
{
    static void Main()
    {
        //Scrivi qui il tuo codice
    }
}
"""
    if code == initial_code or code == "":
        emit('error', {'error': 'No code provided'})
        return

    if not consoleType and "Console.ReadLine()" in code:
        emit('error', {'error': 'Console set to static. Unable to satisfy input request.'})
        return

    try:
        emit('output', {'output': 'start'})

        parse_tree = parse(code)
        csharp_interpreter.visit(parse_tree)
        pydot__tree_to_png(parse_tree, 'parse_tree_program.png')
        with open('parse_tree_program.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        emit('image', {'image': encoded_image})
    except MissingEqual as me:
        emit('error', {'error': f"{str(me)}"})
    except MissingSemicolon as ms:
        emit('error', {'error': f"{str(ms)}"})
    except MissingOpeningBracketError as e:
        emit('error', {'error': f"{str(e)}"})
    except MissingClosingBracketError as e:
        emit('error', {'error': f"{str(e)}"})
    except MissingOpeningSquareBracketError as e:
        emit('error', {'error': f"{str(e)}"})
    except MissingClosingSquareBracketError as e:
        emit('error', {'error': f"{str(e)}"})
    except MissingClosingClawBracketError as e:
        emit('error', {'error': f"{str(e)}"})
    except MissingOpeningClawBracketError as e:
        emit('error', {'error': f"{str(e)}"})
    except Exception as e:
        emit('error', {'error': f"{str(e)}"})

    finally:
        csharp_transformer.symbol_table.symbols.clear()


@socketio.on('input')
def handle_input(data):
    """
    Gestisce l'input fornito dal client e lo imposta nel transformer C#.

    :param data: Un dizionario contenente il valore dell'input.
    """
    input_value = data.get('input')
    csharp_transformer.set_input_value(input_value)


if __name__ == '__main__':
    socketio.run(app, debug=False, port=5000, allow_unsafe_werkzeug=True)
