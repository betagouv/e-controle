<template>
  <div class="card-header" :class="{ 'sidebar-item-selected': selected }">
    <a v-bind:href="link">
      <slot></slot>
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