'use client';
import { createContext, useContext, ReactNode } from 'react';
import { connectionService } from '../services/ws_connection.service';

const WSConnectionContext = createContext(connectionService);

export function WSProvider({ children }: { children: ReactNode }) {
  return (
    <WSConnectionContext.Provider value={connectionService}>
      {children}
    </WSConnectionContext.Provider>
  );
}

export function useWSConnection() {
  return useContext(WSConnectionContext);
}