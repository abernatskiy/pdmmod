#include "relation.h"

Relation::Relation(Specie specI, Specie specJ){

}

std::ostream& operator<<(std::ostream& os, const Relation& rel){
    os << "Relation object\n";
    for( auto itReac = rel.m_listOfReactions.begin(); itReac != rel.m_listOfReactions.end(); itReac++ )
        os << " " << (*itReac) << std::endl;
    return os;
}
