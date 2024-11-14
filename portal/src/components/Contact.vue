<script>
   function onSubmit(token) {
     document.getElementById("demo-form").submit();
   }
</script>
<template>
    <div id="contact">
        <img src="../assets/Horse.png" alt="Ilustración caballo">
        <div>
            <h1>Contactanos</h1>
            <p>Si tenés alguna duda, sugerencia o estás pensando en inscribirte en CEDICA, no dudes en contactarnos.</p>
            <form action="POST" class="d-flex flex-column gap-3">
                <div class="d-flex flex-row gap-3">
                    <input class="form-control" type="text" placeholder="Nombre">
                    <input class="form-control" type="email" placeholder="Correo">
                </div>
                <textarea class="form-control" name="" id="" cols="20" rows="5" placeholder="Mensaje"></textarea>
                <button class="btn btn-submit-custom">Enviar</button>
            </form>
        </div>
    </div>
</template>
<style scoped>
    #contact {
        background-image: url(../assets/bg-images/contact-bg.png);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 80vh;
        margin: 75px 0;
        width: 100%;
        padding: 0 !important;
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
    }

    #contact .form-control:focus {
        border-color: transparent !important;
        box-shadow: 0 0 0 0.2rem rgba(1, 176, 158, 0.43) !important;
    }
    
    textarea.form-control {
        resize: none;
        overflow-y: auto;
    }

    .btn-submit-custom {
        background-color: #01b09e;
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }

    .btn-submit-custom:hover {
        background-color: #018a7f;
    }
</style>