from django.core.validators import MinValueValidator
from django import forms

from core.services import valid_url_extension, valid_url_mimetype
from core.models import Image


class AddImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    url = forms.URLField(required=False, label='Ссылка')

    def clean(self):
        url = self.cleaned_data.get('url')
        image = self.cleaned_data.get('image')
        if not url and not image:
            raise forms.ValidationError('Заполните одно из полей')
        if url and image:
            raise forms.ValidationError('Выберите что-то одно')
        return self.cleaned_data

    def clean_url(self):
        url = self.cleaned_data['url']
        if not valid_url_extension(url.lower()) and url != '':
            raise forms.ValidationError(
                'Не действительное изображение. URL должен иметь расширение изображения (.jpg/.jpeg/.png/.gif)'
            )
        if not valid_url_mimetype(url) and url != '':
            raise forms.ValidationError('Не действительное изображение')
        return url

    class Meta:
        model = Image
        fields = ('url', 'image')
        labels = {'image': 'Файл'}


class ResizeImageForm(forms.Form):
    width = forms.IntegerField(required=False, validators=[MinValueValidator(1)], label='Ширина')
    height = forms.IntegerField(required=False, validators=[MinValueValidator(1)], label='Высота')

    def clean(self):
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')
        if not width and not height:
            raise forms.ValidationError('Заполните одно из полей')
        return self.cleaned_data
