<script lang="ts">
  import { goto } from '$app/navigation'

  let name = ''

  const handleSubmit = () => {
    // Register user and game here. We will need to use localStorage.

    // Normally, we shouldn't need to setTimeout but there is a bug
    setTimeout(() => goto('/game'), 0)
  }
</script>

<div class="mx-auto flex h-[60vh] max-w-sm flex-col justify-center">
  <p class="text-center text-lg font-semibold">Enter your name to start</p>
  <form on:submit={handleSubmit} class="mt-8 flex flex-col gap-4">
    <label class="flex flex-col gap-2">
      Name
      <input bind:value={name} type="text" class="rounded-lg border px-2 py-2" />
    </label>
    <button type="submit" class="rounded-lg bg-gray-300 px-6 py-2">Play</button>
  </form>
</div>
