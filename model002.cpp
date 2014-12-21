#include <map>
#include <string>
#include <iostream>
#include "specie.h"

//std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
    modelName = std::string("");
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
    if (m_id==std::string("")){
        //activated monomers are being imported
        Reaction ai0("", 0, "",0,IMP0);
        ai0.addProduct(std::string("a0"),1);
        allReactions.push_back(ai0);
        Reaction ai1("", 0, "",0,IMP1);
        ai1.addProduct(std::string("a1"),1);
        allReactions.push_back(ai1);
    }
    
    //if our specie is an activated monomer
    else if(m_type==std::string("act")){
        if (specie.m_type==std::string("reg")){//TODO
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
                Reaction elongation(m_id, 1, specie.m_id, 1, FAST_RATE); // TODO fix the dictionary
                elongation.addProduct(m_id+(specie.m_id).substr(1,1), 1);
                allReactions.push_back(elongation);
            }
            Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); // TODO fix the dictionary
            elongation.addProduct(m_id+(specie.m_id).substr(1,1), 1);
            allReactions.push_back(elongation);
        }
        //it can have a monomolecular reaction
        else if (specie.m_id==m_id){
            //and decay
            Reaction decay(m_id,1,m_id,0,DEGR_RATE); // TODO fix the dictionary
            allReactions.push_back(decay);
        }
        //it can react with a regular molecule only if it is a catalyst
        else{}
    }
    else{} 
    return allReactions;
}

Specie::~Specie(){

}
