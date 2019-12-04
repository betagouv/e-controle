<template>
  <div>
    <control-title :control="control" :webdavurl="webdavurl"></control-title>
    <questionnaire-list :control="control" :user="user"></questionnaire-list>
    <user-section :control="control"></user-section>
  </div>

</template>

<script>
  import Vue from 'vue'

  import ControlCreate from './ControlCreate'
  import ControlTitle from "./ControlTitle"
  import QuestionnaireList from '../questionnaires/QuestionnaireList'
  import UserSection from '../users/UserSection'

  export default Vue.extend({
    props: [
      'control',
      'user',
      'webdavurl',
    ],
    components: {
      ControlCreate,
      ControlTitle,
      QuestionnaireList,
      UserSection,
    },
  })
</script>