#include <iostream>
#include "relation.h"

Relation::Relation(Specie specI, MOLINT popSpecI, Specie specJ){
    std::cout << "Relation: constructing, from " << specI << " (population " << popSpecI << ") to " << specJ << std::endl;
    m_listOfReactions = specI.reactions(specJ);
    std::cout << "Relation: list of reactions obtained\n";
    m_psi = 0.f;
    for( auto itRea = m_listOfReactions.begin(); itRea != m_listOfReactions.end(); itRea++){
        std::cout << "Computing propensity for reaction " << (*itRea) << std::endl;
        itRea->computePartialPropensity(specI.m_id, popSpecI);
        m_psi += itRea->m_partialPropensity;
    }
}

Reaction Relation::sampleReaction(float remainingJuice){
    Reaction reac("a", 1, "3", 1, 5.f);
    reac.addProduct("4", 2);
    return reac;
}

std::ostream& operator<<(std::ostream& os, const Relation& rel){
    os << "Relation object\n";
    for( auto itReac = rel.m_listOfReactions.begin(); itReac != rel.m_listOfReactions.end(); itReac++ )
        os << " " << (*itReac) << std::endl;
    return os;
}
