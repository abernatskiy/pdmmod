#ifndef __TOTAL_POPULATION_H
#define __TOTAL_POPULATION_H

#include <string>
#include <list>
#include "population.h"
#include "reaction.h"
#include "randomGenerator.h"

/* Root class:
 * Simulation works by creating a single object of this class, then updating them with stepSimulation().
 */

class TotalPopulation
{
public:
    // Constructors/Destructors
    TotalPopulation(std::string source);
    /* constructs the object from the file listing all initial species and their populations
     */
    // TODO generation from distribution

    // Methods
    void stepSimulation(); // runs one step of a simulation

    // Operator overloads
    friend std::ostream& operator<<(std::ostream& os, const TotalPopulation& pop);
private:
    // Attributes
    float m_t; // current simulation time
    float m_a; // sum of sigmas, full propensity of the system
    std::list<Population> m_listOfPopulations;
    RandomGenerator m_randGen; // TODO organize civilized seeding

    // Methods
    std::list<Population>::iterator findPopulation(std::string specie);
    void removePopulation(std::list<Population>::iterator itToPopToRemove);
    /* takes an iterator to a Population, requests the population to remove all its dependencies
     * and removes the Population from the list
     * Complexity O(n)
     */
    void addPopulation(std::string specie, int initPop);
    /* creates and appends to the list a Population of a specie
     * and builds relations from all preceding populations to the new population
     * Complexity O(n)
     */

    void computeTotalPropensity();
    /* recomputes the total propensity of the population
     * Complexity O(n)
     */

    Reaction sampleReaction();
    /* finds out which reaction happens next, according to the Gillespie distribution
     * computed using Partial-propensity Direct Method
     * Complexity O(n)
     */
    float sampleTime();
    /* finds out when the next reaction happens
     * Complexity O(1)
     */

    void addPopulationsFromFile(std::string fileName);
    /* reads the file with two columns, specie ids in column 0 and specie population in column 1,
     * into the internal list of populaitons
     */
};

#endif // __TOTAL_POPULATION_H
