import {io} from "socket.io-client";

/**
 * Definizione e inizializzazione della connessione socket.io
 * */

export const newSocket = io("http://localhost:5000");

