import { writable } from 'svelte/store';

export interface AppState {
  isLoading: boolean;
  response: string | null;
  error: string | null;
  lastQuery: string | null;
  csvProcessing: boolean;
  htmlProcessing: boolean;
  neo4jConnected: boolean;
}

const initialState: AppState = {
  isLoading: false,
  response: null,
  error: null,
  lastQuery: null,
  csvProcessing: false,
  htmlProcessing: false,
  neo4jConnected: false,
};

export const appState = writable<AppState>(initialState);
