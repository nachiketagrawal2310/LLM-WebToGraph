<script lang="ts">
  import { appState } from '../stores/appState';
  import { processCSV } from '../api/client';

  async function handleCSV() {
    appState.update(s => ({ ...s, csvProcessing: true, error: null, response: null }));
    
    try {
      const result = await processCSV();
      if (result.status === 'success') {
        appState.update(s => ({ ...s, response: result.data?.message || 'CSV processing complete', csvProcessing: false }));
      } else {
        throw new Error(result.message || 'Processing failed');
      }
    } catch (e) {
      appState.update(s => ({ ...s, error: `CSV Error: ${e instanceof Error ? e.message : 'Unknown error'}`, csvProcessing: false }));
    }
  }
</script>

<div class="p-6 bg-card border border-border rounded-xl flex flex-col justify-between space-y-4 shadow-sm">
  <div class="flex flex-col space-y-2">
    <div class="flex items-center gap-3">
      <div class="p-2 bg-secondary rounded-lg text-secondary-foreground shadow-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 1.1.9 2 2 2h12a2 2 0 002-2V7a2 2 0 00-2-2H6a2 2 0 00-2 2zM9 5v14M15 5v14M4 11h16M4 15h16" /></svg>
      </div>
      <div class="font-semibold text-sm">CSV Tabular Ingestion</div>
    </div>
    <p class="text-[12px] text-muted-foreground leading-relaxed">
      Analyzes local CSV files to identify nodes and edges. It maps tabular columns to graph properties and persists them into Neo4j.
    </p>
  </div>
  <button
    on:click={handleCSV}
    disabled={$appState.csvProcessing}
    class="w-full py-2.5 bg-secondary text-secondary-foreground text-xs font-bold rounded-md shadow-md hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center justify-center gap-2 border border-secondary/20"
  >
    {#if $appState.csvProcessing}
      <div class="w-3 h-3 border-2 border-secondary-foreground/30 border-t-secondary-foreground rounded-full animate-spin"></div>
      Ingesting
    {:else}
      Ingest CSV Data
    {/if}
  </button>
</div>
