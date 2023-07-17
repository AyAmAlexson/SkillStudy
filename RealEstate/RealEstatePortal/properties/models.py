from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import *

rented = 'RE'
available = 'AV'
soon = 'SO'
to_call = 'TC'

PROP_STATUSES = [
    (rented, 'Rented'),
    (available, 'Available'),
    (soon, 'Coming soon'),
    (to_call, 'To call'),
]

residential = 'QL'
commercial = 'QC'
sales = 'ZH'

PROP_DIVISION = [
    (residential, 'Residential'),
    (commercial, 'Commercial'),
    (sales, 'Sales'),
]


class CustomUser(AbstractUser):
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True)
    phone_3 = models.CharField(max_length=15, null=True)

class Agents(models.Model):
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contracts_closed = models.IntegerField(default=0, null=True)
    revenue_generated = models.FloatField(default=0.0, null=True)

    def close_contract(self, value):
        self.contracts_closed += 1
        self.revenue_generated += value
        self.save()

    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'

class Owners(models.Model):
    owner_ql_id = models.CharField(max_length=10, unique=True)
    activated = models.BooleanField(default=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True)
    phone_3 = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    added_by = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(auto_now_add=True)


class Clients(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_1 = models.CharField(max_length=15)
    phone_2 = models.CharField(max_length=15, null=True)
    phone_3 = models.CharField(max_length=15, null=True)
    email = models.EmailField()
    added_by = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(auto_now_add=True)


class Features(models.Model):
    prop_feature = models.CharField(max_length=32, unique=True)


class ResProperties(models.Model):
    ref = models.IntegerField(unique=True)
    prop_division = models.CharField(max_length=2,choices=PROP_DIVISION, default='QL')
    prop_type = models.CharField(max_length=25)
    location = models.CharField(max_length=25)
    area = models.CharField(max_length=15)
    address = models.TextField(null=True)
    link = models.URLField()
    _price = models.FloatField(default=0.0, db_column="Price")
    status = models.CharField(max_length=2, choices=PROP_STATUSES, default='RE')
    status_valid = models.CharField(max_length=25)
    off_the_market = models.BooleanField(default=False)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=0)

    prop_features = models.ManyToManyField(Features, through='PropertiesFeatures')
    prop_description = models.TextField()

    date_added = models.DateField(auto_now_add=True)
    date_rented = models.DateField(null=True)
    date_expected = models.DateField(null=True)
    time_updated = models.TimeField(auto_now=True)

    owner = models.ForeignKey(Owners, on_delete=models.CASCADE)
    added_by = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)

    lf = models.CharField(max_length=50, null=True)

    @property
    def exiref(self):
        return f'e-{str(oct(self.ref))[2:]}'


    def preview(self):
        return f'REF {self.ref} - {self.bedrooms}-bedroom {self.prop_type} in {self.location}.'

    def make_off_the_market(self, _date: datetime):
        self.off_the_market = True
        self.date_rented = _date
        self.date_expected = (datetime.strptime(_date, '%Y-%m-%d') + timedelta(180)).strftime('%Y-%m-%d')
        self.status = 'RE'
        self.status_valid = 'Rented'
        self.save()

    def make_on_the_market(self, _date):
        self.off_the_market = False
        self.date_expected = _date
        if _date <= datetime.date.today():
            self.status = 'AV'
            self.status_valid = 'Available'
        else:
            self.status = 'SO'
            self.status_valid = 'Soon'
        self.save()

    def move_the_date(self, _date):
        self.date_expected = _date
        self.save()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        self.save()

    def __str__(self):
        return f'REF {self.ref} - {self.bedrooms}-bedroom {self.prop_type} in {self.location}.'


class PropertiesFeatures(models.Model):
    re_property = models.ForeignKey(ResProperties, on_delete=models.CASCADE)
    re_feature = models.ForeignKey(Features, on_delete=models.CASCADE)


class Comments(models.Model):
    re_property = models.ForeignKey(ResProperties, on_delete=models.CASCADE)
    added_by = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)


class Viewings(models.Model):
    re_property = models.ForeignKey(ResProperties, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True)


class Contracts(models.Model):
    re_property = models.ForeignKey(ResProperties, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(Agents, on_delete=models.SET_NULL, null=True)
    move_in_date = models.DateField()
    sign_date = models.DateField()
    period = models.IntegerField(default=12)
    final_price = models.FloatField(default=0.0)
    af_paid = models.BooleanField(default=False)
    deposit_paid = models.BooleanField(default=False)
    contract_signed = models.BooleanField(default=False)



