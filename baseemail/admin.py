from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import format_html
from django.urls import reverse
from  django.core.exceptions import ObjectDoesNotExist

import json

from baseemail.models import EmailTemplate, Country, ObjectVariableMap
from baseemail.forms import CountryModelForm, EmailTemplateModelForm, ObjectVariableMapModelForm


def replace_variables(html):
    html = html.replace("*|FORENAME|*", "Mehmet Eray Serter")
    html = html.replace("*|CARD LAST 4|*", "0456")
    html = html.replace("*|AMOUNT|*", "1000")
    html = html.replace("*|DATE|*", "05/02/2023")
    return html.replace("*|COMPANYNAME|*", "Bumper")


def get_template_ovm_fields_json(template_id):
    email_template = EmailTemplate.objects.get(pk=template_id)

    try:
        ovm = ObjectVariableMap.objects.get(
            app_label=email_template.related_model_application,
            model_name=email_template.related_model_name
        )
    except ObjectDoesNotExist as e:
        print(f'Error: {e}')
        return None

    return json.loads(ovm.fields.replace("\'", "\""))


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

    actions = ('action', )

    list_display = (
        'select_checkbox', 'id', 'name', 'template_name', 'email_class', 'subject', 'contents', 'variables',
        'row_variables', 'to_email', 'to_email_function', 'from_email', 'related_model_application',
        'related_model_name', 'attachment_type', 'additional_parameters', 'test_email_buttons',
    )

    list_per_page = 25

    search_fields = ('name', )

    def get_urls(self):
        url = super().get_urls()
        custom_urls = [
            path('<int:template_id>/test/', self.test_without_email_view, name="test"),
            path('<int:template_id>/testemail/', self.test_with_email_view, name="test-email"),
            path('<int:template_id>/testdata/', self.test_with_real_data_view, name="test-data"),
            path('testselected/', self.test_selected_without_email_view, name="test-selected"),
            path('testselectedemail/', self.test_selected_with_email_view, name="test-selected-email"),
            path('testselecteddata/', self.test_selected_with_real_data_view, name="test-selected-data"),
        ]

        return custom_urls + url

    def test_without_email_view(self, request, template_id):
        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")
        template_string = replace_variables(template_string)

        ovm_fields_json = get_template_ovm_fields_json(template_id)

        return super().changelist_view(request, extra_context={
            'email_template': template_string,
            'fields_array': [ovm_fields_json],
        })

    def test_with_email_view(self, request, template_id):
        email = request.POST['email']

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")
        template_string = replace_variables(template_string)

        ovm_fields_json = get_template_ovm_fields_json(template_id)

        return super().changelist_view(request, extra_context={
            'email_template': template_string,
            'fields_array': [ovm_fields_json],
        })

    def test_with_real_data_view(self, request, template_id):
        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")
        template_string = replace_variables(template_string)

        ovm_fields_json = get_template_ovm_fields_json(template_id)

        return super().changelist_view(request, extra_context={
            'email_template': template_string,
            'fields_array': [ovm_fields_json],
        })

    def test_selected_without_email_view(self, request):
        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('selected'))
        # queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('_selected_action'))

        fields_array = list(map(lambda query: get_template_ovm_fields_json(query.pk), queryset))

        return super().changelist_view(request, extra_context={
            'fields_array': fields_array,
        })

    def test_selected_with_email_view(self, request):
        email = request.POST['email']
        print(email)

        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('_selected_action'))

        fields_array = list(map(lambda query: get_template_ovm_fields_json(query.pk), queryset))

        return super().changelist_view(request, extra_context={
            'fields_array': fields_array,
        })

    def test_selected_with_real_data_view(self, request):
        queryset = EmailTemplate.objects.filter(pk__in=request.POST.getlist('_selected_action'))

        fields_array = list(map(lambda query: get_template_ovm_fields_json(query.pk), queryset))

        return super().changelist_view(request, extra_context={
            'fields_array': fields_array,
        })

    def action(self):
        pass

    def select_checkbox(self, obj):
        return format_html(
            f'<input type="checkbox" name="selected" value="{obj.pk}">'
        )
    select_checkbox.short_description = "Select"

    def test_email_buttons(self, obj):
        return format_html(
            '<input type="submit" formaction="{}" value="Test Without Email" style="margin:2px;width:100%">'
            '<input type="submit" formaction="{}" value="Test With Email" style="margin:2px;width:100%">'
            '<input type="submit" formaction="{}" value="Test With Real Data" style="margin:2px;width:100%">',
            reverse('admin:test', args=[obj.pk]),
            reverse('admin:test-email', args=[obj.pk]),
            reverse('admin:test-data', args=[obj.pk]),
        )

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
