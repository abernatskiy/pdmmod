#ifndef __TOTAL_POPULATION_H
#define __TOTAL_POPULATION_H

#include <string>
#include <list>
#include "population.h"
//#include "reaction.h"
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
    float m_deltaA; // the change in full propensity during the current step
    std::list<Population> m_listOfPopulations;

    // Methods
    std::list<Population>::iterator findPopulation(std::string specie);
    void removeSpecie(std::string specie);
    /* takes specie and removes the Population entity corresponding to this Specie, then checks
     * corrects all Population's in TotalPopulation for dependent on this Specie
     */
    void addSpecie(std::string specie, int initPop);
    /* creates and appends Population corresponding to the Specie to TotalPopulation
     * and TODO
     */

    std::list<Reaction>::iterator samplePopulation();
    float sampleTime();

    void readPopulationsFromFile(std::string fileName);
    /* reads the file with two columns, specie ids in column 0 and specie population in column 1,
     * into the internal list of populaitons
     */
};

#endif // __TOTAL_POPULATION_H
