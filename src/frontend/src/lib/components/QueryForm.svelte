<script lang="ts">
  import { appState } from '../stores/appState';
  import { queryGraph } from '../api/client';

  let question = '';

  async function handleSubmit() {
    if (!question.trim()) return;

    appState.update(s => ({ ...s, isLoading: true, error: null, response: null }));
    
    try {
      const result = await queryGraph(question);
      
      if (result.status === 'success') {
        appState.update(s => ({
          ...s,
          response: result.data?.answer || 'No response',
          lastQuery: question,
          isLoading: false
        }));
      } else {
        throw new Error(result.message || 'Query failed');
      }
    } catch (e) {
      appState.update(s => ({
        ...s,
        error: `Error: ${e instanceof Error ? e.message : 'Unknown error'}`,
        isLoading: false
      }));
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  }
</script>

<div class="space-y-4">
  <div class="flex flex-col gap-4">
    <textarea
      id="question"
      bind:value={question}
      on:keydown={handleKeydown}
      placeholder="Type your question..."
      class="w-full px-4 py-3 bg-background text-foreground border-2 border-border rounded-lg focus:ring-1 focus:ring-ring focus:border-ring font-sans text-sm leading-relaxed resize-none min-h-[120px] transition-all placeholder:text-muted-foreground outline-none shadow-inner"
      disabled={$appState.isLoading}
    />
    
    <div class="flex items-center justify-between">
      <div class="text-[11px] text-muted-foreground font-medium uppercase tracking-wider">
        {#if $appState.lastQuery}
          Last: {$appState.lastQuery.slice(0, 30)}{$appState.lastQuery.length > 30 ? '...' : ''}
        {/if}
      </div>
      
      <div class="flex gap-3">
        {#if question.trim()}
          <button
            on:click={() => question = ''}
            disabled={$appState.isLoading}
            class="px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground transition-colors"
          >
            Clear
          </button>
        {/if}
        <button
          on:click={handleSubmit}
          disabled={$appState.isLoading || !question.trim()}
          class="px-6 py-2.5 bg-primary text-primary-foreground text-xs font-bold rounded-md shadow-md hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:shadow-none disabled:translate-y-0 transition-all flex items-center gap-2 border border-primary/20"
        >
          {#if $appState.isLoading}
            <div class="w-3 h-3 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin"></div>
            Running
          {:else}
            Execute
          {/if}
        </button>
      </div>
    </div>
  </div>
</div>
