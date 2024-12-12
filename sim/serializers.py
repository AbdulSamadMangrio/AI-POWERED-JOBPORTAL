from rest_framework import serializers
from .models import JobSeekers, JobListing, Employers


class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekers
        fields = '__all__'


class EmployersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employers
        fields = "__all__"


class JobListingSerializers(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = "__all__"


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekers
        fields = ['id', 'user', 'resume', 'bio']


class EmployersProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employers
        fields = ['id', 'user', 'company_name', 'company_website']
