#ifndef __RELATION_H
#define __RELATION_H

#include <list>
//#include "reaction.h"
#include "specie.h"

/* This class represents the relation from
 * a population of some species SI to a population
 * of other species SJ. It contains a list of all
 * reactions that can happen between SI and SJ,
 * together with the sum of partial propensities
 * of the reactions
 */

class Relation
{
public:
    // Constructors
    Relation(Specie specI, Specie specJ);
    bool isEmpty(){return m_listOfReactions.empty();};

private:
    // Attributes
    std::list<Reaction> m_listOfReactions;
    float m_psi;
};

#endif // __RELATION_H
