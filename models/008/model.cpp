#include <map>
#include <string>
#include <iostream>
#include "model.h"

/* colliding particles  #008
 * there are several types of particles 
 * reactions are binary collisions, particles don't change when interact.
 */

//std::map<std::string,Parameter> globParams;

Specie::Specie(std::string id){
    modelName = std::string("colliding_particles");
    m_id = id;
    
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

    //nothing is being produced from vacuum in this model
    if (m_id==std::string("")){}
    else {
        Reaction collision(m_id, 1, specie.m_id, 1, COLL_RATE);
        collision.addProduct(m_id,1);
        collision.addProduct(specie.m_id,1);
        allReactions.push_back(collision);
    }
        
    return allReactions;
}

Specie::~Specie(){

}
