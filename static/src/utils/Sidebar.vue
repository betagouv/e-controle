<template>
  <div id="sidebar" class="col-lg-4">
        <div class="card">
          <div class="card-header bg-blue text-white">
            <h4 class="card-title">{{ title }}</h4>
          </div>
          <div class="sidebar-body">
            <slot></slot>
          </div>
        </div>
  </div>

</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'title',
    ],
  })
</script>