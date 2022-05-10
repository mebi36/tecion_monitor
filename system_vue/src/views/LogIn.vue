<template>
    <div class="log-in-page p-5 rounded-3">
        <div class="row">
            <div class="col-sm-4"></div>
            <div class="col-sm-4 bg-dark">
                <h1 class="title">Log In</h1>
                <form @submit.prevent="submitForm">
                    <div class="ps-3 my-4 d-flex justify-content-start">
                        <label for="Username" class="form-label pe-2">Username:</label>
                        <!-- <div> -->
                            <input type="text" class="form-control" v-model="username">
                        <!-- </div> -->
                    </div>

                    <div class="ps-3 mb-3 d-flex justify-content-start">
                        <label for="Password" class="form-label pe-2">Password:</label>
                        <!-- <div> -->
                            <input type="password" class="form-control" v-model="password">
                        <!-- </div> -->
                    </div>

                    <div class="alert alert-danger" role="alert" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                    
                    <!-- <BIconExclamationDiamond /> -->
                    <div class="ps-3 my-4 d-flex justify-content-center">
                        <button class="btn btn-warning"><BIconBoxArrowInRight class="pe-1" style="height: 1.5rem; width:1.5rem"/> Log In</button>
                    </div>
                    <hr>

                    <div class="form-group">

                    </div>
                </form>
            </div>
            <div class="col-sm-4"></div>
        </div>
        <!-- <div class="col"></div> -->
    </div>
</template>

<script>
import axios from 'axios'
import {BIconBoxArrowInRight} from 'bootstrap-icons-vue'
export default {
    name: 'LogIn',
    components: {
        BIconBoxArrowInRight
    },
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Log In | Tecion'
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    
                    this.$store.commit('setToken', token)

                    localStorage.setItem("token", token)

                    axios.get("api/v1/users/me/", {
                        headers: {
                            Authorization: 'Token ' + token
                        }
                    }).then(response => {
                        localStorage.setItem("username", response.data.username)
                        localStorage.setItem("userId", response.data.id)
                        localStorage.setItem("email", response.data.email)
                    })
                    const toPath = this.$route.query.to || '/'

                    this.$router.push(toPath)
            })
            .catch(error => {
                if(error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`)
                    }
                } else {
                    this.errors.push('Something went wrong. Please try again')

                    console.log(JSON.stringify(error))
                }
            })
        }
    }
}
</script>