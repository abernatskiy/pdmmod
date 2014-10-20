#include "relation.h"

Relation::Relation(Specie specI, Specie specJ){
    m_psi = 1.f;
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
