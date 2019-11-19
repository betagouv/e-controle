<template>
  <div>
    <div class="mb-4 flex-row justify-content-between">
      <div class="page-title">
        <i class="fa fa-archive mr-2"></i>
        Mon espace de dépôt
      </div>
      <control-create v-if="user.is_inspector"></control-create>
    </div>

    <control-title :control="control"></control-title>

    <questionnaire-list :control="control" :user="user"></questionnaire-list>

    <user-section :control="control"></user-section>

    <webdav-tip v-if="user.is_inspector" :webdavurl="webdavurl + '/' + control.reference_code"></webdav-tip>

  </div>

</template>

<script>
  import Vue from 'vue'

  import ControlCreate from './ControlCreate'
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
      ControlCreate,
      ControlTitle,
      QuestionnaireList,
      UserSection,
      WebdavTip,
    },
  })
</script>