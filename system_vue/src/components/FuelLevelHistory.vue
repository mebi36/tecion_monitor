<template>
<div>
    <v-chart class="chart" :option="option" />
</div>
    
</template>

<script>
import { customTheme } from './echartsThemes';
import {use, registerTheme } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    DataZoomComponent,
    ToolboxComponent,
    GridComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent, toRef} from "vue";


registerTheme('customVintage', customTheme);

use([
    CanvasRenderer,
    LineChart,
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    DataZoomComponent,
    ToolboxComponent,
    GridComponent
]);

export default defineComponent({
    name: "FuelLevelHistoryComponent",
    components: {
        VChart
    },
    provide: {
        [THEME_KEY]: "customVintage"
    },
    props: {
        chartData: Array,
    },
    setup: (props) => {
        const recv_data = toRef(props, 'chartData')
        // console.log(datas)
         const option = ref({
         title: {
             text: 'Fuel Level History',
             show: false
         },
         tooltip:{
             formatter: '{a}<br/> {c}%',
             trigger: 'axis',
             position: function(pt) {
                 return [pt[0], '10%'];
             }
         },
         toolbox: {
             feature: {
                 dataZoom: {
                     yAxisIndex: 'none'
                 },
                 resore: {},
                 saveAsImage: {}
             }
         },
         xAxis: {
             type: 'time',
             boundaryGap: false
         },
         yAxis:{
             type: 'value',
             boundaryGap: [0, '100%']
         },
         dataZoom: [
             {
                 type: 'inside',
                 start: 0,
                 end: 20
             },
             {
                 start: 0,
                 end: 20
             }
         ],
         series: [
             {
                 name: 'Fuel Level History',
                 type: 'line',
                 smooth: true,
                 symbol: 'none',
                 areaStyle: {},
                 data: recv_data
             }
         ]
         })
    return { option };
    }
})
</script>
<style scoped>
.chart {
  height: 300px;
}
</style>

