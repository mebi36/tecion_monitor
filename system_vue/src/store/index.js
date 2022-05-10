import {createStore} from 'vuex'
import axios from 'axios'

export default createStore({
    state: {
        isAuthenticated: false,
        token: '',
        monitoredItems: {}

    },
    mutations: {
        initializeStore(state){
            if (localStorage.getItem('token')){
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
        },
        setToken(state, token){
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state){
            state.token = ''
            state.isAuthenticated = false
        },

        async getMonitoredItems(state){
            await axios
                .get(`/api/v1/monitor/equipment/${localStorage.getItem('userId')}/`)
                .then(response =>{
                    state.monitoredItems = response.data
            })

        }
    },
    actions: {
    },
    modules: {
    }
})