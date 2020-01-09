<template>
  <div>
    <div>TODO REMOVE DEBUG OUTPUT</div>
    <div>{{ title }}</div>
    <div>{{ description }}</div>
    <div>{{ end_date }}</div>

    <div class="card">
      <div class="card-header">
        <div class="card-title">Etape 1 : Renseigner l'introduction</div>
      </div>
      <div class="card-body pb-6">
        <form @submit.prevent="next" ref="form">
          <div class="form-group">
            <label class="form-label" id="questionnaireTitle">
              Quel titre souhaitez vous donner au questionnaire n°{{ questionnaireNumbering }} ?
              <span class="form-required">*</span>
            </label>
            <span class="text-muted" id="questionnaireTitleHelp">
              Exemple :
              <strong>"Présentation générale"</strong>
              ou
              <strong>"Suite à la réunion du 7 Mars 2019"</strong>. 255 caractères maximum.
            </span>
            <input type="text"
                   aria-labelledby="questionnaireTitle"
                   aria-describedby="questionnaireTitleHelp"
                   class="form-control"
                   v-model="title"
                   maxlength="255"
                   required>
          </div>
          <div class="form-group">
            <label class="form-label" id="questionnaireDescription">
              Vous pouvez modifier le texte d'introduction du questionnaire n°{{ questionnaireNumbering }}, si vous le souhaitez :
            </label>
            <textarea class="form-control"
                      aria-labelledby="questionnaireDescription"
                      placeholder="Si nécessaire, décrivez votre questionnaire ici"
                      rows="6"
                      v-bind:class="{ 'state-invalid': errors.description }"
                      v-model="description">
            </textarea>
            <p class="text-muted pl-2" v-if="errors.description">
              <i class="fa fa-warning"></i> {{ errors.description.join(' / ')}}
            </p>
          </div>
          <div class="form-group">
            <label class="form-label" id="questionnaireEndDate">Vous pouvez indiquer la date limite de réponse :</label>
            <datepicker class="blue"
                        aria-labelledby="questionnaireEndDate"
                        v-model="end_date"
                        :language="fr"
                        :monday-first="true">
            </datepicker>
          </div>
          <div class="text-right">
            <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">
              <i class="fe fe-save"></i>
              Enregistrer le brouillon
            </button>
            <button type="submit" class="btn btn-secondary">
              Suivant >
            </button>
          </div>
        </form>

      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import Datepicker from 'vuejs-datepicker'
import { mapFields } from 'vuex-map-fields'
import fr from '../utils/vuejs-datepicker-locale-fr'
import reportValidity from 'report-validity'

// eslint-disable-next-line no-multi-str
const DESCRIPTION_DEFAULT = 'À l’occasion de ce contrôle, \
je vous demande de me transmettre des renseignements et des justifications \
sur les points énumérés dans ce questionnaire.\nVous voudrez bien me faire \
parvenir au fur et à mesure votre réponse. \
\nJe reste à votre disposition ainsi qu’à celle de vos \
services pour toute information complémentaire qu’appellerait ce questionnaire.'

const QuestionnaireMetadataCreate = Vue.extend({
  props: {
    questionnaireNumbering: Number,
  },
  data() {
    return {
      errors: [],
      fr: fr, // locale for datepicker
    }
  },
  computed: {
    ...mapFields([
      'currentQuestionnaire.description',
      'currentQuestionnaire.end_date',
      'currentQuestionnaire.title',
    ]),
  },
  methods: {
    validateForm: function() {
      const form = this.$refs.form
      return reportValidity(form)
    },
    next: function () {
      if (!this.validateForm()) {
        return
      }
      this.$emit('next')
    },
    saveDraft(event) {
      console.debug('save draft', event)
      if (!this.validateForm()) {
        return
      }
      this.$emit('save-draft')
    },
  },
  components: {
    Datepicker,
  },
})

QuestionnaireMetadataCreate.DESCRIPTION_DEFAULT = DESCRIPTION_DEFAULT
export default QuestionnaireMetadataCreate

</script>

<style></style>
