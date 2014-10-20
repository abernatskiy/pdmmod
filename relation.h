#ifndef __RELATION_H
#define __RELATION_H

#include <list>
#include "reaction.h"
#include "specie.h"
#include "types.h"

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
    // Attributes
    float m_psi;

    // Constructors
    Relation(Specie specI, MOLINT popSpecI, Specie specJ);

    // Methods
    Reaction sampleReaction(float remainingJuice);
    bool isEmpty(){return m_listOfReactions.empty();};

    // Operator overloads
    friend std::ostream& operator<<(std::ostream& os, const Relation& rel);
private:
    // Attributes
    std::list<Reaction> m_listOfReactions;
};

#endif // __RELATION_H
