from django.core.management.base import BaseCommand
import requests
from main_app.models import Payment, MetaData
from datetime import datetime

class Command(BaseCommand):
    help = "Imports most recent year data from OpenPayments API"

    def handle(self, *args, **options):
        dataset_metadata = self.get_most_recent_dataset_metadata()
        action = self.update_metadata(dataset_metadata)
        identifier = dataset_metadata['identifier']
        api_url = f'https://openpaymentsdata.cms.gov/api/1/datastore/query/{identifier}/0'

        if action == 'full_import':
            self.full_import(api_url)
        elif action == 'update_import':
            self.update_import(api_url)
        elif action == 'skip':
            self.stdout.write(self.style.SUCCESS("No new updates found. Dataset is up-to-date."))

    def full_import(self, api_url):
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

    def update_import(self, api_url):
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

        for payment in data['results']:
            change_type = payment.get('change_type')
            if change_type in ['NEW', 'ADD']:
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
                

    def get_most_recent_dataset_metadata(self):
        # Returns the dataset identifier and year of the most recent General Payments publication
        api_url = 'https://openpaymentsdata.cms.gov/api/1/metastore/schemas/dataset/items'

        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            general_datasets = []

            for ds in data:
                if "General Payments" in ds.get('theme'):
                    general_datasets.append(ds)
            
            sorted_ds = sorted(general_datasets, key=lambda x: x.get('keyword')[0], reverse=True)
            if sorted_ds:
                most_recent_dataset = sorted_ds[0]
                year = most_recent_dataset.get('keyword')[0]
                return {
                    'year': year,
                    'identifier': most_recent_dataset.get('identifier'),
                    'modified': most_recent_dataset.get('modified')
                }
            
            return None
        
        else:
            return None
        
    def update_metadata(self, ds_metadata):
        try:
            metadata = MetaData.objects.get(name='Main')
            new_year = int(ds_metadata['year']) > metadata.recent_year
            modified_changed = datetime.strptime(ds_metadata['modified'], "%Y-%m-%dT%H:%M:%S%z") > metadata.modified

            if new_year or not metadata:
                self.clear_database()
                action = 'full_import'
            elif modified_changed:
                action = 'update_import'
            else:
                action = 'skip'

            if action in ['full_import', 'update_import']:
                metadata.recent_year = ds_metadata['year']
                metadata.identifier = ds_metadata['identifier']
                metadata.modified = datetime.strptime(ds_metadata['modified'], "%Y-%m-%dT%H:%M:%S%z")
                metadata.save()
            
            return action
        
        except MetaData.DoesNotExist:
            MetaData.objects.create(
                name = 'Main',
                recent_year = ds_metadata['year'],
                identifier = ds_metadata['identifier'],
                modified = datetime.strptime(ds_metadata['modified'], "%Y-%m-%dT%H:%M:%S%z")
            )
            return 'full_import'