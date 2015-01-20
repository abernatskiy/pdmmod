#include <map>
#include <string>
#include <iostream>
#include "specie.h"

/* rigid growing balls
 * binary polymers
 * sequences grow on its own and never decay
 */

//std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
    modelName = std::string("");
    m_id = id;
    m_length = m_id.length();
}
//Overloading <<
std::ostream& operator<<(std::ostream& os, const Specie& sp)
{
    os << sp.m_id << " (of length " << sp.m_length << ")";
    return os;
}
//methods


//Defining reactions here

std::list<Reaction> Specie::reactions(Specie specie){
    //all the reactions two species can have
    std::list<Reaction> allReactions;

    //nothing is being produced from vacuum in this model
    if (m_id==std::string("")){}
    else if(m_id==specie.m_id){
            if (m_id.find(std::string("1"))==std::string::npos){
                Reaction growth1(m_id, 1, specie.m_id, 1, GROWTH_RATE);
                growth1.addProduct(m_id+std::string("1"),2);
                allReactions.push_back(growth1);
                Reaction growth0(m_id, 1, specie.m_id, 1, FAST_RATE);
                growth0.addProduct(m_id+std::string("0"),2);
                allReactions.push_back(growth0);
            }
            else{
                
            }
        }
    else{
        Reaction growth1(m_id, 1, specie.m_id, 1, GROWTH_RATE);
        growth1.addProduct(m_id+std::string("1"),1);
        growth1.addProduct(specie.m_id+std::string("1"),1);
        allReactions.push_back(growth1);
        Reaction growth0(m_id, 1, specie.m_id, 1, GROWTH_RATE);
        growth0.addProduct(m_id+std::string("0"),1);
        growth0.addProduct(specie.m_id+std::string("0"),1);
        allReactions.push_back(growth0);
    }
    
    return allReactions;
}

Specie::~Specie(){

}
