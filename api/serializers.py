from rest_framework import serializers

from .models import SalaryDetails


PENSION_RATES = {
    "tier_1_employee": 0,
    "tier_1_employer": 13,
    "tier_2_employee": 5.5,
    "tier_2_employer": 0,
    "tier_3_employee": 5,
    "tier_3_employer": 5,
}

# Define the PAYE tax brackets and rates as per GRA
# structure: [(cumulative_income_limit, rate)]
PAYE_BRACKETS = [
    (312, 0),  # Up to GHS 312 is tax-free
    (600, 5),  # Next GHS 110 is taxed at 5%
    (730, 10),
    (3896.67, 17.5),
    (19896.67, 25),
    (50416.67, 30),
    (100416.67, 35),
]


class AllowancesSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    amount = serializers.FloatField(min_value=0, required=True)


class InputSerializer(serializers.Serializer):
    net_salary = serializers.FloatField(min_value=0, write_only=True, required=True)
    allowances = AllowancesSerializer(many=True, write_only=True, required=False)

    @staticmethod
    def calculate_total_allowances(allowances_data):
        total_allowances = 0
        for allowance in allowances_data:
            total_allowances += allowance["amount"]
        return total_allowances

    @staticmethod
    def calculate_paye_tax(taxable_income):
        tax = 0
        for bracket in PAYE_BRACKETS:
            if taxable_income > bracket[0]:
                tax += (min(taxable_income, bracket[0]) - tax) * (bracket[1] / 100)
        else:
            last_bracket = PAYE_BRACKETS[-1]
            if taxable_income > last_bracket[0]:
                tax += (min(taxable_income, last_bracket[0]) - tax) * (last_bracket[1] / 100)

        return tax

    @classmethod
    def calculate_salary(cls, net_salary, allowances) -> SalaryDetails:

        total_allowances = cls.calculate_total_allowances(allowances)

        # Calculate pension contributions
        tier_1_employee_contribution = 0  # As per the given rates
        tier_2_employee_contribution = (
            PENSION_RATES["tier_2_employee"] / 100
        ) * net_salary
        tier_3_employee_contribution = (
            PENSION_RATES["tier_3_employee"] / 100
        ) * net_salary

        employee_total_contribution = (
            tier_1_employee_contribution
            + tier_2_employee_contribution
            + tier_3_employee_contribution
        )

        taxable_income = net_salary - employee_total_contribution + total_allowances

        # Calculate PAYE tax
        total_paye_tax = cls.calculate_paye_tax(taxable_income)

        # Calculate basic salary
        basic_salary = taxable_income - total_paye_tax

        # Calculate employer pension contributions
        tier_1_employer_contribution = (
            PENSION_RATES["tier_1_employer"] / 100
        ) * basic_salary
        tier_3_employer_contribution = (
            PENSION_RATES["tier_3_employer"] / 100
        ) * basic_salary

        employer_total_contribution = (
            tier_1_employer_contribution + tier_3_employer_contribution
        )

        # Calculate gross salary
        gross_salary = basic_salary + total_allowances + employer_total_contribution

        return SalaryDetails(
            gross_salary=gross_salary,
            basic_salary=basic_salary,
            total_paye_tax=total_paye_tax,
            employee_total_contribution=employee_total_contribution,
            employer_total_contribution=employer_total_contribution,
        )

    def create(self, validated_data):
        allowances = validated_data.get("allowances", [])
        net_salary = validated_data["net_salary"]
        return self.calculate_salary(net_salary, allowances)
