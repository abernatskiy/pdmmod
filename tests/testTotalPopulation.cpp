#include "totalPopulation.h"

int main (int argc, char** argv){
    TotalPopulation tp("populations.txt");
    std::cout << "before stepping:\n"<< tp;
    tp.stepSimulation();
    std::cout << "after stepping:\n" << tp;
    while(true){
    tp.stepSimulation();
    std::cout << "after stepping:\n" << tp;
    }
    return 0;
}
