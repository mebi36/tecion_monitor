<template>
    <gauge
        heading="A title goes here"
        :min="0"
        :max="100"
        :value="exampleValue" 
    />
</template>

<script>
import Gauge from '@chrisheanan/vue-gauge';

export default {
    name: 'OtherGauge',
    components: { Gauge },
    data () {
        return {
            exampleValue: 35
    }
    }
}
</script>