from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import re_path
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.validators import validate_email

from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from baseemail.models import EmailTemplate, Country, ObjectVariableMap
from baseemail.forms import CountryModelForm, EmailTemplateModelForm, ObjectVariableMapModelForm
from baseemail.helpers import render_site_with_context, replace_variables, get_template_ovm_fields_json
from baseemail.serializers import EmailTemplateSerializer


class TestTemplateAPIView(RetrieveAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        return render_site_with_context(request)


class TestTemplateWithoutEmailAPIView(CreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, id=None, *args, **kwargs):

        # TODO: get html template from AWS S3
        try:
            email_template = EmailTemplate.objects.get(pk=self.kwargs.get('id'))
            template_string = render_to_string(f'admin/baseemail/emailtemplate/{email_template.template_name}.html')
        except Exception as e:
            print(f'Error: {e} Email Template ID: {self.kwargs.get("id")}')
            return redirect(reverse('admin:test_template'))

        ovm_fields_json = get_template_ovm_fields_json(request, email_template)

        if not ovm_fields_json:
            return redirect(reverse('admin:test_template'))

        return render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })


class TestTemplateWithEmailAPIView(CreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, id=None, *args, **kwargs):
        try:
            validate_email(request.POST['email'])
        except Exception as e:
            messages.error(request, 'Invalid Email.')
            return redirect(reverse('admin:test_template'))

        # TODO: get html template from AWS S3
        try:
            email_template = EmailTemplate.objects.get(pk=self.kwargs.get('id'))
            template_string = render_to_string(f'admin/baseemail/emailtemplate/{email_template.template_name}.html')
        except Exception as e:
            print(f'Error: {e} Email Template ID: {self.kwargs.get("id")}')
            return redirect(reverse('admin:test_template'))

        ovm_fields_json = get_template_ovm_fields_json(request, email_template)

        if ovm_fields_json:
            # TODO: .send_email() will be added
            messages.success(request, "Email successfully sent.")

        return redirect(reverse('admin:test_template'))


class TestTemplateWithDataAPIView(CreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, id=None, *args, **kwargs):
        # TODO: get html template from AWS S3
        try:
            email_template = EmailTemplate.objects.get(pk=self.kwargs.get('id'))
            template_string = render_to_string(f'admin/baseemail/emailtemplate/{email_template.template_name}.html')
        except Exception as e:
            print(f'Error: {e} Email Template ID: {self.kwargs.get("id")}')
            return redirect(reverse('admin:test_template'))

        ovm_fields_json = get_template_ovm_fields_json(request, email_template)

        if not ovm_fields_json:
            return redirect(reverse('admin:test_template'))

        template_string = replace_variables(request, email_template, template_string, ovm_fields_json.get('fields'))

        return render_site_with_context(request, extra_context={
            'email_template': template_string,
            'ovm_fields_list': [ovm_fields_json],
        })


class TestTemplateSelectedWithoutEmailAPIView(CreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        queryset = EmailTemplate.objects.all()

        if not request.POST.get('all'):
            queryset = queryset.filter(pk__in=request.POST.getlist('selected'))

        ovm_fields_list = []
        # TODO: OVM will be removed
        for query in queryset:
            ovm_fields = get_template_ovm_fields_json(request, query)
            ovm_fields_list.append(ovm_fields)

        if not queryset:
            messages.error(request, "You should first select templates to test them.")
            return redirect(reverse('admin:test_template'))

        return render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })


