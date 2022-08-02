<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import 'chartjs-adapter-date-fns'
import Chart from 'chart.js/auto'
import autocolors from 'chartjs-plugin-autocolors'

Chart.register(autocolors)

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  isLegend: {
    type: Boolean
  }
})

const chartOptions = computed(() => {
  return {
    animation: false,
    responsive: true,
    interaction: {
      intersect: false
    },
    parsing: {
      xAxisKey: 'date',
      yAxisKey: 'price'
    },
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'second',
          displayFormats: {
            second: 'kk:mm:ss'
          }
        }
      }
    },
    datasets: {
      line: {
        borderWidth: 1,
        radius: 0
      }
    },
    plugins: {
      autocolors: {
        offset: 3
      },
      legend: {
        display: props.isLegend
      },
      tooltip: {
        callbacks: {
          title: function (tooltipItems) {
            return tooltipItems[0].raw.date
          }
        }
      }
    },
    layout: {
      padding: {
        top: (props.isLegend ? 6 : 38)
      }
    }
  }
})
</script>

<template>
  <Line
    :chart-options="chartOptions"
    :chart-data="chartData"
  />
</template>
