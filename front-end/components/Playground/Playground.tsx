'use client';

import React, {useEffect} from 'react';
import Editor, {useMonaco} from '@monaco-editor/react'

import {Avatar, AvatarFallback, AvatarImage} from '@/components/ui/avatar';
import {Button} from "@/components/ui/button";

import {newSocket} from '@/actions/socket';

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

            <header className={'p-4 border-b-2 flex items-center gap-2'}>

                <Avatar className={'flex items-center gap-2'}>
                    <AvatarImage src={'./Csharp.svg'} alt={'Csharp'} width={20} height={20}/>
                    <AvatarFallback>C#</AvatarFallback>
                </Avatar>

                <h1 className={'text-xl'}>Interpreter</h1>

            </header>

            <main className={'h-full p-4'}>

                <section className={'flex-1 p-4 flex flex-col gap-4 h-full'}>

                    <div className={'flex items-center justify-end gap-4'}>

                        <section className={'text-right'}>

                            <Button
                                variant={"default"}
                                onClick={() => handleSocketRunCode()}>
                                Esegui
                            </Button>

                        </section>

                    </div>

                    <div className={'h-[48rem] overflow-y-auto border border-gray-300 rounded'}>

                        <Editor
                            options={{
                                minimap:{enabled:false},
                                fontSize: 20,
                                contextmenu: false,
                                cursorWidth: 6,
                                quickSuggestions: false
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

                </section>
            </main>
        </div>
    )

}