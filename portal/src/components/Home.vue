<template>
    <div id="home" class="d-flex flex-column justify-content-center align-items-center" style="height: 80vh; width: 100%;">
        <img src="../assets/logos/Logo.png" width="25%" alt="">
        <div class="mt-3">
            Acá iría el home
        </div>
    </div>
</template>
<style scoped>
    #home {
        margin: 0 !important;
        padding: 0 !important;
        display: flex;
        justify-content: center;
        align-items: center;
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
</style>