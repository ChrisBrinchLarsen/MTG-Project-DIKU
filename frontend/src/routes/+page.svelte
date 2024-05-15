<script lang="ts">
  import { goto } from '$app/navigation'
</script>

<div class="mx-auto flex h-[60vh] max-w-sm flex-col justify-center">
  <button on:click={() => goto('/game')} class="rounded-lg bg-gray-300 px-6 py-2">Play</button>
</div>
