<script lang="ts">
  import { Button } from './ui/button';
  import { Alert, AlertDescription, AlertTitle } from './ui/alert';

  export let type: 'success' | 'error';
  export let content: string;

  function copyToClipboard() {
    navigator.clipboard.writeText(content);
  }
</script>

<Alert variant={type === 'success' ? 'default' : 'destructive'} class="border-l-4">
  <div class="flex items-start gap-4">
    <div class="flex-1">
      {#if type === 'success'}
        <AlertTitle class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Query Successful
        </AlertTitle>
      {:else}
        <AlertTitle class="flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
              d="M12 8v4m0 4v.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Error Processing Query
        </AlertTitle>
      {/if}
      
      <AlertDescription class="mt-4 font-mono text-sm max-h-96 overflow-y-auto whitespace-pre-wrap">
        {content}
      </AlertDescription>
    </div>
  </div>

  <Button 
    variant="ghost" 
    size="sm" 
    on:click={copyToClipboard}
    class="mt-4 text-xs"
  >
    Copy
  </Button>
</Alert>
