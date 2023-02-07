from django.contrib import admin, messages
from django.urls import path, re_path
from django.template.loader import render_to_string

from rest_framework.views import APIView

from baseemail.models import EmailTemplate, Country, ObjectVariableMap
from baseemail.forms import CountryModelForm, EmailTemplateModelForm, ObjectVariableMapModelForm
from baseemail.helpers import render_site_with_context, replace_variables, get_template_ovm_fields_json


class TestTemplateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return render_site_with_context(request)


class TestTemplateWithoutEmailAPIView(APIView):
    def post(self, request, template_id):
        try:
            email_template = EmailTemplate.objects.get(pk=template_id)
        except Exception as e:
            print(f'Error: {e} Email Template ID: {template_id}')
            return render_site_with_context(request)

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")

        ovm_fields_json = get_template_ovm_fields_json(email_template)

        if ovm_fields_json is None:
            messages.error(request, "This template does not matched with an ovm.")
            return render_site_with_context(request)

        return render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })

    def get(self, request):
        return render_site_with_context(request)


class TestTemplateWithEmailAPIView(APIView):
    def post(self, request, template_id):
        email = request.POST['email']
        print(email)

        try:
            email_template = EmailTemplate.objects.get(pk=template_id)
        except Exception as e:
            print(f'Error: {e} Email Template ID: {template_id}')
            return render_site_with_context(request)

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")

        ovm_fields_json = get_template_ovm_fields_json(email_template)

        if ovm_fields_json is None:
            messages.error(request, "This template does not matched with an ovm.")
            return render_site_with_context(request)

        return render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })


class TestTemplateWithDataAPIView(APIView):
    def post(self, request, template_id):
        try:
            email_template = EmailTemplate.objects.get(pk=template_id)
        except Exception as e:
            print(f'Error: {e} Email Template ID: {template_id}')
            return render_site_with_context(request)

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")

        ovm_fields_json = get_template_ovm_fields_json(email_template)

        if ovm_fields_json is not None:
            template_string = replace_variables(template_string, ovm_fields_json.get('fields'))
        else:
            messages.error(request, "This template does not matched with an ovm.")
            return render_site_with_context(request)

        return render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })


class TestTemplateSelectedWithoutEmailAPIView(APIView):
    def post(self, request):
        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = []

        for query in queryset:
            ovm_fields = get_template_ovm_fields_json(query)
            if ovm_fields is not None:
                ovm_fields_list.append(ovm_fields)

        if len(queryset) <= 0:
            messages.error(request, "You should first select templates to test them.")
            return render_site_with_context(request)

        if len(ovm_fields_list) <= 0:
            messages.error(request, "Selected templates does not matched with an ovm.")
            return render_site_with_context(request)

        return render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })

    def get(self, request):
        return render_site_with_context(request)


class TestTemplateSelectedWithEmailAPIView(APIView):
    def post(self, request):
        email = request.POST['email']
        print(email)

        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = []

        for query in queryset:
            ovm_fields = get_template_ovm_fields_json(query)
            if ovm_fields is not None:
                ovm_fields_list.append(ovm_fields)

        if len(queryset) <= 0:
            messages.error(request, "You should first select templates to test them.")
            return render_site_with_context(request)

        if len(ovm_fields_list) <= 0:
            messages.error(request, "Selected templates does not matched with an ovm.")
            return render_site_with_context(request)

        return render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })


class TestTemplateSelectedWithDataAPIView(APIView):
    def post(self, request):
        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = []

        for query in queryset:
            ovm_fields = get_template_ovm_fields_json(query)
            if ovm_fields is not None:
                ovm_fields_list.append(ovm_fields)

        if len(queryset) <= 0:
            messages.error(request, "You should first select templates to test them.")
            return render_site_with_context(request)

        if len(ovm_fields_list) <= 0:
            messages.error(request, "Selected templates does not matched with an ovm.")
            return render_site_with_context(request)

        return render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })


class EmailTemplateModelAdmin(admin.ModelAdmin):
    form = EmailTemplateModelForm

    fieldsets = (
        (None, {
            'fields': (
                'name', 'template_name', 'email_class', 'subject', 'contents', 'variables', 'row_variables',
                'to_email', 'to_email_function', 'from_email', 'related_model_application', 'related_model_name',
                'attachment_type', 'additional_parameters',
            ),
            'classes': ('d-flex', 'flex-wrap', 'column-gap-3', ),
        }),
        (None, {
            'fields': ('code', 'country', 'type', 'version', 'active_status', ),
            'classes': ('d-flex', 'flex-wrap', 'column-gap-3', ),
        }),
    )

    list_per_page = 25

    search_fields = ('name', )

    def get_urls(self):
        url = super().get_urls()
        custom_urls = [
            path(
                r'test-template/',
                TestTemplateAPIView.as_view(),
                name="test-template"
            ),
            re_path(
                r'^test-template/(?P<template_id>\d+)/test/$',
                TestTemplateWithoutEmailAPIView.as_view(),
                name="test-template-test"
            ),
            re_path(
                r'^test-template/(?P<template_id>\d+)/testemail/$',
                TestTemplateWithEmailAPIView.as_view(),
                name="test-template-email-test"
            ),
            re_path(
                r'^test-template/(?P<template_id>\d+)/testdata/$',
                TestTemplateWithDataAPIView.as_view(),
                name="test-template-data-test"
            ),
            path(
                'test-template/test-selected/',
                TestTemplateSelectedWithoutEmailAPIView.as_view(),
                name="test-template-selected-test"
            ),
            path(
                'test-template/test-selected-email/',
                TestTemplateSelectedWithEmailAPIView.as_view(),
                name="test-template-selected-email-test"
            ),
            path(
                'test-template/test-selected-data/',
                TestTemplateSelectedWithDataAPIView.as_view(),
                name="test-template-selected-data-test"
            ),
        ]

        return custom_urls + url

    def has_delete_permission(self, request, obj=None):
        return False


class CountryModelAdmin(admin.ModelAdmin):
    form = CountryModelForm
    list_per_page = 25
    search_fields = ('name', 'code', )

    def has_delete_permission(self, request, obj=None):
        return False


class ObjectVariableMapModelAdmin(admin.ModelAdmin):
    form = ObjectVariableMapModelForm
    list_per_page = 25
    search_fields = ('app_label', 'model_name', )

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(EmailTemplate, EmailTemplateModelAdmin)
admin.site.register(Country, CountryModelAdmin)
admin.site.register(ObjectVariableMap, ObjectVariableMapModelAdmin)
