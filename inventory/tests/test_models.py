import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.db.utils import IntegrityError

from inventory.models import Location, Accommodation, LocalizeAccommodation
from inventory.enums import LocationType, LanguageCode


class LocationModelTest(TestCase):
    """
    Test case for the Location model.
    """

    def setUp(self):
        """
        Setup the initial data for testing.
        """
        self.location_data = {
            'title': 'New York',
            'center': Point(-73.935242, 40.730610),  # Example Point for New York
            'location_type': 'CITY',  # Using valid enum choice
            'country_code': 'US',
            'state_abbr': 'NY',
            'city': 'New York'
        }
        self.location = Location.objects.create(**self.location_data)

    def test_location_creation(self):
        """
        Test that a Location object is created successfully.
        """
        location = Location.objects.get(id=self.location.id)
        self.assertEqual(location.title, 'New York')
        self.assertEqual(location.country_code, 'US')
        self.assertEqual(location.state_abbr, 'NY')
        self.assertEqual(location.city, 'New York')
        self.assertTrue(location.center.x, -73.935242)  # Longitude of New York
        self.assertTrue(location.center.y, 40.730610)  # Latitude of New York

    def test_location_get_location_type_display(self):
        """
        Test that the method `get_location_type_display()` returns correct values.
        """
        location = Location.objects.get(id=self.location.id)
        self.assertEqual(location.get_location_type_display(), 'CITY')

    def test_invalid_location_type(self):
        """
        Test that an invalid location_type raises a validation error.
        """
        with self.assertRaises(ValidationError):
            location = Location.objects.create(
                title='Invalid Location',
                center=Point(0, 0),
                location_type='INVALID',  # Invalid choice for location_type
                country_code='XX',
                state_abbr='XX',
                city='Invalid City'
            )
            location.full_clean()  # Explicitly call full_clean to trigger validation

