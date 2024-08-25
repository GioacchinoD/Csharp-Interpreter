'use client';

import React, {useEffect} from 'react';
import Editor, {useMonaco} from '@monaco-editor/react'

import {Avatar, AvatarFallback, AvatarImage} from '@/components/ui/avatar';
import {Button} from "@/components/ui/button";

import {newSocket} from '@/actions/socket';
import Console from '@/components/Console/Console';
import Menu from '@/components/Menu/Menu';

/**
 * Definizione dell'interfaccia utilizzata dalla variabile di stato output
 */
export type IOutput = {
    chiave: 'message' | 'value',
    valore: any
}

export default function Playground() {
    const [code, setCode] = React.useState<string>(`using System;    
  
class Program
{
    static void Main()
    {
        //Scrivi qui il tuo codice
    }
}
`);

    const [consoleType, setConsoleType] = React.useState<boolean>(false);
    const [output, setOutput] = React.useState<IOutput[]>([]);
    const [error, setError] = React.useState<string>('');
    const [imageSrc, setImageSrc] = React.useState<string>('');


    const monaco = useMonaco();

    useEffect(() => {
        if (monaco) {
            import('monaco-themes/themes/Twilight.json').then((theme: any) => {
                monaco.editor.defineTheme('twilight', theme);
                monaco.editor.setTheme('twilight');
            })
        }
    }, [monaco]);

    const handleSocketRunCode = () => {

        // Svuota l'output prima di eseguire il codice
        setOutput([]);
        setError('');
        setImageSrc('')


        // Rimuove eventuali listener duplicati prima di aggiungerne di nuovi
        newSocket.off("output");
        newSocket.off("error");
        newSocket.off("image");
        newSocket.off("clear");


        newSocket.emit("run_code", {code: code, consoleType: consoleType});

        newSocket.on("error", (data) => {
            setError(data.error);
        });

        newSocket.on("output", (data) => {
            setOutput(prevOutput => [...prevOutput, {chiave: "message", valore: data.output}]);

        });

        newSocket.on("image", (data) =>{
            setImageSrc('data:image/png;base64,' + data.image);
        });

        newSocket.on("clear", () => {
            setOutput([]);
            setError('');
            setImageSrc('');
        });
    };

    return (
        <div className={'min-h-screen max-h-screen h-screen flex flex-col'}>

            <header className={'p-2 border-b-2 flex items-center gap-2'}>

                <Avatar className={'h-8 w-8'}>
                    <AvatarImage src={'./Csharp.svg'} alt={'Csharp'} width={16} height={16}/>
                    <AvatarFallback>C#</AvatarFallback>
                </Avatar>

                <h1 className={'text-xl'}>Interpreter</h1>

            </header>

            <main className={'h-full p-2'}>

                <section className={'flex-1 flex flex-col gap-4 h-full'}>

                    <div className={"flex items-center justify-between gap-4"}>

                        <Menu
                            onClickVoiceItem={(content) => setCode(content)}
                            onUploadFile={(content) => setCode(content)}
                            getCode={() => code}
                        />

                        <div className={'flex items-center justify-end gap-4'}>

                            <section className={'text-right'}>

                                <Button
                                    size={'sm'}
                                    variant={'default'}
                                    onClick={() => handleSocketRunCode()}>
                                    Esegui
                                </Button>

                            </section>

                        </div>

                    </div>

                    <div className={'overflow-y-auto border border-gray-300 rounded'} style={{height: "100%"}}>
                        <Editor
                            options={{
                                minimap: {enabled: false},
                                fontSize: 16,
                                contextmenu: false,
                                cursorWidth: 6,
                                quickSuggestions: false,

                            }}
                            width="100%"
                            defaultLanguage={'csharp'}
                            value={code}
                            onChange={(value) => {
                                if (value != undefined) {
                                    setCode(value)
                                }
                            }}
                            theme={'twilight'}
                        />

                    </div>

                    <Console
                        consoleType={consoleType}
                        setConsoleType={setConsoleType}
                        output={output}
                        setOutput={setOutput}
                        error={error}
                        setError={setError}
                        img={imageSrc}
                    />

                </section>
            </main>
        </div>
    )

}