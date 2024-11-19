<template>
    <section id="about" class="d-flex flex-row justify-content-center align-items-center gap-4">
      <div
        class="d-flex flex-column justify-content-center align-items-center gap-4 text-white"
        style="max-width: 600px; text-align: justify;"
      >
        <h1>Sobre nosotros</h1>
        <div 
          class="text-container" 
          :class="{ 'is-expanded': isExpanded }"
          ref="textContainer"
        >
          {{ aboutText }}
        </div>
        <button @click="toggleExpand" class="btn btn-link p-0 text-decoration-none">
          {{ isExpanded ? 'Ver menos' : 'Ver más' }}
        </button>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    data() {
      return {
        aboutText:
          "El Centro de Equitación para Personas con Discapacidad y Carenciadas, CEDICA, es una Asociación Civil sin Fines de Lucro, fundada en 1994 en la ciudad de La Plata, Provincia de Buenos Aires. La misión de CEDICA es la INCLUSIÓN SOCIAL: trabajamos con la finalidad de igualar oportunidades en procura de la reinserción familiar, el logro de la escolaridad, la integración laboral y la mejora integral de la calidad de vida de nuestros alumnos y alumnas. La actividad que realizamos se denomina internacionalmente Rehabilitación Ecuestre y es una terapia integral que apunta a la recuperación de la persona en sus dimensiones biológica, psíquica y social. La Rehabilitación Ecuestre utiliza al caballo de manera terapéutica, aprovechando las características de su naturaleza innata y de su medio ambiente como facilitadores del proceso rehabilitador.",
        isExpanded: false,
      };
    },
    methods: {
      toggleExpand() {
        this.isExpanded = !this.isExpanded;
  
        const container = this.$refs.textContainer;
        if (this.isExpanded) {
          container.style.height = `${container.scrollHeight}px`;
        } else {
          container.style.height = `100px`; 
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .text-container {
    overflow: hidden;
    height: 100px; 
    transition: height 0.5s ease;
  }
  
  .text-container.is-expanded {
    height: auto;
  }
  
  button {
    color: #0d6efd;
    border: none;
    background: none;
    cursor: pointer;
  }
  
  button:hover {
    text-decoration: underline;
  }


#about {
        background-image: url(../assets/bg-images/about-bg.png);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
        width: 100%;
        display: flex;
        justify-content: space-evenly;
        align-items: center;
    }

</style>