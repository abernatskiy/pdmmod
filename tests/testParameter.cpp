#include "parameter.h"
#include <stdio.h>
#include <iostream>

int main(int argc, char** argv){
    Parameter a(0.0f);
    printf("getFloat: %f\n",a.getFloat());
    std::cout << "getType: " << a.getType()<<"\n";
}

