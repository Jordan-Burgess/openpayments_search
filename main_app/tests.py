from django.test import TestCase
from django.core.management import call_command
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from .documents import PaymentDocument
from .models import Payment
from datetime import date
from unittest import mock
from .mock_data import data

class PaymentTest(TestCase):
    # Test for successful creation of Payment document in database
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

@mock.patch('main_app.management.commands.import_payments.requests.get')
class ImportOpenPaymentCommandTest(TestCase):
    # Test for import open database command
    def test_command_output(self, mock_get):
        mock_data = data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        call_command('import_payments')

        self.assertEqual(Payment.objects.count(), 3)
        self.assertTrue(Payment.objects.filter(doctor_first_name="JUSTIN").exists())

class PaymentIndexTest(TestCase):
    # Test for search match on indexed data
    def setUp(self):
        PaymentDocument.init()
        self.payment = Payment.objects.create(
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
        PaymentDocument().update(self.payment)

    def test_indexing_data(self):
        search_results = PaymentDocument.search().query('match', doctor_first_name='John').execute()
        self.assertTrue(search_results.hits.total.value > 0)

    def tearDown(self):
        self.payment.delete()