<template>
  <div class="card-header" :class="{ 'sidebar-item-selected': selected }">
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
      'selected',
      'text',
    ],
  })
</script>