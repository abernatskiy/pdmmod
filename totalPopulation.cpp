#include "totalPopulation.h"

std::list<Population>::iterator TotalPopulation::findPopulation(std::string specie){
    return m_listOfPopulations.begin();
}

void TotalPopulation::removeSpecie(std::string specie){
}

void TotalPopulation::addSpecie(std::string specie, int initPop){
}

std::list<Reaction>::iterator TotalPopulation::samplePopulation(){
    std::list<Reaction> testList;
    return testList.begin();
}

void TotalPopulation::stepSimulation(){
    
}

