#include <map>
#include <string>
#include <iostream>
#include "model.h"

/*binary polymers #002
 * hydrolysis, growth
 * hydrolysis rates are slower if the sequences is all 0
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
        Reaction elongation1(m_id, 1, specie.m_id, 0, GROWTH_RATE); 
        elongation1.addProduct(m_id+"1", 1);
        allReactions.push_back(elongation1);
        Reaction elongation0(m_id, 1, specie.m_id, 0, GROWTH_RATE); 
        elongation0.addProduct(m_id+"0", 1);
        allReactions.push_back(elongation0);
        Reaction del(m_id, 1, specie.m_id, 0, DEL_RATE); 
        allReactions.push_back(del);
        if (m_id.find(std::string("1"))==std::string::npos){
            for (int i=1; i<m_id.length();i++){
                Reaction hidr(m_id, 1, specie.m_id, 0, SLOWHIDR_RATE);
                hidr.addProduct(m_id.substr(0,i),1);
                hidr.addProduct(m_id.substr(i,m_id.length()-i),1);
                allReactions.push_back(hidr); 
            }
        }
        else{
            for (int i=1; i<m_id.length();i++){
                Reaction hidr(m_id, 1, specie.m_id, 0, HIDR_RATE);
                hidr.addProduct(m_id.substr(0,i),1);
                hidr.addProduct(m_id.substr(i,m_id.length()-i),1);
                allReactions.push_back(hidr);
            }
        }
    }
    else{}
    return allReactions;
}

Specie::~Specie(){

}