class TestTemplateSelectedWithEmailAPIView(CreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        try:
            validate_email(request.POST['email'])
        except Exception as e:
            messages.error(request, 'Invalid Email.')
            return redirect(reverse('admin:test_template'))

        queryset = EmailTemplate.objects.all()

        if not request.POST.get('all'):
            queryset = queryset.filter(pk__in=request.POST.getlist('selected'))

        if not queryset:
            messages.error(request, "You should first select templates to test them.")
            return redirect(reverse('admin:test_template'))

        ovm_fields_list = []

        for query in queryset:
            ovm_fields = get_template_ovm_fields_json(request, query)
            ovm_fields_list.append(ovm_fields) if ovm_fields is not None else None

        if ovm_fields_list:
            # TODO: .send_email() will be added
            messages.success(request, "Email successfully sent.")

        return redirect(reverse('admin:test_template'))


class TestTemplateSelectedWithDataAPIView(CreateAPIView):
    serializer_class = EmailTemplateSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        queryset = EmailTemplate.objects.all()

        if not request.POST.get('all'):
            queryset = queryset.filter(pk__in=request.POST.getlist('selected'))

        if not queryset:
            messages.error(request, "You should first select templates to test them.")
            return redirect(reverse('admin:test_template'))

        ovm_fields_list = []

        for query in queryset:
            ovm_fields = get_template_ovm_fields_json(request, query)
            if ovm_fields is not None:
                ovm_fields_list.append(ovm_fields)
                template_string = render_to_string(f'admin/baseemail/emailtemplate/{ovm_fields.get("template").template_name}.html')
                replace_variables(request, query, template_string, ovm_fields.get('fields'))

        return render_site_with_context(request, extra_context={
            'ovm_fields_list': ovm_fields_list,
        })


class EmailTemplateModelAdmin(admin.ModelAdmin):
    form = EmailTemplateModelForm

    fieldsets = (
        (None, {
            'fields': (
                'name', 'email_class', 'attachment_type',
            ),
            'classes': ('d-flex', 'flex-wrap', 'column-gap-3',),
        }),
        (None, {
            'fields': ('code', 'country', 'type', 'version', 'active_status',),
            'classes': ('d-flex', 'flex-wrap', 'column-gap-3',),
        }),
        (None, {
            'fields': (
                'template_name', 'subject', 'contents',
                'to_email', 'to_email_function', 'from_email', 'related_model_application', 'related_model_name',
                'additional_parameters',
            ),
            'classes': ('d-flex', 'flex-wrap', 'column-gap-3', ),
        }),
    )

    list_per_page = 25

    search_fields = ('name', 'template_name', 'subject', )

    def get_urls(self):
        url = super().get_urls()
        custom_urls = [
            re_path(
                r'^test_template$',
                TestTemplateAPIView.as_view(),
                name="test_template"
            ),
            re_path(
                r'^test_without_email/(?P<id>\d+)$',
                TestTemplateWithoutEmailAPIView.as_view(),
                name="test_without_email"
            ),
            re_path(
                r'^test_with_email/(?P<id>\d+)$',
                TestTemplateWithEmailAPIView.as_view(),
                name="test_with_email"
            ),
            re_path(
                r'^test_with_data/(?P<id>\d+)$',
                TestTemplateWithDataAPIView.as_view(),
                name="test_with_data"
            ),
            re_path(
                r'^test_selected_without_email$',
                TestTemplateSelectedWithoutEmailAPIView.as_view(),
                name="test_selected_without_email"
            ),
            re_path(
                r'^test_selected_with_email$',
                TestTemplateSelectedWithEmailAPIView.as_view(),
                name="test_selected_with_email"
            ),
            re_path(
                r'^test_selected_with_data$',
                TestTemplateSelectedWithDataAPIView.as_view(),
                name="test_selected_with_data"
            ),
        ]

        return custom_urls + url

    def has_delete_permission(self, request, obj=None):
        return False


# TODO: Will be removed
class CountryModelAdmin(admin.ModelAdmin):
    form = CountryModelForm
    list_per_page = 25
    search_fields = ('name', 'code', )

    def has_delete_permission(self, request, obj=None):
        return False


# TODO: Will be removed
class ObjectVariableMapModelAdmin(admin.ModelAdmin):
    form = ObjectVariableMapModelForm
    list_per_page = 25
    search_fields = ('app_label', 'model_name', )

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(EmailTemplate, EmailTemplateModelAdmin)
admin.site.register(Country, CountryModelAdmin)
admin.site.register(ObjectVariableMap, ObjectVariableMapModelAdmin)
