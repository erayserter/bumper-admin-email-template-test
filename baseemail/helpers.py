import ast

from django.shortcuts import render

from baseemail.models import ObjectVariableMap, EmailTemplate
from baseemail.serializers import EmailTemplateSerializer

import json


def replace_variables(html, merge_variables):
    for var in merge_variables:
        if merge_variables[var] is not None:
            html = html.replace(f'*|{var}|*', merge_variables[var])

    return html


def get_template_ovm_fields_json(email_template):
    try:
        ovm = ObjectVariableMap.objects.get(
            app_label=email_template.related_model_application,
            model_name=email_template.related_model_name
        )
    except Exception as e:
        print(f'Error: {e} Email Template pk: {email_template.pk}')
        return None

    fields_json_format = ast.literal_eval(ovm.fields)

    for field in fields_json_format:
        if fields_json_format[field] == "" or fields_json_format[field].isspace():
            fields_json_format[field] = None

    return {
        'template_name': email_template.name,
        'fields': fields_json_format,
    }


def render_site_with_context(request, extra_context=None):
    all_fields = EmailTemplate._meta.get_fields()
    value_fields = [f.name for f in all_fields]
    email_templates = EmailTemplate.objects.all()

    if request.GET.get('search') is not None:
        email_templates = email_templates.filter(name__icontains=request.GET['search'])

    templates_field_values = email_templates.values_list(*value_fields)

    context = {
        'templates_field_values': templates_field_values,
        'fields': all_fields,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, 'admin/baseemail/testtemplate/test_template.html', context=context)
