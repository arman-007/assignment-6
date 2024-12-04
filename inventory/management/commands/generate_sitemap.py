import json
from django.core.management.base import BaseCommand
from inventory.models import Location
from django.conf import settings


class Command(BaseCommand):
    help = 'Generate sitemap.json for all country locations'

    def handle(self, *args, **kwargs):
        # Fetch all locations and organize them by country
        countries = {}
        locations = Location.objects.filter(location_type='COUNTRY').order_by('title')
        print(locations)

        for country in locations:
            # Get child locations (states, provinces, etc.) for each country
            child_locations = (
                Location.objects.filter(parent_id=country, location_type='STATE')
                .order_by('title')
                .values('title', 'id')
            )
            # Build the JSON structure for the country and its child locations
            country_slug = country.title.lower().replace(" ", "-")
            countries[country.title] = {
                "country_slug": country_slug,
                "locations": [
                    {
                        child["title"]: f"{country_slug}/{child['title'].lower().replace(' ', '-')}"
                    }
                    for child in child_locations
                ],
            }

        # Sort countries alphabetically by their names
        sorted_countries = sorted(countries.items())

        # Create the final JSON structure
        sitemap = [
            {country: {"slug": data["country_slug"], "locations": data["locations"]}}
            for country, data in sorted_countries
        ]

        # Write to the sitemap.json file
        output_path = settings.BASE_DIR / "sitemap.json"
        with open(output_path, "w") as json_file:
            json.dump(sitemap, json_file, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Sitemap generated at {output_path}"))
