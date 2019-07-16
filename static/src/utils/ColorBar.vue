<template>
  <div class="card-status card-status-left" :class="colorClass">
  </div>
</template>

<script>
  import Vue from "vue"

  const color_classes = [
    'bg-blue',
    'bg-red',
    'bg-yellow',
    'bg-purple',
    'bg-green',
    'bg-teal',
  ]

  export default Vue.extend({
    props: [ 'id' ],
    computed: {
      colorClass: function () {
        return color_classes[this.id % color_classes.length]
      }
    },
  })

</script>