#include <map>
#include <string>
#include <iostream>
#include <math.h>
#include <algorithm> // std::min
#include "parameter.h"
#include "model.h"
/* hp-model "hp-basic-hydrolysis-phobicCut-limitMonomers kings-folding" #017
 * monomers import
 * degradation
 * folded degradation
 * growth
 * false degradation
 * polymerization
 * catalyis
 * folding
 * unfolding
 */
/*DATA

 */
#include <map>
#include <algorithm>

extern std::map<std::string,Parameter> configDict;
/* HP-model-specific global variables */
extern std::map<std::string,std::string> catPatterns;
extern std::map<std::string,int> wellDepths;

Specie::Specie(std::string id){
    modelName = std::string("hp-basic-hydrolysis-phobicCut-phenomen.folding");
    m_id = id; //HP sequence
    m_length = m_id.length();

    if (m_length <5 || m_id == ""){
        m_hydrophobicity = 0;
    }
    else{
        size_t n = std::count(m_id.begin(), m_id.end(), 'H');
        m_hydrophobicity = ((float)  n)/m_length;
    }
    
}
//Overloading <<
std::ostream& operator<<(std::ostream& os, const Specie& sp)
{
    os << sp.m_id ;
    return os;
}


//methods
void Specie::importHorP(std::list<Reaction>& allReactions,Specie specie,
                          float impRate,std::string HorP){
    Reaction importIt(m_id, 0, specie.m_id, 0, impRate);
    importIt.addProduct(HorP,1);
    allReactions.push_back(importIt);
}

void Specie::degradeIt(std::list<Reaction>& allReactions,Specie specie,
                       float degrRate){
    Reaction degradation(m_id,1,specie.m_id,0,degrRate);
    allReactions.push_back(degradation);
}

void Specie::aggregateIt(std::list<Reaction>& allReactions,Specie specie,
                     float aggRate,float aggPower){
    if (m_hydrophobicity >aggPower){
        Reaction aggregation(m_id,1,specie.m_id,0,aggRate);
        allReactions.push_back(aggregation);
    }
//     if (aggPower==0){
//         if (m_hydrophobicity >=0.8){
//             Reaction aggregation(m_id,1,specie.m_id,0,aggRate);
//             allReactions.push_back(aggregation);
//         }
//     }
//     else{
//         Reaction aggregation(m_id,1,specie.m_id,0,
//                          aggRate*pow(m_hydrophobicity,aggPower)*m_length);
//         allReactions.push_back(aggregation);
//     }
}

void Specie::hydrolyseIt(std::list<Reaction>& allReactions,Specie specie,
                         float dH){
    for (int i=1; i<(m_length); i++){
        Reaction hydrolysis(m_id,1,specie.m_id,0,dH);
        hydrolysis.addProduct(m_id.substr(0,i),1);
        hydrolysis.addProduct(m_id.substr(i,m_length-i),1);
        allReactions.push_back(hydrolysis);
    }
}


void Specie::growIt(std::list<Reaction>& allReactions,Specie specie,
                    float alpha, std::string HorP, int maxLength){
                        Reaction growth(m_id,1,specie.m_id,0,alpha);
                        if (m_length<maxLength){
                            growth.addProduct(m_id+HorP,1);
                        }
                        allReactions.push_back(growth);
}



//Defining reactions here
std::list<Reaction> Specie::reactions(Specie specie){
    /* Nothing can:
     * - create a monomer (imp.) :implemented 
     * Unfolded polymer (including 1mers and substrates) can:
     * - grow (imp.)
     * - false grow(imp.)
     * - hydrolyze (imp.)
     * - degrade (imp.)
     * - aggregate if condtions met (imp.)
     * - fold (imp.)
     * Substrate is Unfolded polymer + it can:
     * - interact with Catalyst  
     *      to grow(imp.)
     *      or disappear(imp.)
     * Folded polymer (including catalysts) can:
     * - unfold (imp.)
     * - degrade (imp.)
     * Catalyst is Folded polymer + it can:
     * - interact with Substrate 
     *      for substrate to grow(imp.)
     *      or to disappear(imp.)
     */
    //parameters
    float aH = configDict["importH"].getFloat();
    float aP = configDict["importP"].getFloat();
    int maxLength = configDict["maxLength"].getInt();
    float alpha = configDict["growth"].getFloat();
    float d = configDict["degradation"].getFloat();
    float dH = configDict["hydrolysis"].getFloat();
    float dAgg = configDict["aggregation"].getFloat();
    float aggPower = configDict["aggrAt"].getFloat();
    //all the reactions two species can have
//     std::cout << "Loadad" << std::endl;
//     std::cout << aH << "\n" << aP<< "\n" << maxLength<< "\n" << alpha<< "\n" << d<< "\n" << eH<< "\n" << dAgg<< "\n" << aggPower<< "\n" << z << std::endl;
    std::list<Reaction> allReactions;
//     float u_rate = 
    
    // 'H' and 'P' monomers are being produced from activated monomers, concentration of which is const.
    if (m_id==std::string("")){
        if (specie.m_id==std::string("")){
            importHorP(allReactions,specie,aH,std::string("H"));
            importHorP(allReactions,specie,aP,std::string("P"));
        }
    }
    //monomolecular reactions
    else if (m_id == specie.m_id){
        //it degrades
        degradeIt(allReactions,specie,d);
        //it can aggregate
        aggregateIt(allReactions,specie,dAgg,aggPower);
        //hydrolysis of any bond can happen
        hydrolyseIt(allReactions,specie,dH);
        //it can grow
        growIt(allReactions,specie,alpha, std::string("H"),maxLength);
        growIt(allReactions,specie,alpha, std::string("P"),maxLength);
    }
    // no binary reactions
    return allReactions;
}
Specie::~Specie(){
}
