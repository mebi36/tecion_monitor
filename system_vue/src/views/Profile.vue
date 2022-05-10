<template>
    <div class="row">
        <div class="col-sm-4"></div>
        <div class="col-sm-4 py-2">
            <h1>{{ username }}'s Profile</h1>
            <button @click="logOut()" class="btn btn-warning">Log out</button>
        </div>
    </div>    
</template>

<script>
import axios from 'axios'
export default {
    data () {
        return {
            username: ''
        }
    },
    name: 'Profile',
    created(){
        this.username = localStorage.getItem('username')
    },
    methods:{
        logOut() {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            localStorage.removeItem("username")
            localStorage.removeItem("userId")
            localStorage.removeItem("email")

            this.$store.commit('removeToken')

            this.$router.push('/')

        }
    }
}
</script>