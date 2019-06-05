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
    import Vue from "vue"
    import QuestionnaireDetail from "./QuestionnaireDetail"

    export default Vue.extend({
        data: function() {
            return {
                questionnaire: {},
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
                this.$emit('back')
            },
            done: function() {
                this.$emit('save-questionnaire')
            },
        },
        components: {
            QuestionnaireDetail
        }
    });
</script>

<style>
</style>