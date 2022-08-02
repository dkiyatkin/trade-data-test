<template>
  <div :class="$style.appHeader">
    <h1 class="title">
      <router-link :to="{ name: 'home' }">trade-data-view</router-link>
    </h1>
  </div>
</template>

<style module lang="scss">
.appHeader {
  text-align: center;
}
</style>
