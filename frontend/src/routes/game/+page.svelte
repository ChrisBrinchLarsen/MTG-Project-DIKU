<script lang="ts">
  import { onMount } from 'svelte'
  import type { Guess, PartialCard } from '$lib/types/cards'
  import { initGame, guessCard } from '$lib/services/cards'
  import Guesses from '$lib/components/guesses/guesses.svelte'
  import * as HoverCard from '$lib/components/ui/hover-card'
  import { goto } from '$app/navigation'

  let cards: PartialCard[] | undefined
  let correctCard: PartialCard | undefined
  let guesses: Guess[] = []

  $: handleCardClick = async (id: number) => {
    if (!cards || !correctCard) {
      return
    }

    if (id === correctCard.cardid) {
      goto(`/game/won?cardId=${correctCard.cardid}&guesses=${guesses.length + 1}`)
    }

    const data = await guessCard({
      guessedCardId: id,
      correctCardId: correctCard.cardid,
      cardIds: cards.map((card) => card.cardid)
    })

    cards = data.cards
    guesses = [data.guess, ...guesses]
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
  <Guesses {guesses} {correctCard} />
  <ul class="mt-8 grid grid-cols-5 gap-4">
    {#each sortedCards as card (card.cardid)}
      <li class="flex justify-center">
        <HoverCard.Root openDelay={700}>
          <HoverCard.Trigger>
            <button on:click={() => handleCardClick(card.cardid)}>
              <img src={card.imagesmall} alt={card.name} class="rounded-md" />
            </button>
          </HoverCard.Trigger>
          <HoverCard.Content>
            <img src={card.imagenormal} alt={card.name} class="rounded-md" />
          </HoverCard.Content>
        </HoverCard.Root>
      </li>
    {/each}
  </ul>
{:else}
  Initializing game...
{/if}
