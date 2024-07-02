from django.test import TestCase
from rest_framework.test import APITestCase

from .serializers import InputSerializer


class TestIncomeCalculatorTestCase(TestCase):
    def setUp(self):
        self.test_data_1 = {
            "net_salary": 1000,
        }
        self.test_data_2 = {
            "net_salary": 1000,
            "allowances": [
                {
                    "name": "Travel",
                    "amount": 40,
                },
                {
                    "name": "Sitting",
                    "amount": 20,
                },
            ],
        }
        self.test_data_3 = 20000

    def test_calculate_salary_details_without_allowances(self):
        input_serializer = InputSerializer(data=self.test_data_1)
        self.assertTrue(input_serializer.is_valid())

        instance = input_serializer.save()

        self.assertIsNotNone(instance)
        self.assertEqual(instance.gross_salary, 938.1)
        self.assertEqual(instance.basic_salary, 795.0)
        self.assertEqual(instance.total_paye_tax, 100.0)
        self.assertEqual(instance.employee_total_contribution, 105.0)
        self.assertEqual(instance.employer_total_contribution, 143.10000000000002)

    def test_calculate_salary_details_with_allowances(self):
        input_serializer = InputSerializer(data=self.test_data_2)
        self.assertTrue(input_serializer.is_valid())

        instance = input_serializer.save()

        self.assertIsNotNone(instance)
        self.assertEqual(instance.gross_salary, 1068.9)
        self.assertEqual(instance.basic_salary, 855.0)
        self.assertEqual(instance.total_paye_tax, 100.0)
        self.assertEqual(instance.employee_total_contribution, 105.0)
        self.assertEqual(instance.employer_total_contribution, 153.9)

    def test_calculate_paye_tax(self):
        self.assertEqual(
            InputSerializer.calculate_paye_tax(self.test_data_3), 5547.4804375
        )

    def test_calculate_allowance(self):
        self.assertEqual(
            InputSerializer.calculate_total_allowances(
                self.test_data_1.get("allowances", [])
            ),
            0,
        )
        self.assertEqual(
            InputSerializer.calculate_total_allowances(
                self.test_data_2.get("allowances")
            ),
            60,
        )


class TestIncomeCalculatorAPITestCase(APITestCase):
    api_url = "/api/salary/details"

    def setUp(self):
        self.test_data_1 = {
            "net_salary": 1000,
        }
        self.test_data_2 = {
            "net_salary": 1000,
            "allowances": [
                {
                    "name": "Travel",
                    "amount": 40,
                },
                {
                    "name": "Sitting",
                    "amount": 20,
                },
            ],
        }

    def test_endpoint_returns_200_using_data_without_allowances(self):
        response = self.client.post(self.api_url, data=self.test_data_1, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["gross_salary"], 938.1)
        self.assertEqual(response.data["total_paye_tax"], 100.0)
        self.assertEqual(response.data["employee_total_contribution"], 105.0)
        self.assertEqual(
            response.data["employer_total_contribution"], 143.10000000000002
        )
        self.assertEqual(response.data["basic_salary"], 795.0)

    def test_endpoint_returns_200_using_data_with_allowances(self):
        response = self.client.post(self.api_url, data=self.test_data_2, format="json")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["gross_salary"], 1068.9)
        self.assertEqual(response.data["total_paye_tax"], 100.0)
        self.assertEqual(response.data["employee_total_contribution"], 105.0)
        self.assertEqual(response.data["employer_total_contribution"], 153.9)
        self.assertEqual(response.data["basic_salary"], 855.0)
