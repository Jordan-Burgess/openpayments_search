from django.db import models

class Payment(models.Model):
    doctor_profile_id = models.BigIntegerField()
    doctor_npi = models.BigIntegerField()
    doctor_first_name = models.CharField(max_length=50)
    doctor_middle_name = models.CharField(max_length=50)
    doctor_last_name = models.CharField(max_length=50)
    doctor_primary_address_line1 = models.CharField()
    doctor_primary_address_line2 = models.CharField()
    doctor_city = models.CharField(max_length=50)
    doctor_state = models.CharField(max_length=2)
    doctor_zip_code = models.CharField(max_length=10)
    doctor_country = models.CharField(max_length=50)
    doctor_primary_type = models.CharField()
    doctor_specialty = models.CharField()
    doctor_license_state_code = models.CharField(max_length=2)
    submitting_manufacturer_name = models.CharField()
    submitting_manufacturer_id = models.BigIntegerField()
    submitting_manufacturer_state = models.CharField(max_length=2)
    submitting_manufacturer_country = models.CharField(max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_quantity = models.IntegerField()
    payment_type = models.CharField()
    program_year = models.IntegerField()
    publication_date = models.DateField()   


