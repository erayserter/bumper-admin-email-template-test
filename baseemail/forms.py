from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget

from baseemail.models import Country, EmailTemplate, ObjectVariableMap


class CountryModelForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class EmailTemplateModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmailTemplateModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.__class__ == AdminTextareaWidget:
                field.widget.attrs.update({'class': 'email-template-textarea'})

    class Meta:
        model = EmailTemplate
        exclude = ('id', )


class ObjectVariableMapModelForm(forms.ModelForm):
    class Meta:
        model = ObjectVariableMap
        fields = '__all__'
