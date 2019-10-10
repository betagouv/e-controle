<template>
  <div id="sidebar" class="col-lg-4">
    <div class="row sticky">
      <div class="col-md-6 col-lg-12">
        <div class="card">
          <div class="card-header bg-blue text-white">
            <h4 class="card-title">{{ title }}</h4>
          </div>
          <table class="table card-table">
            <tbody>
              <slot></slot>
            </tbody>
          </table>
        </div>
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