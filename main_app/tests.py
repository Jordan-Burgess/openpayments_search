from django.test import TestCase
from .models import Payment
from datetime import date

class PaymentTest(TestCase):
    def setUp(self):
        Payment.objects.create(
            doctor_profile_id = 1234567,
            doctor_npi = 1110123456,
            doctor_first_name = "John",
            doctor_middle_name = "Test",
            doctor_last_name = "Smith",
            doctor_primary_address_line1 = "123 Cherry St.",
            doctor_primary_address_line2 = "Apt. 123",
            doctor_city = "New York",
            doctor_state = "NY",
            doctor_zip_code = "11413",
            doctor_country = "United States",
            doctor_primary_type = "Medical Doctor",
            doctor_specialty = "Podiatric Medicine",
            doctor_license_state_code = "NY",
            submitting_manufacturer_name = "Test Manufacturer",
            submitting_manufacturer_id = 100000123456,
            submitting_manufacturer_state = "NY",
            submitting_manufacturer_country = "United States",
            payment_amount = 130.00,
            payment_date = date.today(),
            payment_quantity = 1,
            payment_type = "Education",
            program_year = 2022,
            publication_date = date.today(),
        )

    def test_payment_create(self):
        record = Payment.objects.get(doctor_profile_id=1234567)
        self.assertEqual(record.doctor_npi, 1110123456)
        self.assertEqual(record.doctor_first_name, "John")
        self.assertEqual(record.doctor_middle_name, "Test")
        self.assertEqual(record.doctor_last_name, "Smith")
        self.assertEqual(record.submitting_manufacturer_name, "Test Manufacturer")
        self.assertEqual(record.submitting_manufacturer_id, 100000123456)
        self.assertEqual(record.payment_amount, 130.00)
        self.assertEqual(record.payment_date, date.today())
        self.assertEqual(record.payment_type, "Education")
        self.assertEqual(record.program_year, 2022)