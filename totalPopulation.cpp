#include "totalPopulation.h"
#include <string>
#include <fstream>
#include <iostream>
#include <list>
#include <sstream>

TotalPopulation::TotalPopulation(std::string source){
    std::string line;
    std::cin.sync_with_stdio(false);
    std::string filename(source);
    std::cout << "Filename is " << filename << std::endl;
    std::ifstream file(filename);
    
    if (file.is_open())
    {
        while (std::getline(file, line))
        {
            std::stringstream   linestream(line);
            std::string         name;
            MOLINT                 population;
            
            linestream >> name >> population;
            m_listOfPopulations.push_back(Population(name, population));
            
        }
    }
    
}

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

