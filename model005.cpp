#include <map>
#include <string>
#include <iostream>
#include "specie.h"

/* rigid growing binary polymers #005
 * monomers: 0, 1
 * sequences grow on its own and  decay
 * 0, 1 are imported
 * if specis is all 0 and 0 is added it grows faster
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
    if (m_id==std::string("")){
        if (specie.m_id==std::string("")){
            Reaction importH(m_id, 0, specie.m_id, 0, IMPORT);
            importH.addProduct(std::string("0"),1);
            allReactions.push_back(importH);
            Reaction importP(m_id, 0, specie.m_id, 0, IMPORT);
            importP.addProduct(std::string("1"),1);
            allReactions.push_back(importP);
        }
    }
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
                Reaction growth1(m_id, 1, specie.m_id, 1, GROWTH_RATE);
                growth1.addProduct(m_id+std::string("1"),2);
                allReactions.push_back(growth1);
                Reaction growth0(m_id, 1, specie.m_id, 1, GROWTH_RATE);
                growth0.addProduct(m_id+std::string("0"),2);
                allReactions.push_back(growth0);
            }
            Reaction del(m_id,1,specie.m_id,0,DEL_RATE);
            allReactions.push_back(del);
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
