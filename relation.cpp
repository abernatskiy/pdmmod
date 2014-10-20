#include <iostream>
#include "relation.h"

Relation::Relation(Specie specI, Specie specJ, MOLINT popSpecJ){
//    std::cout << "Relation: constructing, from " << specI << " (population " << popSpecI << ") to " << specJ << std::endl;
    m_fromSpId = specI.m_id;
    m_listOfReactions = specI.reactions(specJ);
    update(popSpecJ);
}

Reaction Relation::sampleReaction(float remainingJuice){
    Reaction reac("a", 1, "3", 1, 5.f);
    reac.addProduct("4", 2);
    return reac;
}

void Relation::update(MOLINT newNToSp){
    m_psi = 0.f;
    for( auto itRea = m_listOfReactions.begin(); itRea != m_listOfReactions.end(); itRea++){
        itRea->computePartialPropensity(m_fromSpId, newNToSp);
        m_psi += itRea->m_partialPropensity;
    }
}

std::ostream& operator<<(std::ostream& os, const Relation& rel){
    os << "Relation object from " << rel.m_fromSpId << std::endl;
    for( auto itReac = rel.m_listOfReactions.begin(); itReac != rel.m_listOfReactions.end(); itReac++ )
        os << " " << (*itReac) << std::endl;
    return os;
}
