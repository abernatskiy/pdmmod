#include <iostream>
#include "randomGenerator.h"

int main(){
    RandomGenerator randGen;
    std::cout << randGen.getSeed() << std::endl;
//    randGen.seedWithC
    return 0;
}
