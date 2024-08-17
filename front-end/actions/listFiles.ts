'use server';

/**
 * 'use server' consente di utilizzare codice javascript/typescript per definire funzioni
 * lato server. In questo caso, vengono utilizzate le librerie fs e path per la lettura del filesystem e la lettura
 * dei file contenuti all'interno di una specifica cartella.
 * */

import fs from 'fs'
import path from 'path'

export const getExampleFolderCode = async (pathExample: string) => {
    const postsDirectory = path.join(process.cwd(), pathExample);

    const fileNames = fs.readdirSync(postsDirectory);

    return fileNames.map(fileName => {

        // Read markdown file as string
        const fullPath = path.join(postsDirectory, fileName)
        const fileContents = fs.readFileSync(fullPath, 'utf8')

        return {
            nome: fileName,
            content: fileContents,
        }
    });

}