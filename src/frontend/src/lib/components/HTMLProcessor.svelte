<script lang="ts">
  import { appState } from '../stores/appState';
  import { processHTML } from '../api/client';

  async function handleHTML() {
    appState.update(s => ({ ...s, htmlProcessing: true, error: null, response: null }));
    
    try {
      const result = await processHTML();
      if (result.status === 'success') {
        appState.update(s => ({ ...s, response: result.data?.message || 'HTML processing complete', htmlProcessing: false }));
      } else {
        throw new Error(result.message || 'Processing failed');
      }
    } catch (e) {
      appState.update(s => ({ ...s, error: `HTML Error: ${e instanceof Error ? e.message : 'Unknown error'}`, htmlProcessing: false }));
    }
  }
</script>

<div class="p-6 bg-card border border-border rounded-xl flex flex-col justify-between space-y-4 shadow-sm">
  <div class="flex flex-col space-y-2">
    <div class="flex items-center gap-3">
      <div class="p-2 bg-secondary rounded-lg text-secondary-foreground shadow-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" /></svg>
      </div>
      <div class="font-semibold text-sm">HTML Semantic Extraction</div>
    </div>
    <p class="text-[12px] text-muted-foreground leading-relaxed">
      Scrapes and parses web content to extract unstructured relationships. It uses NLP to identify entities and links them to the existing graph.
    </p>
  </div>
  <button
    on:click={handleHTML}
    disabled={$appState.htmlProcessing}
    class="w-full py-2.5 bg-secondary text-secondary-foreground text-xs font-bold rounded-md shadow-md hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 transition-all flex items-center justify-center gap-2 border border-secondary/20"
  >
    {#if $appState.htmlProcessing}
      <div class="w-3 h-3 border-2 border-secondary-foreground/30 border-t-secondary-foreground rounded-full animate-spin"></div>
      Extracting
    {:else}
      Extract HTML Knowledge
    {/if}
  </button>
</div>
