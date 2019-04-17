<template>
    <div>
        {{questionnaire}}
    </div>
</template>

<script>
    import Vue from "vue"

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
        }
    });
</script>

<style>
</style>