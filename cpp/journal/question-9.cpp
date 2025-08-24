#include <iostream>
#include <stack>
#include <algorithm>
#include <cctype>
using namespace std;

// Function to return precedence of operators
int precedence(char c) {
    if (c == '^') return 3;
    if (c == '*' || c == '/') return 2;
    if (c == '+' || c == '-') return 1;
    return -1;
}

// Check if operator is right associative
bool isRightAssociative(char op) {
    return (op == '^');
}

// Convert infix to postfix (helper function)
string infixToPostfix(const string& exp) {
    stack<char> st;
    string result;

    for (char c : exp) {
        if (isalnum(c)) {
            result += c;  // Operand goes directly to result
        }
        else if (c == '(') {
            st.push(c);
        }
        else if (c == ')') {
            while (!st.empty() && st.top() != '(') {
                result += st.top();
                st.pop();
            }
            if (!st.empty()) st.pop(); // Pop '('
        }
        else { // Operator
            while (!st.empty() && (
                precedence(st.top()) > precedence(c) ||
                (precedence(st.top()) == precedence(c) && !isRightAssociative(c))
            )) {
                if (st.top() == '(') break;
                result += st.top();
                st.pop();
            }
            st.push(c);
        }
    }
    while (!st.empty()) {
        result += st.top();
        st.pop();
    }
    return result;
}

// Convert infix to prefix
string infixToPrefix(string infix) {
    // Step 1: Reverse infix and swap '(' with ')'
    reverse(infix.begin(), infix.end());
    for (char& c : infix) {
        if (c == '(') c = ')';
        else if (c == ')') c = '(';
    }

    // Step 2: Get postfix of reversed infix
    string postfix = infixToPostfix(infix);

    // Step 3: Reverse postfix to get prefix
    reverse(postfix.begin(), postfix.end());
    return postfix;
}

int main() {
    string infix;
    cout << "Enter an infix expression (no spaces): ";
    cin >> infix;

    string prefix = infixToPrefix(infix);
    cout << "Prefix expression: " << prefix << endl;

    cout << "Conversion complete!" << endl;
    return 0;
}
