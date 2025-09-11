//area of rectangle with some constructors and encapsulation
#include<iostream>
using namespace std;

class Rectangle {
    double length, width;

public:
    Rectangle() : length(0), width(0) {}

    Rectangle(double l, double w) : length(l), width(w) {}

    // setters
    void setlength(double l) { if (l >= 0) length = l; }
    void setwidth(double w) { if (w >= 0) width = w; }

    // getters
    double getlength() const { return length; }
    double getwidth() const { return width; }

    // return area
    double area() const { return length * width; }
    double perimeter() const { return 2 * (length + width); }
};

int main()
{
    Rectangle R1, R2;
    R1.setlength(5);
    R1.setwidth(3);
    cout << "length is :" << R1.getlength() << endl;
    cout << "width is :" << R1.getwidth() << endl;
    cout << "Area :" << R1.area() << endl;
    cout << "perimeter :" << R1.perimeter() << endl;

    R2.setlength(2.5);
    R2.setwidth(4.2);
    cout << "length is :" << R2.getlength() << endl;
    cout << "width is :" << R2.getwidth() << endl;
    cout << "Area :" << R2.area() << endl;
    cout << "perimeter :" << R2.perimeter() << endl;

    return 0;
}
