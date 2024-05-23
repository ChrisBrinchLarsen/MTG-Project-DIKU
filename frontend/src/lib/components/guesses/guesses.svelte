<script lang="ts">
  import type { Guess } from '$lib/types/cards'
  import { TRAITS_TO_GUESS } from '$lib/types/cards'

  export let guesses: Guess[]

  const getBackgroundColor = ({ correctValues, incorrectValues }: Guess['type']) => {
    if (correctValues.length > 0 && incorrectValues.length > 0) {
      return 'bg-orange-500'
    } else if (correctValues.length > 0 && incorrectValues.length === 0) {
      return 'bg-green-500'
    } else {
      return 'bg-red-500'
    }
  }
</script>

{#if guesses.length > 0}
  <div class="flex flex-col items-center">
    <div class="flex gap-4">
      {#each TRAITS_TO_GUESS as trait}
        <p class="w-24 text-center">{trait}</p>
      {/each}
    </div>
    <ul class="mt-2 flex flex-col gap-4">
      {#each guesses as guess}
        <li class="flex gap-4">
          {#each Object.entries(guess) as [_, values]}
            <div
              class="flex h-16 w-24 items-center justify-center p-2 text-xs {getBackgroundColor(
                values
              )}"
            >
              {#each values.correctValues as value}
                {value}
              {/each}
              {#each values.incorrectValues as value}
                {value}
              {/each}
            </div>
          {/each}
        </li>
      {/each}
    </ul>
  </div>
{/if}
