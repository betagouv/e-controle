<template>
  <div v-bind:id="'theme' + themeNumbering"
       class="card">
    <div class="card-status card-status-top bg-blue"></div>
    <div class="card-header">
      <h3 class="card-title">{{ themeNumbering }}. {{ theme.title }}</h3>
    </div>

    <slot></slot>

  </div>
</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'theme',
      'themeNumbering',
    ],
  })
</script>