from django.contrib.auth.forms import AuthenticationForm


class StyledFormMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Добавьте свои стили или изменения здесь
        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['password'].widget.attrs.update({'class': 'form-control'})
        return form
