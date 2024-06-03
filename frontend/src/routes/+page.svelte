<script lang="ts">
  import { goto } from '$app/navigation'
  import { Button } from '$lib/components/ui/button'
</script>

<div class="mx-auto flex h-[60vh] max-w-sm flex-col justify-center">
  <Button on:click={() => goto('/game')} size="lg" class="text-xl">Play regular mode</Button>
</div>
