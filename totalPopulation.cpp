#include "totalPopulation.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <cmath>

TotalPopulation::TotalPopulation(std::string source){
    m_t = 0.f;

    m_listOfPopulations.push_back(Population(std::string(""), 1)); // adding "vacuum"
    readPopulationsFromFile(source);

    m_a = 0.f;
    m_deltaA = 0.f;
    for(auto popIt1 = m_listOfPopulations.begin(); popIt1 != m_listOfPopulations.end(); popIt1++){
        for(auto popIt2 = popIt1; popIt2 != m_listOfPopulations.end(); popIt2++)
            popIt1->buildRelation(popIt2);
            // small optimization is possible here: "vacuum" only reacts with itself
        popIt1->computeKsi();
        m_a += popIt1->m_ksi;
    }
}

void TotalPopulation::stepSimulation(){
    Reaction reac = sampleReaction();
    m_t += sampleTime();
}

std::ostream& operator<<(std::ostream& os, const TotalPopulation& pop){
    os << "Current simulation time: " << pop.m_t << std::endl;
    os << "Total propensity: " << pop.m_a << std::endl;
    for (auto pops_it = pop.m_listOfPopulations.begin(); pops_it != pop.m_listOfPopulations.end(); pops_it++)
        os << " " << *pops_it << std::endl;
    return os;
}

/***** Private methods *****/

std::list<Population>::iterator TotalPopulation::findPopulation(std::string specie){
    return m_listOfPopulations.begin();
}

void TotalPopulation::removeSpecie(std::string specie){
}

void TotalPopulation::addSpecie(std::string specie, int initPop){
}

Reaction TotalPopulation::sampleReaction(){
    /* To find which reaction is to be performed, PDM associates with each reaction
     * a number proportional to its probability - full propensity of reaction, Pi*n.
     * To find out which reaction will happen, it gets a uniformly distributed random
     * number (juice) from 0 to the sum (m_a) of all total propensities and starts adding
     * full propensities up until the sum exceeds the random number. Last propensity
     * for which it did not exceed that number gives us the reaction (RG-SS (2)-(5)).
     *
     * Sum of full propensities of all reactions associated with a population is called
     * m_ksi. First we determine which population keeps the record of the reaction, then
     * the method of class Population handles the rest of the sampling.
     */
    float juice = m_randGen.getFloat01() * m_a;
    for(auto pop = m_listOfPopulations.begin(); pop != m_listOfPopulations.end(); pop++){
        juice -= pop->m_ksi;
        if( juice < 0.f ){
            float remainingJuice = juice + pop->m_ksi;
            return pop->sampleReaction( remainingJuice );
        }
    }
    std::cout << "ERROR: Sampling failed. Full propensity m_a is likely broken.\n";
    exit(EXIT_FAILURE);
}

float TotalPopulation::sampleTime(){
    float r2 = m_randGen.getFloat01();
    if( r2 == 0.f ){
        std::cout << "ERROR: Random number of 0.f got whan computing time step, corresponding to a timestep of infinity.\n";
        exit(EXIT_FAILURE);
    } // TODO do something about it
    return -1.f*log(r2)/m_a;
}

void TotalPopulation::readPopulationsFromFile(std::string source){
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
            MOLINT              population;

            linestream >> name >> population;
            m_listOfPopulations.push_back(Population(name, population));
        }
    }

    file.close();
}
