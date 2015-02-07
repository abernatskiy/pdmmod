#ifndef __OUTPUT_H
#define __OUTPUT_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
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

    void writeHeaderToFile(totalPopulation, totalTime, period, filename, file)
        // Writes a header of the output file. Format:
        // line 0: # Model: <modelName>
        // line 1: # <parameterName0>=<value0> <parameterName1>=<value1> ...
        // line 2: # TotalTime=<T> RecordPeriod=<tau> Filename=<filename>
        // where modelName is the name of the model as indicated in the Specie
        // object associated with the first population in totalPopulation,
        // parameters described by line 1 are the model parameters from parameters.ini, and
        // parameters described by line 2 are command-line parameters: T is the total time
        // of the simulation (0 if indefinite), tau is the simulation time between records,
        // filename is the name of the original output file. All times are in seconds.
 *
*/

std::string storePopulations(TotalPopulation* tp);
    //stores a list of entities of class Population

void writeHeaderToFile(TotalPopulation* tp, int argc, char** argv, std::ofstream* myfile);
void writeToFile(std::string populations, float time, std::ofstream* myfile);
std::string convToString(TotalPopulation* tp);
std::string writeOrNotTo(float stepLen, TotalPopulation* tp, float prevStep, std::string prevPops, std::ofstream* myfile);
int closeFile(std::string filename);
int openFile(std::string filename);
float getPrevStep(float stepLen, float prevStep, float currTime);

#endif // __OUTPUT_H
