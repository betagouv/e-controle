<template>
  <div>
    <form @submit.prevent="createBody">

      <div class="card" v-for="(group, groupIndex) in body">
        <div class="card-status card-status-top bg-blue">
        </div>

        <div class="card-header">
          <label v-bind:for="'theme' + (groupIndex + 1)">
            <h3 class="card-title">{{groupIndex + 1}}.</h3>
          </label>
          <input class="form-control"
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

        <div @click="addQuestion(groupIndex)">
          +
        </div>

      </div>

      <div @click="addGroup()">
        +
      </div>

      <div>
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
