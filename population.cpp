#include <iostream>
#include <cstdlib>
#include "population.h"

Population::Population(std::string id, int initPop){
    m_specie = Specie(id);
    m_n = (MOLINT) initPop;
    m_ksi = 0.f;
}

Reaction Population::sampleReaction(float remainingJuice){
    std::cout << "Sampling reaction from the following population:\n" << (*this) << std::endl;
    float localJuice = remainingJuice;
    for( auto itRel = m_listOfRelations.begin(); itRel != m_listOfRelations.end(); itRel++ ){
        localJuice -= itRel->m_psi;
        if( localJuice < 0.f ){
            float juiceRemainingAfterLocalSampling = localJuice + itRel->m_psi;
            return itRel->sampleReaction(juiceRemainingAfterLocalSampling);
        }
    }
    std::cout << "ERROR: Population-level sampling failed. Full propensity m_a is likely broken.\n";
    exit(EXIT_FAILURE);
}

void Population::update(int moleculesAdded){
    // note that the argument may negative
    std::cout << "Population::update called on " << (*this) << " with molecular change of " << moleculesAdded << std::endl;

    m_n += moleculesAdded;
}

void Population::buildRelation(std::list<Population>::reverse_iterator itOther){
    std::cout << "Building relation\nof " << (*this) << "\nto " << (*itOther) << std::endl;
}

void Population::removeDependentRelations(){
    std::cout << "Population::removeDependentRelations called on " << (*this) << std::endl;
}

void Population::removeRelation(std::list<Relation>::iterator itReaction){
    std::cout << "Population::removeRelation called on " << (*this) << " to remove " << *itReaction << std::endl;
}

std::ostream& operator<<(std::ostream& os, const Population& pop){
    os << "Population of specie " << pop.m_specie << " with " << pop.m_n << " molecules in it";
    return os;
}
