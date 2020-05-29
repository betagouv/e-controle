<template>
  <div class="card-status card-status-left" :class="colorClass">
  </div>
</template>

<script>
import Vue from 'vue'

const colorClasses = [
  'bg-blue',
  'bg-red',
  'bg-yellow',
  'bg-purple',
  'bg-green',
  'bg-teal',
]

export default Vue.extend({
  props: ['id'],
  computed: {
    colorClass: function () {
      return colorClasses[this.id % colorClasses.length]
    },
  },
})

</script>
