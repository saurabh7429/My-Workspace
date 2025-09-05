// classs and objects
#include<iostream>
using namespace std;
class Ractangle {
    public:
    double length,weidth;
    public:
    void area()
    {
        cout<<"Area of ractangle is "<<length*weidth<<endl;
    }
};
int main()
{
    Ractangle r1,r2;
    r1.length=5;
    r1.weidth=3;
    r1.area();

    r2.length=2.5;
    r2.weidth=4.2;
    r2.area();
    return 0;
}