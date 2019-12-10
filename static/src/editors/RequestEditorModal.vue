<template>
    <div class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog large-modal" role="document">
        <div class="modal-content">
          <div class="modal-header border-bottom-0">
            <i class="fa fa-share mr-2 mt-2"></i>
            <div class="modal-title">
            <h3 class="modal-title">Demander les droits de rédaction du questionnaire</h3>
            </div>
            <button type="button"
                    class="close"
                    data-dismiss="modal"
                    aria-label="Close">
            </button>
          </div>

          <div class="modal-body">
            <div class="ml-6">
              Pour modifier ce questionnaire, votre collègue doit vous transférer les droits.
              <br/>Nous vous recommandons donc de contacter directement
              <strong>{{ questionnaire.editor.first_name }} {{ questionnaire.editor.last_name }}</strong>
              - <a href="mailto:demo@demo.com">utilisateur@demo.com</a>.
            </div>

            <div calss="card">
              <div class="card-body alert alert-info" role="alert">
                <div class="mb-4">
                  <h4><i class="fe fe-help-circle mr-1"></i>Votre collègue n'est pas disponible ?</h4>
                  Vous pouvez forcer le transfert des droits.
                  <br />
                  <strong>Attention, dans ce cas toute modification non enregistrée par votre collègue sera perdue.
                </div>
                <button type="submit"
                  class="btn btn-primary"
                  title="Contacter le support e-contrôle">
                  <i class="fe fe-mail mr-1"></i>
                  Contacter le support e.contrôle
                </button>
                <button type="submit"
                  class="btn btn-secondary ml-2"
                  title="Forcer le transfert des droits"
                  data-toggle="modal"
                  data-target="#becomeEditorModal"
                  @click="clickBecomeEditor()">
                  <i class="fa fa-share mr-1"></i>
                  Forcer le transfert des droits
                </button>
              </div>
            </div>

          </div>

          </div>
      </div>
    </div>
</template>

<script>
  import Vue from "vue";


  export default Vue.extend({
    props: [ 'questionnaire'],
    methods: {
      clickBecomeEditor() {
        console.log("becoming....")
        $("#requestEditorModal").modal('hide')
      },
    },
  });
</script>
<style scoped>
  .large-modal {
      width: 1000px;
      max-width: 100%;
      margin: 2% auto;
  }
</style>
