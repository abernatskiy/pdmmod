#include <iostream>
#include "totalPopulation.h"

/*
 *  //DATA
    Time        // total time of simulatios
    Steps       //how many time points we want to keep
    currentTime //time which is being stored
    currentPop  //population at currentTime calculate via calcPopAtTime

    //METHODS
    storePopulations(tp)
        //stores couple of (name, population)
    storeTime(tp)
        //stores time of population
    float writeToFile(step, currentTime, currentPop)
        //writes data into file
        //AND returns next stored time

    float
 *
*/

std::list<Population> storePopulations(TotalPopulation tp);
    //stores a list of entities of class Population
void writeToFile(std::list<Population> currPops, filename);

void writeOrNotTo(float stepLen, float currTime, float prevStep);







