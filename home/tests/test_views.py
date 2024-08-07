from django.test import TestCase, Client
from django.urls import reverse
from real_estate.models import Property, User
from real_estate.forms import PropertySearchForm

class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.property1 = Property.objects.create(
            title='Property 1',
            location='Location 1',
            property_type='detached-houses',  # Ensure this matches the valid choices in the model
            bedrooms=3,
            bathrooms=2,
            price=250000,
            garden=True,
            parking=True,
            pets_allowed=True,
            transaction_type='sale',
            publication_status='published',
            agent=self.user
        )
        self.property2 = Property.objects.create(
            title='Property 2',
            location='Location 2',
            property_type='apartments',  # Ensure this matches the valid choices in the model
            bedrooms=2,
            bathrooms=1,
            price=150000,
            garden=False,
            parking=False,
            pets_allowed=False,
            transaction_type='rent',
            publication_status='published',
            agent=self.user
        )

    def test_home_view_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertIsInstance(response.context['form'], PropertySearchForm)

    def test_home_view_search(self):
        response = self.client.get(reverse('home'), {'search': 'Location 1'})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['search'], 'Location 1')

    def test_home_view_filter_property_type(self):
        response = self.client.get(reverse('home'), {'property_type': 'detached-houses'})  # Use a valid choice
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['property_type'], 'detached-houses')

    def test_home_view_filter_bedrooms(self):
        response = self.client.get(reverse('home'), {'bedrooms_min': 3})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertEqual(int(form.cleaned_data['bedrooms_min']), 3)

    def test_home_view_filter_price(self):
        response = self.client.get(reverse('home'), {'price_min': 200000})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertEqual(int(form.cleaned_data['price_min']), 200000)

    def test_home_view_filter_garden(self):
        response = self.client.get(reverse('home'), {'garden': True})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['garden'])

    def test_home_view_filter_parking(self):
        response = self.client.get(reverse('home'), {'parking': True})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['parking'])

    def test_home_view_filter_pets_allowed(self):
        response = self.client.get(reverse('home'), {'pets_allowed': True})
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['pets_allowed'])


class PropertySaleViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_property_sale_view(self):
        response = self.client.get(reverse('property_sale'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'real_estate/property_sale.html')


class PropertyRentViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_property_rent_view(self):
        response = self.client.get(reverse('property_rent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'real_estate/property_rent.html')
