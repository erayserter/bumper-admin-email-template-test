from django import forms
from django.contrib.admin.helpers import ActionForm
from django.contrib.admin.widgets import AdminTextareaWidget

from baseemail.constants import EMAIL_CODES, EMAIL_TYPES

from baseemail.models import Country, EmailTemplate, ObjectVariableMap


class EmailActionForm(ActionForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email-action',
    }), required=False)


class CountryModelForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class EmailTemplateModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailTemplateModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == AdminTextareaWidget:
                field.widget = forms.TextInput(attrs={
                    'class': "email-template-text-input",
                })

    class Meta:
        model = EmailTemplate
        fields = [
            'name', 'template_name', 'email_class', 'subject', 'contents', 'variables', 'row_variables', 'to_email',
            'to_email_function', 'from_email', 'related_model_application', 'related_model_name', 'attachment_type',
            'additional_parameters', 'code', 'country', 'type', 'version', 'active_status', ]

        # widgets = {
        #     'template_name': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'subject': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'contents': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'variables': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'row_variables': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'to_email': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'to_email_function': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'from_email': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'related_model_application': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'related_model_name': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        #     'additional_parameters': forms.TextInput(attrs={
        #         'class': "email-template-text-input",
        #     }),
        # }


class ObjectVariableMapModelForm(forms.ModelForm):
    class Meta:
        model = ObjectVariableMap
        fields = '__all__'
