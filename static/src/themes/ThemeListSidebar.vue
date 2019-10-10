<template>
  <div id="sidebar" class="col-lg-4">
    <div class="row sticky">
      <div class="col-md-6 col-lg-12">
        <div class="card">
          <div class="card-header bg-blue text-white">
            <h4 class="card-title">Thèmes</h4>
          </div>
          <table class="table card-table">
            <tbody>
            <tr v-for="(theme, themeIndex) in themes">
              <td>
                <a v-bind:href="'#theme' + (themeIndex + 1)">
                  {{ themeIndex + 1 }}. {{ theme.title }}
                </a>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import Vue from 'vue'

  export default Vue.extend({
    props: [
      'themes',
    ],
  })
</script>