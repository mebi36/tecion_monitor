<template>
<div :class="checkRoute">  
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#"><img src="../src/assets/logo-dark.png" style="height:50px; width:auto;"></a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <!-- <a class="nav-link active" aria-current="page" href="#">Home</a> -->
            <router-link to="/" class="nav-link" 
            >Home</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/monitored-items">Dashboard</a>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link"
            >About Us</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" tabindex="-1" aria-disabled="true">Contact Us</a>
          </li>
          <li class="nav-item">
            <router-link v-if="$store.state.isAuthenticated" to="/profile" class="nav-link">
            <BIconPerson class="pe-1" style="fill:#ffdf00; height: 1.3rem; width: 1.3rem;" />Profile</router-link>

            <router-link v-else to="/log-in" class="nav-link">
            Log In</router-link>
          </li>

        </ul>
      </div>
    </div>
  </nav>

<section class="section">
  <router-view />
</section>

<footer class="footer mt-auto py-3 bg-dark" style="margin-top: 50px;">
  <div class="container text-warning">Tecion Technology Solutions &copy;2022</div>
</footer>

</div>  
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import axios from 'axios'
import { BIconPerson } from 'bootstrap-icons-vue'
export default {
  name: 'App',
  components: {
    BIconPerson
  },
  beforeCreate(){
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if(token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  computed: {
    checkRoute() {
      if (this.$route.name === 'Home'){
        return 'wrapper-home'
      }else if (this.$route.name === 'Dashboard'){
        return 'wrapper-dashboard'
      }
      return 'wrapper'
    }
  }
  }

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700&display=swap');
:root {
  --primary: #eeeeee;
  --secondary: #333333;
  --body: #ffdf00;
}
h1, h2, h3, h4 h5, h6, .display-4 {
  color: var(--body);
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
  
}

.wrapper {
  color: var(--body);
  font-family: Sora, "san-serif";
  line-height: 1.7;
  background-position: center;
  background-size: cover;
  background-color: rgba(51, 51, 51, 0.9);
  z-index: 2;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-x: hidden;
  overflow-y: auto;
}
.wrapper-dashboard {
  color: var(--body);
  font-family: Sora, "san-serif";
  line-height: 1.7;
  background-position: center;
  background-size: cover;
  background-color: rgba(51, 51, 51, 0.9);
  z-index: 2;
  position: relative;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-x: hidden;
  overflow-y: auto;
}

.wrapper-home {
  color: var(--body);
  font-family: Sora, "san-serif";
  line-height: 1.7;
  background-position: center;
  background-size: cover;
  background-image: url('~@/assets/bg-board-bw.png');
  z-index: 2;
  position: relative;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}

.wrapper-home:after {
  content: "";
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(51, 51, 51, 0.85);
  z-index: -1;
  overflow-y: auto;
}

.router-link-active {
  color: white;
  font-weight: bold;
}
.section {
  height: 90%;
  /* position: sticky; */
}
</style>