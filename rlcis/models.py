import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Reviewer(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    employee_id = models.IntegerField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Incident(models.Model):
    CASH = 'CA'
    FAVORS = 'FA'
    GRATUITY = 'GR'
    GIFTS = 'GI'

    AGENT = 'AG'
    THIRD_PARTY = 'TP'
    PUBLIC_OFFICIAL = 'PO'

    OTHER = 'OT'

    BRIBE_TYPE_CHOICES = [
        (CASH, 'Cash'),
        (FAVORS, 'Favors'),
        (GRATUITY, 'Gratuity'),
        (GIFTS, 'Gifts'),
        (OTHER, 'Other Bribe Type'),
    ]
    BRIBED_BY_CHOICES = [
        (AGENT, 'Agent'),
        (THIRD_PARTY, 'Third Party'),
        (PUBLIC_OFFICIAL, 'Public Official'),
        (OTHER, 'Bribed by Other'),
    ]

    country = models.CharField(max_length=60)
    region = models.CharField(max_length=60)
    bribed_by = models.CharField(
        max_length=2,
        choices=BRIBED_BY_CHOICES,
        default=OTHER,
    )

    bribed_by_other = models.CharField(
        max_length=100,
        blank=True,
    )
    bribe_type = models.CharField(
        max_length=2,
        choices=BRIBE_TYPE_CHOICES,
        default=OTHER,
    )
    bribe_type_other = models.CharField(
        max_length=60,
        blank=True,
    )
    location = models.CharField(max_length=60)
    first_occurence = models.DateTimeField('first occurence')
    resolution_date = models.DateTimeField('resolution date')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)

    # def was_published_recently(self):
    #	return self.resolution_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.first_occurence.strftime("%Y/%m/%d, %H:%M:%S") + ' ' + self.bribed_by if not self.bribe_type_other else self.bribe_type_other + ' ' + self.bribe_type if not self.bribe_type_other else self.bribe_type_other
