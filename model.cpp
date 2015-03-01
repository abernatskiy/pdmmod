#include <map>
#include <string>
#include <iostream>
#include "model.h"

/*binary polymers #003
 * hydrolysis, growth
 * rates are bigger if all 1's are elongated by 1
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
    
    //if our specie is an activated monomer
    else if (m_id==specie.m_id){
        //hydrolysis
        for (int i=1; i<m_id.length();i++){
            Reaction hidr(m_id, 1, specie.m_id, 0, HIDR_RATE);
            hidr.addProduct(m_id.substr(0,i),1);
            hidr.addProduct(m_id.substr(i,m_id.length()-i),1);
            allReactions.push_back(hidr);
        //growth
        }
    }
    else if (m_id.find(std::string("1"))==std::string::npos && specie.m_id==std::string("0")){
        Reaction elongation(m_id, 1, specie.m_id, 1, FAST_RATE); 
        elongation.addProduct(m_id+specie.m_id, 1);
        allReactions.push_back(elongation);
    }
    else if (specie.m_id.find(std::string("1"))==std::string::npos && m_id==std::string("0")){
        Reaction elongation(m_id, 1, specie.m_id, 1, FAST_RATE); 
        elongation.addProduct(specie.m_id+m_id, 1);
        allReactions.push_back(elongation);
    }
    else if (specie.m_length == 1){
        Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); 
        elongation.addProduct(m_id+specie.m_id, 1);
        allReactions.push_back(elongation);
    }
    else if (m_length ==1){
        Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); 
        elongation.addProduct(specie.m_id+m_id, 1);
        allReactions.push_back(elongation);
    }
        
    return allReactions;
}

Specie::~Specie(){

}
