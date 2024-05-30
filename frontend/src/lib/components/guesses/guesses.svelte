<script lang="ts">
  import type { Guess, PartialCard } from '$lib/types/cards'

  export let guesses: Guess[]
  export let correctCard: PartialCard | undefined

  const getBackgroundColor = ({ correctValues, incorrectValues }: Guess['type']) => {
    if (correctValues.length > 0 && incorrectValues.length > 0) {
      return 'bg-orange-500'
    } else if (correctValues.length > 0 && incorrectValues.length === 0) {
      return 'bg-green-500'
    } else {
      return 'bg-red-500'
    }
  }

  const getBoxStyle = (
    style: 'correct' | 'incorrect',
    value: string | null,
    values: {
      correctValues: (string | null)[]
      incorrectValues: (string | null)[]
    }
  ) => {
    let className = ''

    if (values.correctValues.length > 0 && values.incorrectValues.length > 0) {
      className += style === 'correct' ? 'text-green-800' : 'text-red-800'
    }

    if (value === null) {
      className += 'italic'
    }

    return className
  }
  const getArrow = (
    trait: string | null,
    correctCard: PartialCard | undefined,
    value: string | null
  ) =>
  {
    if (correctCard && value) {
      if (trait == "cmc") {
        if (correctCard.cmc > parseInt(value)) {
          return '↑';
        }
        return '↓'
      }
    }
    return ''
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
      {#each guesses as guess}
        <li class="flex gap-4">
          {#each Object.entries(guess) as [trait, values]}
            <div
              class="flex h-16 w-24 flex-col items-center justify-center gap-1 p-2 text-center text-xs font-bold capitalize {getBackgroundColor(
                values
              )}"
            >
              {#each values.correctValues as value}
                <p class={getBoxStyle('correct', value, values)}>
                  {value === null ? `No ${trait}` : value}
                </p>
              {/each}
              {#each values.incorrectValues as value}
                <p class={getBoxStyle('incorrect', value, values)}>
                  {value === null ? `No ${trait}` : value} {getArrow(trait, value, correctCard)}
                </p>
              {/each}
            </div>
          {/each}
        </li>
      {/each}
    </ul>
  </div>
{/if}
