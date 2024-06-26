<script lang="ts">
  import type { Guess, PartialCard } from '$lib/types/cards'
  import { Button } from '$lib/components/ui/button'

  export let guesses: Guess[]
  export let correctCard: PartialCard | undefined

  let isShowingAllGuesses = false

  const getBackgroundColor = (status: Guess['type']['status']) => {
    if (status === 'partial') {
      return 'bg-orange-500'
    } else if (status === 'correct') {
      return 'bg-green-500'
    } else {
      return 'bg-red-600'
    }
  }

  const getBoxStyle = (
    style: 'correct' | 'incorrect',
    values: {
      correctValues: (string | null)[]
      incorrectValues: (string | null)[]
    }
  ) => {
    if (values.correctValues.length > 0 && values.incorrectValues.length > 0) {
      return style === 'correct' ? 'text-green-800' : 'text-red-800'
    }
    return ''
  }

  const getArrow = (trait: string, correctCard: PartialCard | undefined, value: string | null) => {
    if (correctCard && value) {
      if (trait == 'cmc') {
        if (correctCard.cmc > parseInt(value)) {
          return '↑'
        }
        return '↓'
      }
    }
    return ''
  }

  const getValueLabel = (trait: string, value: string) => {
    if (trait == 'color') {
      switch (value) {
        case 'G':
          return 'Green'
        case 'R':
          return 'Red'
        case 'U':
          return 'Blue'
        case 'B':
          return 'Black'
        case 'W':
          return 'White'
        case 'C':
          return 'Colorless'
        default:
          return ''
      }
    }

    return value
  }

  $: labels = guesses.length > 0 ? Object.keys(guesses[0]) : null
</script>

{#if labels && guesses.length > 0}
  <div class="flex flex-col items-center">
    <div class="flex gap-4 text-xs uppercase">
      {#each labels as label}
        <p class="w-24 text-center">{label}</p>
      {/each}
    </div>
    <ul class="mt-2 flex flex-col gap-4">
      {#each guesses.slice(0, isShowingAllGuesses ? guesses.length : 3) as guess}
        <li class="flex gap-4">
          {#each Object.entries(guess) as [trait, values]}
            <div
              class="flex h-16 w-24 flex-col items-center justify-center gap-1 rounded p-2 text-center text-xs font-bold capitalize {getBackgroundColor(
                values.status
              )}"
            >
              {#each values.correctValues as value}
                <p class={getBoxStyle('correct', values)}>
                  {value === null ? `No ${trait}` : getValueLabel(trait, value)}
                </p>
              {/each}
              {#each values.incorrectValues as value}
                <p class={getBoxStyle('incorrect', values)}>
                  {value === null ? `No ${trait}` : getValueLabel(trait, value)}
                  {getArrow(trait, correctCard, value)}
                </p>
              {/each}
            </div>
          {/each}
        </li>
      {/each}
    </ul>
    {#if guesses.length > 3}
      <Button
        variant="link"
        class="mt-4 text-white"
        on:click={() => (isShowingAllGuesses = !isShowingAllGuesses)}
      >
        {#if isShowingAllGuesses}
          Hide guesses ↑
        {:else}
          Show all guesses ↓
        {/if}
      </Button>
    {/if}
  </div>
{/if}
