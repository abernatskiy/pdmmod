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

/* Class representing a population of molecules of a specie.
 */

#define relationAddr_t std::tuple<std::list<Population>::iterator, std::list<Relation>::iterator>
/* Defines a type for records of the lookup table listing dependents (a.k.a. U3). Each record contains an
 * iterator to the population and an iterator to the relationship of that population.
 */

class Population
{
public:
    // Attributes
    float m_ksi;
    MOLINT m_n;
    Specie m_specie;

    // Constructors
    Population(std::string id, MOLINT initPop);

    // Methods
    void update(int molNoDifference){};
    Reaction sampleReaction(float remainingJuice);
    /* Take the remaining juice from the higher level sampler and subsamples
     * within the Population. See comment to TotalPopulation::sampleReaction()'s
     * implementation in totalPopulation.cpp for details
     */
    void removeDependentRelations(){};
    void removeRelation(std::list<Relation>::iterator itReaction);
    void buildRelation(std::list<Population>::reverse_iterator itOther);
    /* Checks if this Population's Specie can react with itOther's and appends
     * Relation object to its internal list of relationships (if the Relation
     * object is not empty). Updates the intermediate sums of propensities
     * accordingly.
     */
    void computeKsi();
    void updateKsi();

    // Operator overloads
    friend std::ostream& operator<<(std::ostream& os, const Population& pop);

private:
//public:
    // Attributes
    std::list<Relation> m_relations;
    std::list<relationAddr_t> m_depenedentRelations;
    float m_lambda;
};

#endif // __POPULATION_H
