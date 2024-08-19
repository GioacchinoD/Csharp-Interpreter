import base64
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from lark import Lark
from interpreter import CsharpInterpreter
from transformer import CSharpTransformer
from error_handler import *

# Carica la grammatica dal file 'csharp_grammar.lark'
with open('csharp_grammar.lark', 'r') as file:
    grammar = file.read()

# Creazione il parser utilizzando la grammatica caricata
parser = Lark(grammar, parser='lalr', start='start')

# Inizializzazione l'app Flask
app = Flask(__name__)

# Abilita il supporto CORS per l'app Flask
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Inizializzazione del server SocketIO con l'app Flask
socketio = SocketIO(app=app, cors_allowed_origins="http://localhost:3000")

# Inizializzazione il trasformatore e l'interprete per il codice C#
csharp_transformer = CSharpTransformer()
csharp_interpreter = CsharpInterpreter(csharp_transformer)

@socketio.on('run_code')
def run(data):
    emit('clear')
    print(f"Received data: {data}")
    code = data.get('code')
    consoleType = data.get('consoleType')
    initial_code = 'using System;    \n  \nclass Program\n{\n    static void Main()\n    {\n        //Scrivi qui il tuo codice\n    }\n}\n'

    if code == initial_code:
        emit('error', {'error': 'No code provided'})
        return

    # Controlla se è richiesto un input ma il consoleType è impostato su Statico, e nel caso invia un evento per dichiarare un errore.
    if not consoleType and "Console.ReadLine()" in code:
        emit('error', {'error': 'Console set to static. Unable to satisfy input request.'})
        return

    try:
        emit('output', {'output': 'start'})

        parse_tree = parser.parse(code) # Tenta di fare il parsing del codice C#
        csharp_interpreter.visit(parse_tree) # Visita l'albero di parsing con l'interprete C#

    except Exception as e:
        # Gestione di errori generici durante l'esecuzione
        emit('error', {'error': f"Errore di esecuzione: {str(e)}"})
        print(f"Errore di esecuzione: {e}")

    finally:
        # Pulisce la tabella dei simboli
        csharp_transformer.symbol_table.symbols.clear()


@socketio.on('input')
def handle_input(data):
    print(f"Received input: {data}")
    input_value = data.get('input')
    csharp_transformer.set_input_value(input_value)


if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)
