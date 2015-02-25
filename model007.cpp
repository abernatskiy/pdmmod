#include <map>
#include <string>
#include <iostream>
#include "specie.h"

/* colliding particles  #007
 * there are several types of particles 
 * reactions are binary collisions, particles transform when interact into particles with higher index
 */

//std::map<std::string,Parameter> globParams;
extern std::map<std::string,Parameter> configDict;

Specie::Specie(std::string id){
    modelName = std::string("colliding_changing_particles");
    m_id = id;
    
}
//Overloading <<
std::ostream& operator<<(std::ostream& os, const Specie& sp)
{
    os << sp.m_id ;
    return os;
}
//methods


//Defining reactions here BUG

std::list<Reaction> Specie::reactions(Specie specie){
    //all the reactions two species can have
    std::list<Reaction> allReactions;
    float N = configDict["specNumber"].getInt();
    float COLL_RATE = configDict["collRate"].getFloat();
    //nothing is being produced from vacuum in this model
    if (m_id==std::string("")){}
    else {
        Reaction collision(m_id, 1, specie.m_id, 1, COLL_RATE);
        if (atoi(m_id.c_str())<N){
            collision.addProduct(std::to_string(atoi(m_id.c_str())+1),1);
        }
        else{
            collision.addProduct(std::to_string(1),1);
        }
        if (atoi(specie.m_id.c_str())<N){
            collision.addProduct(std::to_string(atoi(specie.m_id.c_str())+1),1);
            
        }
        else{
            collision.addProduct(std::to_string(1),1);
        }
        allReactions.push_back(collision);
    }
    
    return allReactions;
}

Specie::~Specie(){
    
}