<template>
  <div>
    Got questionnaire: {{ questionnaire.title }}
  </div>

</template>

<script>
  import Vue from "vue";

  import axios from 'axios'

  const questionnaire_url = "/api/questionnaire/";

  export default Vue.extend({
    props: [ 'questionnaireId' ],
    data : function () {
      return {
        questionnaire: ''
      }
    },
    mounted: function(){
      this.getQuestionnaire()
    },
    methods: {
      getQuestionnaire: function() {
        axios.get(questionnaire_url + this.questionnaireId).then(response => {
          this.questionnaire = response.data
        });
      },
    },
  })

</script>