from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_questionnaires(context, control):
    user = context['request'].user
    questionnaires = control.questionnaires.all()
    if user.profile.is_audited:
        questionnaires = questionnaires.filter(is_draft=False)
    return questionnaires
