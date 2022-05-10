<template>
    <div class="py-1">
        <ContentDiv>
            <h1>Equipment Under Monitoring</h1><hr>
            <ul>
                <li
                    class="d-flex justify-start" 
                    v-for="item in monitoredItems" :key="item.id">
                    
                    <a :href="`/dashboard/${item.id}`" class="link link-light">
                    <BIconArrowRightCircleFill class="me-2" />{{ item.type.name }} {{ item.id }}
                    </a>
                </li>
            </ul>
        </ContentDiv>
        <div style="position:absolute; height:30%;"></div>
    </div>
</template>

<script>
import { BIconArrowRightCircleFill } from 'bootstrap-icons-vue'
import ContentDiv from '../components/ContentDiv.vue'
export default{
    name: "MonitoredItems",
    components: {
        ContentDiv,
        BIconArrowRightCircleFill
    },
    async mounted(){
        this.$store.commit('getMonitoredItems')
    },
    computed: {
        monitoredItems(){
            return this.$store.state.monitoredItems
        }
    }
}
</script>
