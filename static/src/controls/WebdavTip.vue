<template>
  <div>
    <empty-modal :id="'webdav-tip-modal-' + controlId" class="webdav-tip">
      <div class="modal-header parent-fake-icon">
        <h4 class="modal-title">
          <i class="fe fe-folder mr-4"></i>
          <img :src="'/static/img/file-explorer.png'"
                alt="Explorateur Windows"
                class="title-fake-icon" />
          <span>Comment voir les réponses classées dans l’Explorateur Windows ?</span>
        </h4>
        <button type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close">
        </button>
      </div>

      <div class="modal-body">
        <div class="card">
          <div class="card-body flex-row">
            <div class="flex-column justify-content-around mr-6">
              <p>
                <strong>
                Copiez puis collez ce lien dans la barre de navigation de votre explorateur de
                fichiers windows.
                </strong>
              </p>
              <div>
                <div id="link-text" class="mb-4">{{webdavurl}}</div>
                <div id="copy-success-message-parent">
                  <button class="btn btn-primary"
                          @click="copyLink">
                    <i class="fe fe-copy"></i>
                    Copier le lien
                  </button>
                  <transition name="fade" v-on:enter="enterFade">
                    <div id="copy-success-message" class="tag tag-success" v-if="showCopySuccess">
                      C'est copié !
                    </div>
                  </transition>
                </div>
              </div>
            </div>
            <div class="flex-column">
              <img :src="'/static/img/vpn.png'"
                  class="vpn-img"
                  alt="Je suis bien à mon poste de travail ou sur VPN"/>
            </div>

          </div>
        </div>

        <div class="alert alert-icon alert-primary" role="alert">
          <i class="fe fe-help-circle mr-2" aria-hidden="true"></i>
          <h5 class="mt-1">Besoin d’aide ?</h5>
          <p>
            Toutes les réponses déposées sont automatiquement classées et renommées dans un dossier
            accessible à tous les membres de l’équipe de contrôle.
          </p>
          <div class="flex-row">
            <button id="videoModalButton"
                    type="submit"
                    data-toggle="modal"
                    :data-target="'#file-explorer-video-modal-' + controlId"
                    class="btn btn-primary mr-4"
                    title="Voir les instructions en vidéo">
              <i class="fa fa-play-circle mr-1"></i>
              Suivez les instructions en vidéo
            </button>
            <a target="_blank"
              rel="noopener noreferrer"
              :href="PDF_FILE_URL"
              class="btn btn-primary"
              title="Suivez les instructions en images."
            >
              <i class="fe fe-image mr-1"></i>
              Suivez les instructions en images
            </a>
          </div>
        </div>

      </div>
    </empty-modal>
    <video-modal
      v-if="canDisplayVideoPlayer"
      :id="'file-explorer-video-modal-' + controlId"
      :video-versions="[
        {
          url: videoUrlMp4,
          type: 'video/mp4'
        },
        {
          url: videoUrlWebm,
          type: 'video/webm'
        },
      ]"
    >
    </video-modal>
  </div>
</template>

<script>
import { mapFields } from 'vuex-map-fields'
import EmptyModal from '../utils/EmptyModal'
import { loadStatuses } from '../store'
import VideoModal from '../utils/VideoModal'
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const SUCCESS_MESSAGE_FADE_SECONDS = 5
const VIDEO_FILE_PATH_MP4 = 'videos/file-explorer.mp4'
const VIDEO_FILE_PATH_WEBM = 'videos/file-explorer.webm'
const PDF_FILE_URL = 'https://github.com/betagouv/e-controle/raw/develop/docs/guides/e-controle-explorateur-de-fichiers.pdf'

export default Vue.extend({
  props: {
    referenceCode: String,
    controlId: Number,
  },
  components: {
    EmptyModal,
    VideoModal,
  },
  data: function () {
    return {
      showCopySuccess: false,
      PDF_FILE_URL: PDF_FILE_URL,
    }
  },
  computed: {
    ...mapFields([
      'config',
      'configLoadStatus',
    ]),
    // Wait for the config to load (so that we have the video urls) before displaying the video
    // player. Otherwise it breaks on some browsers and machines.
    canDisplayVideoPlayer() {
      return this.configLoadStatus === loadStatuses.SUCCESS
    },
    webdavurl: function() {
      return this.config.webdav_url + '/' + this.referenceCode
    },
    videoUrlMp4() {
      return this.config.static_files_url + VIDEO_FILE_PATH_MP4
    },
    videoUrlWebm() {
      return this.config.static_files_url + VIDEO_FILE_PATH_WEBM
    },
  },
  methods: {
    // Parent calls this method to show the tip.
    start() {
      $('#webdav-tip-modal-' + this.controlId).modal('show')
    },
    copyLink() {
      const copyElementContents = (el) => {
        if (window.clipboardData) { // IE
          console.debug('Copying for IE, user agent : ', window.navigator.userAgent)
          window.clipboardData.setData('Text', el.innerText)
        } else { // Other browsers
          console.debug('Copying for non-IE browser, user agent : ', window.navigator.userAgent)
          const range = document.createRange()
          range.selectNodeContents(el)
          const sel = window.getSelection()
          sel.removeAllRanges()
          sel.addRange(range)
          document.execCommand('copy')
        }
      }
      const linkEl = document.getElementById('link-text')
      copyElementContents(linkEl)
      this.showCopySuccess = true
    },

    enterFade: function(el, done) {
      setTimeout(() => {
        this.showCopySuccess = false
      }, SUCCESS_MESSAGE_FADE_SECONDS * 1000)
    },

  },
})
</script>

  <style scoped>
    .title-fake-icon {
      position: absolute;
      top: 14px;
      left: 14px;
    }

    #copy-success-message-parent {
      position: relative;
    }
    #copy-success-message {
      position: absolute;
      top: 0.5rem;
      left: 8.5rem;
      z-index: 100;
    }
  </style>

  <style>
    .webdav-tip .modal-dialog {
      max-width: 1000px;
    }

    .webdav-tip .vpn-img {
      max-height: 190px;
    }
  </style>
