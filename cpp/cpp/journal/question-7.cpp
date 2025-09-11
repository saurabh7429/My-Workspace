/*Write a C++ program to demonstrate runtime polymorphism using
inheritance and virtual functions.
• Create a base class Shape with a virtual function
calculateArea().
• Derive two classes from Shape: Circle and Square.
• Override the calculateArea() function in both derived classes
to compute and display the area of the respective shape.
• In the main() function, use a base class pointer to call the
calculateArea() function for both a Circle and a Square object.
• Show how dynamic binding works using this approach.
*/

#include <iostream>
#include <cmath> // for M_PI
using namespace std;

// Base class for shapes
class Shape {
public:
    // Virtual function for area calculation
    virtual void calculateArea() const {
        cout << "Area calculation not defined for generic shape." << endl;
    }
    virtual ~Shape() {}
};

// Derived class for Circle
class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {}
    void calculateArea() const override {
        double area = M_PI * radius * radius;
        cout << "Area of Circle: " << area << endl;
    }
};

// Derived class for Square
class Square : public Shape {
    double side;
public:
    Square(double s) : side(s) {}
    void calculateArea() const override {
        double area = side * side;
        cout << "Area of Square: " << area << endl;
    }
};

int main() {
    Shape* shapePtr = nullptr;

    // Demonstrate with Circle
    double r;
    cout << "Enter radius for the circle: ";
    cin >> r;
    Circle c(r);
    shapePtr = &c;
    cout << "\nCalling calculateArea() using Shape pointer (Circle):" << endl;
    shapePtr->calculateArea();

    // Demonstrate with Square
    double s;
    cout << "\nEnter side length for the square: ";
    cin >> s;
    Square sq(s);
    shapePtr = &sq;
    cout << "\nCalling calculateArea() using Shape pointer (Square):" << endl;
    shapePtr->calculateArea();

    cout << "\nThis demonstrates runtime polymorphism using virtual functions." << endl;
    return 0;
}
