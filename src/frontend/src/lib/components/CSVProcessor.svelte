<script lang="ts">
  import { appState } from '../stores/appState';
  import { processCSV } from '../api/client';
  
  import { Button } from './ui/button';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

  async function handleCSV() {
    appState.update(s => ({ ...s, csvProcessing: true, error: null, response: null }));
    
    try {
      const result = await processCSV();
      
      if (result.status === 'success') {
        appState.update(s => ({
          ...s,
          response: result.data?.message || 'CSV processing started',
          csvProcessing: false
        }));
      } else {
        throw new Error(result.message || 'CSV processing failed');
      }
    } catch (e) {
      appState.update(s => ({
        ...s,
        error: `Error: ${e instanceof Error ? e.message : 'Unknown error'}`,
        csvProcessing: false
      }));
    }
  }
</script>

<Card>
  <CardHeader>
    <div class="flex items-start gap-3">
      <div class="p-2 bg-primary/10 rounded-md">
        <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <div>
        <CardTitle>CSV Data Processing</CardTitle>
        <CardDescription>Extract knowledge from CSV files</CardDescription>
      </div>
    </div>
  </CardHeader>
  
  <CardContent class="space-y-4">
    <p class="text-sm text-muted-foreground">
      Analyze and extract entities and relationships from CSV files to populate the knowledge graph.
    </p>
    
    <Button 
      on:click={handleCSV}
      disabled={$appState.csvProcessing}
      variant="secondary"
      class="w-full text-foreground"
    >
      {#if $appState.csvProcessing}
        <span class="flex items-center gap-2">
          <span class="inline-block w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></span>
          Processing...
        </span>
      {:else}
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Process CSV Files
      {/if}
    </Button>
  </CardContent>
</Card>
