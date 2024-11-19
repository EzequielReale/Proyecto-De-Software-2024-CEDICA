<template>
    <section id="home" class="d-flex flex-column justify-content-center align-items-center" style="height: 80vh; width: 100%;">
      <img src="../assets/logos/Logo.png" width="25%" alt="Logo">

      <div class="mt-5 text-center">
        Centro de Equitación para Personas con Discapacidad y Carenciados
      </div>

      <div class="mt-4 contact-info d-flex flex-column align-items-center gap-3">

        <!-- Dirección -->
        <div class="d-flex align-items-center gap-2">
          
          <p class="mb-0 text-center">
            Calle 44 y 115 (1900) La Plata, La Plata, B 1900, Argentina
          </p>
        </div>

        <!-- Teléfono -->
        <div class="d-flex align-items-center gap-2">
          
          <p class="mb-0 text-center">+54 9 11 6763 0247</p>
        </div>

      </div>

    </section>
  </template>
  
  <style scoped>
  #home {
    margin: 0 !important;
    padding: 0 !important;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-size: 1rem;
  }
  
  #home::after {
    content: '';
    background-image: url('../assets/bg-images/baner-dec-right.png');
    background-size: contain;
    background-repeat: no-repeat;
    position: absolute;
    top: 0;
    right: 0;
    height: 500px;
    width: 115px;
    z-index: -1;
    opacity: 1;
  }
  
  #home::before {
    content: '';
    background-image: url('../assets/bg-images/baner-dec-left.png');
    background-size: contain;
    background-repeat: no-repeat;
    position: absolute;
    top: 0;
    left: 0;
    height: 500px;
    width: 150px;
    z-index: -1;
    opacity: 1;
  }
  
  .contact-info p {
    margin: 0;
  }
  </style>