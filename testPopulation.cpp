#include "population.h"
#include <iostream>
#include <string>

int main(int argc, char** argv){
    Population pop(std::string("10"), 50);
    std::cout << pop << "\n";
    return 0;
}
