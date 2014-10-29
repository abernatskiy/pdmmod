#include <iostream>
#include "output.h"

std::list<Population> storePopulations(TotalPopulation tp){
    std::list<Population> currentPops = tp.m_listOfPopulations;
    
    return currentPops;
}

void writeOrNotTo(float stepLen, float currTime, float prevStep){
    //if stepLen = 0, no questions: write every stepLen
    writeToFile(std::list<Population> currPops, filename)
}