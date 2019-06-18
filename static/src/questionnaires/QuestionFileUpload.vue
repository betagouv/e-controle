<template>
  <div>
    <vue-dropzone id="drop1" :options="dropOptions"></vue-dropzone>
    HERE {{ questionId }}
  </div>
</template>


<script>
  import Vue from "vue";
  import vueDropzone from "vue2-dropzone";


  export default Vue.extend({
    props: {
      questionId: Number
    },
    data: () => ({
      dropOptions: {
        url: "https://httpbin.org/post"
      }
    }),
    components: {
      vueDropzone
    }
  });
</script>
