<template>
  <div class="card-header">
    <a v-bind:href="link">
      {{ text }}
    </a>
  </div>
</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'link',
      'text',
    ],
  })
</script>