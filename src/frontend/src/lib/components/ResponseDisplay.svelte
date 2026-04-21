<script lang="ts">
  export let type: 'success' | 'error';
  export let content: string;
</script>

<div class="rounded-xl border animate-in fade-in slide-in-from-bottom-2 duration-300 overflow-hidden
  {type === 'success' 
    ? 'bg-card border-border' 
    : 'bg-destructive/10 border-destructive/20'
  }">
  
  <div class="px-6 py-4 border-b border-border flex items-center justify-between">
    <div class="flex items-center gap-2">
      <div class="w-2 h-2 rounded-full {type === 'success' ? 'bg-emerald-500' : 'bg-destructive'}"></div>
      <h4 class="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
        {type === 'success' ? 'Output' : 'Error'}
      </h4>
    </div>
    <button
      on:click={() => navigator.clipboard.writeText(content)}
      class="text-[10px] font-semibold text-muted-foreground hover:text-foreground transition-colors uppercase tracking-wider"
    >
      Copy
    </button>
  </div>

  <div class="px-6 py-6">
    <div class="text-sm leading-relaxed font-mono {type === 'success' ? 'text-foreground' : 'text-destructive'} whitespace-pre-wrap max-h-[400px] overflow-y-auto">
      {content}
    </div>
  </div>
</div>
