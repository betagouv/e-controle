<template>
  <div>

    <form @submit.prevent="createMetadata">
      <fieldset class="form-fieldset">
        <div class="form-group">
          <label class="form-label">
            Description<span class="form-required"></span>
          </label>
          <textarea class="form-control"
                    placeholder="Si nécessaire, décrivez votre questionnaire ici"
                    rows="4"
                    v-bind:class="{ 'state-invalid': errors.description }"
                    v-model="metadata.description">
          </textarea>
          <p class="text-muted pl-2" v-if="errors.description"><i class="fa fa-warning"></i> {{ errors.description.join(' / ')}}</p>
        </div>
        <div class="form-group">
          <label class="form-label">Date de transmission du questionnaire<span class="form-required"></span></label>
          <datepicker class="blue" v-model="metadata.sent_date" :language="fr" :monday-first="true">
          </datepicker>
        </div>
        <div class="form-group">
          <label class="form-label">Date de réponse souhaitée<span class="form-required"></span></label>
          <datepicker class="blue" v-model="metadata.end_date" :language="fr" :monday-first="true">
          </datepicker>
        </div>
      </fieldset>
      <div class="text-right">
        <button type="submit" class="btn btn-primary">Suivant</button>
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
            'sent_date': '',
            'end_date': '',
        },
        'errors': [],
        'fr': fr // locale for datepicker
      }
    },
    methods: {
      createMetadata: function () {
        console.log('metadata created sortof')
        console.log(this.metadata)
        this.$emit('metadata-created', this.metadata)
      }
    },
    components: {
      Datepicker
    }
  });
</script>

<style></style>
