<template>
  <div>

    <form @submit.prevent="createMetadata">
      <div class="card-header">
        <div class="card-options">
          <button type="submit" @click.prevent="saveDraft" class="btn btn-primary">Enregistrer le brouillon</button>
        </div>
      </div>
      <fieldset class="form-fieldset">
        <div class="form-group">
          <label class="form-label">Titre<span class="form-required">*</span></label>
          <input type="text" class="form-control" v-model="metadata.title" required>
        </div>
        <div class="form-group">
          <label class="form-label">
            Description
          </label>
          <textarea class="form-control"
                    placeholder="Si nécessaire, décrivez votre questionnaire ici"
                    rows="4"
                    v-bind:class="{ 'state-invalid': errors.description }"
                    v-model="metadata.description">
          </textarea>
          <p class="text-muted pl-2" v-if="errors.description">
            <i class="fa fa-warning"></i> {{ errors.description.join(' / ')}}
          </p>
        </div>
        <div class="form-group">
          <label class="form-label">Date de réponse souhaitée</label>
          <datepicker class="blue" v-model="metadata.end_date" :language="fr" :monday-first="true">
          </datepicker>
        </div>
      </fieldset>
      <div class="text-right">
        <button type="submit" class="btn btn-primary">Suivant ></button>
      </div>
    </form>

  </div>
</template>

<script>
  import Vue from "vue";
  import Datepicker from 'vuejs-datepicker';
  import {fr} from 'vuejs-datepicker/dist/locale';

  let DESCRIPTION_DEFAULT = "À l’occasion de ce contrôle, \
je vous demande de me transmettre des renseignements et des justifications \
sur les points énumérés dans ce questionnaire. Vous voudrez bien me faire \
parvenir au fur et à mesure votre réponse, au plus tard avant la date \
de réponse indiquée. Je reste à votre disposition ainsi qu’à celle de vos \
services pour toute information complémentaire qu’appellerait ce questionnaire.";

  export default Vue.extend({
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
        if (!event.target.form.reportValidity()) {
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
