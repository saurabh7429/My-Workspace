#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

// Base class for employee details
class Employee {
protected:
    int emp_id;
    string ename;

public:
    // Input employee details
    void input() {
        cout << "Enter Employee ID: ";
        cin >> emp_id;
        cin.ignore(); // Clear newline from input buffer
        cout << "Enter Employee Name: ";
        getline(cin, ename);
    }

    // Display employee details
    void display() const {
        cout << "Employee ID   : " << emp_id << endl;
        cout << "Employee Name : " << ename << endl;
    }
};

// Derived class for salary components and gross salary
class Calculate : public Employee {
protected:
    double basic = 0, hra = 0, da = 0, pf = 0;

public:
    // Input salary components
    void input_components() {
        cout << "Enter Basic Salary: ";
        cin >> basic;
        cout << "Enter HRA: ";
        cin >> hra;
        cout << "Enter DA: ";
        cin >> da;
        cout << "Enter PF (deduction): ";
        cin >> pf;
    }

    // Calculate gross salary (before PF deduction)
    virtual double getsalary() const {
        return basic + hra + da;
    }

    // Display employee details and basic salary
    virtual void display() const {
        Employee::display();
        cout << fixed << setprecision(2);
        cout << "Basic Salary  : " << basic << endl;
    }
};

// Derived class for net salary calculation
class Salary : public Calculate {
public:
    // Calculate net salary (after PF deduction)
    double getsalary() const override {
        return (basic + hra + da) - pf;
    }

    // Display employee details, basic salary, and net salary
    void display() const override {
        Employee::display();
        cout << fixed << setprecision(2);
        cout << "Basic Salary  : " << basic << endl;
        cout << "Net Salary    : " << getsalary() << endl;
    }
};

int main() {
    cout << "=== Employee Salary Management ===" << endl << endl;

    Salary emp;

    // Input employee and salary details
    emp.input();
    emp.input_components();

    cout << "\n--- Employee Basic Details ---\n";
    emp.Calculate::display();

    cout << "\n--- Employee Net Salary Details ---\n";
    emp.display();

    cout << "\nSummary:" << endl;
    cout << "Gross Salary (Basic + HRA + DA): " << fixed << setprecision(2) << emp.Calculate::getsalary() << endl;
    cout << "Net Salary   (Gross - PF)     : " << fixed << setprecision(2) << emp.getsalary() << endl;

    cout << "\nThank you!\n";

    return 0;
}
