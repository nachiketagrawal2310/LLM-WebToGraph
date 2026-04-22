<script lang="ts">
  import { appState } from '../stores/appState';
  import { queryGraph } from '../api/client';
  
  // shadcn imports
  import { Button } from './ui/button';
  import { Textarea } from './ui/textarea';

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
    if (event.key === 'Enter' && event.ctrlKey) {
      handleSubmit();
    }
  }
</script>

<div class="space-y-6">
  <div>
    <label for="question" class="block text-sm font-semibold mb-2">
      Natural Language Query
    </label>
  </div>

  <div class="space-y-3">
    <Textarea
      id="question"
      bind:value={question}
      on:keydown={handleKeydown}
      placeholder="E.g.: What are the relationships between X and Y? or Summarize the main topics in the dataset."
      disabled={$appState.isLoading}
      class="min-h-24 font-mono text-sm"
    />
    
    <div class="flex gap-3">
      <Button
        on:click={handleSubmit}
        disabled={$appState.isLoading || !question.trim()}
        class="px-6"
      >
        {#if $appState.isLoading}
          <span class="flex items-center gap-2">
            <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Processing...
          </span>
        {:else}
          Submit Query
        {/if}
      </Button>
      
      {#if question.trim()}
        <Button
          variant="outline"
          on:click={() => question = ''}
          disabled={$appState.isLoading}
        >
          Clear
        </Button>
      {/if}
    </div>
  </div>

  {#if $appState.lastQuery}
    <div class="bg-muted border border-border rounded-md p-3">
      <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
        Previous Query
      </p>
      <p class="text-sm text-foreground mt-2">{$appState.lastQuery}</p>
    </div>
  {/if}
</div>
