<template>
  <div class="card">
    <div class="card-status card-status-left bg-blue">
    </div>
    <div class="card-header">
      <control-title :control="control" :key="control.id"></control-title>
    </div>
    <div class="card-body">

      <questionnaire-list :control="control" :user="user"></questionnaire-list>

      <user-section :control="control" :key="control.id"></user-section>

      <webdav-tip v-if="user.is_inspector" :webdavurl="webdavurl + '/' + control.reference_code"></webdav-tip>

    </div>
  </div>

</template>

<script>
  import Vue from 'vue'

  import ControlTitle from "./ControlTitle"
  import QuestionnaireList from '../questionnaires/QuestionnaireList'
  import UserSection from '../users/UserSection'
  import WebdavTip from './WebdavTip'

  export default Vue.extend({
    props: [
      'control',
      'user',
      'webdavurl',
    ],
    components: {
      ControlTitle,
      QuestionnaireList,
      UserSection,
      WebdavTip,
    },
  })
</script>