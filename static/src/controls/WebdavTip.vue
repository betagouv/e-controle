<template>
  <collapsible-section buttonicon="fe-folder" buttontext="Comment voir les réponses dans l’Explorateur Windows ?">
    <info-bar noclose="true">
      <p>
        Toutes les réponses déposées sont automatiquement classées et renommées dans un dossier accessible
        à tous les membres de l’équipe de contrôle.
        Pour les consulter, veuillez copier puis coller ce lien dans votre barre de navigation
        et épinglez-le dans vos accès rapide.
      </p>

      <div class="flex-row mb-4">
        <span>{{ webdavurl}}</span>
        <button class="btn btn-sm btn-secondary ml-4"
                v-clipboard="webdavurl"
                v-clipboard:success="clipboardSuccessHandler"
                style="position: relative;">
          <i class="fe fe-copy"></i>
          Copier le lien
        </button>
        <transition name="fade" v-on:enter="enterFade">
          <span class="tag tag-success ml-4" v-if="showCopySuccess">C'est copié !</span>
        </transition>
      </div>

      <a target="_blank" href="https://github.com/betagouv/e-controle/raw/develop/docs/guides/e-controle-explorateur-de-fichiers.pdf">
        Besoin d’aide ? Suivez les instructions en images.
      </a>
    </info-bar>

  </collapsible-section>

</template>

<script>
  import Vue from 'vue'
  import Clipboard from 'v-clipboard'
  import CollapsibleSection from '../utils/CollapsibleSection'
  import InfoBar from '../utils/InfoBar'

  Vue.use(Clipboard)

  export default Vue.extend({
    props: [ 'webdavurl' ],
    components: {
      CollapsibleSection,
      InfoBar,
    },
    data: function (){
      return {
        showCopySuccess: false
      }
    },
    methods: {
      clipboardSuccessHandler ({ value, event }) {
        this.showCopySuccess = true
      },

      enterFade: function(el, done) {
        var that = this;
        setTimeout(function() {
          that.showCopySuccess = false;
        }, 3000); // hide the message after 3 seconds
      }

    }
  })
</script>