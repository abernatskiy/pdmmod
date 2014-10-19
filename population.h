#ifndef __POPULATION_H
#define __POPULATION_H

#include <string>
#include <list>
#include <tuple>
#include <iostream>
#include "types.h"
#include "reaction.h"
#include "specie.h"
#include "relation.h"

/* Class representing a population of a specie.
 */

#define relationAddr_t std::tuple<std::list<Population>::iterator, std::list<Relation>::iterator>
/* Defines a type for records of the lookup table listing dependents (a.k.a. U3). Each record contains an
 * iterator to the population and an iterator to the relationship of that population.
 */

class Population
{
public:
    // Constructors
    Population(std::string id, MOLINT initPop);

    // Methods
//    void removeReaction(std::list<Reaction>::iterator ptrReaction);
    void buildRelation(std::list<Population>::iterator itOther);
    /* Checks if this Population's Specie can react with *ptrOther's and appends
     * Relationship object to its internal list of relationships. Returns
     * iterator to the Relationship object if there were some possible
     * reactions and NULL otherwise.
     */
    float computeKsi(){return 0.f;};
    float updateKsi(){return 0.f;};

    // Operator overloads
    friend std::ostream& operator<<(std::ostream& os, const Population& pop);

private:
//public:
    // Attributes
    MOLINT m_n;
    Specie m_specie;
    std::list<relationAddr_t> m_depenedents;
    float m_lambda;
    float m_ksi;
};

#endif // __POPULATION_H
