#include <iostream>
#include <cstdlib>
#include "relation.h"

Relation::Relation(Specie specI, Specie specJ, MOLINT popSpecJ){
//    std::cout << "Relation: constructing, from " << specI << " (population " << popSpecI << ") to " << specJ << std::endl;
    m_fromSpId = specI.m_id;
    m_listOfReactions = specI.reactions(specJ);
    update(popSpecJ);
}

Reaction Relation::sampleReaction(PROPFLOAT remainingJuice){
    PROPFLOAT localJuice = remainingJuice;
    for( auto itRea = m_listOfReactions.begin(); itRea != m_listOfReactions.end(); itRea++ ){
        if( m_fromSpId != itRea->m_pPWRespectTo ){
            std::cout << "Reaction: Found a reaction with partial propensity calculated with respect to a wrong specie. Something is wrong here. Exiting.\n";
            exit(EXIT_FAILURE);
        }

        localJuice -= itRea->m_partialPropensity;
        if( localJuice < 0.f )
            return *itRea;
    }
/*  See lines 28-34 of population.cpp for explanation of what's going on in this function below this line */

//    std::cout << "WARNING: Relation-level sampling failed, perhaps due to the numerical error. Returning an invalid reaction to cause resampling.\n";
//    std::cout << std::scientific << "Sampled with remaining juice of " << remainingJuice << ", sum of partial propensities of " << m_psi << ", difference " << remainingJuice - m_psi << std::endl;

    Reaction invalidReaction("", -100, "", -100, 1000000.0);
    return invalidReaction;

////  Older, less precise solution to the problem of numerical errors at sampling phase
//    auto itRea = m_listOfReactions.end();
//    itRea--;
//    return *itRea;
}

void Relation::update(MOLINT newNToSp){
    m_psi = 0.f;
    for( auto itRea = m_listOfReactions.begin(); itRea != m_listOfReactions.end(); itRea++ ){
        itRea->computePartialPropensity(m_fromSpId, newNToSp);
        m_psi += itRea->m_partialPropensity;
    }
}

std::ostream& operator<<(std::ostream& os, const Relation& rel){
    os << "Relation from " << rel.m_fromSpId << std::endl;
    os << "Sum of partial propensities (Psi) is " << rel.m_psi << std::endl;
    for( auto itReac = rel.m_listOfReactions.begin(); itReac != rel.m_listOfReactions.end(); itReac++ )
        os << "  " << (*itReac);
    return os;
}
