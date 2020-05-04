<template>
  <div class="card border-0 mb-0">

    <div class="card-header border-0 pl-0"
         data-toggle="collapse"
         :data-target="'#' + id"
         aria-expanded="false"
         :aria-controls="id">
      <div class="card-title m-0">
        <button type="button" class="btn btn-secondary">
          <i class="fe mr-2" :class="buttonicon"></i>
          {{ buttontext }}
        </button>
      </div>
    </div>

    <div class="collapse" :id="id">
      <slot></slot>
    </div>
  </div>

</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: ['buttontext', 'buttonicon'],
  data: function () {
    return {
      id: '',
    }
  },
  mounted: function() {
    this.id = 'collapsible-' + Math.floor(Math.random() * 1000000)
  },
})
</script>
