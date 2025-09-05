//area of rectangle with some constructora and encapsulation
#include<iostream>
using namespace std;

class Rectangle {
    double length,weidth;

    public:
    Rectangle(): length(0) , weidth(0) {}

    Rectangle(double l,double w) : length(l), weidth(w) {}

    //setters
    void setlength(double l) { if (l>=0) length = l; }
    void setweidth(double w) { if (w>=0) weidth = w; }
    
    //getters
    int getlength() const { return length; }
    int getweidth() const { return weidth; }

    //return area
    int area() const { return length*weidth; }
};
int main()
{
    // double l,w;
    Rectangle R;
    R.setlength(5);
    R.setweidth(3);

    cout<<"length is :"<<R.getlength() <<endl;
    cout<<"weidth is :"<<R.getweidth() <<endl;
    cout<<"Area :"<<R.area() <<endl;
    return 0;
}
