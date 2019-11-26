<template>
  <empty-modal class="webdav-tip">
    <div class="modal-header parent-fake-icon">
      <div class="modal-title">
        <i class="fe fe-folder mr-4"></i>
        <img :src="'/static/img/file-explorer.png'" 
              alt="Explorateur Windows"
              class="fake-icon" />
        <span>Comment voir les réponses dans l’Explorateur Windows ?</span>
      </div>
      <button type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close">
      </button>
    </div>

    <div class="modal-body">
      <p>
        Toutes les réponses déposées sont automatiquement classées et renommées dans un dossier accessible
        à tous les membres de l’équipe de contrôle.
        Pour les consulter, veuillez copier puis coller ce lien dans la barre de navigation de votre explorateur de fichiers windows
        et épinglez-le dans vos accès rapide.
      </p>

      <div class="flex-row mb-4">
        <span id="link-text" class="mr-4">{{ webdavurl}}</span>
        <button class="btn btn-sm btn-secondary pr-4"
                @click="copyLink"
                style="position: relative;">
          <i class="fe fe-copy"></i>
          Copier le lien
        </button>
        <transition name="fade" v-on:enter="enterFade">
          <span class="tag tag-success ml-4" v-if="showCopySuccess">C'est copié !</span>
        </transition>
      </div>

      <div class="alert alert-icon alert-primary" role="alert">
        <i class="fe fe-help-circle mr-2" aria-hidden="true"></i> Besoin d’aide ?
        <p class="pt-4">
          <button id="videoModalButton"
                  type="submit"
                  data-toggle="modal"
                  data-target="#fileExplorerVideoModal"
                  class="btn btn-primary"
                  title="Voir les instructions en vidéo">
            <i class="fa fa-play-circle mr-1"></i>
            Suivez les instructions en vidéo
          </button>
        </p>
        <p>
          <a target="_blank" href="https://github.com/betagouv/e-controle/raw/develop/docs/guides/e-controle-explorateur-de-fichiers.pdf"
              class="btn btn-primary"
              title="Suivez les instructions en images."
          >
            <i class="fe fe-image mr-1"></i>
            Suivez les instructions en images
          </a>
        </p>

      </div>
    </div>
  </empty-modal>
</template>

<script>
  import Vue from 'vue'
  import EmptyModal from '../utils/EmptyModal'
  import InfoBar from '../utils/InfoBar'

  export default Vue.extend({
    props: [ 'webdavurl' ],
    components: {
      EmptyModal,
      InfoBar,
    },
    data: function (){
      return {
        showCopySuccess: false
      }
    },
    methods: {
      copyLink() {
        const selectElementContents = (el) => {
          var range = document.createRange();
          range.selectNodeContents(el);
          var sel = window.getSelection();
          sel.removeAllRanges();
          sel.addRange(range);
        }
        const linkEl = document.getElementById('link-text')
        selectElementContents(linkEl)
        document.execCommand("copy")
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

<style scoped>
  .parent-fake-icon {
    position: relative;
  }
  .fake-icon {
    position: absolute;
    top: 10px;
    left: 14px;
  }

</style>

<style>
  .webdav-tip .modal-dialog {
    max-width: 800px;
  }
</style>