#include <map>
#include <string>
#include <iostream>
#include <math.h>
#include <algorithm> // std::min
#include "parameter.h"
#include "model.h"
/* hp-model "hp-full-limited-food" #018
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
 * catPattern -- string. (cases)
 * interp.:
 * - if consists of 'H' and 'P' then represents a catalytic site of a given catalyst.
 * - if it's 'N' then it means the sequence is NOT a catalyst
 *
 * catPatterns -- dict. {string: string}
 * interp. a dictionary from sequence string to catalytic pattern string
 *
 * wellDepth -- dict. {string: int}
 * interp. a dictionary form monomer sequence string to potential well depth (energy of folded state)
 * z -- number of rotational freedoms
 * sequence:
 * fHP... - folded
 * f*HP... - catalyst
 */
#include <map>
#include <algorithm>

extern std::map<std::string,Parameter> configDict;
/* HP-model-specific global variables */
extern std::map<std::string,std::string> catPatterns;
extern std::map<std::string,int> wellDepths;

Specie::Specie(std::string id){
    modelName = std::string("hp-full-hydrolysis-phobicCut-phenomen.folding");
    m_folded = false;
    m_id = id; //HP sequence
    if (m_id==""){}
    else if(m_id.length()==1){
        m_folded = false;

    }
    //if sequence isn't folded (it doesn't have 'f' letter)
    if (m_id.find(std::string("f"))==std::string::npos){
        m_folded = false;
        //its length is the length of the m_id
        m_length = m_id.length();
        auto it = wellDepths.find(m_id);
        if (it!=wellDepths.end()){
            m_native = (it -> second);
        }
        else{
            m_native = 0;
        }
    }
    //if sequence is folded (it has 'f' in front of the actual sequence)
    else{
        m_folded = true;
        //so the length of the sequence is shorter than m_id by 1.
        m_length = m_id.length()-1;
        m_native = wellDepths.find(m_id.substr(1,m_length)) -> second;
    }

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
//FOLDING
float Specie::URate(float eH, float z){
    return exp(12-0.1*sqrt(m_length)-0.5*m_length*eH+1.34*eH);}

void Specie::foldIt(std::list<Reaction>& allReactions,Specie specie,
                    float eH, float z)//TEST!!!!!!!!!!
{
    float u_rate = URate(eH, z)*exp(eH*m_native)*1/(pow(z,m_length));
    Reaction fold(m_id,1,specie.m_id,0,u_rate);
    fold.addProduct(std::string("f")+m_id,1);
    allReactions.push_back(fold);
}

void Specie::unfoldIt(std::list<Reaction>& allReactions,Specie specie,
                    float eH, float z)//TEST
{
    float u_rate = URate( eH, z);
    Reaction unfold(m_id,1,specie.m_id,0,u_rate);
    if (m_id.find(std::string("*")) == std::string::npos){
        unfold.addProduct(m_id.substr(1,m_length),1);
    }
    else{
        unfold.addProduct(m_id.substr(2,m_length),1);
    }
    allReactions.push_back(unfold);
}

void Specie::growIt(std::list<Reaction>& allReactions,Specie specie,
                    float alpha, int maxLength){
    Reaction growth(m_id,1,specie.m_id,1,alpha);
    if (m_length<maxLength){
        growth.addProduct(m_id+specie.m_id,1);
    }
    allReactions.push_back(growth);
}

void Specie::growOther(std::list<Reaction>& allReactions,Specie specie,
                    float alpha, int maxLength){
    
    Reaction growth(m_id,1,specie.m_id,1,alpha);
    if (specie.m_length<maxLength){
        growth.addProduct(specie.m_id+m_id,1);
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
     * Folded polymer (including catalysts) can:
     * - unfold (imp.)
     * - degrade (imp.)
     */
    //parameters
    float aH = configDict["importH"].getFloat();
    float aP = configDict["importP"].getFloat();
    int maxLength = configDict["maxLength"].getInt();
    float alpha = configDict["growth"].getFloat();
    float d = configDict["degradation"].getFloat();
    float eH = configDict["eH"].getFloat();
    float dH = configDict["hydrolysis"].getFloat();
    float dAgg = configDict["aggregation"].getFloat();
    float aggPower = configDict["aggrAt"].getFloat();
    float z = configDict["z"].getFloat();
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
        //if it's not folded
        if (m_folded == false){
            //it can aggregate
            aggregateIt(allReactions,specie,dAgg,aggPower);
            //hydrolysis of any bond can happen
            hydrolyseIt(allReactions,specie,dH);
            //and might fold
            if (m_native!=0 && m_length>6){
                foldIt(allReactions,specie,eH,z);
            }
        }
        else{
            //it unfolds
            unfoldIt(allReactions,specie,eH,z);
        }
    }
    //binary reactions
    //if the other molecule is a catalyst 
    //and a given one isn't folded and is a substate
    //it can grow
    else if (m_folded == false && specie.m_length == 1){
        growIt(allReactions,specie,alpha,maxLength);
    }
    else if (m_length == 1 && specie.m_folded == false && specie.m_id!=std::string("")){
        growOther(allReactions,specie,alpha,maxLength);
    }
    return allReactions;
}
Specie::~Specie(){
}
