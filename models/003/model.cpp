#include <map>
#include <string>
#include <iostream>
#include "model.h"

/* colliding particles  #003
 * there are several types of particles 
 * they are present in the system 1 each
 * they have index and length. their name is represented like index_length
 * when particles collide length of both increases
 * when particles length reaches maxLength, they go back to 1mers
 */

extern std::map<std::string,Parameter> configDict;

Specie::Specie(std::string id){
    modelName = std::string("colliding_changing_particles");
    m_id = id; //int number + _ +length i.e. 324_16
    std::string tmp = m_id;
    m_len = atoi((tmp.erase(0,5)).c_str());
    
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
    int maxLength = configDict["maxLength"].getInt();
    //nothing is being produced from vacuum in this model
    if (m_id==std::string("")){}
    else {
        Reaction collision(m_id, 1, specie.m_id, 1, COLL_RATE);
        if (m_len>maxLength || specie.m_len> maxLength){
            throw std::invalid_argument( "received m_len>maxLength" );
        }
        std::string tmp1 = m_id;
        std::string tmp2 = specie.m_id;
        if (m_id == specie.m_id){
            if (m_len<maxLength){
                collision.addProduct(m_id.substr(0,5)+std::to_string(atoi((tmp1.erase(0,5)).c_str())+1),2);
            }
            else{
                collision.addProduct(m_id.substr(0,5)+std::string("1"),2);
            }
        }
        else{
            if (m_len<maxLength){
                collision.addProduct(m_id.substr(0,5)+std::to_string(atoi((tmp1.erase(0,5)).c_str())+1),1);
            }
            else if (m_len == maxLength){
                collision.addProduct(m_id.substr(0,5)+std::string("1"),1);
            }
            if (specie.m_len<maxLength){
                collision.addProduct(specie.m_id.substr(0,5)+std::to_string(atoi((tmp2.erase(0,5)).c_str())+1),1);
            }
            else if (specie.m_len==maxLength){
                collision.addProduct(specie.m_id.substr(0,5)+std::string("1"),1);
            }
            allReactions.push_back(collision);
        }
    }
    
    return allReactions;
}

Specie::~Specie(){
    
}
