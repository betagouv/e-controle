<template>
  <div>

    <form @submit.prevent="createBody">
      <fieldset v-for="(group, index) in body" class="form-fieldset" id="'group-' + index">
        <div class="form-group theme">
          <label class="form-label">Thème<span class="form-required"></span></label>
          <input type="text" class="form-control" v-model="body[index].theme">
        </div>
        <div class="form-group questions">
          <div v-for="(question, qIndex) in body[index].questions">
            <label class="form-label">Question {{qIndex + 1}}<span class="form-required"></span></label>
            <input type="text" class="form-control" v-model="body[index].questions[qIndex]">
          </div>
        </div>
        <div @click="addQuestion(index)">
          +
        </div>
      </fieldset>
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

<style></style>
