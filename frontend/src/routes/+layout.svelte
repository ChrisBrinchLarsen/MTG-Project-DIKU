<script lang="ts">
  import '../app.css'
  import { onMount } from 'svelte'
  import { Navbar } from '$lib/components/navbar'
  import bg1 from '$lib/assets/bg1.jpg'
  import bg2 from '$lib/assets/bg2.jpg'
  import bg3 from '$lib/assets/bg3.jpg'
  import bg4 from '$lib/assets/bg4.jpg'
  import bg5 from '$lib/assets/bg5.jpeg'
  import bg6 from '$lib/assets/bg6.jpeg'
  import bg7 from '$lib/assets/bg7.jpg'
  import bg8 from '$lib/assets/bg8.jpg'
  import bg9 from '$lib/assets/bg9.jpg'
  import bg10 from '$lib/assets/bg10.jpg'
  import bg11 from '$lib/assets/bg11.jpg'
  import bg12 from '$lib/assets/bg12.jpg'

  let bg: string | null = null

  onMount(() => {
    const backgrounds = [bg1, bg2, bg3, bg4, bg5, bg6, bg7, bg8, bg9, bg10, bg11, bg12]

    bg = backgrounds[Math.floor(Math.random() * backgrounds.length)]
  })
</script>

<Navbar />

<main class="container mx-auto max-w-4xl px-4 text-gray-200">
  <div class="fixed left-0 top-0 -z-50 h-full w-full bg-black">
    <img src={bg} alt="Background" class="h-full w-full object-cover brightness-50" />
  </div>
  <slot />
</main>
