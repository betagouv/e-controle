<template>
    <div>
        <div class="preview">
            <questionnaire-detail v-bind:questionnaire="questionnaire">
            </questionnaire-detail>
        </div>
        <div class="text-right">
            <a href="javascript:void(0)" @click.prevent="back()" class="btn btn-link">
                < Retour
            </a>
            <button type="submit" @click.prevent="done()" class="btn btn-primary ml-auto">
                Confirmer la création
            </button>
        </div>
    </div>
</template>

<script>
    import axios from "axios"
    import moment from "moment"
    import Vue from "vue"
    import QuestionnaireDetail from "./QuestionnaireDetail"

    const create_questionnaire_url = "/api/questionnaire/"
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

    export default Vue.extend({
        data: function() {
            return {
                questionnaire: {}
            }
        },
        mounted() {
            let updateQuestionnaire = function(data) {
                // Use Vue's $set to make the properties reactive.
                for (const [key, value] of Object.entries(data)) {
                    this.$set(this.questionnaire, key, value)
                }
            }.bind(this);

            this.$parent.$on('questionnaire-updated', function(data) {
                console.log('new questionnaire', data);
                updateQuestionnaire(data);
            });
        },
        methods: {
            back: function() {
                this.$emit('back');
            },
            done: function() {
                if (this.questionnaire.end_date) {
                    this.questionnaire.end_date = moment(String(this.questionnaire.end_date)).format('YYYY-MM-DD')
                }
                console.log('Questionnaire to save : ', this.questionnaire)
                this.createQuestionnaire()
            },
            createQuestionnaire(){
                axios.post(create_questionnaire_url, this.questionnaire)
                    .then(function (response) {
                        console.log(response)
                    }).catch(function(e) {
                        console.log(e)
                    });
            }
        },
        components: {
            QuestionnaireDetail
        }
    });
</script>

<style>
</style>