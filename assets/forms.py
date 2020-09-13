from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div
from django.forms import forms, ModelForm
from django.urls import reverse

from assets.models import MediaType


class MediaTypeForm(ModelForm):
    class Meta:
        model = MediaType
        fields = ('name','type_code','notes','parent_type','file_extension','pattern')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.add_input(
                Submit('submit', 'Submit', css_class='btn-default '))
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('media_types_create')
