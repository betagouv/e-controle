<template>
  <tr>
    <td>
      <a v-bind:href="link">
        {{ text }}
      </a>
    </td>
  </tr>

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