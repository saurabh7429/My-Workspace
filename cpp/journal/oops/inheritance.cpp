#include <iostream>
using namespace std;

// Rectangle class (base)
class Rectangle {
protected: // promote to protected for derived class access
    double length{0}, width{0};
public:
    Rectangle() = default;
    Rectangle(double l, double w): length(l), width(w) {}

    // Setters with validation
    void setLength(double l) { length = l >= 0 ? l : 0; }
    void setWidth(double w) { width = w >= 0 ? w : 0; }

    // Getters
    double getLength() const { return length; }
    double getWidth() const { return width; }

    double area() const { return length * width; }
};

// Box class (derived from Rectangle)
class Box : public Rectangle {
    double height{0};
public:
    Box() = default;
    Box(double l, double w, double h) : Rectangle(l, w) {
        setHeight(h); // use setter for validation
    }

    // Setter with validation
    void setHeight(double h) { height = h >= 0 ? h : 0; }

    // Getter
    double getHeight() const { return height; }

    // Volume uses Rectangle::area()
    double volume() const { return area() * height; }
};

int main() {
    // Default box
    Box b1;
    cout << "Default box volume: " << b1.volume() << endl;

    // Parameterized box
    Box b2(4, 3, 5);
    cout << "Box(4,3,5) volume: " << b2.volume() << endl;

    // Bonus: Try to set negative height
    b2.setHeight(-10);
    cout << "After setting negative height, volume: " << b2.volume() << endl;

    return 0;
}