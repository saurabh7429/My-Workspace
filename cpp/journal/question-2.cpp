/*Write a program to create class Customer that contains Customer Id,
Name, Address as data member and add customer and
display_customer as member function. A derived class Order is
created from the class Customer with publicly inherited. The derived
class contains Price1, Price2, Price3 as Prices of three Products and
input_prices and display_result as member functions. Create an
array of object of the Order class and display the result of
5 customers.*/

#include <iostream>
#include <string>
using namespace std;

// Base class for customer details
class Customer {
protected:
    int customerId;
    string name;
    string address;

public:
    // Function to input customer details
    void add_customer() {
        cout << "Enter Customer ID: ";
        cin >> customerId;
        cin.ignore(); // Clear input buffer
        cout << "Enter Customer Name: ";
        getline(cin, name);
        cout << "Enter Customer Address: ";
        getline(cin, address);
    }

    // Function to display customer details
    void display_customer() const {
        cout << "Customer ID   : " << customerId << endl;
        cout << "Name          : " << name << endl;
        cout << "Address       : " << address << endl;
    }
};

// Derived class for order details
class Order : public Customer {
    float price1 = 0, price2 = 0, price3 = 0;

public:
    // Function to input product prices
    void input_prices() {
        cout << "Enter price for Product 1: ";
        cin >> price1;
        cout << "Enter price for Product 2: ";
        cin >> price2;
        cout << "Enter price for Product 3: ";
        cin >> price3;
    }

    // Function to display order summary
    void display_result() const {
        display_customer();
        float total = price1 + price2 + price3;
        cout << "Product 1 Price: " << price1 << endl;
        cout << "Product 2 Price: " << price2 << endl;
        cout << "Product 3 Price: " << price3 << endl;
        cout << "Total Price    : " << total << endl;
    }
};

int main() {
    const int num_customers = 5;
    Order customers[num_customers];

    // Input details for each customer
    for (int i = 0; i < num_customers; ++i) {
        cout << "\n--- Enter details for Customer " << (i + 1) << " ---" << endl;
        customers[i].add_customer();
        customers[i].input_prices();
    }

    // Display all customer order details
    cout << "\n\n===== Customer Order Details =====" << endl;
    for (int i = 0; i < num_customers; ++i) {
        cout << "\n--- Customer " << (i + 1) << " ---" << endl;
        customers[i].display_result();
    }

    return 0;
}
