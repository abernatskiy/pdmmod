#ifndef __DATALOGGER_H
#define __DATALOGGER_H

#include <fstream>
#include <string>

#include "totalPopulation.h"

/* // TODO - rewrite for the new API
 *  DATA
    Time        // total time of simulatios
    Steps       //how many time points we want to keep
    currentTime //time which is being stored
    currentPop  //population at currentTime calculate via calcPopAtTime

    METHODS
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

class DataLogger
{
public:
    DataLogger(){};
    DataLogger(TotalPopulation* tp, float timeStep, float totalTime, std::string fileName); // will cause the program to fail if called with bad arguments
    DataLogger(TotalPopulation* tp, int recordingPeriod, int totalReactions, std::string fileName); // will cause the program to fail if called with bad arguments
    ~DataLogger();
    void makeHeader(int argc, char** argv);
    bool makeRecords();
    void makePostsimulationRecords();

private:
    TotalPopulation* m_tp;
    int m_type;
    float m_timeStep;
    float m_totalTime;
    int m_recPeriod;
    int m_numSteps;
    int m_i;
    float m_prevTime;
    std::string m_prevPop;
    std::ofstream m_file;

    bool checkTimes(float timeStep, float totalTime); // makes the app exit with error as soon as totalTime is not float-divisible by timeStep
    bool checkReacNum(int recordingPeriod, int totalReactions); // makes the app exit with error as soon as totalReactions is not divisible by recordingPeriod
    void memorizePopulations(); // stores a list of entities of class Population from the saved pointer to TotalPopulation into the internal representation string
    void makeRecord(float time);
};

#endif // __DATALOGGER_H
