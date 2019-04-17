<template>
  <div>

    <form @submit.prevent="createMetadata">
      <fieldset class="form-fieldset">
        <div class="form-group">
          <label class="form-label">Date de transmission du questionnaire<span class="form-required"></span></label>
          <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.sent_date }" v-model="metadata.sent_date">
          <p class="text-muted pl-2" v-if="errors.sent_date"><i class="fa fa-warning"></i> {{ errors.sent_date.join(' / ')}}</p>
        </div>
        <div class="form-group">
          <label class="form-label">Date de réponse souhaitée<span class="form-required"></span></label>
          <input type="text" class="form-control" v-bind:class="{ 'state-invalid': errors.end_date }" v-model="metadata.end_date">
          <p class="text-muted pl-2" v-if="errors.end_date"><i class="fa fa-warning"></i> {{ errors.end_date.join(' / ')}}</p>
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

  export default Vue.extend({
    data() {
      return {
        metadata: {
            'sent_date': '',
            'end_date': '',
        },
        'errors': [],
      }
    },
    methods: {
      createMetadata: function () {
        console.log('metadata created sortof')
        console.log(this.metadata)
        this.$emit('metadata-created', this.metadata)
      }
    }
  });
</script>

<style></style>
