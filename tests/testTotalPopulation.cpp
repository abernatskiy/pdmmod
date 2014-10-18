#include "totalPopulation.h"

int main (int argc, char** argv){
    TotalPopulation tp("populations.txt");
    std::list<Population>::iterator pops_it=tp.m_listOfPopulations.begin();
    std::cout << "names and populations:\n";
    for (pops_it = tp.m_listOfPopulations.begin(); pops_it != tp.m_listOfPopulations.end(); pops_it++)
        std::cout << " " << *pops_it << std::endl;;
    
    // Here we should have something like
    // fileObject = open("initialPopualtionFileName", "r");
    // totalPopulation totPop = TotalPopulation(fileObject);

    return 0;
}
