import datetime
import json
from configparser import RawConfigParser

import jwt
import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from rest_framework import permissions, request, response, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from movie_app.models import Collection
from movie_app.serializers import (CollectionSerializer, GroupSerializer,
                                   MyTokenObtainPairSerializer, UserSerializer)
from movie_app.utils import format_output, getGenreField, validateMovies

config = RawConfigParser()
config.read('movie_app/config/settings.ini')
username = config.get('section', 'username')
password = config.get('section', 'password')


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(http_method_names=['POST'])
def register(request):
    body = json.loads(request.body)
    host = request.get_host()
    serialized = UserSerializer(data=body)
    if serialized.is_valid():
        uname = body['username']
        pas = body['password']
        User.objects.create(
            username=uname, password=make_password(pas), is_active=True)
    else:
        return response.Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(username=body['username'])
    access_token = str(
        MyObtainTokenPairView.serializer_class.get_token(user).access_token)
    # access_token = requests.post('http://'+host+'/auth', body)
    # token = access_token.json()['access']
    return response.Response({"access_token": access_token}, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['GET'])
@permission_classes((permissions.IsAuthenticated, ))
def getMovies(request):
    qparams = request.query_params
    url = config.get('section', 'url')
    if 'page' in qparams.keys():
        url += '?page='+qparams['page']
    data = requests.get(url, auth=(username,
                        password))

    if data.status_code == 200:
        rdata = format_output(data, request)
        return response.Response(rdata)
    else:
        return response.Response("Some error occured", data.status_code)


@api_view(['POST', 'GET'])
@permission_classes((permissions.IsAuthenticated,))
def CRCollection(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serialized = CollectionSerializer(data=data)
        isValidMovies = validateMovies(data['movies'])
        if serialized.is_valid() and isValidMovies:
            val = Collection.objects.create(
                user=request.user.username, title=data['title'], description=data['description'], movies=data['movies'])

        return response.Response({'collection_uuid': val.uuid}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        uname = request.user.username
        vals = Collection.objects.filter(user=uname).values()
        topGenres = getGenreField(vals)
        for x in vals:
            del x['movies']
        data = dict()
        data['collections'] = vals
        data['favourite_genres'] = topGenres
        return response.Response({'is_success': True, "data": data})


@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes((permissions.IsAuthenticated,))
def UDCollection(request, uuid):
    if request.method == 'DELETE':
        collection = Collection.objects.get(uuid=uuid)
        collection.delete()
        return response.Response({'message': "deleted succesfully"})
    elif request.method == 'GET':
        collection = Collection.objects.filter(uuid=uuid).values()
        return response.Response(collection)
    elif request.method == 'PUT':
        collection = Collection.objects.get(uuid=uuid)
        data = json.loads(request.body)
        serializer = CollectionSerializer(collection, data)
        if serializer.is_valid():
            serializer.save()
            val = Collection.objects.filter(uuid=uuid).values()
            return response.Response(val[0])
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
