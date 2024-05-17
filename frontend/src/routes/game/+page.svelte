<script lang="ts">
  import { onMount } from 'svelte'
  import type { PartialCard } from '$lib/types/cards'
  import { initGame, guessCard } from '$lib/services/cards'

  let cards: PartialCard[] | undefined
  let correctCard: PartialCard | undefined

  $: handleCardClick = async (id: number) => {
    if (!cards || !correctCard) {
      return
    }

    const data = await guessCard({
      guessedCardId: id,
      correctCardId: correctCard.cardid,
      cardIds: cards.map((card) => card.cardid)
    })

    cards = data.cards
  }

  onMount(async () => {
    const data = await initGame()
    cards = data.cards
    correctCard = data.correctCard
  })

  $: sortedCards =
    cards && correctCard ? [...cards, correctCard].sort((a, b) => a.cardid - b.cardid) : []
</script>

{#if cards && correctCard}
  <ul class="grid grid-cols-5 gap-4">
    {#each sortedCards as card (card.cardid)}
      <li class="flex justify-center">
        <button on:click={() => handleCardClick(card.cardid)}>
          <img src={card.imagesmall} alt={card.name} />
        </button>
      </li>
    {/each}
  </ul>
{:else}
  Initializing game...
{/if}
