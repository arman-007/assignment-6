# myapp/management/commands/populate_location_table.py
import csv
import os
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from inventory.models import Location
from inventory.enums import LocationType
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Populates the Location table from a CSV file.'

    def add_arguments(self, parser):
        # Add an argument to specify the directory of the CSV file
        parser.add_argument('csv_directory', type=str, help='The directory of the CSV file.')

    def handle(self, *args, **kwargs):
        # Get the directory and path of the CSV file
        csv_directory = kwargs['csv_directory']
        csv_file_path = os.path.join(csv_directory, 'location_data.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_file_path}"))
            return

        # Open and read the CSV file
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            # Loop over each row in the CSV
            for row in reader:
                title = row['title']
                center = row['center']
                location_type = row['location_type']
                country_code = row['country_code']
                state_abbr = row['state_abbr']
                city = row['city']
                created_at = parse_datetime(row['created_at'])
                updated_at = parse_datetime(row['updated_at'])

                # Parse the center (Point field)
                longitude, latitude = center.replace('POINT(', '').replace(')', '').split(' ')
                point = Point(float(longitude), float(latitude))

                # Get parent location if exists
                parent_location = None
                if row['parent_id']:
                    parent_location = Location.objects.get(title=row['parent_id'])

                # Create the Location object
                location = Location.objects.create(
                    title=title,
                    center=point,
                    parent_id=parent_location,
                    location_type=LocationType[location_type.upper()].value,  # Map to LocationType enum
                    country_code=country_code,
                    state_abbr=state_abbr,
                    city=city,
                    created_at=created_at,
                    updated_at=updated_at
                )

                self.stdout.write(self.style.SUCCESS(f"Successfully added location: {title}"))