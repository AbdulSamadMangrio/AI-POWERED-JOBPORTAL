from django.db import models
from django.db.models import Model


class JobSeekers(models.Model):
    # name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="jobseekers")
    # email = models.EmailField(unique=True)
    resume = models.FileField(upload_to='resume/')

    def __str__(self):
        return self.name


class Employers(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.company_name


class JobListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    employer = models.ForeignKey(Employers, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
