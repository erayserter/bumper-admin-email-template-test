from django.contrib.admin.templatetags.admin_modify import InclusionAdminNode, submit_row
from django import template

register = template.Library()


@register.tag(name='custom_submit_row')
def submit_row_tag(parser, token):
    return InclusionAdminNode(
        parser,
        token,
        func=submit_row,
        template_name='baseemail/submit_line.html'
    )
