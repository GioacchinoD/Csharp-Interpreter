'use client';

import React, {useEffect} from 'react';
import Editor, {useMonaco} from '@monaco-editor/react'

import {Avatar, AvatarFallback, AvatarImage} from '@/components/ui/avatar';
import {Button} from "@/components/ui/button";

import {newSocket} from '@/actions/socket';
import Console from '@/components/Console/Console';


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


    const monaco = useMonaco();

    useEffect(() => {
        if (monaco){
            import('monaco-themes/themes/Twilight.json').then((theme:any) => {
                monaco.editor.defineTheme('twilight', theme);
                monaco.editor.setTheme('twilight');
            })
        }
    }, [monaco]);

    const handleSocketRunCode = () => {

        newSocket.emit('run_code', {code: code});
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

                    <div className={'overflow-y-auto border border-gray-300 rounded'} style={{height: "100%"}}>
                        <Editor
                            options={{
                                minimap:{enabled:false},
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
                    />

                </section>
            </main>
        </div>
    )

}