from dataclasses import dataclass


@dataclass()
class SalaryDetails(object):
    gross_salary: float
    basic_salary: float
    total_paye_tax: float
    employee_total_contribution: float
    employer_total_contribution: float

    def to_dict(self):
        return {
            "gross_salary": self.gross_salary,
            "basic_salary": self.basic_salary,
            "total_paye_tax": self.total_paye_tax,
            "employee_total_contribution": self.employee_total_contribution,
            "employer_total_contribution": self.employer_total_contribution
        }
