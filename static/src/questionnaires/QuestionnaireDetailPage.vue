<template>
  <div>
    <questionnaire-detail :questionnaire="questionnaire"></questionnaire-detail>
  </div>

</template>

<script>
  import Vue from "vue";

  import axios from 'axios'
  import QuestionnaireDetail from './QuestionnaireDetail'

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
    components: {
      QuestionnaireDetail
    }
  })

</script>