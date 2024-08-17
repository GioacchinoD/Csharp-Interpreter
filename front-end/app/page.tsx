'use client';

import React, {useEffect} from 'react';
import Playground from "@/components/Playground/Playground";
import {newSocket} from "@/actions/socket";

export default function Home(){
  useEffect(() => {
    newSocket.connect()
  }, []);

  return(
      <main className={"min-h-screen"}>
        <Playground />
      </main>
  );
}