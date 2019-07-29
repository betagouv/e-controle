<template>
  <div class="table-responsive" v-if="files && files.length">
    <div class="form-label">Fichier{{ answer_count===1 ? '': 's' }} déposé{{ answer_count===1 ? '': 's' }}:</div>
    <table class="table table-hover table-outline table-vcenter text-nowrap card-table">
      <thead>
        <tr>
          <th>Date de dépôt</th>
          <th>Nom du document</th>
          <th>Déposant</th>
          <th v-if="isAudited"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="file in files" :key="file.id">
          <td>
            <div>{{  file.creation_date }}</div>
            <div class="small text-muted">{{  file.creation_time }}</div>
          </td>
          <td>
            <div class="truncate"><a target="_blank" :href="file.url">{{ file.basename }}</a></div>
          </td>
          <td class="text-center">
            <div>{{ file.author.first_name }} {{ file.author.last_name }}</div>
          </td>
          <td v-if="isAudited" class="text-center">
            <a href="javascript:void(0)"
               data-toggle="modal"
               :data-target="'#trash-confirm-modal-' + file.id"
            >
              <div class="fe fe-trash-2"></div>
            </a>
          </td>
          <confirm-modal
                         :id="'trash-confirm-modal-' + file.id"
                         title="Corbeille"
                         confirm-button="Oui, envoyer à la corbeille"
                         cancel-button="Non, annuler"
                         @confirm="sendToTrash(file.id)"
          >
            <p>
              Vous allez envoyer “{{ file.basename }}” à la corbeille.
            </p>
          </confirm-modal>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

  import Vue from "vue";

  import ConfirmModal from '../utils/ConfirmModal'
  import EventBus from '../events'

  export default Vue.extend({
    data() {
      return {
        files: {}
      };
    },
    mounted() {
      this.files = this.question.response_files.filter(file => !file.is_deleted)

      var _this = this
      EventBus.$on('response-files-updated-' + this.question.id, function (files) {
        _this.files = files.filter(file => !file.is_deleted)
      })
    },
    computed: {
      answer_count: function () {
         return this.files ? this.files.length: 0
      }
    },
    props: {
      question: Object,
      isAudited: Boolean,
    },
    methods: {
      sendToTrash: function(fileId) {
        console.log('sendToTrash', fileId)
      }
    },
    components: {
      ConfirmModal,
    }
  });
</script>

<style scoped>

</style>
