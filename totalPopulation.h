#include <string>
#include <list>
#include "population.h"
//#include "reaction.h"

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
//    TotalPopulation(); // parameter-less constructor is supposed to never be required
    void stepSimulation();
//    ~TotalPopulation(); // default compiler-defined destructor should be fine, as long as we do not add any pointers here
};
