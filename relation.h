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
    Relation(Specie fromSp, Specie toSp, MOLINT popToSp);
    /* fromSp is the owner, Specie object of the Populaiton which keeps this Relation
     * toSp is the Specie, on the population of which partial propensities may depend
     * popToSp is the population of the latter
     */

    // Methods
    Reaction sampleReaction(float remainingJuice);
    void update(MOLINT newNToSp);
    bool isEmpty(){return m_listOfReactions.empty();};

    // Operator overloads
    friend std::ostream& operator<<(std::ostream& os, const Relation& rel);
private:
    // Attributes
    std::string m_fromSpId;
    std::list<Reaction> m_listOfReactions;
};

#endif // __RELATION_H
