# coding=utf-8
from django import forms

from infra.apps.catalog.models import CatalogUpload

FORMAT_OPTIONS = [
        ('json', 'JSON'),
        ('xlsx', 'XLSX')
    ]


class CatalogForm(forms.ModelForm):
    class Meta:
        model = CatalogUpload
        fields = ['format', 'file', 'node']

    file = forms.FileField(required=False)
    format = forms.CharField(label='Formato', widget=forms.Select(choices=FORMAT_OPTIONS))
    url = forms.URLField(required=False)


class DistributionForm(forms.Form):

    file = forms.FileField(required=False)
    url = forms.URLField(required=False)

    def __init__(self, node):
        super(DistributionForm, self).__init__()
        latest = node.get_latest_catalog_upload()
        datasets = [(x['identifier'], x['identifier']) for x in latest.get_datasets()]
        self.fields['dataset'] = forms.ChoiceField(choices=datasets)
