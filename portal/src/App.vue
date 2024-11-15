<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'

const header = ref(null)
const router = useRouter()

const scrollToTop = () => {
  if (router.currentRoute.value.path === '/') {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

onMounted(() => {
  const handleScroll = () => {
    if (window.scrollY > 50) {
  header.value.classList.add('collapsed')
    } else {
  header.value.classList.remove('collapsed')
    }
  }

  document.addEventListener('scroll', handleScroll)

  onUnmounted(() => {
    document.removeEventListener('scroll', handleScroll)
  })
})
</script>

<template>
  <header ref="header" class="rounded-4 shadow-sm d-flex flex-row justify-content-center align-items-center">
    <div id="header-container">
      <RouterLink to="/" @click.native="scrollToTop">
        <img alt="CEDICA logo" class="logo" src="@/assets/logos/Imagotipo CEDICA.png" height="35" />
      </RouterLink>
  
      <div class="wrapper">
        <nav class="d-flex flex-row">
          <RouterLink to="/" @click.native="scrollToTop">Sobre nosotros</RouterLink>
          <RouterLink to="/articles">Artículos</RouterLink>
          <a class="nav-button" href="/#contact">Contactanos</a>
        </nav>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  position: fixed;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  max-width: 1300px;
  width: 90%;
  padding: 1.25rem 1.75rem;
  justify-self: center;
  background-color: rgba(245, 245, 245, 0.75);
  backdrop-filter: blur(10px);
  transition: all 0.3s;
  animation: fadeIn 0.75s;
  z-index: 1000;
}

#header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  width: 100%;
}

main {
  padding-top: 175px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-50px) translateX(-50%);
  }
  to {
    opacity: 1;
    transform: translateY(0px) translateX(-50%);
  }
}

header.collapsed {
  top: 0;
  width: 100%;
  max-width: 100%;
  border-radius: 0px !important;
  box-shadow: none !important;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  align-items: center;
}

nav a {
  padding: 0 1rem;
  color: black;
  font-size: 1rem;
}

nav a:not(.nav-button):hover {
  color: #2197a2;
}

nav .nav-button {
  padding: 0.5rem 1rem;
  margin-left: 1.5rem;
  border: none;
  border-radius: 12px;
  background-color: #2197a2;
  color: white;
  font-size: 1rem;
  transition: background-color 0.3s;
}

nav .nav-button:hover {
  background-color: #1c7c8c;
}

@media (max-width: 768px) {
  nav a:nth-child(1),
  nav a:nth-child(2) {
    display: none;
  }
}
</style>