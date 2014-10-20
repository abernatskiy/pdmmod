#include <iostream>
#include <cstdlib>
#include "population.h"

Population::Population(std::string id, int initPop){
    m_specie = Specie(id);
    m_n = (MOLINT) initPop;
    m_ksi = 0.f;
    m_lambda = 0.f;
}

Reaction Population::sampleReaction(float remainingJuice){
    std::cout << "Sampling reaction from the following population:\n" << (*this) << std::endl;
    if( m_n <= 0 ){
        std::cout << "ERROR: Sampling from a population of " << m_n << " molecules. This shouldn't happen. Exiting.\n";
        exit(EXIT_FAILURE);
    }

    float localJuice = remainingJuice/((float) m_n);
    for( auto itRel = m_listOfRelations.begin(); itRel != m_listOfRelations.end(); itRel++ ){
        localJuice -= itRel->m_psi;
        if( localJuice < 0.f ){
            float juiceRemainingAfterLocalSampling = localJuice + itRel->m_psi;
            return itRel->sampleReaction(juiceRemainingAfterLocalSampling);
        }
    }
    std::cout << "ERROR: Population-level sampling failed. Full propensity of population m_ksi is likely broken.\n";
    exit(EXIT_FAILURE);
}

void Population::update(int moleculesAdded){
    // note that the argument may negative
    std::cout << "Population::update called on " << (*this) << " with molecular change of " << moleculesAdded << std::endl;

    m_n += moleculesAdded;
}

void Population::buildRelation(std::list<Population>::iterator itSelf, std::list<Population>::reverse_iterator itOther){
//    std::cout << "Building relation\nof " << (*this) << "to " << (*itOther) << std::endl;

    Relation newRel(m_specie, m_n, itOther->m_specie);
    if( newRel.isEmpty() ){
        std::cout << "Done building empty relation from " << m_specie.m_id << " to " << itOther->m_specie.m_id << std::endl;
        return;
    }

    std::cout << "Nonempty relation found from " << m_specie.m_id << " to " << itOther->m_specie.m_id << ": " << newRel << std::endl;

    m_lambda += newRel.m_psi;
    m_ksi = m_lambda*((float) m_n);
    m_listOfRelations.push_back(newRel);
    auto itToNewRelation = m_listOfRelations.end();
    itToNewRelation--;
    itOther->addDependentRelation(itSelf, itToNewRelation);

    std::cout << "Done building relation\n\n";
}

void Population::addDependentRelation(std::list<Population>::iterator itPop, std::list<Relation>::iterator itRel){
    relationAddr_t relRecord(itPop, itRel);
    m_dependentRelations.push_back(relRecord);
}

void Population::removeDependentRelations(){
    std::cout << "Population::removeDependentRelations called on " << (*this) << std::endl;
}

void Population::removeRelation(std::list<Relation>::iterator itReaction){
    std::cout << "Population::removeRelation called on " << (*this) << " to remove " << *itReaction << std::endl;
}

std::ostream& operator<<(std::ostream& os, const Population& pop){
    os << "Population of specie " << pop.m_specie << " with " << pop.m_n << " molecules in it\n";
    os << "Relations: ";
    for( auto itRel = pop.m_listOfRelations.begin(); itRel != pop.m_listOfRelations.end(); itRel++ )
        os << (*itRel);
    os << "Dependent relations: " << pop.m_dependentRelations.size() << " pc\n";
    return os;
}
