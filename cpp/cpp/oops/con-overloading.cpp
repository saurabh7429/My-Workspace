//area of rectangle with some constructors and encapsulation
#include<iostream>
using namespace std;

class Rectangle {
    double length, width;

public:
    Rectangle() : length(0), width(0) {}

    Rectangle(double l, double w=1) : length(l), width(w) {}
    
    // setters
    void setlength(double l) { if (l >= 0)  length = l; }
    void setwidth(double w) { if (w >= 0) width = w; }

    // getters
    double getlength() const { return length; }
    double getwidth() const { return width; }

    // return area
    double area() const { return length * width; }
    double perimeter() const { return 2 * (length + width); }
};

int main() {
    Rectangle r1;
    cout << "Rectangle r1 (default): " << r1.getlength() << " x " << r1.getwidth() << endl;
    cout << "Area: " << r1.area() << ", Perimeter: " << r1.perimeter() << endl << endl;

    Rectangle r2(5);
    cout << "Rectangle r2 (Rectangle(5)): " << r2.getlength() << " x " << r2.getwidth() << endl;
    cout << "Area: " << r2.area() << ", Perimeter: " << r2.perimeter() << endl << endl;

    Rectangle r3(2.5, 4.2);
    cout << "Rectangle r3 (Rectangle(2.5, 4.2)): " << r3.getlength() << " x " << r3.getwidth() << endl;
    cout << "Area: " << r3.area() << ", Perimeter: " << r3.perimeter() << endl << endl;

    r1.setlength(7);
    r1.setwidth(3);
    cout << "Rectangle r1 after setters: " << r1.getlength() << " x " << r1.getwidth() << endl;
    cout << "Area: " << r1.area() << ", Perimeter: " << r1.perimeter() << endl;

    return 0;
}
