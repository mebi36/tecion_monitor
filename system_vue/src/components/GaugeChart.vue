<template>
    <div>
        <v-chart class="chart" :option="option" />
    </div>
</template>

<script>
import { customTheme } from './echartsThemes';
import { use, registerTheme } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { GaugeChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, defineComponent, toRef } from "vue";

registerTheme('customVintage', customTheme);


use([
  CanvasRenderer,
  GaugeChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

export default defineComponent({
  name: "GaugeComponent",
  components: {
    VChart
  },
  provide: {
    [THEME_KEY]: "customVintage"
  },
  props: {
      gaugeValue : Number
  },
  setup: (props) => {
    const reading = toRef(props, 'gaugeValue')
    const option = ref({
      tooltip: {
          formatter: '{a} <br/>{b} : {c}%'
      },
      series: [
          {
              name: 'Fuel Level',
              type: 'gauge',
              detail: {
                  formatter: '{value}'
              },
              data: [
                  {
                      value: reading,
                      name: 'Fuel Level'
                  }
              ]
          }
      ]
    });

    return { option };
  }
});
</script>

<style scoped>
.chart {
  height: 300px;
}
</style>

