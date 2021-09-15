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
        assert response.status_code == 302

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
        assert response.context[0]['message'] == 'dates cannot be greater than today'

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
        assert response.data['registers'][0]['id'] == db.id
        assert response.data['registers'][0]['date_and_time_attention'] == db.date_and_time_attention
        assert response.data['registers'][0]['end_time_attention'] == db.end_time_attention
        assert response.data['registers'][0]['company'] == db.company
        assert response.data['registers'][0]['city'] == db.city
        assert response.data['registers'][0]['subject'] == db.subject
        assert response.data['registers'][0]['answer'] == db.answer
        assert response.data['registers'][0]['application_date'] == db.application_date

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

        response = self.client.get(
            '/crud/{}/detail'.format(db.id), format='json')
        assert response.status_code == 200

    def test_try_get_main_by_not_existent_id(self):
        response = self.client.get('/crud/-1/detail', format='json')
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

        response = self.client.post(
            '/crud/{}/detail'.format(db.id), request_data, format='json')
        assert response.status_code == 302
        response = self.client.get(
            '/crud/{}/detail'.format(db.id), format='json')
        assert response.status_code == 200

    def test_delete_main_by_id(self):
        db = MainTableModel.objects.create(**{
            "date_and_time_attention": "2010-10-20 10:00",
            "end_time_attention": "12:30",
            "company": "Carritos SA",
            "city": "Bogota",
            "subject": "algo importante",
            "answer": "no era tan importante",
            "application_date": "2010-10-10"
        })

        response = self.client.post(
            '/crud/{}/delete'.format(db.id), format='json')
        assert response.status_code == 302
        response = self.client.get(
            '/crud/{}/detail'.format(db.id), format='json')
        assert response.status_code == 404
