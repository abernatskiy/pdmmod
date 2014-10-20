#include "population.h"

Population::Population(std::string id, int initPop){
    m_specie = Specie(id);
    m_n = (MOLINT) initPop;
    m_ksi = 1.f;
}

Reaction Population::sampleReaction(float remainingJuice){
    std::cout << "Sampling reaction from the following population:\n" << (*this) << std::endl;
    Reaction reac("a", 1, "3", 1, 5.f);
    reac.addProduct("4", 2);
    return reac;
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
