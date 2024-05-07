<script lang="ts">
  import { getEmployees } from '$lib/services/employees'
  import { onMount } from 'svelte'

  let data: { id: number; name: string }[] | null = null

  onMount(async () => {
    data = await getEmployees()
  })
</script>

{#if data}
  <p class="mb-4">Here's some test data!</p>
  <ul>
    {#each data as employee (employee.id)}
      <li class="flex gap-2 text-lg">
        <p>{employee.id}</p>
        <p>{employee.name}</p>
      </li>
    {/each}
  </ul>
{:else}
  Fetching employees...
{/if}
