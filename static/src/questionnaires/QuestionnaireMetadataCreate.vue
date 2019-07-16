<template>
  <div class="card">
    <div class="card-header">
      <div class="card-title">Etape 1 : Renseigner l'introduction</div>
    </div>
    <div class="card-body">
      <form @submit.prevent="createMetadata">
        <div class="form-group">
          <label class="form-label" id="questionnaireTitle">Quel titre souhaitez vous donner au questionnaire n°{{ questionnaireNumbering }} ?</label>
          <span class="text-muted" id="questionnaireTitleHelp">
            Exemple :
            <strong>"Présentation générale"</strong>
            ou
            <strong>"Suite à la réunion du 7 Mars 2019"</strong>
          </span>
          <input type="text"
                 aria-labelledby="questionnaireTitle"
                 aria-describedby="questionnaireTitleHelp"
                 class="form-control"
                 v-model="metadata.title"
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
                    v-model="metadata.description">
          </textarea>
          <p class="text-muted pl-2" v-if="errors.description">
            <i class="fa fa-warning"></i> {{ errors.description.join(' / ')}}
          </p>
        </div>
        <div class="form-group">
          <label class="form-label" id="questionnaireEndDate">Vous pouvez indiquer la date limite de réponse :</label>
          <datepicker class="blue"
                      aria-labelledby="questionnaireEndDate"
                      v-model="metadata.end_date"
                      :language="fr"
                      :monday-first="true">
          </datepicker>
        </div>
        <div class="text-right">
          <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">Enregistrer le brouillon</button>
          <button type="submit" class="btn btn-secondary">Suivant ></button>
        </div>
      </form>

    </div>
  </div>
</template>

<script>
  import Vue from "vue";
  import Datepicker from 'vuejs-datepicker';
  import fr from "../utils/vuejs-datepicker-locale-fr"
  import reportValidity from 'report-validity';


  let DESCRIPTION_DEFAULT = "À l’occasion de ce contrôle, \
je vous demande de me transmettre des renseignements et des justifications \
sur les points énumérés dans ce questionnaire.\nVous voudrez bien me faire \
parvenir au fur et à mesure votre réponse. \
\nJe reste à votre disposition ainsi qu’à celle de vos \
services pour toute information complémentaire qu’appellerait ce questionnaire.";

  export default Vue.extend({
    props: {
      questionnaireNumbering: Number
    },
    data() {
      return {
        metadata: {
            'description': DESCRIPTION_DEFAULT,
            'end_date': '',
            'title': ''
        },
        'errors': [],
        'fr': fr // locale for datepicker
      }
    },
    mounted() {
      let loadMetadata = function(data) {
        // Use Vue's $set to make the properties reactive.
        for (const key of Object.keys(this.metadata)) {
          console.debug('key', key)
          this.$set(this.metadata, key, data[key])
        }
      }.bind(this);

      this.$parent.$on('questionnaire-loaded', function(data) {
        console.debug('new metadata', data);
        loadMetadata(data);
      });
    },
    methods: {
      createMetadata: function (event) {
        console.debug('event', event)
        console.debug('metadata created', this.metadata)
        this.$emit('metadata-created', this.metadata)
      },
      saveDraft(event) {
        console.debug('save draft', event)
        let isValid = reportValidity(event.target.form)
        if (!isValid) {
          return
        }
        this.$emit('save-draft', this.metadata)
      },
    },
    components: {
      Datepicker
    }
  });
</script>

<style></style>
