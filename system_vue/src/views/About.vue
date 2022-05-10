<template>
    <div class="mt-2 bg-dark">
    <h1>About Us</h1>
    </div>
</template>


<script>
export default {
    beforeCreate: function() {
        document.body.name = 'wrapper';
    },
      mounted() {
    document.title = this.$route.name + ' | Tecion'
  }
}
</script>