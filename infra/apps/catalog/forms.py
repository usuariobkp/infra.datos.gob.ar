# coding=utf-8
from django import forms

from infra.apps.catalog.models import CatalogUpload, DistributionUpload

FORMAT_OPTIONS = [
        ('json', 'JSON'),
        ('xlsx', 'XLSX')
    ]


class CatalogForm(forms.ModelForm):
    class Meta:
        model = CatalogUpload
        fields = ['format', 'file']

    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'class': 'form-control-file',
                                                         'style': 'height: 44px;'}))
    format = forms.CharField(label='Formato', widget=forms.Select(attrs={'class': 'form-control'},
                                                                  choices=FORMAT_OPTIONS))
    url = forms.URLField(required=False,
                         widget=forms.URLInput(
                             attrs={
                                 'placeholder': 'URL',
                                 'class': 'form-control'
                             }))


class DistributionForm(forms.ModelForm):
    class Meta:
        model = DistributionUpload
        fields = ['distribution_identifier', 'file']

    file = forms.FileField(required=False,
                           widget=forms.FileInput(attrs={'class': 'form-control-file',
                                                         'style': 'height: 44px;'}))
    file_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    distribution_identifier = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        node = kwargs.pop('node')
        super(DistributionForm, self).__init__(*args, **kwargs)
        latest = node.get_latest_catalog_upload()
        datasets = [(dataset['identifier'], dataset['title'] + " - " + dataset['identifier'])
                    for dataset in latest.get_datasets()]
        initial_choice = self.instance.dataset_identifier if self.instance.pk else None
        self.fields['dataset_identifier'] = \
            forms.ChoiceField(choices=datasets, initial=initial_choice,
                              widget=forms.Select(attrs={'class': 'form-control'}))

        self.fields['file_name'].initial = self.instance.file_name if self.instance.pk else None
