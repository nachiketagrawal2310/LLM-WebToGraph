# LLM-WebToGraph: Academic Design System with shadcn/svelte

## ⚠️ CRITICAL DESIGN PRINCIPLE

**This is an ACADEMIC PROJECT, not a startup product. Do NOT vibecode it.**

The UI must reflect scientific rigor, institutional authority, and professional research standards. Think:
- **Research papers**, not TikTok
- **University dashboards**, not Figma trends
- **Lab interfaces**, not design agency portfolios
- **Enterprise research tools**, not marketing websites

---

## Design Philosophy: Academic First

| Principle | DO ✓ | DON'T ✗ |
|-----------|------|---------|
| **Color** | Neutral grays, professional blue, subtle accents | Neon, gradients, "fun" colors |
| **Typography** | System fonts, clear hierarchy, readable sizes | Trendy fonts, decorative styles |
| **Animations** | Purposeful transitions, accessibility-first | Flashy, distracting effects |
| **Layout** | Clean grids, whitespace, structured flow | Scattered elements, asymmetric chaos |
| **Buttons** | Semantic, consistent, clearly interactive | Skeuomorphic, novelty designs |
| **Spacing** | Generous, mathematically consistent | Cramped, arbitrary |
| **Shadows** | Subtle depth cues only | Box shadows everywhere |
| **Interactions** | Direct, predictable, keyboard-friendly | Experimental, mouse-dependent |

---

## Part 0: Setup shadcn/svelte

```bash
# Install shadcn/svelte
npm install -D shadcn-svelte
npx shadcn-svelte@latest init

# This will set up components in src/lib/components/ui/
# Your custom components remain in src/lib/components/
```

---

## Color System (Academic Professional)

Based on your Tailwind config and shadcn defaults:

```
Semantic Colors:
├─ primary:      #0F172A (Professional Navy)     - Headers, primary actions
├─ primary-fg:   #FFFFFF (Pure White)            - Text on primary
├─ secondary:    #64748B (Slate)                 - Secondary text, borders
├─ accent:       #3B82F6 (Professional Blue)    - Interactive elements
├─ muted:        #F1F5F9 (Off-white)             - Backgrounds
├─ muted-fg:     #64748B (Slate)                 - Muted text
├─ background:   #FFFFFF (White)                 - Main background
├─ foreground:   #1E293B (Near Black)            - Primary text
├─ destructive:  #DC2626 (Research Red)          - Errors only
├─ border:       #E2E8F0 (Light Gray)            - Subtle dividers
└─ ring:         #3B82F6 (Focus ring)            - Accessibility

Status Colors (Academic Context):
├─ Success:      #059669 (Forest Green)          - Completed, verified
├─ Warning:      #D97706 (Amber)                 - Processing, caution
├─ Error:        #DC2626 (Red)                   - Failed, invalid
└─ Info:         #0284C7 (Blue)                  - Informational
```

---

## Part 1: App.svelte with shadcn/svelte

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
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

  onMount(async () => {
    try {
      const health = await healthCheck();
      if (health.status === 'success' || (health as any).status === 'healthy') {
        appState.update(s => ({ 
          ...s, 
          neo4jConnected: (health as any).neo4j_connected || false 
        }));
      }
    } catch (e) {
      console.error('Health check failed:', e);
    }
  });
</script>

