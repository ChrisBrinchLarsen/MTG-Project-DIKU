<script lang="ts">
  import { onMount } from 'svelte'
  import { goto } from '$app/navigation'
  import type { Guess, PartialCard } from '$lib/types/cards'
  import { initGame, guessCard } from '$lib/services/cards'
  import { Guesses } from '$lib/components/guesses'
  import { Cards } from '$lib/components/cards'

  let cards: PartialCard[] | undefined
  let correctCard: PartialCard | undefined
  let guesses: Guess[] = []

  $: handleCardClick = async (id: number) => {
    if (!cards || !correctCard) {
      return
    }

    if (id === correctCard.cardid) {
      return goto(`/game/won?cardId=${correctCard.cardid}&guesses=${guesses.length + 1}`)
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
</script>

{#if cards && correctCard}
  <Guesses {guesses} {correctCard} />
  <Cards cards={[...cards, correctCard]} on:cardClick={(e) => handleCardClick(e.detail)} />
{:else}
  Initializing game...
{/if}
