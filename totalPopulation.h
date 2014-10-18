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
private:
    // Attributes

    float m_a; // sum of sigmas, full propensity of the system


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

public:
    // Constructors/Destructors
    TotalPopulation(std::string source);// or maybe not string, IDK how to implement generation from distribution TODO
    /* Can construct the Object from various sources:
     * 1) filename: каждую строчку файла он парсит на строчку (idшник) и int (количество молекул), после чего
     *    добавляет к своему внутреннему листу Population'ов в конец новый Population, коструируемый из строчки и инта
     * 2) Raise an Error so far.
     */

    //Attributes
    std::list<Population> m_listOfPopulations;//private

    // Methods
    void stepSimulation(); // runs one step of a simulation
};
