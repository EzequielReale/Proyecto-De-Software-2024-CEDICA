<template>
  <section id="contact">
    <img src="../assets/Horse.png" alt="Ilustración caballo" class="slide-in-left">
    <div class="position-relative h-100 d-flex align-items-center justify-content-center slide-in-right">
      <div class="position-absolute" style="transform: skew(15deg);">
        <h1 class="fw-bolder">Contactanos</h1>
        <p>Si tenés alguna duda, sugerencia o estás pensando en inscribirte en CEDICA, no dudes en contactarnos.</p>
        <form @submit.prevent="onSubmit" class="d-flex flex-column gap-3">
          <div class="d-flex flex-row gap-3">
            <input class="form-control" type="text" placeholder="Nombre" required v-model="name">
            <input class="form-control" type="email" placeholder="Correo" required v-model="email" >
          </div>
          <textarea class="form-control" cols="20" rows="4" placeholder="Mensaje" required v-model="message"></textarea>
          <div class="d-flex flex-row gap-3 justify-content-between align-items-center">
            <div class="g-recaptcha" :data-sitekey="siteKey"></div>
            <button class="btn btn-submit-custom">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send"><path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/></svg>
              Enviar
            </button>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>
<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const message = ref('')
const siteKey = '6Lf4Dn8qAAAAANy2sdBnHEZsGwi7Fs5SbpczyM8t' // Reemplaza con tu site key

const onSubmit = () => {
  const recaptchaResponse = grecaptcha.getResponse()
  if (!recaptchaResponse) {
    alert('Por favor, completa el captcha')
    return
  }

  // Aquí puedes manejar el envío del formulario, por ejemplo, mostrando los datos en la consola
  console.log('Nombre:', name.value)
  console.log('Correo:', email.value)
  console.log('Mensaje:', message.value)
  console.log('reCAPTCHA:', recaptchaResponse)

  // Restablecer el captcha después de la verificación
  grecaptcha.reset()
}
</script>
<style scoped>
  #contact {
    background-image: url(../assets/bg-images/contact-bg.png);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 80vh;
    margin: 75px 0;
    width: 100%;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
  }

  #contact .form-control {
    padding: 0.6rem 1rem !important;
    border-radius: 5px !important;
    border: 1px solid #aaa !important;
    backdrop-filter: blur(10px) !important;
    background-color: rgba(255, 255, 255, 0.65) !important;
    transition: 0.3s;
  }

  #contact .form-control:focus {
    border-color: transparent !important;
    box-shadow: 0 0 0 0.2rem rgba(1, 176, 158, 0.43) !important;
    background-color: rgba(255, 255, 255, 0.8) !important;
  }

  #contact > img {
    width: 35%;
    max-width: 626px;
    min-width: 400px;
  }

  #contact > div {
    background-color: rgba(255, 255, 255, 0.65);
    border-radius: 10px;
    flex-grow: 0.75;
    min-width: 700px;
  }
  
  #contact > div > div {
    padding: 9rem;
    padding-top: 7rem;
  }

  textarea.form-control {
    resize: none;
    overflow-y: auto;
  }

  .btn-submit-custom {
    background-color: #01b09e;
    color: white;
    border: none;
    padding: 0.7rem 3rem;
    border-radius: 5px;
    cursor: pointer;
  }

  .btn-submit-custom:hover {
    background-color: #018a7f;
  }

  @media (max-width: 1024px) {
    #contact {
      flex-direction: column;
    }

    #contact > img {
      display: none;
    }

    #contact > div > div {
      padding: 7rem;
    }
  }
</style>