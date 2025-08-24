#include <iostream>
using namespace std;

class Rectangle {
    int length, width, height;

public:
    // Default Constructor
    Rectangle() {
        length = width = height = 1;
        cout << "Default Constructor Called!" << endl;
    }

    // Parameterized Constructor
    Rectangle(int l, int w, int h) {
        length = l;
        width = w;
        height = h;
        cout << "Parameterized Constructor Called!" << endl;
    }

    // Copy Constructor
    Rectangle(const Rectangle &r) {
        length = r.length;
        width = r.width;
        height = r.height;
        cout << "Copy Constructor Called!" << endl;
    }

    // Function to calculate area
    int area() {
        return length * width;
    }

    // Function to calculate volume
    int volume() {
        return length * width * height;
    }

    // Destructor
    ~Rectangle() {
        cout << "Destructor Called for object with dimensions: "
             << length << " x " << width << " x " << height << endl;
    }
};

int main() {
    int l, w, h;

    // Using default constructor
    Rectangle r1;
    cout << "Area: " << r1.area() << endl;
    cout << "Volume: " << r1.volume() << endl;

    cout << "--------------------------" << endl;

    // Taking user input for parameterized constructor
    cout << "Enter length, width and height: ";
    cin >> l >> w >> h;

    Rectangle r2(l, w, h);
    cout << "Area: " << r2.area() << endl;
    cout << "Volume: " << r2.volume() << endl;

    cout << "--------------------------" << endl;

    // Using copy constructor
    Rectangle r3(r2);
    cout << "Area: " << r3.area() << endl;
    cout << "Volume: " << r3.volume() << endl;

    return 0;
}
