from django.db import models
from django.db.models import Model

"""
Define all your drop down classes here and you can then dynamically update them
through the database.
"""

class BribeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribedBy(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribeInitiator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribeFacilitator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BribeRecipient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IndustryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LevelOfAuthority(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name