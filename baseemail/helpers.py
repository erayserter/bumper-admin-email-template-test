import ast

from django.contrib import messages
from django.shortcuts import render

from baseemail.models import ObjectVariableMap, EmailTemplate

import re


def replace_variables(request, email_template, html, merge_variables):
    for var in merge_variables:
        if merge_variables[var] is not None:
            html = html.replace(f'*|{var}|*', merge_variables[var])

    # Email template variable regex like *|DEALERSHIP|*. Finds all not replaced variable names.
    not_found_list = re.findall(r'\*\|(.+?)\|\*', html)

    if not_found_list:
        messages.warning(request, f'{email_template.template_name.upper()}: {not_found_list} variable(s) not found in merge variables')

    return html


def get_template_ovm_fields_json(request, email_template):
    try:
        ovm = ObjectVariableMap.objects.get(
            app_label=email_template.related_model_application,
            model_name=email_template.related_model_name
        )
    except Exception as e:
        messages.error(request, f"{email_template.template_name} does not matched with an ovm.")
        return None

    fields_json_format = ast.literal_eval(ovm.fields)

    for field in fields_json_format:
        if fields_json_format[field].strip() == "":
            fields_json_format[field] = None

    return {
        'template': email_template,
        'fields': fields_json_format,
    }


def render_site_with_context(request, extra_context=None):
    context = {
        'email_template_objs': EmailTemplate.objects.all(),
    }

    if extra_context:
        context.update(extra_context)

    return render(request, 'admin/baseemail/testtemplate/test_template.html', context=context)
