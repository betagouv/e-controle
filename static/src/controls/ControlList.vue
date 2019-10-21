<template>
  <div id="control-list">
    <div v-if="controls.length === 0" class="card">
      <div class="card-body">
        <span v-if="user.is_inspector">
          Vous n'avez aucun espace de dépôt ouvert.
        </span>
        <span v-else>
          Vous n'avez accès à aucun espace de dépôt. Si vous avez besoin d'un accès, contactez l'équipe de contrôle.
        </span>
      </div>
    </div>

    <template v-else>
      <control-card v-for="control in controls"
                    :key="control.id"
                    :control="control"
                    :user="user"
                    :webdavurl="webdavurl"
      >
      </control-card>
    </template>
  </div>
</template>

<script>
  import ControlCard from './ControlCard'
  import Vue from 'vue'

  // todo display card according to hash

  export default Vue.extend({
    props: [
      'controls',
      'user',
      'webdavurl',
    ],
    components: {
      ControlCard,
    },
  })
</script>