class AccommodationModelTest(TestCase):
    
    def setUp(self):
        """
        Setup test data.
        """
        # Create a sample user
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password'
        )

        # Create a location
        self.location = Location.objects.create(
            title='New York', 
            center=Point(-73.935242, 40.730610),  # Longitude, Latitude
            location_type='CITY',
            country_code='US',
            state_abbr='NY',
            city='New York'
        )

    def test_create_accommodation(self):
        """
        Test creating an accommodation instance.
        """
        accommodation = Accommodation.objects.create(
            title="Test Accommodation",
            country_code="US",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["WiFi", "Parking"],
            published=True,
        )
        
        # Test that the accommodation was created successfully
        self.assertEqual(accommodation.title, "Test Accommodation")
        self.assertEqual(accommodation.country_code, "US")
        self.assertEqual(accommodation.bedroom_count, 2)
        self.assertEqual(accommodation.review_score, 4.5)
        self.assertEqual(accommodation.usd_rate, 150.00)
        self.assertEqual(accommodation.center.x, -73.935242)
        self.assertEqual(accommodation.center.y, 40.730610)
        self.assertEqual(accommodation.location_id, self.location)
        self.assertEqual(accommodation.user, self.user)
        self.assertEqual(accommodation.amenities, ["WiFi", "Parking"])
        self.assertTrue(accommodation.published)

    def test_accommodation_images_field(self):
        """
        Test that the images field works as expected (ArrayField).
        """
        accommodation = Accommodation.objects.create(
            title="Test Accommodation with Images",
            country_code="US",
            bedroom_count=3,
            review_score=4.0,
            usd_rate=200.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["WiFi", "Gym"],
            published=True,
            images=["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
        )
        
        # Test that images are stored correctly in the ArrayField
        self.assertEqual(accommodation.images, ["https://example.com/image1.jpg", "https://example.com/image2.jpg"])

    def test_accommodation_str_method(self):
        """
        Test the __str__ method of Accommodation model.
        """
        accommodation = Accommodation.objects.create(
            title="Test Accommodation",
            country_code="US",
            bedroom_count=1,
            review_score=4.0,
            usd_rate=100.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["WiFi"],
            published=True,
        )
        
        # Test the string representation of the accommodation model
        self.assertEqual(str(accommodation), "Test Accommodation")

    def test_accommodation_user_association(self):
        """
        Test that the accommodation is correctly associated with a user.
        """
        accommodation = Accommodation.objects.create(
            title="Test Accommodation for User",
            country_code="US",
            bedroom_count=1,
            review_score=5.0,
            usd_rate=200.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["WiFi", "TV"],
            published=True,
        )

        # Test user association
        self.assertEqual(accommodation.user, self.user)

    def test_default_published_value(self):
        """
        Test the default value of the published field (should be False by default).
        """
        accommodation = Accommodation.objects.create(
            title="Test Accommodation with Default Published",
            country_code="US",
            bedroom_count=1,
            review_score=3.5,
            usd_rate=120.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["Parking"],
        )
        
        # By default, the 'published' field should be False
        self.assertFalse(accommodation.published)
        
    def test_review_score_max_value(self):
        """
        Test that the review score is capped at 9.9
        """
        accommodation = Accommodation.objects.create(
            title="Test Accommodation with Max Review",
            country_code="US",
            bedroom_count=1,
            review_score=9.9,
            usd_rate=120.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["Pool"],
            published=True,
        )
        
        # Ensure that the review_score is 10.0
        self.assertEqual(accommodation.review_score, 9.9)
        
    def test_review_score_invalid_value(self):
        """
        Test that an invalid review score (greater than 9.9) is not allowed.
        """
        accommodation = Accommodation(
            title="Test Accommodation with Invalid Review",
            country_code="US",
            bedroom_count=1,
            review_score=15.0,  # Invalid value (greater than max 9.9)
            usd_rate=120.00,
            center=Point(-73.935242, 40.730610),
            location_id=self.location,
            user=self.user,
            amenities=["WiFi"],
            published=True,
        )

        with self.assertRaises(ValidationError):
            accommodation.clean()


class LocalizeAccommodationTest(TestCase):

    def setUp(self):
        # Create a Location instance (for foreign key reference)
        self.location = Location.objects.create(
            title="San Francisco",
            center="POINT(37.7749 -122.4194)",
            location_type="CITY",
            country_code="US",
            state_abbr="CA",
            city="San Francisco",
        )
        # Create an Accommodation instance (for foreign key reference)
        self.accommodation = Accommodation.objects.create(
            title="Beautiful Beach House",
            country_code="US",
            bedroom_count=3,
            review_score=9.5,
            usd_rate=300.00,
            center="POINT(37.7749 -122.4194)",
            location_id=self.location,
            amenities=["WiFi", "Pool"],
            published=True,
        )

    def test_create_localize_accommodation(self):
        # Test the creation of a LocalizeAccommodation object
        localize = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language='en',  # assuming 'EN' is part of the LanguageCode enum
            description="Test Description",
            policy={"pet_policy": "allowed"}
        )
        
        self.assertEqual(localize.property_id, self.accommodation)
        self.assertEqual(localize.language, LanguageCode.ENGLISH.value)
        self.assertEqual(localize.description, "Test Description")
        self.assertEqual(localize.policy, {"pet_policy": "allowed"})
        self.assertIsInstance(localize, LocalizeAccommodation)
    
    def test_invalid_language_code(self):
        # Test that assigning an invalid language code raises a validation error
        with self.assertRaises(ValidationError):
            localize = LocalizeAccommodation(
                property_id=self.accommodation,
                language="INVALID",  # Invalid language code
                description="Test Description",
                policy={"pet_policy": "allowed"}
            )
            localize.full_clean()  # This will trigger validation
            localize.save()
    
    def test_str_method(self):
        # Test the string representation of the model
        localize = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language=LanguageCode.ENGLISH.value,
            description="Test Description",
            policy={"pet_policy": "allowed"}
        )
        
        expected_str = f"Localized description for Beautiful Beach House (en)"
        self.assertEqual(str(localize), expected_str)
    
    def test_policy_field_default(self):
        # Test that the policy field defaults to an empty dict if not provided
        localize = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language=LanguageCode.ENGLISH.value,
            description="Test Description"
        )
        self.assertEqual(localize.policy, {})
    
    def test_create_localize_with_no_property(self):
        # Test creating a LocalizeAccommodation without a property_id
        with self.assertRaises(IntegrityError):
            LocalizeAccommodation.objects.create(
                language=LanguageCode.ENGLISH.value,
                description="Test Description",
                policy={"pet_policy": "allowed"}
            )
    
    def test_create_localize_with_invalid_policy(self):
        # Test creating LocalizeAccommodation with invalid policy type (should raise ValidationError)
        localize = LocalizeAccommodation(
            property_id=self.accommodation,
            language='en',  # Assuming 'EN' is part of the LanguageCode enum
            description="Test Description",
            policy="invalid_policy_format"  # Invalid policy format, should be a dict
        )
        
        # This will trigger validation, and a ValidationError should be raised
        with self.assertRaises(ValidationError):
            localize.full_clean()
    
    def test_language_choices(self):
        # Test that the language field only accepts valid language choices from LanguageCode
        valid_languages = [LanguageCode.ENGLISH.value, LanguageCode.FRENCH.value, LanguageCode.SPANISH.value]
        for language in valid_languages:
            print(self.accommodation)
            localize = LocalizeAccommodation.objects.create(
                property_id=self.accommodation,
                language=language,
                description="Test Description",
                policy={"pet_policy": "allowed"}
            )
            self.assertEqual(localize.language, language)
        
        # Check invalid language code, should raise validation error
        with self.assertRaises(ValidationError):
            localize = LocalizeAccommodation.objects.create(
                property_id=self.accommodation,
                language="XX",  # Invalid language code
                description="Test Description",
                policy={"pet_policy": "allowed"}
            )
            localize.full_clean()  # Trigger validation
