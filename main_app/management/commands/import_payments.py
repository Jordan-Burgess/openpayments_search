from django.core.management.base import BaseCommand
import requests
from main_app.models import Payment
from datetime import datetime

class Command(BaseCommand):
    help = "Imports most recent year data from OpenPayments API"

    def handle(self, *args, **options):
        api_url = 'https://openpaymentsdata.cms.gov/api/1/datastore/query/df01c2f8-dc1f-4e79-96cb-8208beaf143c/0?limit=50'

        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            for payment in data['results']:
                payment_instance = Payment(
                    doctor_profile_id = int(payment["covered_recipient_profile_id"]),
                    doctor_npi = int(payment["covered_recipient_npi"]),
                    doctor_first_name = payment["covered_recipient_first_name"],
                    doctor_middle_name = payment["covered_recipient_middle_name"],
                    doctor_last_name = payment["covered_recipient_last_name"],
                    doctor_primary_address_line1 = payment["recipient_primary_business_street_address_line1"],
                    doctor_primary_address_line2 = payment["recipient_primary_business_street_address_line2"],
                    doctor_city = payment["recipient_city"],
                    doctor_state = payment["recipient_state"],
                    doctor_zip_code = payment["recipient_zip_code"],
                    doctor_country = payment["recipient_country"],
                    doctor_primary_type = payment["covered_recipient_primary_type_1"],
                    doctor_specialty = payment["covered_recipient_specialty_1"],
                    doctor_license_state_code = payment["covered_recipient_license_state_code1"],
                    submitting_manufacturer_name = payment["submitting_applicable_manufacturer_or_applicable_gpo_name"],
                    submitting_manufacturer_id = int(payment["applicable_manufacturer_or_applicable_gpo_making_payment_id"]),
                    submitting_manufacturer_state = payment["applicable_manufacturer_or_applicable_gpo_making_payment_state"],
                    submitting_manufacturer_country = payment["applicable_manufacturer_or_applicable_gpo_making_payment_country"],
                    payment_amount = float(payment["total_amount_of_payment_usdollars"]),
                    payment_date = datetime.strptime(payment["date_of_payment"],"%m/%d/%Y").date(),
                    payment_quantity = int(payment["number_of_payments_included_in_total_amount"]),
                    payment_type = payment["nature_of_payment_or_transfer_of_value"],
                    program_year = int(payment["program_year"]),
                    publication_date = datetime.strptime(payment["payment_publication_date"], "%m/%d/%Y").date(),
                )

                payment_instance.save()
            
            self.stdout.write(self.style.SUCCESS("Successfully imported Open Payments Dataset"))

        else:
            self.stdout.write(self.style.ERROR("Failed to fetch dataset from Open Payments Dataset"))