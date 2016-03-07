from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def sessionid(context):
    return context['request'].session.get_session_key()
