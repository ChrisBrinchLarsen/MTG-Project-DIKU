<script lang="ts">
  import { createEventDispatcher } from 'svelte'
  import type { PartialCard } from '$lib/types/cards'
  import * as HoverCard from '$lib/components/ui/hover-card'

  export let cards: PartialCard[]

  const dispatch = createEventDispatcher<{ cardClick: number }>()
</script>

<ul class="mt-8 grid grid-cols-5 gap-4">
  {#each cards as card (card.cardid)}
    <li class="flex justify-center">
      <HoverCard.Root openDelay={700}>
        <HoverCard.Trigger>
          <button on:click={() => dispatch('cardClick', card.cardid)}>
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
