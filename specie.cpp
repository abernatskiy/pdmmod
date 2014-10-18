#include <map>
#include <string>
#include "specie.h"
#include <iostream>

std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
    m_id = id;
    if (m_id==std::string("a")){
        m_length=1;
    }
    else
        m_length = std::atoi(m_id.c_str());
}
//Overloading <<
std::ostream& operator<<(std::ostream& os, const Specie& sp)
{
    os << sp.m_id << " (of length " << sp.m_length << ")";
    return os;
}
//methods

bool Specie::ifCatalyst(){
    int X = (globParams[std::string("X")]).getInt();
    if(m_length > X)
       return true;
    else
        return false;
}
//Defining reactions here

std::list<Reaction> Specie::reactions(Specie specie){
    //all the reactions two species can have
    std::list<Reaction> allReactions;
    
    //nothing is produced
    if (m_id==std::string("")){}
    //if our specie is an activated monomer
    else if(m_id==std::string("a")){
        //it cannot react with itself of decay
        if ( (specie.m_id!=std::string("")) && (specie.m_id!=std::string("a")) ){}
        //in the reaction with a regular molecule
        else{
            //it elongates the molecule by one.
            Reaction elongation(m_id, 1, specie.m_id, 1, globParams[std::string("a")].getFloat());
            elongation.addProduct(std::to_string(specie.m_length+1), 1);
            allReactions.push_back(elongation);
        }
    }
    //if our specie is a regular molecule (n-mer)
    else{
        //it cannot react with "vacuum" 
        if (specie.m_id==std::string("")){}
        //it can react with an activated monomer
        else if(specie.m_id==std::string("a")){
            //and elongate itself by one.
            Reaction elongation(m_id, 1, specie.m_id, 1, globParams[std::string("a")].getFloat());
            elongation.addProduct(std::to_string(m_length+1), 1);
            allReactions.push_back(elongation);
        }
        //it can have a monomolecular reaction
        else if (specie.m_id==m_id){
            //and decay
            Reaction decay(m_id,1,m_id,0,globParams[std::string("d")].getFloat());
              
        }
        //it can react with a regular molecule only if it is a catalyst
        else{}
    }
    
    return allReactions;
}




Specie::~Specie(){
    
}
