<script lang="ts">
  import { appState } from '../stores/appState';
  import { processHTML } from '../api/client';
  
  import { Button } from './ui/button';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

  async function handleHTML() {
    appState.update(s => ({ ...s, htmlProcessing: true, error: null, response: null }));
    
    try {
      const result = await processHTML();
      
      if (result.status === 'success') {
        appState.update(s => ({
          ...s,
          response: result.data?.message || 'HTML processing started',
          htmlProcessing: false
        }));
      } else {
        throw new Error(result.message || 'HTML processing failed');
      }
    } catch (e) {
      appState.update(s => ({
        ...s,
        error: `Error: ${e instanceof Error ? e.message : 'Unknown error'}`,
        htmlProcessing: false
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
            d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
        </svg>
      </div>
      <div>
        <CardTitle>HTML Web Processing</CardTitle>
        <CardDescription>Extract knowledge from web pages</CardDescription>
      </div>
    </div>
  </CardHeader>
  
  <CardContent class="space-y-4">
    <p class="text-sm text-muted-foreground">
      Parse web content to extract structured entities and integrate them into the knowledge graph.
    </p>
    
    <Button 
      on:click={handleHTML}
      disabled={$appState.htmlProcessing}
      variant="secondary"
      class="w-full text-foreground"
    >
      {#if $appState.htmlProcessing}
        <span class="flex items-center gap-2">
          <span class="inline-block w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></span>
          Processing...
        </span>
      {:else}
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Process HTML
      {/if}
    </Button>
  </CardContent>
</Card>