<div class="min-h-screen bg-background text-foreground">
  <!-- Academic Header -->
  <header class="border-b border-border sticky top-0 z-50 bg-white">
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
            <Badge variant="outline" class="bg-green-50 text-green-900 border-green-200">
              <span class="inline-block w-2 h-2 bg-green-600 rounded-full mr-2 animate-pulse"></span>
              Connected
            </Badge>
          {:else}
            <Badge variant="outline" class="bg-red-50 text-red-900 border-red-200">
              <span class="inline-block w-2 h-2 bg-red-600 rounded-full mr-2 animate-pulse"></span>
              Disconnected
            </Badge>
          {/if}
        </div>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-6xl mx-auto px-6 py-12">
    <!-- Hero Section (Academic) -->
    <section class="mb-12">
      <div class="bg-slate-900 text-white rounded-lg p-8 border border-slate-800">
        <h2 class="text-3xl font-bold tracking-tight mb-4">
          Extract Structured Knowledge from Unstructured Data
        </h2>
        <p class="text-slate-200 mb-6 leading-relaxed">
          LLM-WebToGraph transforms CSV files and web content into machine-readable knowledge 
          graphs using advanced language models. Query with natural language, get structured answers 
          from your knowledge base.
        </p>
        
        <!-- Tech Stack Grid -->
        <div class="grid grid-cols-3 gap-4 text-sm">
          <div>
            <div class="font-semibold text-white">Language Model</div>
            <div class="text-slate-400">Hugging Face Qwen</div>
          </div>
          <div>
            <div class="font-semibold text-white">Graph Database</div>
            <div class="text-slate-400">Neo4j AuraDB</div>
          </div>
          <div>
            <div class="font-semibold text-white">Framework</div>
            <div class="text-slate-400">LangChain + Svelte</div>
          </div>
        </div>
      </div>
    </section>

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
      <div class="bg-white border border-border rounded-lg p-8">
        <QueryForm />
      </div>
    </section>

    <!-- Results Section -->
    <section>
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
```

---

## Part 2: QueryForm.svelte with shadcn/svelte

```svelte
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
    <p class="text-sm text-muted-foreground">
      Enter your question in natural language. The system will search the knowledge graph 
      and synthesize answers from the extracted entities and relationships.
    </p>
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
```

---

## Part 3: CSVProcessor.svelte with shadcn/svelte

```svelte
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
      <div class="p-2 bg-blue-100 rounded-md">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      Load and process CSV files from the data directory. The system analyzes structure, 
      extracts entities, identifies relationships, and populates the knowledge graph.
    </p>
    
    <Button 
      on:click={handleCSV}
      disabled={$appState.csvProcessing}
      class="w-full"
    >
      {#if $appState.csvProcessing}
        <span class="flex items-center gap-2">
          <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
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
```

---

## Part 4: HTMLProcessor.svelte with shadcn/svelte

```svelte
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
      <div class="p-2 bg-emerald-100 rounded-md">
        <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
      Process HTML and web content to extract structured information. The system parses 
      web pages, identifies key entities and concepts, and integrates them into the knowledge graph.
    </p>
    
    <Button 
      on:click={handleHTML}
      disabled={$appState.htmlProcessing}
      class="w-full"
    >
      {#if $appState.htmlProcessing}
        <span class="flex items-center gap-2">
          <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
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
```

---

## Part 5: ResponseDisplay.svelte with shadcn/svelte

```svelte
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
```

---

## Part 6: LoadingSpinner.svelte

```svelte
<div class="flex flex-col items-center justify-center py-20 gap-4">
  <!-- Academic Spinner -->
  <div class="relative w-12 h-12">
    <div class="absolute inset-0 border-2 border-border rounded-full"></div>
    <div class="absolute inset-0 border-2 border-transparent border-t-primary rounded-full animate-spin"></div>
  </div>

  <!-- Loading Text -->
  <div class="text-center space-y-1">
    <p class="font-semibold text-foreground">Processing Query</p>
    <p class="text-sm text-muted-foreground">
      Analyzing knowledge graph and generating response...
    </p>
  </div>

  <!-- Progress Bar -->
  <div class="w-48 h-1 bg-border rounded-full overflow-hidden mt-2">
    <div class="h-full bg-primary rounded-full animate-pulse" style="width: 60%;"></div>
  </div>
</div>
```


---

## Part 7: Typography & Spacing System

```css
/* Academic typography hierarchy */
--text-xs: 0.75rem;       /* 12px - labels, captions */
--text-sm: 0.875rem;      /* 14px - body text, small content */
--text-base: 1rem;        /* 16px - default body */
--text-lg: 1.125rem;      /* 18px - section titles */
--text-xl: 1.25rem;       /* 20px - major titles */
--text-2xl: 1.5rem;       /* 24px - page headers */
--text-3xl: 1.875rem;     /* 30px - hero titles */

--spacing: 0.25rem;       /* 4px - base unit */
--spacing-2: 0.5rem;      /* 8px */
--spacing-3: 0.75rem;     /* 12px */
--spacing-4: 1rem;        /* 16px - standard padding */
--spacing-6: 1.5rem;      /* 24px - section padding */
--spacing-8: 2rem;        /* 32px - major sections */
--spacing-12: 3rem;       /* 48px - layout padding */
```

---

## Part 8: CRITICAL DESIGN CHECKLIST

### ✅ DO (Academic Standards)
- [ ] Use semantic HTML and shadcn components
- [ ] Maintain consistent spacing (multiples of 4px)
- [ ] Use the professional color palette only
- [ ] Include focus states for keyboard navigation
- [ ] Write descriptive labels and help text
- [ ] Test with screen readers
- [ ] Ensure 4.5:1 contrast ratio minimum
- [ ] Use professional sans-serif fonts
- [ ] Keep animations under 300ms
- [ ] Design mobile-first, then enhance

### ❌ DON'T (Never Do This)
- [ ] NO gradients (except subtle hero bg)
- [ ] NO vibrant colors or neon accents
- [ ] NO novelty fonts or typography
- [ ] NO flashy hover effects
- [ ] NO dark/light mode without purpose
- [ ] NO excessive shadows
- [ ] NO auto-playing animations
- [ ] NO custom styled scrollbars
- [ ] NO emojis in UI text
- [ ] NO "cute" design elements

---

## Part 9: Component Usage Examples

### Using Button (shadcn)
```svelte
<Button variant="default">Primary Action</Button>
<Button variant="outline">Secondary Action</Button>
<Button variant="ghost">Tertiary</Button>
<Button disabled>Disabled</Button>
```

### Using Card (shadcn)
```svelte
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
</Card>
```

### Using Alert (shadcn)
```svelte
<Alert>
  <AlertTitle>Heads up!</AlertTitle>
  <AlertDescription>You can add components to your app using the cli.</AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Your session has expired.</AlertDescription>
</Alert>
```

---

## Part 10: Academic Typography Rules

**Never use:**
- Comic Sans, cursive, decorative fonts
- Serif fonts in UI (only in content)
- More than 2-3 font weights

**Always use:**
- System font stack (SF Pro, Segoe UI, Helvetica)
- 400 (regular) and 600 (semibold) weights
- Line-height of 1.5-1.6 for body text
- Letter-spacing of 0 (default)

---

## Part 11: Accessibility Requirements (Non-Negotiable)

- [ ] All buttons/interactive elements have focus rings
- [ ] Color is not the only indicator (use icons, text)
- [ ] Form labels are always visible (not placeholders)
- [ ] Skip links for keyboard navigation
- [ ] ARIA attributes where needed
- [ ] Contrast ratio ≥ 4.5:1 for text
- [ ] Touch targets ≥ 48px for mobile
- [ ] Keyboard shortcuts are documented
- [ ] Error messages are descriptive
- [ ] Loading states are clear

---

## Part 12: Implementation Checklist

- [ ] Run `npm install shadcn-svelte`
- [ ] Run `npx shadcn-svelte@latest init`
- [ ] Replace App.svelte with academic version
- [ ] Update QueryForm.svelte with Button/Textarea
- [ ] Update CSVProcessor.svelte with Card component
- [ ] Update HTMLProcessor.svelte with Card component
- [ ] Update ResponseDisplay.svelte with Alert component
- [ ] Update LoadingSpinner.svelte
- [ ] Verify all colors use semantic tokens
- [ ] Test keyboard navigation
- [ ] Test mobile responsiveness
- [ ] Audit with Lighthouse a11y
- [ ] Get design review from academic stakeholder

---

## FINAL WARNING

**This is NOT a startup landing page. This is NOT a design portfolio. This is NOT competing with Dribbble.**

Your audience is:
- Researchers and data scientists
- Academic institutions
- Enterprise research teams

They will judge this on:
- **Clarity** - Can I understand what this does in 10 seconds?
- **Reliability** - Does it look stable and trustworthy?
- **Usability** - Can I use this without training?
- **Professionalism** - Does this look like a real research tool?

Every design decision must serve these goals. If something is "trendy" or "fun," it has no place here.
