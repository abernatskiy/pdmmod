#include <map>
#include <string>
#include <iostream>
#include "specie.h"

/* colliding particles  #006
 * there are several types of particles 
 * they are present in the system 1 each
 * they have index and length. their name is represented like index_length
 * when particles collide length of both increases
 */

//std::map<std::string,Parameter> globParams;
extern std::map<std::string,Parameter> configDict;

Specie::Specie(std::string id){
    modelName = std::string("colliding_changing_particles");
    m_id = id; //int number + _ +length i.e. 324_16
    
}
//Overloading <<
std::ostream& operator<<(std::ostream& os, const Specie& sp)
{
    os << sp.m_id ;
    return os;
}
//methods


//Defining reactions here 

std::list<Reaction> Specie::reactions(Specie specie){
    //all the reactions two species can have
    std::list<Reaction> allReactions;
    
    float COLL_RATE = configDict["collRate"].getFloat();
    //nothing is being produced from vacuum in this model
    if (m_id==std::string("")){}
    else {
        Reaction collision(m_id, 1, specie.m_id, 1, COLL_RATE);
        std::string tmp1 = m_id;
        std::string tmp2 = specie.m_id;
        collision.addProduct(m_id.substr(0,5)+std::to_string(atoi((tmp1.erase(0,5)).c_str())+1),1);
        collision.addProduct(specie.m_id.substr(0,5)+std::to_string(atoi((tmp2.erase(0,5)).c_str())+1),1);
        allReactions.push_back(collision);
    }
    
    return allReactions;
}

Specie::~Specie(){
    
}