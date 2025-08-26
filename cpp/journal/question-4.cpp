/*Write a program to create three class; Vehicle, Twowheeler and
Fourwheeler. In Vehicle class data members are company name, and
methods are input and display. Twowheeler inherit the properties of
Vehical class and data members are name, type(gear,non gear) ; and
methods are input and display. FourWheeler class inherit the
properties of Vehical and it’s data members are name, model no, fuel
type; and methods are input and display. Use overriding techniques
for input and display methods.
*/

#include <iostream>
#include <string>
#include <vector>
using namespace std;

// Base class for all vehicles
class Vehicle {
protected:
    string company_name;

public:
    // Input company name
    virtual void input() {
        cout << "Enter company name: ";
        getline(cin, company_name);
    }

    // Display company name
    virtual void display() const {
        cout << "Company Name: " << company_name << endl;
    }

    virtual ~Vehicle() {}
};

// Class for two-wheelers, inherits from Vehicle
class Twowheeler : public Vehicle {
    string name;
    string type; // gear or non-gear

public:
    // Input details for two-wheeler
    void input() override {
        Vehicle::input();
        cout << "Enter two-wheeler name: ";
        getline(cin, name);
        cout << "Enter type (gear/non-gear): ";
        getline(cin, type);
    }

    // Display details for two-wheeler
    void display() const override {
        Vehicle::display();
        cout << "Two-wheeler Name: " << name << endl;
        cout << "Type: " << type << endl;
    }
};

// Class for four-wheelers, inherits from Vehicle
class Fourwheeler : public Vehicle {
    string name;
    string model_no;
    string fuel_type;

public:
    // Input details for four-wheeler
    void input() override {
        Vehicle::input();
        cout << "Enter four-wheeler name: ";
        getline(cin, name);
        cout << "Enter model number: ";
        getline(cin, model_no);
        cout << "Enter fuel type: ";
        getline(cin, fuel_type);
    }

    // Display details for four-wheeler
    void display() const override {
        Vehicle::display();
        cout << "Four-wheeler Name: " << name << endl;
        cout << "Model Number: " << model_no << endl;
        cout << "Fuel Type: " << fuel_type << endl;
    }
};

int main() {
    cout << "Welcome to the Garage Inventory System!\n" << endl;

    vector<Vehicle*> garage;

    // Input for two two-wheelers
    for (int i = 0; i < 2; i++) {
        cout << "\n--- Enter details for TwoWheeler " << i + 1 << " ---" << endl;
        Vehicle* v = new Twowheeler();
        v->input();
        garage.push_back(v);
    }

    // Input for two four-wheelers
    for (int i = 0; i < 2; i++) {
        cout << "\n--- Enter details for FourWheeler " << i + 1 << " ---" << endl;
        Vehicle* v = new Fourwheeler();
        v->input();
        garage.push_back(v);
    }

    // Display all vehicles in the garage
    cout << "\n===== Garage Inventory =====" << endl;
    for (size_t i = 0; i < garage.size(); ++i) {
        cout << "\nVehicle #" << (i + 1) << ":" << endl;
        garage[i]->display();
    }

    // Clean up memory
    for (auto* v : garage) {
        delete v;
    }

    cout << "\nThank you for using the Garage Inventory System!" << endl;
    return 0;
}
