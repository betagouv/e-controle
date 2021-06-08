<template>
  <div class="card">
    <confirm-modal
      ref="modal"
      cancel-button="Annuler"
      confirm-button-prevent="Dupliquer l'espace de dépôt"
      title="Dupliquer un espace de dépôt"
      @confirm="cloneControl"
    >
      <info-bar>
        Veuillez sélectionner les questionnaires que vous souhaitez dupliquer.
      </info-bar>
      <error-bar v-if="referenceError" :noclose="true">
        Ce nom abrégé est vide ou existe déjà. Veuillez saisir un nouveau nom abrégé.
      </error-bar>
      <form>
        <div class="form-group mb-4">
          <label id="reference-label" class="form-label">
            Nom abrégé<span class="form-required">*</span>
          </label>
          <div class="flex-row align-items-center">
            <span class="input-group-prepend" id="prepend">
              <span class="input-group-text">{{new Date().getFullYear()}}_</span>
            </span>
            <input type="text"
                   class="form-control"
                   v-model="reference_code"
                   required aria-labelledby="reference-label"
                   maxlength="255"
                   @focus="referenceChanged">
          </div>
        </div>
        <div class="form-group mb-6">
          <label class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" @click="checkAllQuestionnaires" v-model="allChecked">
            <span class="custom-control-label font-weight-bold">Sélectionner Tout
          </label>
          <label v-for="q in accessibleQuestionnaires"
                :key="q.id"
                class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" :value="q.id" v-model="checkedQuestionnaires">
            <span class="custom-control-label">Questionnaire {{ q.numbering }} - {{ q.title }}</span>
          </label>
        </div>
      </form>
    </confirm-modal>
    <confirm-modal
      ref="modalexp"
      cancel-button="Annuler"
      confirm-button-prevent="Exporter l'espace de dépôt"
      title="Exporter un espace de dépôt"
      @confirm="exportControl"
    >
      <info-bar>
        Veuillez sélectionner les questionnaires dont vous souhaitez exporter les fichiers-réponses.
      </info-bar>
      <form>
        <div class="form-group mb-6">
          <label class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" @click="checkAllQuestionnaires" v-model="allChecked">
            <span class="custom-control-label font-weight-bold">Sélectionner Tout
          </label>
          <label v-for="q in accessibleQuestionnaires"
                :key="q.id"
                class="custom-control custom-checkbox">
            <input type="checkbox" class="custom-control-input" :value="q.id" v-model="checkedQuestionnaires">
            <span class="custom-control-label">Questionnaire {{ q.numbering }} - {{ q.title }}</span>
          </label>
        </div>
      </form>
    </confirm-modal>
    <div class="card-status card-status-top bg-blue"></div>
    <template v-if="editMode">
      <div class="card-body">
        <error-bar v-if="hasErrors" :noclose="true">
            L'espace de dépôt n'a pas pu être modifié. Erreur : {{JSON.stringify(errors)}}
        </error-bar>

        <form @submit.prevent="updateControl">
          <div class="card-title">Modifier l'espace de dépôt</div>
          <fieldset class="form-fieldset">
            <div class="form-group">
              <label id="organization-label" class="form-label">
                Quel est le nom de l’organisme qui va déposer les réponses ?
                <span class="form-required">*</span>
              </label>
              <div class="flex-row align-items-center">
                <i class="fa fa-building mr-2 text-muted"></i>
                <input type="text" class="form-control" v-model="organization" required aria-labelledby="organization-label" maxlength="255">
              </div>
            </div>
            <div class="form-group">
              <label id="title-label" class="form-label">
                Quel est le nom de la procédure pour laquelle vous ouvrez cet espace de dépôt ?
                <span class="form-required">*</span>
              </label>
              <div class="flex-row align-items-center">
                <i class="fa fa-award mr-2 text-muted"></i>
                <input type="text" class="form-control" v-model="title" required aria-labelledby="title-label" maxlength="255">
              </div>
            </div>
          </fieldset>
          <div class="text-right">
            <button @click="cancel"
                    type="button"
                    class="btn btn-secondary">
              Annuler
            </button>
            <button id="control-title-submit-button"
                    type="submit"
                    class="btn btn-primary">
              Modifier l'espace de dépôt
            </button>
          </div>
        </form>

      </div>
    </template>

    <template v-else>
      <div class="card-body flex-row justify-content-between">

        <div v-if="organization">
          <div class="mb-3">
            <div class="text-muted font-italic">
              <i class="fa fa-building mr-2"></i>
              Organisme interrogé
            </div>
            <div class="page-title">{{ organization }}</div>
          </div>
          <div class="mb-3">
            <div class="text-muted font-italic">
              <i class="fa fa-award mr-2"></i>
              Procédure
            </div>
            <div class="card-title">{{ title }}</div>
          </div>
        </div>
        <div v-else>
          <div class="page-title">{{ title }}</div>
        </div>

        <div v-if="sessionUser.is_inspector" class="col-4 flex-column ie-flex-column-fix align-items-end ml-6">
          <div class="mb-6 flex-column ie-flex-column-fix align-items-end">
            <div class="text-muted card-title mb-1 break-word text-right">
              <strong>../{{control.reference_code}}</strong>
            </div>
            <a class="btn btn-secondary parent-fake-icon"
               @click="showWebdavTip">
              <i class="fe fe-folder mr-3"></i>
              <img :src="'/static/img/file-explorer.png'"
                   alt="Explorateur Windows"
                   class="fake-icon" />
              Comment voir les réponses ?
            </a>
          </div>

          <div class="btn-group">
            <button type="button"
                    class="btn btn-secondary"
                    @click="enterEditMode">
              <i class="fe fe-edit mr-2"></i>
              Modifier
            </button>
            <button type="button"
                    class="btn btn-secondary dropdown-toggle dropdown-toggle-split"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false">
              <span class="sr-only">Menu d'actions</span>
            </button>
            <div class="dropdown-menu dropdown-menu-right">
              <button class="dropdown-item"
                      type="button"
                      @click="showCloneModal"
              >
                <i class="fas fa-file-export mr-2"></i>
                Dupliquer
              </button>
               <button class="dropdown-item"
                      type="button"
                      @click="showExportModal"
              >
                <i class="fas fa-file-export mr-2"></i>
                Exporter (.zip)
              </button>
              <button class="dropdown-item text-danger"
                      type="button"
                      @click="startControlDeleteFlow"
              >
                <i class="fe fe-trash-2 mr-2"></i>
                Supprimer cet espace...
              </button>
            </div>
          </div>

        </div>

      </div>
    </template>

    <control-delete-flow ref="controlDeleteFlow" :control="control"></control-delete-flow>
    <webdav-tip :control-id="control.id"
                :ref="'webdavTip' + control.id"
                :reference-code="control.reference_code">
    </webdav-tip>

  </div>
