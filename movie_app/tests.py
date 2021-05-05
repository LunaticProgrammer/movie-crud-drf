import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from movie_app.serializers import UserSerializer
from rest_framework.test import APIRequestFactory

from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient

body = {
    "title": "some",
    "description": "somedescription",
    "movies": [
        {
            "name": "somoename",
                    "uuid": "someuuid",
                    "genres": "horror",
                    "description": "somedescription"
        }
    ]
}

update = {
    "title": "newtitle",
    "description": "somedescription",
    "movies": [
        {
            "name": "somoename",
                    "uuid": "someuuid",
                    "genres": "horror",
                    "description": "somedescription"
        }
    ]
}


class RegistrationTestCase(APITestCase):

    def test_userRegistration(self):
        data = {"username": "someuser", "password": "somepassword"}
        client = RequestsClient()
        response = client.post('http://testserver/register',
                               json.dumps(data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.json()['access_token'] != None


class MoviesTestCase(APITestCase):
    def setUp(self):
        data = {"username": "someuser", "password": "somepassword"}
        client = RequestsClient()
        response = client.post('http://testserver/register',
                               json.dumps(data))
        self.access_token = response.json()['access_token']

    def test_movie_listing(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)
        data = self.client.get('/movies')
        assert data.status_code == 200


class CollectionTestCase(APITestCase):
    def setUp(self):
        data = {"username": "someuser", "password": "somepassword"}
        client = RequestsClient()
        response = client.post('http://testserver/register',
                               json.dumps(data))
        self.access_token = response.json()['access_token']

    def test_add_collection(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)

        response = self.client.post(
            '/collection', json.dumps(body), content_type='application/json')
        assert response.status_code == 201

    def test_get_all_collections(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)
        self.client.post(
            '/collection', json.dumps(body), content_type='application/json')

        response = self.client.get('/collection')
        assert response.status_code == 200

    def test_get_single_test(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)
        val = self.client.post(
            '/collection', json.dumps(body), content_type='application/json')

        response = self.client.get(
            '/collection/'+val.json()['collection_uuid'])
        assert response.status_code == 200

    def test_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)
        val = self.client.post(
            '/collection', json.dumps(body), content_type='application/json')

        response = self.client.put(
            '/collection/'+val.json()['collection_uuid'], json.dumps(update), content_type='application/json')
        assert response.status_code == 200
        assert response.json()['title'] == 'newtitle'

    def test_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.access_token)
        val = self.client.post(
            '/collection', json.dumps(body), content_type='application/json')

        respose = self.client.delete(
            '/collection/'+val.json()['collection_uuid'])
        assert respose.status_code == 200
        assert respose.json()['message'] == 'deleted succesfully'


# Create your tests here.
