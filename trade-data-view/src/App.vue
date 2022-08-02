<script setup>
import { ref, watch, provide } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar.vue'

const route = useRoute()

const tickerIds = ref([])
watch(() => route.query.t, (queryTickerIds) => {
  if (queryTickerIds) {
    if (queryTickerIds.splice) {
      tickerIds.value = [...queryTickerIds].splice(-10)
    } else {
      tickerIds.value = [queryTickerIds]
    }
  } else {
    tickerIds.value = []
  }
})

provide('tickerIds', tickerIds)
</script>

<template>
  <div :class="$style.app">
    <AppHeader :class="$style.appHeader" />
    <div :class="$style.wrapper">
      <router-view :class="$style.mainView"></router-view>
      <AppSidebar :class="$style.appSidebar" />
    </div>
  </div>
</template>

<style module lang="scss">
.app {
  max-width: 1000px;
  min-height: 100%;
  margin: 0 auto;
  padding: 30px;
  display: flex;
  flex-direction: column;
}
.appHeader {
  margin-bottom: 30px;
}
.wrapper {
  display: flex;
}
  .mainView {
    width: 100%;
  }
  .appSidebar {
    flex-shrink: 0;
    width: 200px;
    margin-left: 30px;
    padding-bottom: 28px;
  }
</style>
