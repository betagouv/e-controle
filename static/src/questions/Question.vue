<template>
  <div class="card-header border-0 p-0">
    <span class="stamp stamp-md bg-blue mr-3 cursor-pointer">
      {{ themeNumbering }}.{{ questionNumbering }}
    </span>

    <div class="card-text cursor-pointer">
      <div class="with-line-breaks">{{ question.description }}</div>
      <div class="tags">
        <template v-if="questionFileCount > 0">
          <span class="tag tag-orange pull-left cursor-pointer">
            {{ questionFileCount }} fichier{{ questionFileCount === 1 ? '': 's' }}
            annexe{{ questionFileCount === 1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-paperclip"></i>
            </span>
          </span>
        </template>
        <template v-if="responseFileCount">
          <span class="tag tag-azure pull-left cursor-pointer">
            {{ responseFileCount }} fichier{{ responseFileCount === 1 ? '': 's' }}
            déposé{{ responseFileCount === 1 ? '': 's' }}
            <span class="tag-addon">
              <i class="fe fe-file"></i>
            </span>
          </span>
        </template>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import Vue from 'vue'

import EventBus from '../events'

export default Vue.extend({
  props: {
    themeNumbering: Number,
    questionNumbering: Number,
    question: Object,
  },
  data() {
    return {
      questionFileCount: 0,
      responseFileCount: 0,
    }
  },
  mounted() {
    const numNotDeleted = files => files.filter(file => !file.is_deleted).length
    this.responseFileCount = 0
    if (this.question.response_files) {
      this.responseFileCount = numNotDeleted(this.question.response_files)
    }
    if (this.question.question_files) {
      this.questionFileCount = this.question.question_files.length
    }
    EventBus.$on('response-files-updated-' + this.question.id, responseFiles => {
      this.responseFileCount = numNotDeleted(responseFiles)
    })
    EventBus.$on('question-file-count-changed-' + this.question.id, (questionFileCount) => {
      this.questionFileCount = questionFileCount
    })
  },
})
</script>

<style scoped>
  .cursor-pointer {
    cursor: pointer;
  }
</style>
