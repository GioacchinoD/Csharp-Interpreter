import React, {useEffect, useRef} from "react";
import {TerminalIcon, FileImageIcon} from "lucide-react";
import {Switch} from "@/components/ui/switch";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription} from "@/components/ui/dialog";

import {newSocket} from "@/actions/socket";
import {IOutput} from "@/components/Playground/Playground";


/**
 * Definizione delle proprietà utilizzate dal componente Console ricevute dal componente Playground
 */

type IConsole = {
    consoleType: boolean;
    setConsoleType: (value: boolean) => void;

    output: IOutput[];
    setOutput: (value: (prevOutput: any[]) => any[]) => void;

    error: string;
    setError: (value: string | ((prevError: string) => string)) => void;

    img: string;
};
/**
 *
 * @param consoleType Variabile che indica la tipologia di console utilizzata Statica/Dinamica
 * @param setConsoleType
 * @param output Variabile utilizzata per memorizzare l'output ricevuto dal back-end Python.
 * @param setOutput
 * @param error Variabile utilizzata per contenere un eventuale errore ricevuto dal back-ed Python.
 * @param setError
 * @param img contiene il base64 dell'immagine generata dal parser di Python
 */

export default function Console({
    consoleType,
    setConsoleType,
    output,
    setOutput,
    error,
    setError,
    img}: IConsole){

    const [inputRequired, setInputRequired] = React.useState<boolean>(false);
    const [userInput, setUserInput] = React.useState<string>('')

    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        //Scorre fino in fondo automaticamente ogni volta che output o error cambiano.
        if (containerRef.current){
            containerRef.current.scrollTo({
                top: containerRef.current.scrollHeight,
                left: 0,
                behavior: 'instant'
            });
        }
    }, [output, error]);

    newSocket.on('input_required', (data) => {
        setInputRequired(true);
    })

    /**
     * Funzione per inviare il valore del campo input al back-end Python
     * attraverso l'utilizzo del tasto Enter o del click del Button.
     */
    const handleInputSubmit = () => {
        setOutput(prevOutput => [...prevOutput, {chiave: 'value', valore: userInput}]);
        newSocket.emit('input', {input: userInput})
        setUserInput('');
        setInputRequired(false);
    };

    return(
        <div className={'flex flex-col gap-0'}>

            <div className={'flex justify-between items-center bg-gray-800 p-2 rounded-t border border-gray-800 border-b-0 gap-2'}>

                <h4 className={'text-lg font-bold text-white'}>Console</h4>

                {img !== "" ? (
                    <Dialog modal={true}>
                        <DialogTrigger asChild>
                            <Button variant="ghost" className={"text-lg font-bold"}>
                                <FileImageIcon className="mr-2 h-6 w-6"/>
                                Visualizza Parse Tree
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="w-full h-full max-w-none p-4 m-0 overflow-auto">
                            <DialogHeader>
                                <DialogTitle>Parse Tree</DialogTitle>
                                <DialogDescription className="flex justify-center items-center min-h-full">
                                    <img
                                        src={img}
                                        className="max-w-full max-h-full object-contain"
                                        alt={"Parse Tree"}
                                    />
                                </DialogDescription>
                            </DialogHeader>
                        </DialogContent>
                    </Dialog>
                ) : undefined}


                <div className={'flex items-center gap-2'}>

                    <span className={'text-lg font-bold text-white'}>

                        {consoleType ? 'Dinamico' : 'Statico'}

                    </span>

                    <Switch
                        id={'consoleSwitch'}
                        checked={consoleType}
                        onCheckedChange={(checked) => setConsoleType(checked)}
                    />

                </div>

            </div>

            <div className={'border-t-0 border border-zinc-600 rounded-b bg-background p-4 h-44 overflow-y-auto'} ref={containerRef}>

                <div className={'flex items-start gap-2'}>

                    <div className={'columns-1'}>

                        <TerminalIcon className={'w-6 h-6 text-amber-50'}/>

                    </div>

                    <div className={'columns-auto flex-col'}>

                        <span>
                            {output.map((element, index) => {
                                return(
                                    <pre key={index}
                                    className={`whitespace-pre-wrap ${element.chiave === "message" ? "text-white" : "text-green-800"} text-xl mb-2`}>

                                        {element.valore}

                                    </pre>
                                );
                            })}

                            {error !== '' ?
                            <pre className={'whitespace-pre-wrap text-destructive text-xl'}>{error}</pre> : undefined}

                        </span>

                    </div>

                </div>

                {inputRequired && error === '' ?
                    <div className={'flex w-full max-w-sm items-center space-x-2 ml-7'}>

                        <Input
                            type={'text'}
                            autoFocus={inputRequired && error === ''}
                            className={'text-xl'}
                            placeholder={'Inserisci input...'}
                            onKeyDown={(event) => {
                                if(event.key === 'Enter') {
                                    event.preventDefault();
                                    handleInputSubmit();
                                }
                            }}
                            value={userInput}
                            onChange={(e) => setUserInput(e.target.value)}/>

                        <Button onClick={handleInputSubmit} type={'button'}>Submit</Button>

                    </div> : undefined}

            </div>

        </div>
    );
}