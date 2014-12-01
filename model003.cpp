#include <map>
#include <string>
#include <iostream>
#include "model003.h"

/*binary polymers
 * hydrolysis, decay, activated monomers convert to monomres
 * rates are bigger if all 1's are elongated by 1
 */

//std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
    m_id = id;
    if (m_id==std::string("a0") || m_id==std::string("a1")){
        m_length=1;
        m_type=std::string("act");
    }
    else{
        m_length = m_id.length();
        m_type=std::string("reg");}
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
    else if(m_type==std::string("act")){
        if (specie.m_type==std::string("reg")){
            //it elongates all 0 polymers with 0 very fast
            if (specie.m_id.find(std::string("1"))==std::string::npos && m_id==std::string("a0")){
                Reaction elongation(m_id, 1, specie.m_id, 1, FAST_RATE); 
                elongation.addProduct(specie.m_id+m_id[1], 1);
                allReactions.push_back(elongation);
            }
            else{
                Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); 
                elongation.addProduct(specie.m_id+m_id[1], 1);
                allReactions.push_back(elongation);
            }
        }
        //it can decay into a regular monomer
        else if (specie.m_id==m_id){
            Reaction dec(m_id,1,m_id,0,DECAY_RATE);
            dec.addProduct(m_id.substr(1,1), 1);
            allReactions.push_back(dec);
        }
        else {}
    }
    //if our specie is a regular molecule (n-mer)
    else if (m_type==std::string("reg")){
        //it cannot react with "vacuum"
        if (specie.m_id==std::string("")){}
        //it can react with an activated monomer
        else if(specie.m_type==std::string("act")){
            //and elongate itself by one.
            if (m_id.find(std::string("1"))==std::string::npos && specie.m_id==std::string("a0")){
                Reaction elongation(m_id, 1, specie.m_id, 1, FAST_RATE); 
                elongation.addProduct(m_id+(specie.m_id).substr(1,1), 1);
                allReactions.push_back(elongation);
            }
            Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); 
            elongation.addProduct(m_id+(specie.m_id).substr(1,1), 1);
            allReactions.push_back(elongation);
        }
        else if (m_id==specie.m_id){
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
