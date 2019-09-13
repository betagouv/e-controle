<template>
  <confirm-modal :id="id"
                 title="Confirmer la publication"
                 confirm-button="Oui, j'ai compris"
                 cancel-button="Retour"
                 @confirm="$emit('confirm')"
  >
    <p>
      <strong>
      En publiant ce questionnaire, il sera visible par l'organisme interrogé et vous ne pourrez plus le modifier.
      </strong>
    </p>

    <p>
      Pensez à informer l'organisme interrogé que vous
      avez publié ce nouveau questionnaire et qu'il est disponible à cette adresse : https://e-controle-beta.ccomptes.fr
    </p>

    <p>
        Si des réponses sont déposées par l'organisme interrogé, l'équipe de contrôle recevra un email d'information dès le lendemain à huit heures.
    </p>

  </confirm-modal>
</template>

<script>
  import Vue from "vue"
  import ConfirmModal from "../utils/ConfirmModal"

  export default Vue.extend({
    props: [ 'id' ],
    components: {
      ConfirmModal
    },
  })

</script>