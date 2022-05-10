<template>
<div>
    <div class="row mx-1 mt-2">
        <h3 class="bg-dark py-1">Dashboard ({{ itemName }})</h3>
        <div class="col-sm-4">
            <div class="card bg-dark" style="height: 100%">
                <div class="card-header"><h3>Last System Update</h3></div>
                <div class="card-body time" >{{ getLastUpdateTime }}</div>
            </div>
        </div>
        <div class="col-sm-4">
            <div class="card bg-dark" style="height: 100%">
                <div class="card-body"><GaugeChart :gaugeValue="getFuelLevel" /></div>
            </div>
        </div>
        <div class="col-sm-4">
            <div class="card bg-dark" style="height: 100%">
                <div class="card-header"><h3>Last Ignition State</h3></div>
                <div class="card-body" ><BIconPower class="ignition" :class="getIgnitionStyling" /></div>
                <div class="card-footer" :class="getIgnitionStyling">{{ computeIgnitionState }}</div>
            </div>
        </div>
    </div>
    <div class="row my-2 mx-1">
        <div class="card bg-dark">
            <div class="card-header"><h3>Fuel Level History</h3></div>
            <div class="card-body">
                <select v-model="period" class="d-flex bg-dark text-light col-sm-3">
                    <option 
                        v-for="item in periods" 
                        :value="item.value"
                        :key="item.value">
                        {{ item.label }}
                    </option>
                </select>
                <div class="bg-dark row"><FuelLevelHistory :chartData="getFuelLevelHistory" /></div>
            </div>
        </div>
    </div>
</div> 
</template>

<script>
import axios from 'axios'
import GaugeChart from "../components/GaugeChart.vue"
import FuelLevelHistory from '../components/FuelLevelHistory.vue'
import {BIconPower} from 'bootstrap-icons-vue'
export default {
    name: 'Dashboard',
    components: {
        GaugeChart, FuelLevelHistory,
        BIconPower
    },
    data(){
        return{
            systemUpdate: null,
            fuel_level_history: null,
            item_id: '',
            itemName: '',
            ignitionState: 'N/A',
            updateIntervalID: 0,
            updateIntervalID2: 0,
            periods: [{value: 1, label: '24 Hours'},
                        {value: 7, label: '1 Week'},
                        {value: 30, label: '1 month'},
                        {value: 90, label: '3 months'},
                        // {value: 365, label: '1 year'},
                        // {value: 777, label: 'Entire History'}
                        ],
            period: 1
        }
    },
    methods: {
        updateSystemParams(){
            //method for updating the system parameter values
            this.item_id = this.$route.params.item_id
            axios
                .get(`/api/v1/monitor/latest-system-parameters/${this.item_id}/`)
                .then(response => {
                    this.systemUpdate = response.data
                    this.itemName = this.systemUpdate.item.type.name
                })
                .catch(error => {
                    console.log(error)
                })
        },
        updateFuelLevelHistory(){
            this.item_id = this.$route.params.item_id
            axios
                .get(`/api/v1/monitor/fuel-level-history/${this.item_id}/`)
                .then(response => {
                    var fuel_level_raw = response.data
                    this.fuel_level_history = fuel_level_raw.map( Object.values )
                    this.fuel_level_history = this.fuel_level_history.map(d => [new Date(d[0]), d[1]])
                })
                .catch(error => {
                    console.log(error)
                })
        },
        findArrIndex(arr, item, start, end){
            if (start > end){
                return -1
            }
            let mid = Math.floor((start + end)/2)
            let midValue = new Date(arr[mid][0])
            let itemDate = new Date(item)
            if (midValue.getTime() === itemDate.getTime()){
                return mid
            }

            if(midValue.getTime() > itemDate.getTime()){
                return this.findArrIndex(arr, item, start, mid-1)
            }else{
                return this.findArrIndex(arr, item, mid+1, end)
            }
        },
        transformChartData(period){
            const dateNow = new Date()
            dateNow.setSeconds(0, 0)
            const dateStart = new Date(dateNow.getTime() - period*24*60*60000)
            var count = 1
            var chartData = []
            var data = this.fuel_level_history.map(arr => {
                return arr.slice()
            })
            data = data.map(x => {
                return [x[0].setSeconds(0,0), x[1]]
            })

            data = data.filter(item => {
                let dateObj = new Date(item[0])
                return dateObj.getTime() >= dateStart.getTime() && dateObj.getTime() <= dateNow.getTime()
            })
            while(count <= period*24*60){
                chartData.push([new Date(dateNow.getTime() - count*60000), null])
                count++
            }
            chartData.reverse()
            const result = chartData.map(x => {
                var criteria = this.findArrIndex(data, x[0], 0, data.length-1)
                if(criteria < 0){ 
                    return x
                }else{
                    return [x[0], data[criteria][1]]
                }
            })
            return result

        },
        getIgnitionState(){
            if(this.systemUpdate){
                if (this.systemUpdate.ignition)
                {
                    this.ignitionState = 'ON'
                }
                if (!this.systemUpdate.ignition){
                    this.ignitionState =  'OFF'
                }else{
                    this.ignitionState = 'N/A'
                }
            }
            else{
                this.ignitionState = 'N/A'
            }
            return this.ignitionState
        },
    },
    mounted(){
      this.updateSystemParams()
      this.updateIntervalID = setInterval(() => {this.updateSystemParams()}, 15*1000)

      this.updateFuelLevelHistory()
      this.updateIntervalID2 = setInterval(() => {this.updateFuelLevelHistory()}, 300*1000)
    },
    unmounted(){
        // clearTimeout(this.updateTimeoutID)
    },
    computed: {
        getFuelLevel () {
            if(this.systemUpdate){
            return parseInt(this.systemUpdate.fuel_level)
            }else{ return 0}
        },
        getOilLevel () {
            if(this.systemUpdate){
                return parseInt(this.systemUpdate.oil_level)
            }else { return 0}
        },
        getLastUpdateTime () {
            if(this.systemUpdate){
                var updateTime =  new Date(this.systemUpdate.time_stamp)
                var timeForDisplay = ''
                timeForDisplay = updateTime.getHours() + ':' + updateTime.getMinutes() + ' ' + updateTime.getDay()+'/'+(updateTime.getMonth() + 1)+'/'+updateTime.getFullYear().toString().substr(-2)
                return timeForDisplay
            }else{ 
                return 'N/A'}
        },
        getFuelLevelHistory () {
            var computedChartData = []
            if(this.fuel_level_history){
                computedChartData = this.transformChartData(this.period)
            }
            return computedChartData
        },
        getIgnitionStyling(){
            if(this.ignitionState === 'ON'){
                return 'ignition-on'

            }
            else if (this.ignitionState === 'OFF'){
                return 'ignition-off'
            }
            else{
                return 'ignition-na'
            }
        },
        computeIgnitionState(){
            return this.getIgnitionState()
        }
    },
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');

.time {
    font-family: Orbitron, "san-serif";
    line-height: 1.7;
    font-size: 3rem;
}

.ignition {
    height: 8rem;
    width: 8rem;
}
.ignition-on {
    color: #3ab027;
}
.ignition-off {
    color: #ff4249;
}
.ignition-na {
    color: #7d7c7c;
}
</style>