<template>
  <!--div class="card card-collapsed mb-0 border-0">
    remove collapse for now
    <div class="card-header" data-toggle="card-collapse"-->
  <div class="card mb-0 border-0">
    <div class="card-header">
      <a v-bind:href="link">
        {{ text }}
      </a>
    </div>

    <div>
      <div class="card-header flex-column align-items-start">
        <slot></slot>
      </div>
    </div>

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