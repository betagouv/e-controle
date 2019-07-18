<template>
  <div class="card border-0 mb-0 card-collapsed">

    <div class="card-header border-0 pl-0" data-toggle="card-collapse">
      <div class="card-title m-0">
        <button type="button" class="btn btn-secondary">
          <i class="fe mr-2" :class="buttonicon"></i>
          {{ buttontext }}
        </button>
      </div>
    </div>

    <div>
      <slot></slot>
    </div>
  </div>

</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['buttontext', 'buttonicon']
  })
</script>