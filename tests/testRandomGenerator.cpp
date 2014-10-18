#include <iostream>
#include "randomGenerator.h"

int main(){
    RandomGenerator randGen;
    unsigned int seedVal1 = randGen.getSeed();
    std::cout << "seed from clock: " << seedVal1 << std::endl;
    for(int i=0; i<10; i++)
        std::cout << randGen.getFloat01() << " ";
    std::cout << std::endl;

    randGen.seedWithUInt(seedVal1);
    std::cout << "reseeding with " << seedVal1 << std::endl;
    for(int i=0; i<10; i++)
        std::cout << randGen.getFloat01() << " ";
    std::cout << std::endl;

    std::string str("Lynx on the cactus");
    randGen.seedWithString(str);
    std::cout << "reseeding with string " << str << std::endl;
    std::cout << "generated uint seed is " << randGen.getSeed() << std::endl;
    for(int i=0; i<10; i++)
        std::cout << randGen.getFloat01() << " ";
    std::cout << std::endl;

    return 0;
}
