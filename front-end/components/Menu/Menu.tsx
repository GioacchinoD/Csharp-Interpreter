import {
    Menubar,
    MenubarContent,
    MenubarItem,
    MenubarMenu, MenubarSeparator, MenubarSub, MenubarSubContent, MenubarSubTrigger,
    MenubarTrigger
} from '@/components/ui/menubar';

import React, {useEffect, useRef} from 'react';
import {SaveIcon, UploadIcon} from 'lucide-react';

import {getExampleFolderCode} from '@/actions/listFiles';

type IMenu = {
    onClickVoiceItem: (content: string) => void;
    onUploadFile: (content: string) => void;
    getCode: () => string;
}

export default function Menu({
                                 onClickVoiceItem,
                                 onUploadFile,
                                 getCode
                             }: IMenu) {

    const [menuItemExample, setMenuItemExample] = React.useState<any[]>([]);
    const [menuItemErrorExample, setMenuItemErrorExample] = React.useState<any[]>([]);
    /**
     * reference del campo input nascosto utilizzato da CARICA FILE per poter leggere il contenuto
     * di un file .cs dal filesystem e inserirlo all'interno dell'editor.
     */
    const ref = useRef<HTMLInputElement>(null);

    useEffect(() => {
        /**
         * Funzione asincrona che richiama l'azione server definita nel file listFiles.ts,
         * l'interno del blocco try consente di reperire tutti i file presenti all'interno del
         * path `./esempi`.
         * nel blocco catch viene stampato un errore all'interno della console del browser
         */
        (async () => {
            try{
                const result = await getExampleFolderCode(`./esempi/Esempi`);
                const result1 = await getExampleFolderCode(`./esempi/Esempi errori`);
                setMenuItemExample(result);
                setMenuItemErrorExample(result1);
            } catch (error) {
                console.error("error get file c#: ", error);
            }
        })();

    }, []);

    /**
     * Funzione che consente il salvataggio del contenuto dell'editor come file .cs all'interno del filesystem
     */

    const handleSaveFile = () => {
        const code = getCode();
        let extension = '.cs';

        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `code${extension}`;
        a.click();
        URL.revokeObjectURL(url);
    };

    return(
        <Menubar>
            <MenubarMenu>
                <MenubarTrigger className={'cursor-pointer'}>File</MenubarTrigger>
                <MenubarContent>
                    <MenubarItem className={'cursor-pointer'} onClick={() => {
                        /**
                         * sul click della voce di menù CARICA FILE viene richiamata
                         * la reference del campo input e attivato il click del campo
                         */
                        if (ref && ref.current) {
                            ref.current.click();
                        }
                    }}>
                        <div className={'flex items-center gap-2'}>
                            <UploadIcon className={'w-4 h-4'}/>
                            <span>Upload file</span>
                        </div>

                    </MenubarItem>
                    <MenubarItem className={'cursor-pointer'} onClick={handleSaveFile}>
                        <div className={'flex items-center gap-2'}>
                            <SaveIcon className={'w-4 h-4'}/>
                            <span>Save file</span>
                        </div>
                    </MenubarItem>
                </MenubarContent>
            </MenubarMenu>

            <MenubarMenu>
                <MenubarTrigger className={'cursor-pointer'}>Example</MenubarTrigger>
                <MenubarContent>

                <MenubarSub>
                    <MenubarSubTrigger>Code example</MenubarSubTrigger>
                    <MenubarSubContent>
                        {menuItemExample.map((element, index) => {
                            return <MenubarItem
                                key={index}
                                className={"cursor-pointer"}
                                onClick={() => onClickVoiceItem(element.content)}
                            >
                                {element.nome}
                            </MenubarItem>
                        })}
                    </MenubarSubContent>
                </MenubarSub>
                <MenubarSeparator/>

                    <MenubarSub>
                        <MenubarSubTrigger>Error example</MenubarSubTrigger>
                        <MenubarSubContent>
                            {menuItemErrorExample.map((element, index) => {
                                return <MenubarItem
                                    key={index}
                                    className={"cursor-pointer"}
                                    onClick={() => onClickVoiceItem(element.content)}
                                >
                                    {element.nome}
                                </MenubarItem>
                            })}
                        </MenubarSubContent>
                    </MenubarSub>

                </MenubarContent>
            </MenubarMenu>

            <input ref={ref} className={'hidden'} accept={'.cs'} type='file' onChange={(e) => {

                /**
                 * Funzione che permette la lettura del file caricato,
                 * la funzione onUploadFile serve a settare il contenuto del file letto
                 * all'interno della varibiale di stato CODE
                 */
                const fileReader = new FileReader();
                const files = e.currentTarget.files;

                if (files !== null) {
                    fileReader.readAsText(files[0], 'UTF-8');
                    fileReader.onload = ev => {
                        const content = ev.target?.result;
                        if(content !== null && content !== undefined) {
                            onUploadFile(content.toString());
                        }
                    };
                }

            }}/>
        </Menubar>

    );
}