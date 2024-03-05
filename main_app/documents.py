from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Payment

@registry.register_document
class PaymentDocument(Document):
    class Index:
        name = 'payments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Payment
        fields = [
            'doctor_profile_id',
            'doctor_npi',
            'doctor_first_name',
            'doctor_middle_name',
            'doctor_last_name',
            'doctor_primary_address_line1',
            'doctor_primary_address_line2',
            'doctor_city',
            'doctor_state',
            'doctor_zip_code',
            'doctor_country',
            'payment_type',
            'payment_amount',
            'payment_date',
            'payment_quantity',
            'doctor_primary_type',
            'doctor_specialty',
            'doctor_license_state_code',
            'submitting_manufacturer_name',
            'submitting_manufacturer_id',
            'submitting_manufacturer_state',
            'submitting_manufacturer_country',
            'program_year',
            'publication_date',
        ]