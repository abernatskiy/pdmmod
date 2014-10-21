#include "population.h"
#include <iostream>
#include <string>

int main(int argc, char** argv){
    Population pop0(std::string("10"), 50);
    Population pop1(std::string("a"), 100);
    std::cout << "Populations before any relations were built:\n" << pop0 << std::endl << pop1 << std::endl;

    std::list<Population> listPop;
    listPop.push_back(pop0);
    auto it0 = listPop.begin();
    auto it1 = listPop.rbegin();
    std::cout << "\nBuilding relation from pop0 to itself...\n";
    it0->buildRelation(it0, it1);
    std::cout << "New population:\n" << *it0 << std::endl;

    listPop.push_back(pop1);
    it1 = listPop.rbegin();
    std::cout << "\nBuilding relation from pop0 to pop1...\n";
    it0->buildRelation(it0, it1);
    std::cout << "New populations:\n" << *it0 << std::endl << *it1 << std::endl;

    it0++;
    std::cout << "\nBuilding relation from pop1 to itself...\n";
    it0->buildRelation(it0, it1);
    it0--;
    std::cout << "New populations:\n" << *it0 << std::endl << *it1 << std::endl;

    std::cout << "\nSampling reactions from pop0:\n";
    for( float ju = 0.0001; ju <= 0.0015; ju+=0.0001 )
        std::cout << "  juice: " << ju*(it0->m_ksi) << " reaction: " << it0->sampleReaction(ju*(it0->m_ksi)) << std::endl;
    std::cout << "  juice: " << 0.5*(it0->m_ksi) << " reaction: " << it0->sampleReaction(0.5*(it0->m_ksi)) << std::endl;

    std::cout << "\nTesting update: updating pop1 to contain 99 molecules less\n";
    it1->update(-99);
    std::cout << "New populations:\n" << *it0 << std::endl << *it1 << std::endl;
    it0->update(-25);
    std::cout << "After removing 25 molecules from pop0:\n" << *it0 << std::endl << *it1 << std::endl;
    it1->update(-1);
    std::cout << "After removing 1 molecule from pop1:\n" << *it0 << std::endl << *it1 << std::endl;

    std::cout << "\nTesting population deletion: removing dependent relations from pop1\n";
    it1->removeDependentRelations();
    std::cout << "New populations:\n" << *it0 << std::endl << *it1 << std::endl;

    return 0;
}
