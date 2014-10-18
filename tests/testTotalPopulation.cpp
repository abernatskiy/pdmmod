#include "totalPopulation.h"

int main (int argc, char** argv){
    TotalPopulation tp("populations.txt");
    std::cout << "names and populations:\n" << tp;
    return 0;
}
