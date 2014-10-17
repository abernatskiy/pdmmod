#include <string>
#include <list>
#include "population.h"
#include "reaction.h"

class TotalPopulation
{
private:
    std::list<Population> m_listOfPopulations;
    float m_a; // sum of sigmas

    std::list<Population>::iterator findPopulation(std::string specie);
    void removeSpecie(std::string specie);
    void addSpecie(std::string specie, int initPop);

    std::list<Reaction>::iterator samplePopulation();
    float sampleTime();
public:
    TotalPopulation();
    void stepSimulation();
    ~TotalPopulation();
};
