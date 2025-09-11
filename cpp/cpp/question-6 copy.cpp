/*Write a program to create an event class, create dynamic objects of
event class, and release the memory of the created object before
program terminates.*/

#include <iostream>
#include <string>
using namespace std;

class Event {
    string name;
    string date;

public:
    void input() {
        cout << "Enter event name: ";
        getline(cin, name);
        cout << "Enter event date: ";
        getline(cin, date);
    }
    void display() const {
        cout << "Event: " << name << ", Date: " << date << endl;
    }
};

int main() {
    int n;
    cout << "How many events do you want to add? ";
    cin >> n;
    cin.ignore(); // Clear newline

    // Dynamically allocate array of Event pointers
    Event** events = new Event*[n];

    // Input event details
    for (int i = 0; i < n; ++i) {
        cout << "\n--- Event " << (i + 1) << " ---" << endl;
        events[i] = new Event();
        events[i]->input();
    }

    // Display event details
    cout << "\n--- Event Details ---" << endl;
    for (int i = 0; i < n; ++i) {
        events[i]->display();
    }

    // Free allocated memory
    for (int i = 0; i < n; ++i) {
        delete events[i];
    }
    delete[] events;

    return 0;
}