</template>

<script>
import { mapState } from 'vuex'
import { mapFields } from 'vuex-map-fields'
import axios from 'axios'
import backendUrls from '../utils/backend'
import Vue from 'vue'
import WebdavTip from '../controls/WebdavTip'
import ControlDeleteFlow from './ControlDeleteFlow'

import ConfirmModal from '../utils/ConfirmModal'
import InfoBar from '../utils/InfoBar'
import ErrorBar from '../utils/ErrorBar'

import JSZip from 'jszip'
import JSZipUtils from 'jszip-utils'
import { saveAs } from 'file-saver'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

export default Vue.extend({
  props: {
    control: Object,
  },
  data: function() {
    return {
      editMode: false,
      title: '',
      organization: '',
      errors: '',
      hasErrors: false,
      referenceError: false,
      reference_code: '',
      allChecked: false,
      checkedQuestionnaires: [],
      users: [],
    }
  },
  computed: {
    ...mapState({
      controls: 'controls',
    }),
    ...mapFields([
      'sessionUser',
    ]),
    accessibleQuestionnaires() {
      return this.control.questionnaires.filter(q => !q.is_draft)
    },
  },
  components: {
    InfoBar,
    ErrorBar,
    WebdavTip,
    ControlDeleteFlow,
    ConfirmModal,
  },
  mounted() {
    this.getUsers()
    this.restoreForm()
  },
  methods: {
    showCloneModal() {
      $(this.$refs.modal.$el).modal('show')
    },
    hideCloneModal() {
      $(this.$refs.modal.$el).modal('hide')
    },
    referenceChanged() {
      this.referenceError = false
    },
    getUsers() {
      axios.get(backendUrls.getUsersInControl(this.control.id))
        .then((response) => {
          this.users = response.data
        })
    },
    cloneControl() {
      // reference code given by user (2021_SOMETHING)
      const newRefCode = new Date().getFullYear() + '_' + this.reference_code

      const valid = this.reference_code &&
                    !this.controls.find(ctrl => ctrl.reference_code === newRefCode)

      if (!valid) {
        this.referenceError = true
        return
      }

      const getCreateMethodCtrl = () => axios.post.bind(this, backendUrls.control())

      if (this.checkedQuestionnaires.length) {
        const questionnaires = this.accessibleQuestionnaires
          .filter(aq => this.checkedQuestionnaires.includes(aq.id))
        const ctrl = {
          title: this.control.title,
          depositing_organization: this.control.depositing_organization,
          reference_code: newRefCode,
          questionnaires: questionnaires,
        }

        getCreateMethodCtrl()(ctrl).then(response => {
          // Copy users for new control
          const controlId = response.data.id

          this.users
            .filter(u => u.profile_type === 'inspector')
            .map(i => {
              const inspector = { ...i, control: controlId }
              axios.post(backendUrls.user(), inspector)
            })

          // Copy questionnaires for new control
          const promises = this.accessibleQuestionnaires
            .filter(aq => this.checkedQuestionnaires.includes(aq.id))
            .map(q => {
              const themes = q.themes.map(t => {
                const qq = t.questions.map(q => { return { description: q.description } })
                return { title: t.title, questions: qq }
              })

              const newQ = { ...q, control: controlId, is_draft: true, id: null, themes: [] }
              return this.cloneQuestionnaire(newQ, themes, q.themes)
            })

          Promise.all(promises)
        })

        this.hideCloneModal()
      }
    },
    async cloneQuestionnaire(questionnaire, themes, oldThemes) {
      const getCreateMethod = () => axios.post.bind(this, backendUrls.questionnaire())
      const getUpdateMethod = (qId) => axios.put.bind(this, backendUrls.questionnaire(qId))

      const promise = await getCreateMethod()(questionnaire).then(async response => {
        const qId = response.data.id
        const newQ = { ...questionnaire, themes: themes }

        await getUpdateMethod(qId)(newQ).then(response => {
          const updatedQ = response.data

          oldThemes.map(t => {
            t.questions.map(q => {
              const qId = updatedQ.themes.find(updatedT => updatedT.order === t.order)
                .questions.find(updatedQ => updatedQ.order === q.order).id

              q.question_files.map(qf => {
                axios.get(qf.url, { responseType: 'blob' }).then(response => {
                  const formData = new FormData()
                  formData.append('file', response.data, qf.basename)
                  formData.append('question', qId)
                  console.log('fileresponse', response.data)
                  axios.post(backendUrls.annexe(), formData, {
                    headers: {
                      'Content-Type': 'multipart/form-data',
                    },
                  })
                })
              })
            })
          })
        })
      })

      return promise
    },
    showExportModal() {
      $(this.$refs.modalexp.$el).modal('show')
    },
    hideExportModal() {
      $(this.$refs.modalexp.$el).modal('hide')
    },
    checkAllQuestionnaires() {
      this.checkedQuestionnaires = []
      this.allChecked = !this.allChecked

      if (this.allChecked) {
        this.accessibleQuestionnaires.map(q => {
          this.checkedQuestionnaires.push(q.id)
        })
      }
    },
    exportControl() {
      if (!this.checkedQuestionnaires.length) return

      const formatFilename = (rf) => {
        const questionnaireNb = String(rf.questionnaireNb).padStart(2, '0')
        const themeId = String(rf.themeId + 1).padStart(2, '0')
        const questionId = String(rf.questionId + 1).padStart(2, '0')
        const filename = `Q${questionnaireNb}-T${themeId}-${questionId}-${rf.basename}`
        return { questionnaireNb, themeId, filename }
      }

      const responseFiles = this.accessibleQuestionnaires
        .filter(aq => this.checkedQuestionnaires.includes(aq.id))
        .flatMap(fq => {
          if (fq.themes) {
            return fq.themes.flatMap(t => {
              if (t.questions) {
                return t.questions.flatMap(q => {
                  return q.response_files.flatMap(rf => {
                    if (rf) {
                      return {
                        questionnaireNb: fq.numbering,
                        themeId: t.order,
                        questionId: q.order,
                        basename: rf.basename,
                        url: rf.url,
                      }
                    }
                  })
                })
              }
            })
          }
        })

      const zipFilename = this.control.reference_code + '.zip'
      const zip = new JSZip()
      let cnt = 0

      responseFiles.map(rf => {
        const url = window.location.origin + rf.url

        JSZipUtils.getBinaryContent(url, (err, data) => {
          if (err) throw err

          const formatted = formatFilename(rf)

          zip.folder(`Q${formatted.questionnaireNb}`)
            .folder(`T${formatted.themeId}`)
            .file(formatted.filename, data, { binary: true })

          cnt++
          if (cnt === responseFiles.length) {
            zip.generateAsync({ type: 'blob' }).then((content) => {
              saveAs(content, zipFilename)
            })
          }
        })
      })

      this.hideExportModal()
    },
    restoreForm() {
      this.title = this.control.title
      this.organization = this.control.depositing_organization
    },
    clearErrors() {
      this.errors = ''
      this.hasErrors = false
    },
    enterEditMode() {
      this.clearErrors()
      this.editMode = true
    },
    quitEditMode() {
      this.clearErrors()
      this.editMode = false
    },
    cancel() {
      this.restoreForm()
      this.quitEditMode()
    },
    updateControl: function() {
      this.clearErrors()
      const payload = {
        title: this.title,
        depositing_organization: this.organization,
      }
      axios.put(backendUrls.control(this.control.id), payload)
        .then(response => {
          console.debug(response)
          this.title = response.data.title
          this.organization = response.data.depositing_organization

          // Display a "loading" spinner on clicked button, while the page reloads, so that they know their click
          // has been registered.
          $('#control-title-submit-button').addClass('btn-loading')
          window.location.reload()
        })
        .catch((error) => {
          console.error(error)
          this.errors = error.response.data
          this.hasErrors = true
        })
    },
    showWebdavTip() {
      this.$refs['webdavTip' + this.control.id].start()
    },
    startControlDeleteFlow() {
      this.$refs.controlDeleteFlow.start()
    },
  },
})

</script>

<style scoped>
  .break-word {
    word-break: break-all;
  }
</style>
