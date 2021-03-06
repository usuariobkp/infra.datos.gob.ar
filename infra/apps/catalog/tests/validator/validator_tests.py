# coding=utf-8

import pytest
from django.core.exceptions import ValidationError
from requests import RequestException

from infra.apps.catalog.tests.helpers.open_catalog import open_catalog
from infra.apps.catalog.helpers.temp_uploaded_file import temp_uploaded_file
from infra.apps.catalog.validator.catalog_data_validator import CatalogDataValidator

pytestmark = pytest.mark.django_db


def test_submit_fails_when_url_and_file_are_empty():
    validator = CatalogDataValidator()
    data_dict = {}
    with pytest.raises(ValidationError):
        validator.get_and_validate_data(data_dict)


def test_submit_fails_when_both_url_and_file_have_content():
    validator = CatalogDataValidator()
    data_dict = {'file': "something", 'url': 'string'}
    with pytest.raises(ValidationError):
        validator.get_and_validate_data(data_dict)


def test_fails_when_response_is_not_successful(node, requests_mock):
    requests_mock.get('https://fakeurl.com/data.json',
                      status_code=404)
    data_dict = {'format': 'json', 'node': node,
                 'url': 'https://fakeurl.com/data.json'}
    validator = CatalogDataValidator()
    with pytest.raises(ValidationError):
        validator.get_and_validate_data(data_dict)


def test_returns_correct_data_when_specifying_url(node, requests_mock):
    with open_catalog('data.json') as sample:
        text = sample.read()
        requests_mock.get("https://datos.gob.ar/data.json", content=text)
        data_dict = {'format': 'json', 'node': node, 'url': 'https://datos.gob.ar/data.json'}
        validator = CatalogDataValidator()
        data = validator.get_and_validate_data(data_dict)
        assert data['json_file'].read() == text


def test_returns_correct_data_when_specifying_url_with_explicit_format(node, requests_mock):
    with open_catalog('xlsx_catalog.xlsx') as sample:
        text = sample.read()
        requests_mock.get('https://fakeurl.com/export?format=xlsx', content=text)
        data_dict = {'format': 'xlsx', 'node': node,
                     'url': 'https://fakeurl.com/export?format=xlsx'}
        validator = CatalogDataValidator()
        data = validator.get_and_validate_data(data_dict)
        assert data['xlsx_file'].read() == text


def test_returns_correct_data_when_uploading_file(node):
    with open_catalog('data.json') as sample:
        temp_file = temp_uploaded_file(sample)
        data_dict = {'format': 'json', 'node': node, 'file': temp_file}
        validator = CatalogDataValidator()
        data = validator.get_and_validate_data(data_dict)
        assert b'dataset' in data['json_file'].read()


def test_invalid_url(node, requests_mock):
    requests_mock.get('https://fakeurl.com/data.json', exc=RequestException)
    data_dict = {'format': 'json', 'node': node,
                 'url': 'https://fakeurl.com/data.json'}
    validator = CatalogDataValidator()
    with pytest.raises(ValidationError):
        validator.get_and_validate_data(data_dict)


def test_raises_validation_error_if_catalog_is_not_valid(node):
    with open_catalog('catalogo-justicia.xlsx') as sample:
        temp_file = temp_uploaded_file(sample)
        data_dict = {'format': 'xlsx', 'node': node, 'file': temp_file}
        validator = CatalogDataValidator()
        with pytest.raises(ValidationError):
            validator.get_and_validate_data(data_dict)
