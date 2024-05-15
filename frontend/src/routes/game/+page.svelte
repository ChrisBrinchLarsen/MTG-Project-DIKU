<script lang="ts">
  import { onMount } from 'svelte'
  import type { Card } from '$lib/types/cards'
  import { getCards, guessCard } from '$lib/services/cards'

  let data: Card[] | null = null

  const handleCardClick = async (id: number) => {
    await guessCard({ id })
  }

  onMount(async () => {
    data = await getCards()
  })
</script>

{#if data}
  <ul class="grid grid-cols-5 gap-4">
    {#each data as card (card.cardid)}
      <li class="flex justify-center">
        <button on:click={() => handleCardClick(card.cardid)}>
          <img src={card.imagesmall} alt={card.name} />
        </button>
      </li>
    {/each}
  </ul>
{:else}
  Fetching cards...
{/if}
