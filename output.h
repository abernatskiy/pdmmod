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

std::string storePopulations(TotalPopulation tp);
    //stores a list of entities of class Population

std::string writeToFile(float currTime, std::list<Population> currPops, std::string filename);

std::string writeOrNotTo(float stepLen, TotalPopulation tp, float prevStep, std::string prevPops, std::string filename);
int closeFile(std::string filename);
int openFile(std::string filename);
float getPrevStep(float stepLen, float prevStep, float currTime);





