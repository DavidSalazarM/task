from django.http import response
from rest_framework.test import APITestCase
from CRUD.models import MainTable as MainTableModel
import json

# Create your tests here.


class MainTest(APITestCase):

    def test_main_post(self):
        request_data = {
            "date_and_time_attention": "2010-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2010-10-10"
        }

        response = self.client.post('/crud/', request_data, format='json')
        assert response.status_code == 201
        data = json.loads(response.content)
        assert data.get('id') is not None
        assert data.get('date_and_time_attention') == "2010-10-20 10:00"
        assert data.get('end_time_attention') == "12:30"
        assert data.get('company') == "Carritos SA"
        assert data.get('city') == "Bogota"
        assert data.get('subject') == "algo importante"
        assert data.get('answer') == "no era tan importante"
        assert data.get('application_date') == "2010-10-10"

    def test_try_main_post_with_blank_values(self):
        request_data = {
            "date_and_time_attention": "",
            "end_time_attention": "",
            "company": "",
            "city": "",
            "subject": "",
            "answer": "",
            "application_date": ""
        }
        response = self.client.post('/crud/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data == {
            'date_and_time_attention': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'],
            'end_time_attention': ['Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].'],
            'company': ['This field may not be blank.'],
            'city': ['This field may not be blank.'],
            'subject': ['This field may not be blank.'],
            'answer': ['This field may not be blank.'],
            'application_date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']}

    def test_try_main_post_with_bad_values(self):
        request_data = {
            "date_and_time_attention": "esto no es una hora",
            "end_time_attention": "esta tampoco",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "lo mismo"
        }

        response = self.client.post('/crud/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data == {
            'date_and_time_attention': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'],
            'end_time_attention': ['Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].'],
            'application_date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']}

    def test_try_main_post_with_bad_values(self):
        request_data = {
            "date_and_time_attention": "2010/10/20 10-00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "10-30-2010"
        }

        response = self.client.post('/crud/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data == {
            'date_and_time_attention': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'],
            'application_date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']}

    def test_try_main_post_with_bad_format(self):
        request_data = {
            "date_and_time_attention": "esto no es una hora",
            "end_time_attention": "esta tampoco",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "lo mismo"
        }

        response = self.client.post('/crud/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data == {
            'date_and_time_attention': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'],
            'end_time_attention': ['Time has wrong format. Use one of these formats instead: hh:mm[:ss[.uuuuuu]].'],
            'application_date': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']}

    def test_try_main_post_with_date_greater_than_today(self):
        request_data = {
            "date_and_time_attention": "2030-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2050-10-10"
        }

        response = self.client.post('/crud/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data == {
            'error': 'the time entered cannot be greater than today'}

    def test_main_get(self):
        db = MainTableModel.objects.create(**{
            "date_and_time_attention": "2010-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2010-10-10"
        })

        response = self.client.get('/crud/', format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data[0]["id"] == db.id
        assert data[0]['date_and_time_attention'] == "2010-10-20 10:00"
        assert data[0]['end_time_attention'] == "12:30"
        assert data[0]['company'] == "Carritos SA"
        assert data[0]['city'] == "Bogota"
        assert data[0]['subject'] == "algo importante"
        assert data[0]['answer'] == "no era tan importante"
        assert data[0]['application_date'] == "2010-10-10"


class MainDetailTest(APITestCase):

    def test_get_main_by_id(self):
        db = MainTableModel.objects.create(**{
            "date_and_time_attention": "2010-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2010-10-10"
        })

        response = self.client.get('/crud/{}/'.format(db.id), format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["id"] == db.id
        assert data['date_and_time_attention'] == "2010-10-20 10:00"
        assert data['end_time_attention'] == "12:30"
        assert data['company'] == "Carritos SA"
        assert data['city'] == "Bogota"
        assert data['subject'] == "algo importante"
        assert data['answer'] == "no era tan importante"
        assert data['application_date'] == "2010-10-10"

    def test_try_get_main_by_not_existent_id(self):
        response = self.client.get('/crud/-1/', format='json')
        assert response.status_code == 404

    def test_put_main_by_id(self):
        db = MainTableModel.objects.create(**{
            "date_and_time_attention": "2010-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2010-10-10"
        })

        request_data = {
            "date_and_time_attention": "2015-10-20 10:00",
            "end_time_attention": "11:30",
            "company": "Enclve CO",
            "city": "Medallin",
            "subject": "no era tan importante",
            "answer": "algo importante",
            "application_date": "2012-10-10"
        }

        response = self.client.put(
            '/crud/{}/'.format(db.id), request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["id"] == db.id
        assert data['date_and_time_attention'] == request_data['date_and_time_attention']
        assert data['end_time_attention'] == request_data['end_time_attention']
        assert data['company'] == request_data['company']
        assert data['city'] == request_data['city']
        assert data['subject'] == request_data['subject']
        assert data['answer'] == request_data['answer']
        assert data['application_date'] == request_data['application_date']

    def test_get_main_by_id(self):
        db = MainTableModel.objects.create(**{
            "date_and_time_attention": "2010-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2010-10-10"
        })

        response = self.client.delete('/crud/{}/'.format(db.id), format='json')
        assert response.status_code == 204
        response = self.client.get('/crud/{}/'.format(db.id), format='json')
        assert response.status_code == 404
