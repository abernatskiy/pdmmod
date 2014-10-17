#include <string>
#include <list>
#include "population.h"
//#include "reaction.h"

/* Root class:
 * Simulation works by creating a single object of this class, then updating them with stepSimulation().
 */

class TotalPopulation
{
private:
    // Attributes
    std::list<Population> m_listOfPopulations;
    float m_a; // sum of sigmas, full propensity of the system

    std::list<Population>::iterator findPopulation(std::string specie);

    // Methods
    void removeSpecie(std::string specie);
        /* takes specie and remomes the Population entity corresponding to this Specie
        also checks all the Population's in TotalPopulation for the dependencies from this Specie and corrects them */
    void addSpecie(std::string specie, int initPop);
        /* creates and append Population corresponding to the Specie to TotalPopulation
         * and TODO
         */
    std::list<Reaction>::iterator samplePopulation();
    float sampleTime();
public:
    // Constructors/Destructors
    TotalPopulation(std::string source);// or maybe not string, IDK how to implement generation from distribution TODO
    /* Can construct the Object from various sources:
     * 1) filename: каждую строчку файла он парсит на строчку (idшник) и int (количество молекул), после чего
     *    добавляет к своему внутреннему листу Population'ов в конец новый Population, коструируемый из строчки и инта
     * 2) Raise an Error so far.
     */

    // Methods
    void stepSimulation(); // runs one step of a simulation
};
