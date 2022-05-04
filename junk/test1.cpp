#include <stdio.h>
#include <malloc.h>
#include <memory>
#include <cmath>

struct Point; int pow_2(int x); float root(int x); float distance(std::shared_ptr<Point> p1,std::shared_ptr<Point> p2); int main();
struct Point{
int x;
int y;
};
int pow_2(int x){
return x * x;
}
float root(int x){
return sqrt ( x ) ;
}
float distance(std::shared_ptr<Point> p1,std::shared_ptr<Point> p2){
int r1 = pow_2(p1->x - p2->x);
int r2 = pow_2(p1->y - p2->y);
return root(r1 + r2);
}
int main(){
using namespace std ;
auto p1 = shared_ptr < Point > ( new Point { 4 , 6 , } ) ;
auto p2 = shared_ptr < Point > ( new Point { 1 , 2 , } ) ;
float d = distance(p1,p2);
printf ( "%.3f" , d ) ;
}