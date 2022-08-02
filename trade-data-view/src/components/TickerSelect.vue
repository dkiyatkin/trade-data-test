<script setup>
import _isEqual from 'lodash-es/isEqual'
import { ref, watch, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useFetch } from '@vueuse/core'

const router = useRouter()

const tickerIds = inject('tickerIds')

const selected = ref([])

watch(tickerIds, (newTickerIds) => {
  selected.value = [...newTickerIds]
})
watch(selected, (newSelectedTickerIds, oldSelectedTickerIds) => {
  if (!newSelectedTickerIds.length) return router.push({ name: 'home' })
  if (_isEqual(newSelectedTickerIds, oldSelectedTickerIds)) return
  router.push({ name: 'home', query: { t: [...newSelectedTickerIds] } })
})

const options = ref([])
const { data } = useFetch('http://127.0.0.1:8000/tickers').get().json()

watch(data, (dataTickerIds) => {
  if (!dataTickerIds) return
  options.value = dataTickerIds.map(tickerId => {
    return {
      text: tickerId,
      value: tickerId
    }
  })
})
</script>

<template>
  <div :class="['select is-multiple mt-2', $style.tickerSelect]">
    <select v-model="selected" multiple>
      <option v-for="option in options" :value="option.value" :key="option.value">
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<style module lang="scss">
html .tickerSelect > select[multiple] {
  width: 100%;
  height: 100%;
}
</style>
