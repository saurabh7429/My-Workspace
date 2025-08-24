#include <iostream>
#include <string>
using namespace std;

// Class to represent a word and support string operations
class Word {
    string value;

public:
    // Constructor
    Word(const string& v = "") : value(v) {}

    // Overload + for concatenation
    Word operator+(const Word& other) const {
        return Word(value + other.value);
    }

    // Overload == for comparison
    bool operator==(const Word& other) const {
        return value == other.value;
    }

    // Display the word
    void display() const {
        cout << value;
    }
};

int main() {
    string s1, s2;

    cout << "Enter the first word: ";
    cin >> s1;

    cout << "Enter the second word: ";
    cin >> s2;

    Word w1(s1), w2(s2);

    // Concatenation
    Word combined = w1 + w2;
    cout << "\nConcatenated word: ";
    combined.display();
    cout << endl;

    // Comparison
    cout << "Comparison result: ";
    if (w1 == w2)
        cout << "Both words are equal." << endl;
    else
        cout << "The words are not equal." << endl;

    return 0;
}
