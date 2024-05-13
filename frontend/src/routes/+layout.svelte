<script>
  import '../app.css'
  import { Navbar } from '$lib/components/navbar'
</script>

<Navbar />

<main class="container mx-auto max-w-4xl px-4">
  <slot />
</main>
