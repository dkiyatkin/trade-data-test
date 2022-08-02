<script setup>
import TickerSelect from '@/components/TickerSelect.vue'
</script>

<template>
  <div :class="$style.appSidebar">
    <div :class="$style.tickers">
      <p class="is-size-5">Please select tickers:</p>
      <TickerSelect :class="$style.tickerSelect" />
    </div>
  </div>
</template>

<style module lang="scss">
.appSidebar {
}
  .tickers {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
    .tickerSelect {
      height: 100%;
    }
</style>
