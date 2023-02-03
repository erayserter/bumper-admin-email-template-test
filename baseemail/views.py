from django.contrib import messages
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from rest_framework.views import APIView

from baseemail.models import EmailTemplate, ObjectVariableMap


import json


def replace_variables(html):
    html = html.replace("*|FORENAME|*", "Mehmet Eray Serter")
    html = html.replace("*|CARD LAST 4|*", "0456")
    html = html.replace("*|AMOUNT|*", "1000")
    html = html.replace("*|DATE|*", "05/02/2023")
    return html.replace("*|COMPANYNAME|*", "Bumper")


def get_template_ovm_fields_json(email_template):
    try:
        ovm = ObjectVariableMap.objects.get(
            app_label=email_template.related_model_application,
            model_name=email_template.related_model_name
        )
    except ObjectDoesNotExist as e:
        print(f'Error: {e} Email Template pk: {email_template.pk}')
        return None

    return json.loads(ovm.fields.replace("\'", "\""))


class TestTemplateAPIView(APIView):
    def get(self, request):

        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        email_templates = EmailTemplate.objects.all()
        templates_field_values = email_templates.values_list(*(value_fields))

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context={
            'email_templates': email_templates,
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        })


class TestTemplateWithoutEmailAPIView(APIView):
    def render_site_with_context(self, request, extra_context=None):
        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        templates = EmailTemplate.objects.all()
        templates_field_values = templates.values_list(*(value_fields))

        context = {
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        }

        context.update(extra_context)

        print(context['ovm_fields_list'])

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context=context)

    def post(self, request, template_id):
        email_template = EmailTemplate.objects.get(pk=template_id)

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")
        template_string = replace_variables(template_string)

        ovm_fields_json = get_template_ovm_fields_json(email_template)

        # if ovm_fields_json is None:
        #     messages.error(request, "This template does not matched with an ovm.")
        #     return super().changelist_view(request)

        return self.render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })

    def get(self, request):
        return self.render_site_with_context(request)


class TestTemplateWithEmailAPIView(APIView):
    def render_site_with_context(self, request, extra_context=None):
        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        templates = EmailTemplate.objects.all()
        templates_field_values = templates.values_list(*(value_fields))

        context = {
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        }

        context.update(extra_context)

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context=context)

    def post(self, request, template_id):
        email = request.POST['email']
        print(email)

        email_template = EmailTemplate.objects.get(pk=template_id)

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")
        template_string = replace_variables(template_string)

        ovm_fields_json = get_template_ovm_fields_json(email_template)

        # if ovm_fields_json is None:
        #     messages.error(request, "This template does not matched with an ovm.")
        #     return super().changelist_view(request)

        return self.render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })


class TestTemplateWithDataAPIView(APIView):
    def render_site_with_context(self, request, extra_context=None):
        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        templates = EmailTemplate.objects.all()
        templates_field_values = templates.values_list(*(value_fields))

        context = {
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        }

        context.update(extra_context)

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context=context)

    def post(self, request, template_id):
        email_template = EmailTemplate.objects.get(pk=template_id)

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")
        template_string = replace_variables(template_string)

        ovm_fields_json = get_template_ovm_fields_json(email_template)

        # if ovm_fields_json is None:
        #     messages.error(request, "This template does not matched with an ovm.")
        #     return super().changelist_view(request)

        return self.render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })


class TestTemplateSelectedWithoutEmailAPIView(APIView):
    def render_site_with_context(self, request, extra_context=None):
        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        templates = EmailTemplate.objects.all()
        templates_field_values = templates.values_list(*(value_fields))

        context = {
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        }

        context.update(extra_context)

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context=context)

    def post(self, request):
        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = list(map(lambda query: get_template_ovm_fields_json(query), queryset))

        return self.render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })

    def get(self, request):
        return self.render_site_with_context(request)


class TestTemplateSelectedWithEmailAPIView(APIView):
    def render_site_with_context(self, request, extra_context=None):
        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        templates = EmailTemplate.objects.all()
        templates_field_values = templates.values_list(*(value_fields))

        context = {
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        }

        context.update(extra_context)

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context=context)

    def post(self, request):
        email = request.POST['email']
        print(email)

        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = list(map(lambda query: get_template_ovm_fields_json(query), queryset))

        return self.render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })


class TestTemplateSelectedWithDataAPIView(APIView):
    def render_site_with_context(self, request, extra_context=None):
        all_fields = EmailTemplate._meta.get_fields()
        value_fields = [f.name for f in all_fields]
        templates = EmailTemplate.objects.all()
        templates_field_values = templates.values_list(*(value_fields))

        context = {
            'templates_field_values': templates_field_values,
            'fields': all_fields,
        }

        context.update(extra_context)

        return render(request, 'admin/baseemail/TestTemplate/test_template.html', context=context)

    def post(self, request):
        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = list(map(lambda query: get_template_ovm_fields_json(query), queryset))

        return self.render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })
