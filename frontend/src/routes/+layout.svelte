<script>
  import '../app.css'
  import { Navbar } from '$lib/components/navbar'
</script>

<Navbar />

<main class="container mx-auto px-4">
  <slot />
</main>
