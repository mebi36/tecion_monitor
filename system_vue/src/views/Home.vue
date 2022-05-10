<template>
    <div class="home">
        <div class="col-md-12 p-2">
            <div class="h-100 p-5 text-white bg-dark rounded-3">
                <h1>Welcome to Tecion Technology Solutions</h1>
                <p>We are here to facilitate your digital transformation</p>
                <button class="btn btn-warning">Get Started <BIconArrowRightSquare  style="height:1.2rem; width: 1.2rem;"/></button>
            </div>
        </div>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        <div style="position:absolute; height:30%;"></div>
    </div>
</template>

<script>
import {BIconArrowRightSquare} from 'bootstrap-icons-vue'
export default {
    components: {
        BIconArrowRightSquare
    },
    beforeCreate: function() {
        document.body.name = 'wrapper-home';
    },
      mounted() {
    document.title = this.$route.name + ' | Tecion'
  }
}
</script>
