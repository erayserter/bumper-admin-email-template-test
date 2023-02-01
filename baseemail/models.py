from django.db import models

from baseemail.constants import EMAIL_CODES, EMAIL_TYPES


class Country(models.Model):
    """Model for Countries"""

    name = models.CharField(max_length=30)
    code = models.CharField(max_length=3)
    currency = models.CharField(max_length=30)
    currency_code = models.CharField(max_length=3)
    currency_symbol = models.CharField(max_length=3)

    @classmethod
    def get_country_from_code(cls, code):
        country = cls.objects.filter(code=code)
        if country.exists():
            return country.latest('id')

        return cls.objects.get(code="GB")

    def __str__(self):
        return f'{self.name} ({self.code})'


class EmailTemplate(models.Model):
    name = models.CharField("Email name", max_length=200)
    template_name = models.TextField(verbose_name="Template Name")
    active_status = models.BooleanField("Active Status", default=False)
    country = models.ForeignKey(Country, related_name='+', null=True, blank=True, on_delete=models.DO_NOTHING)
    email_class = models.CharField(max_length=25, null=True, blank=True)

    subject = models.TextField(blank=True, null=True, verbose_name="Subject")
    contents = models.TextField(blank=True, null=True, verbose_name="Content")
    variables = models.TextField(blank=True, null=True, verbose_name="Merge Variables")
    row_variables = models.TextField(blank=True, null=True, verbose_name="Merge Variables")
    to_email = models.TextField(blank=True, null=True, verbose_name="to_list")
    to_email_function = models.TextField(blank=True, null=True, verbose_name="to_list function")
    from_email = models.TextField(blank=True, null=True, verbose_name="from_list")

    code = models.CharField(max_length=25, choices=EMAIL_CODES)
    type = models.CharField(max_length=25, choices=EMAIL_TYPES, null=True, blank=True)
    related_model_application = models.TextField(blank=True, null=True, verbose_name="related model application")
    related_model_name = models.TextField(blank=True, null=True, verbose_name="related model name")
    attachment_type = models.CharField(verbose_name="attachment type", blank=True, null=True, max_length = 200)
    version = models.IntegerField()
    additional_parameters = models.TextField(blank=True, null=True, verbose_name="Additional parameters")

    def __str__(self):
        return f'{self.name}'


class ObjectVariableMap(models.Model):
    app_label = models.TextField(blank=True, null=True, verbose_name="App Label")
    model_name = models.TextField(blank=True, null=True, verbose_name="Model")
    fields = models.TextField(blank=True, null=True, verbose_name="Fields")

    def __str__(self):
        return f'{self.app_label}_{self.model_name}'
