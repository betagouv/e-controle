<template>
  <div>
    <form @submit.prevent="createBody">

      <div class="card" v-for="(group, groupIndex) in body">
        <div class="card-status card-status-top bg-blue">
        </div>

        <div class="card-header">
          <label v-bind:for="'theme' + (groupIndex + 1)" class="form-label-h3">
            <h3 class="card-title">{{groupIndex + 1}}.</h3>
          </label>
          <input class="form-control form-control-h3"
                 placeholder="Ecrivez un thème ici"
                 type="text"
                 v-bind:id="'theme' + (groupIndex + 1)"
                 v-model="body[groupIndex].theme">
        </div>

        <div v-for="(question, qIndex) in body[groupIndex].questions"
             class="card card-collapsed  border-0 m-0 p-0 pb-0 pt-2 {% cycle '' 'zebra' %}">
          <div class="card-header border-1" data-toggle="card-collapse" >
            <label v-bind:for="'question' + (groupIndex + 1) + '.' + (qIndex + 1)">
              <span class="stamp stamp-md bg-blue mr-3" style="cursor: pointer">
                {{ groupIndex + 1 }}.{{ qIndex + 1 }}
              </span>
            </label>
            <textarea class="form-control"
                      placeholder="Ecrivez une question ici"
                      rows="4"
                      v-bind:id="'question' + (groupIndex + 1) + '.' + (qIndex + 1)"
                      v-model="body[groupIndex].questions[qIndex]">
            </textarea>
          </div>
        </div>

        <div class="card-footer text-right">
          <a href="javascript:void(0)" @click.prevent="addQuestion(groupIndex)" class="btn btn-primary">
            <i class="fe fe-plus"></i>Ajouter une question
          </a>
        </div>

      </div>

      <div class="card">
        <div class="card-footer text-right">
          <div class="card-status card-status-top bg-blue">
          </div>
          <a href="javascript:void(0)" @click="addGroup()" class="btn btn-primary">
            <i class="fe fe-plus"></i>Ajouter un thème
          </a>
        </div>
      </div>

      <div class="d-flex">
        <a href="javascript:void(0)" @click.prevent="back()" class="btn btn-link">
          Précédent
        </a>
        <button type="submit" class="btn btn-primary ml-auto">
          Prévisualiser
        </button>
      </div>

    </form>

  </div>
</template>

<script>
  import Vue from "vue";

  export default Vue.extend({
    data() {
      return {
        body: [
          {
            theme: "",
            questions: [
                    "",
            ]
          }
        ],
        'errors': [],
      }
    },
    methods: {
      back: function() {
        this.$emit('back');
      },
      createBody: function () {
        console.log('body created sortof')
        console.log(this.body)
        this.$emit('body-created', this.body)
      },
      addQuestion: function (groupIndex) {
        console.log('addQuestion', groupIndex)
        this.body[groupIndex].questions.push("");
      },
      addGroup: function (index) {
        console.log('addGroup', index)
        this.body.push({ theme: "", questions: [""]})
      },
    }
  });
</script>

<style>
</style>
