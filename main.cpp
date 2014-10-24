#include "totalPopulation.h"
#include "output.h"

int main (int argc, char** argv){
    float totalTime = std::atoi((std::string(argv[1])).c_str());
    int steps = std::atoi((std::string(argv[2])).c_str());
    float step = totalTime/(float ) steps;
    TotalPopulation tp("populations.txt");
    std::cout << "before stepping:\n"<< tp;
    std::list<Population> currentPops = storePopulations(tp);
    float currTime = 0.f;
    float currStep = 0.f;
    //debugging ->
    std::cout << totalTime << std::endl;
    std::cout << steps << std::endl;
    for (auto pops_it = currentPops.begin(); pops_it != currentPops.end(); pops_it++)
        if( pops_it->m_specie.m_id != "" )
            std::cout << "test " << "  " << pops_it->m_specie.m_id << "  " << pops_it->m_n << std::endl;
    //<- debugging
    while(true){
        tp.stepSimulation();
        std::cout << "after stepping:\n" << tp;
    }
    return 0;
}
