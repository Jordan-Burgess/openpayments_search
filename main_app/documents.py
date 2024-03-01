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
            'doctor_first_name',
            'doctor_middle_name',
            'doctor_last_name',
            'payment_type',
        ]