#include <map>
#include <string>
#include <iostream>
#include "specie.h"

/* rigid growing balls
 * binary polymers
 * sequences grow on its own and never decay
 */

std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
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
        for (int i=1; i<m_id.length();i++){
            Reaction hidr(m_id, 1, specie.m_id, 0, HIDR_RATE);
            hidr.addProduct(m_id.substr(0,i),1);
            hidr.addProduct(m_id.substr(i,m_id.length()-i),1);
            allReactions.push_back(hidr);
        }
            if (m_id.find(std::string("1"))!=std::string::npos){
                Reaction growth0(m_id, 1, specie.m_id, 0, GROWTH_RATE);
                growth0.addProduct(m_id+std::string("0"),1);
                allReactions.push_back(growth0);
                Reaction growth1(m_id, 1, specie.m_id, 0, GROWTH_RATE);
                growth0.addProduct(m_id+std::string("1"),1);
                allReactions.push_back(growth0);
            }
        }
        else if(m_id.find(std::string("1"))==std::string::npos && specie.m_id.find(std::string("1"))==std::string::npos) {
            Reaction fast(m_id, 1, specie.m_id, 1, FAST_RATE);
            fast.addProduct(m_id+std::string("0"),1);
            fast.addProduct(specie.m_id,1);
            allReactions.push_back(fast);
        }
    
    return allReactions;
}

Specie::~Specie(){

}
