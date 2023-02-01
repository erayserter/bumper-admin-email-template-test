from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import format_html
from django.urls import reverse

import json

from baseemail.models import EmailTemplate, Country, ObjectVariableMap
from baseemail.forms import CountryModelForm, EmailTemplateModelForm, ObjectVariableMapModelForm, EmailActionForm


class EmailTemplateModelAdmin(admin.ModelAdmin):
    form = EmailTemplateModelForm
    action_form = EmailActionForm

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

    list_display = (
        'id', 'name', 'template_name', 'email_class', 'subject', 'contents', 'variables', 'row_variables',
        'to_email', 'to_email_function', 'from_email', 'related_model_application', 'related_model_name',
        'attachment_type', 'additional_parameters', 'test_email_buttons',
    )

    list_per_page = 25

    actions = (
        'action',
    )

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
        email_template = EmailTemplate.objects.get(pk=template_id)

        # email_template_content = {
        #     "forename": "Mehmet Eray Serter",
        #     "card last 4": "0456",
        #     "amount": "1000",
        #     "date": "05/02/2023",
        #     "companyname": "Bumper",
        # }

        test_params = {
            1: ["Mark", "Otto", "@mdo"],
            2: ["Mark", "Otto", "@mdo"],
            3: ["Mark", "Otto", "@mdo"],
        }

        param_list = [
            "ID",
            "First",
            "Last",
            "Handle"
        ]

        template_string = render_to_string("admin/baseemail/EmailTemplate/emailtemplate.html")

        template_string = template_string.replace("*|FORENAME|*", "Mehmet Eray Serter")
        template_string = template_string.replace("*|CARD LAST 4|*", "0456")
        template_string = template_string.replace("*|AMOUNT|*", "1000")
        template_string = template_string.replace("*|DATE|*", "05/02/2023")
        template_string = template_string.replace("*|COMPANYNAME|*", "Bumper")

        # for variable in email_template_content:
        #     template_string = template_string.replace(f'*|{variable.upper()}|*', email_template_content[variable])

        return super().changelist_view(request, extra_context={
            'email_template': template_string,
            'test_params': test_params,
            'param_list': param_list,
        })

    def test_with_email_view(self, request, template_id):
        pass

    def test_with_real_data_view(self, request, template_id):
        pass

    def test_selected_without_email_view(self, request):
        # queryset = EmailTemplate.objects.filter(pk__in=request.POST['_selected_action'])
        # print(queryset)
        return super().changelist_view(request)

    def test_selected_with_email_view(self, request):
        # queryset = EmailTemplate.objects.filter(pk__in=request.POST['_selected_action'])
        # print(queryset)
        return super().changelist_view(request)

    def test_selected_with_real_data_view(self, request):
        # queryset = EmailTemplate.objects.filter(pk__in=request.POST['_selected_action'])
        # print(queryset)
        return super().changelist_view(request)










    def action(self, request, queryset):
        pass

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
