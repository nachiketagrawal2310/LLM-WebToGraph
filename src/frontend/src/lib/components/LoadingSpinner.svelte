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
