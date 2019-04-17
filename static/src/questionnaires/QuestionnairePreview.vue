<template>
    <div>
        <questionnaire-detail v-bind:questionnaire="questionnaire">
        </questionnaire-detail>
        <div class="d-flex">
            <a href="javascript:void(0)" @click.prevent="back()" class="btn btn-link">
                Précédent
            </a>
            <button type="submit" class="btn btn-primary ml-auto">
                Enregistrer
            </button>
        </div>
    </div>
</template>

<script>
    import Vue from "vue"
    import QuestionnaireDetail from "./QuestionnaireDetail"

    export default Vue.extend({
        data: function() {
            return {
                questionnaire: {}
            }
        },
        mounted() {
            let updateQuestionnaire = function(data) {
                // Use Vue's $set to make the properties reactive.
                this.$set(this.questionnaire, 'metadata', data.metadata);
                this.$set(this.questionnaire, 'body', data.body);
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
        },
        components: {
            QuestionnaireDetail
        }
    });
</script>

<style>
</style>