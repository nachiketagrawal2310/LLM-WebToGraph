<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { appState } from './lib/stores/appState';
  import { healthCheck } from './lib/api/client';
  
  // shadcn imports
  import { Button } from './lib/components/ui/button';
  import { Badge } from './lib/components/ui/badge';
  
  // Custom components
  import QueryForm from './lib/components/QueryForm.svelte';
  import CSVProcessor from './lib/components/CSVProcessor.svelte';
  import HTMLProcessor from './lib/components/HTMLProcessor.svelte';
  import ResponseDisplay from './lib/components/ResponseDisplay.svelte';
  import LoadingSpinner from './lib/components/LoadingSpinner.svelte';

  let resultsElement: HTMLElement;

  onMount(async () => {
    document.documentElement.classList.add('dark');
    try {
      const health = await healthCheck();
      const isConnected = health.status === 'success' && health.data?.neo4j_connected;
      appState.update(s => ({ 
        ...s, 
        neo4jConnected: !!isConnected
      }));
    } catch (e) {
      console.error('Health check failed:', e);
      appState.update(s => ({ ...s, neo4jConnected: false }));
    }
  });

  // Automatically scroll to results when they are available
  $: if ($appState.response || $appState.error) {
    scrollToResults();
  }

  async function scrollToResults() {
    await tick();
    if (resultsElement) {
      resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
</script>

<div class="min-h-screen bg-background text-foreground">
  <!-- Academic Header -->
  <header class="border-b border-border sticky top-0 z-50 bg-background/95 backdrop-blur">
    <div class="max-w-6xl mx-auto px-6 py-4">
      <div class="flex items-center justify-between">
        <!-- Branding -->
        <div>
          <h1 class="text-2xl font-bold tracking-tight">
            LLM-WebToGraph
          </h1>
          <p class="text-sm text-muted-foreground mt-1">
            Knowledge Graph Construction Framework
          </p>
        </div>

        <!-- Connection Status Badge -->
        <div>
          {#if $appState.neo4jConnected}
            <Badge variant="outline" class="bg-green-500/10 text-green-500 border-green-500/20">
              <span class="inline-block w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              Connected
            </Badge>
          {:else}
            <Badge variant="outline" class="bg-red-500/10 text-red-500 border-red-500/20">
              <span class="inline-block w-2 h-2 bg-red-500 rounded-full mr-2 animate-pulse"></span>
              Disconnected
            </Badge>
          {/if}
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-6xl mx-auto px-6 py-12">
    <!-- Data Processing Section -->
    <section class="mb-12">
      <h2 class="text-2xl font-bold tracking-tight mb-6">Data Sources</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <CSVProcessor />
        <HTMLProcessor />
      </div>
    </section>

    <!-- Query Interface Section -->
    <section class="mb-12">
      <h2 class="text-2xl font-bold tracking-tight mb-6">Query Interface</h2>
      <div class="bg-card border border-border rounded-lg p-8">
        <QueryForm />
      </div>
    </section>

    <!-- Results Section -->
    <section bind:this={resultsElement}>
      {#if $appState.isLoading}
        <LoadingSpinner />
      {/if}

      {#if $appState.error}
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-foreground mb-3">Error</h3>
          <ResponseDisplay type="error" content={$appState.error} />
        </div>
      {/if}

      {#if $appState.response && !$appState.isLoading}
        <div class="mb-6">
          <h3 class="text-lg font-semibold text-foreground mb-3">Results</h3>
          <ResponseDisplay type="success" content={$appState.response} />
        </div>
      {/if}
    </section>
  </main>

  <!-- Academic Footer -->
  <footer class="border-t border-border mt-20 py-8 bg-muted">
    <div class="max-w-6xl mx-auto px-6 text-center text-sm text-muted-foreground">
      <p class="font-medium text-foreground">LLM-WebToGraph</p>
      <p class="mt-1">
        Research Framework • Powered by Hugging Face, LangChain, Neo4j
      </p>
    </div>
  </footer>
</div>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
      'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  :global(html) {
    scroll-behavior: smooth;
  }
</style>
