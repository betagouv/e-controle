<template>
<div>
  Demo User App {{ users }}
</div>
</template>

<script lang="ts">
  import Vue from "vue";

  export default Vue.extend({
    data() {
      return {
        users: [1, 2]
      }
    }
  });
</script>

<style></style>
