<template>
  <div class="alert alert-info alert-icon alert-dismissible">
    <button v-if="!noclose" type="button" class="close" data-dismiss="alert" @click="dismissed"></button>
    <i class="fe fe-info" aria-hidden="true"></i>
    <slot></slot>
  </div>
</template>

<script>
  import Vue from "vue"

  export default Vue.extend({
    props: ['noclose'],
    methods: {
      dismissed: function () {
        this.$emit('dismissed')
      }
    },

  })

</script>
