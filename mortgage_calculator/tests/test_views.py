from django.test import TestCase
from django.urls import reverse

class MortgageCalculatorViewTest(TestCase):
    def test_mortgage_calculator_view(self):
        response = self.client.get(reverse('mortgage_calculator'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mortgage_calculator/mortgage_calculator.html')
