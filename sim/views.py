import os
from tokenize import Token
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.auth.aio.transport.aiohttp import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from httplib2.auth import token
from rest_framework import viewsets
from rest_framework.viewsets import ViewSet
from .serializers import EmployersSerializers, JobSeekerSerializer, JobListingSerializers, JobSeekerProfileSerializer, \
    EmployersProfileSerializers
from .models import JobListing, Employers, JobSeekers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


class RegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": 'Username or Password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)})
        return Response({'error': 'User credential'}, status=status.HTTP_401_UNAUTHORIZED)


class JobSeekersViewSet(viewsets.ModelViewSet):
    queryset = JobSeekers.objects.all()
    serializer_class = JobSeekerSerializer


class JobSeekersProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            jobseeker = JobSeekers.objects.get(user=request.user)
            serializer = JobSeekerProfileSerializer(jobseeker)
            return Response(serializer.data)
        except jobseeker.DoesNotExist:
            return Response({'error': 'Job Seeker Profile Not Found'}, status=404)


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employers.objects.all()
    serializer_class = EmployersSerializers


class JobListingViewSet(viewsets.ModelViewSet):
    queryset = JobListing.objects.all()
    serializer_class = JobListingSerializers


@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']
    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)
    # In a real app, I'd also save any new user here to the database.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data
    return redirect('sign_in')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')