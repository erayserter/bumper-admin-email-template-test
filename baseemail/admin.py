from django.contrib import admin, messages
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist

import json

from baseemail.views import \
    TestTemplateAPIView, \
    TestTemplateWithoutEmailAPIView, \
    TestTemplateWithEmailAPIView, \
    TestTemplateWithDataAPIView, \
    TestTemplateSelectedWithoutEmailAPIView, \
    TestTemplateSelectedWithEmailAPIView, \
    TestTemplateSelectedWithDataAPIView

from baseemail.models import EmailTemplate, Country, ObjectVariableMap
from baseemail.forms import CountryModelForm, EmailTemplateModelForm, ObjectVariableMapModelForm


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

    # list_display = (
    #     'id', 'name', 'template_name', 'email_class', 'subject', 'contents', 'variables',
    #     'row_variables', 'to_email', 'to_email_function', 'from_email', 'related_model_application',
    #     'related_model_name', 'attachment_type', 'additional_parameters',
    # )

    list_per_page = 25

    search_fields = ('name', )

    def get_urls(self):
        url = super().get_urls()
        custom_urls = [
            path('test-template/', TestTemplateAPIView.as_view(), name="test-template"),
            path('test-template/<int:template_id>/test/', TestTemplateWithoutEmailAPIView.as_view(), name="test-template-test"),
            path('test-template/<int:template_id>/testemail/', TestTemplateWithEmailAPIView.as_view(), name="test-template-email-test"),
            path('test-template/<int:template_id>/testdata/', TestTemplateWithDataAPIView.as_view(), name="test-template-data-test"),
            path('test-template/test-selected/', TestTemplateSelectedWithoutEmailAPIView.as_view(), name="test-template-selected-test"),
            path('test-template/test-selected-email/', TestTemplateSelectedWithEmailAPIView.as_view(), name="test-template-selected-email-test"),
            path('test-template/test-selected-data/', TestTemplateSelectedWithDataAPIView.as_view(), name="test-template-selected-data-test"),
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
