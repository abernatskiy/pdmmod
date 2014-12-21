#include <map>
#include <string>
#include <iostream>
#include "specie.h"

//std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
    modelName = std::string("");
    m_id = id;
    if (m_id==std::string("a")){
        m_length=1;
        m_type=std::string("act");
    }
    else{
        m_length = std::atoi(m_id.c_str());
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
        Reaction actImport("", 0, "",0,IMP_RATE);
        actImport.addProduct(std::string("a"),1);
        allReactions.push_back(actImport);
    }
    
    //if our specie is an activated monomer
    else if(m_type==std::string("act")){
        //it cannot react with itself of decay
        if (specie.m_type==std::string("reg")){
            //it elongates the molecule by one.
//            Reaction elongation(m_id, 1, specie.m_id, 1, globParams["a"].getFloat());
            Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); // TODO fix the dictionary
            elongation.addProduct(std::to_string(specie.m_length+1), 1);
            allReactions.push_back(elongation);
        }
        else if (specie.m_id==m_id){
            //it decays int regular monomers
            Reaction decay2(m_id,1,m_id,0,DECAY_RATE);
            decay2.addProduct(std::string("1"), 1);
            allReactions.push_back(decay2);
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
//            Reaction elongation(m_id, 1, specie.m_id, 1, globParams["a"].getFloat());
            Reaction elongation(m_id, 1, specie.m_id, 1, GROWTH_RATE); // TODO fix the dictionary
            elongation.addProduct(std::to_string(m_length+1), 1);
            allReactions.push_back(elongation);
        }
        //it can have a monomolecular reaction
        else if (specie.m_id==m_id){
            //and decay
//            Reaction decay(m_id,1,m_id,0,globParams["d"].getFloat());
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
