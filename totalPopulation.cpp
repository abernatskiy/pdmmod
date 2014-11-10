#include "totalPopulation.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <tuple>
#include <cstdlib>
#include <cmath>

TotalPopulation::TotalPopulation(std::string source){
//    m_randGen.seedWithString("shg;l ivnmsvceg dgfh d0sfdfsd ");
//    // This random seed is known to trigger a numerical error in top-level sampling
//    // with older sampler code (dded6fac3a92ff3aec1d92216a66971dbc9b9605 and older).
//    // I'll just leave it here for a while.
    m_t = 0.f;
    addPopulation("", 1); // adding "vacuum"
    addPopulationsFromFile(source);
    computeTotalPropensity();
}

int TotalPopulation::stepSimulation(){

    if( m_listOfPopulations.size() == 1 && m_a == 0.f ){
        std::cout << "All molecules died off and there are no source reactions, exiting\n";
        //exit(EXIT_SUCCESS);
        //break;
        return 1;
    }

    Reaction reac = sampleReaction();
    //std::cout << "Got reaction " << reac << std::endl;
    m_t += sampleTime();

    // When the reaction is known, iterate through all species involved in the reaction
    for( auto itSpRec = reac.m_records.begin(); itSpRec != reac.m_records.end(); itSpRec++ ){
        // The data structure at the iterator is tuple. We must first unpack it.
        std::string specieId;
        int specieSto;
        std::tie (specieId, specieSto) = *itSpRec;

        // For every specie, we're interested in getting an iterator to its population
        auto itPop = findPopulation(specieId);

        // If such population alrady exists
        if( itPop != m_listOfPopulations.end() ){
            // Update the population
            itPop->update(specieSto);
        }
        else{
            // Otherwise, add the new specie
            addPopulation(specieId, specieSto);
        }
    }

    // After we're done updating, remove all Populations with molecular count of 0
    std::list<std::list<Population>::iterator> blackList;
    for( auto itPop = m_listOfPopulations.begin(); itPop != m_listOfPopulations.end(); itPop++ ){
        if( (itPop->m_n) == 0 )
            blackList.push_back(itPop);
        else if( (itPop->m_n) < 0 ){
            std::cout << "TotalPopulation: Population with negative molecule count found, exiting.\n" << *itPop << std::endl;
            exit(EXIT_FAILURE);
        }
    }
    for( auto itPopToKill = blackList.begin(); itPopToKill != blackList.end(); itPopToKill++ )
        removePopulation(*itPopToKill);

    // Recompute m_a
    computeTotalPropensity();

    if(m_a == 0.f)
        //break;
        return 1;
    else
        return 0;
}

std::ostream& operator<<(std::ostream& os, const TotalPopulation& pop){
    os << "Current simulation time: " << pop.m_t << std::endl;
    os << "Total propensity: " << pop.m_a << std::endl;
    for (auto pops_it = pop.m_listOfPopulations.begin(); pops_it != pop.m_listOfPopulations.end(); pops_it++)
//        os << " " << *pops_it << std::endl;
        if( pops_it->m_specie.m_id != "" )
            os << "  " << pops_it->m_specie.m_id << "  " << pops_it->m_n << std::endl;
    return os;
}

/***** Private methods *****/

std::list<Population>::iterator TotalPopulation::findPopulation(std::string specie){
    int i = 0;
    auto soughtIt = m_listOfPopulations.end();
    for( auto itPop = m_listOfPopulations.begin(); itPop != m_listOfPopulations.end(); itPop++ ){
        if( itPop->m_specie.m_id == specie ){
            soughtIt = itPop;
            i++;
        }
    }
    if( i > 1 ){
        std::cout << "TotalPopulation: More than one poulation of a specie " << specie << " found during search, exiting.";
        exit(EXIT_FAILURE);
    }
    else
        return soughtIt;
}

void TotalPopulation::removePopulation(std::list<Population>::iterator itToPopToRemove){
    itToPopToRemove->eraseTracesOfExistence();
    m_listOfPopulations.erase(itToPopToRemove);
}

void TotalPopulation::addPopulation(std::string specie, int initPop){
    if( initPop <= 0 ){
        std::cout << "TotalPopulation: Addition of a population of 0 of less (" << initPop << ") molecules attempted, exiting." << std::endl;
        exit(EXIT_FAILURE);
    }
    MOLINT initPopN = (MOLINT) initPop;
    m_listOfPopulations.push_back(Population(specie, initPopN));
    auto itNewPop = m_listOfPopulations.rbegin();
    for( auto itOtherPop = m_listOfPopulations.begin(); itOtherPop != m_listOfPopulations.end(); itOtherPop++ ){
        itOtherPop->buildRelation(itOtherPop, itNewPop);
    }
}

void TotalPopulation::computeTotalPropensity(){
    m_a = 0.f;
    for( auto itPop = m_listOfPopulations.begin(); itPop != m_listOfPopulations.end(); itPop++ )
        m_a += itPop->m_ksi;
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
    PROPFLOAT juice = (1.f - m_randGen.getFloat01()) * m_a; // the "one minus" part is here because we need the juice to be in [0, m_a)
    PROPFLOAT sumKsi = 0.f;
    PROPFLOAT prevSumKsi;
//    std::cout << "Sampling a reaction with " << juice << " of juice, total propensity is " << m_a << std::endl;
    for(auto pop = m_listOfPopulations.begin(); pop != m_listOfPopulations.end(); pop++){
        prevSumKsi = sumKsi;
        sumKsi += pop->m_ksi;
        if( juice < sumKsi )
            return pop->sampleReaction( juice - prevSumKsi );
    }
    std::cout << "ERROR: TotalPopulation-level sampling failed. This is likely to be a rare consequence of the numerical error of the juice quantity, which is not handled in the current version\n"; // TODO
    std::cout << "Juice in the end: " << juice << std::endl;
    exit(EXIT_FAILURE);
}

float TotalPopulation::sampleTime(){
    float r2 = m_randGen.getFloat01();
    return -1.f*log(r2)/m_a;
}

void TotalPopulation::addPopulationsFromFile(std::string source){
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
            addPopulation(name, population);
        }
    }

    file.close();
}
