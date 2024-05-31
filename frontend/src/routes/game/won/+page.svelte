<script lang="ts">
  import { onMount } from 'svelte'
  import { goto } from '$app/navigation'
  import { page } from '$app/stores'
  import { browser } from '$app/environment'
  import { getCard } from '$lib/services/cards'
  import type { Card } from '$lib/types/cards'

  const cardId = $page.url.searchParams.get('cardId')
  const guesses = $page.url.searchParams.get('guesses')

  if (!cardId || !guesses) {
    if (browser) {
      goto('/game')
    }
  }

  let card: Card | null = null

  onMount(async () => {
    if (!cardId) {
      return
    }

    card = await getCard({ cardId })
  })
</script>

<div class="flex flex-col items-center">
  <p class="text-lg">You guessed it!</p>
  <h3 class="mt-8 text-3xl">{card?.name}</h3>
  <img src={card?.imagelarge} alt={card?.name} class="mt-4 w-96 rounded-xl" />
</div>
