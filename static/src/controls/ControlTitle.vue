<template>
  <div class="card">
    <div class="card-status card-status-top bg-blue"></div>
    <template v-if="editMode">
      <div class="card-body">
        <error-bar v-if="hasErrors">
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
            <a href="javascript:void(0)"
               @click="cancel"
               class="btn btn-secondary">
              Annuler
            </a>
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
            <a class="btn btn-secondary btn-fake-icon"
               @click="showWebdavTip">
              <i class="fe fe-folder mr-2"></i>
              <img :src="'/static/img/file-explorer.png'"
                   alt="Explorateur Windows"
                   class="fake-icon" />
              Comment voir les réponses ?
            </a>
          </div>
          <a href="javascript:void(0)"
             class="btn btn-secondary"
             title="Modifier l'espace de dépôt"
             @click="enterEditMode"
          >
            <i class="fe fe-edit mr-2"></i>
            Modifier
          </a>
        </div>

      </div>
    </template>

    <webdav-tip :id="'webdav-tip-' + control.id"
                :webdavurl="webdavurl + '/' + control.reference_code">
    </webdav-tip>

  </div>
</template>

<script>
import { mapFields } from 'vuex-map-fields'
import axios from 'axios'
import backendUrls from '../utils/backend'
import Vue from 'vue'
import WebdavTip from '../controls/WebdavTip'

import ErrorBar from '../utils/ErrorBar'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

export default Vue.extend({
  props: {
    control: Object,
    webdavurl: String,
  },
  data: function() {
    return {
      editMode: false,
      title: '',
      organization: '',
      errors: '',
      hasErrors: false,
    }
  },
  computed: {
    ...mapFields([
      'sessionUser',
    ]),
  },
  components: {
    ErrorBar,
    WebdavTip,
  },
  mounted() {
    this.restoreForm()
  },
  methods: {
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
      $('#webdav-tip-' + this.control.id).modal('show')
    },
  },
})

</script>

<style scoped>
  .btn-fake-icon {
    position: relative;
  }
  .fake-icon {
    position: absolute;
    top: 2px;
    left: 5px;
  }

  .break-word {
    word-break: break-all;
  }
</style>
