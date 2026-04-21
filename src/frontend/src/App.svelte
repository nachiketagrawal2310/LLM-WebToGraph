<script lang="ts">
  import { onMount } from 'svelte';
  import { appState } from './lib/stores/appState';
  import { healthCheck } from './lib/api/client';
  import QueryForm from './lib/components/QueryForm.svelte';
  import CSVProcessor from './lib/components/CSVProcessor.svelte';
  import HTMLProcessor from './lib/components/HTMLProcessor.svelte';
  import ResponseDisplay from './lib/components/ResponseDisplay.svelte';
  import LoadingSpinner from './lib/components/LoadingSpinner.svelte';

  let isDarkMode = true;

  function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  onMount(async () => {
    document.documentElement.classList.add('dark');
    
    try {
      const health = await healthCheck();
      if (health.status === 'success' || (health as any).status === 'healthy') {
        appState.update(s => ({ ...s, neo4jConnected: (health as any).neo4j_connected || false }));
      }
    } catch (e) {
      console.error('Health check failed:', e);
    }
  });
</script>

<div class="min-h-screen bg-background text-foreground transition-colors duration-300">
  <header class="border-b border-border sticky top-0 z-50 bg-background/80 backdrop-blur-md">
    <div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
      <div class="flex items-center gap-6">
        <h1 class="text-xl font-semibold tracking-tight">LLM-WebToGraph</h1>
        <div class="h-4 w-[1px] bg-border"></div>
        
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            {#if $appState.neo4jConnected}
              <div class="flex items-center gap-1.5 px-2 py-1 bg-emerald-500/10 rounded border border-emerald-500/20">
                <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 1.1.9 2 2 2h12a2 2 0 002-2V7a2 2 0 00-2-2H6a2 2 0 00-2 2zM9 5v14M15 5v14M4 11h16M4 15h16" />
                </svg>
                <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-500">Neo4j Active</span>
              </div>
            {:else}
              <div class="flex items-center gap-1.5 px-2 py-1 bg-destructive/10 rounded border border-destructive/20">
                <svg class="w-3.5 h-3.5 text-destructive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>
                <span class="text-[10px] font-bold uppercase tracking-wider text-destructive">Neo4j Offline</span>
              </div>
            {/if}
          </div>
        </div>
      </div>
      
      <button 
        on:click={toggleDarkMode}
        class="p-2 hover:bg-accent rounded-md transition-colors text-muted-foreground hover:text-foreground"
      >
        {#if isDarkMode}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M12 5a7 7 0 100 14 7 7 0 000-14z" /></svg>
        {:else}
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
        {/if}
      </button>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
    <section class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <CSVProcessor />
      <HTMLProcessor />
    </section>

    <section class="space-y-4">
      <div class="bg-card border border-border rounded-xl p-8 shadow-sm">
        <QueryForm />
      </div>
    </section>

    <section class="space-y-4 min-h-[100px]">
      {#if $appState.isLoading}
        <LoadingSpinner />
      {/if}

      {#if $appState.error}
        <ResponseDisplay type="error" content={$appState.error} />
      {/if}

      {#if $appState.response && !$appState.isLoading}
        <ResponseDisplay type="success" content={$appState.response} />
      {/if}
    </section>
  </main>
</div>
