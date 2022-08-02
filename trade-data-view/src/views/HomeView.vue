<script setup>
import _sortBy from 'lodash-es/sortBy'
import _sortedUniqBy from 'lodash-es/sortedUniqBy'
import { shallowReactive, watch, nextTick, inject } from 'vue'
import { useFetch, useWebSocket } from '@vueuse/core'
import LineChart from '@/components/LineChart.vue'

function updateChartDataset (tickerId, tickerItems) {
  const datasetIndex = chartData.datasets.findIndex(dataset => (dataset.label === tickerId))
  if (!chartData.datasets[datasetIndex]) return
  chartData.count++
  let datasetData = chartData.datasets[datasetIndex].data
  datasetData = datasetData.concat(tickerItems)
  datasetData = _sortBy(datasetData, item => item.pos)
  datasetData = _sortedUniqBy(datasetData, item => item.pos)
  chartData.datasets[datasetIndex].data = datasetData
}

function fetchTickers () {
  tickerIds.value.forEach((tickerId) => {
    useFetch(`http://127.0.0.1:8000/tickers/${tickerId}`).get().json()
      .then(({ data }) => {
        const tickerItems = data.value
        updateChartDataset(tickerId, tickerItems)
      })
  })
}

function createChartDatasets (newTickerIds) {
  return newTickerIds.map(label => ({ label, data: [] }))
}

const tickerIds = inject('tickerIds')

const chartData = shallowReactive({
  count: 0,
  datasets: createChartDatasets(tickerIds.value)
})

fetchTickers()

const { status, data, send } = useWebSocket('ws://127.0.0.1:8000/ws')

watch(status, (newStatus) => {
  if (newStatus === 'OPEN') {
    send(JSON.stringify(tickerIds.value))
  }
})

watch(tickerIds, async (newTickerIds) => {
  chartData.datasets = []
  await nextTick()
  chartData.count = 0
  chartData.datasets = createChartDatasets(newTickerIds)
  send(JSON.stringify(newTickerIds))
  fetchTickers()
})

watch(data, (newData) => {
  newData = JSON.parse(newData)
  updateChartDataset(newData.ticker_id, [newData.ticker_item])
})
</script>

<template>
  <div :class="$style.homeView">
    <template v-if="!!chartData.datasets.length">
      <LineChart :chart-data="chartData" isLegend />
    </template>
    <template v-else>
      <LineChart :chart-data='{ "datasets": [{}] }' />
    </template>
  </div>
</template>

<style module lang="scss">
.homeView {
}
</style>
