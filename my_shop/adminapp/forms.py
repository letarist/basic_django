from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from django import forms

class ShopUsersAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'

        def __init__(self, *args, **kwargs):

            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''

                if field_name == 'password':
                    field.widget = forms.HiddenInput()
