#include <map>
#include <string>
#include <iostream>
#include <math.h>
#include <algorithm> // std::min
#include "parameter.h"
#include "model.h"
/* hp-model "hp-full-hydrolysis-phobicCut-limitMonomers" #012
 * monomers import
 * degradation
 * folded degradation
 * growth
 * false degradation
 *
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
 */
#include <map>
#include <algorithm>

extern std::map<std::string,Parameter> configDict;
/* HP-model-specific global variables */
extern std::map<std::string,std::string> catPatterns;
extern std::map<std::string,int> wellDepths;

Specie::Specie(std::string id){
    modelName = std::string("hp-full-hydrolysis-phobicCut");
    m_catalyst = std::string("N");
    m_substrate = std::string("N");
    m_product = false;
    m_id = id; //HP sequence
    if (m_id==""){}
    else if(m_id.length()==1){
        m_substrate = std::string("N");
        m_product = false;
        
    }
    //if sequence doesn't have HH as two last monomers in its sequence it cannot be a substrate
    else if (m_id.substr(m_id.length()-2, 2) != std::string("HH")){
        m_substrate = std::string("N");
    }
    //otherwise we need to check how long the substrate site is
    else{
        std::string maxPat = std::string("HHHHHHHH");
        int patLength=8;
        for (int i=0;i<patLength-1;i++){
            //we gonna reduce pattern length by 1 every step and compare
            int subLen=patLength-i;
            //pat is a reduced pattern which we are looking for in the end of the sequence
            std::string pat= maxPat.substr(i,subLen);
            if (m_id.length()<pat.length()){
                continue;
            }
            else if (m_id.substr(m_id.length()-pat.length(), pat.length()) == maxPat.substr(0,pat.length())){
                //if last pat.length() letters of the sequence are all 'H'
                m_substrate = pat;
                if (subLen>2){
                    m_product = true;
                }
                else{
                    if (m_id.length()<3){
                        m_product = false;
                    }
                    else if (m_id.find(std::string("HHH")) != std::string::npos){
                        m_product = true;
                    }
                    else{
                        m_product = false;
                    }
                }
                break;
            }
        }
    }
    //if sequence isn't folded (it doesn't have 'f' letter)
    if (m_id.find(std::string("f"))==std::string::npos){
        m_folded = false;
        //its length is the length of the m_id
        m_length = m_id.length();
        //it's not a catalyst
        m_catalyst = std::string("N");
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
        //it can be a catalyst
        //if it's a catalyst we'll get a catPattern, if not we'll get "N" as m_catalyst
        m_catalyst = catPatterns[m_id.substr(1,m_length+1)];
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

void Specie::hydrolyseIt(std::list<Reaction>& allReactions,Specie specie,
                         float dH){
    for (int i=1; i<(m_length); i++){
        Reaction hydrolysis(m_id,1,specie.m_id,0,dH);
        hydrolysis.addProduct(m_id.substr(0,i),1);
        hydrolysis.addProduct(m_id.substr(i,m_length-i),1);
        allReactions.push_back(hydrolysis);
    }
}

void Specie::foldIt(std::list<Reaction>& allReactions,Specie specie,
                    float eH, float k_unf){
        Reaction fold(m_id,1,specie.m_id,0,k_unf*exp(eH*m_native));
        fold.addProduct(std::string("f")+m_id,1);
        allReactions.push_back(fold);
}

void Specie::unfoldIt(std::list<Reaction>& allReactions,Specie specie,
                    float k_unf){
    Reaction unfold(m_id,1,specie.m_id,0,k_unf);
    unfold.addProduct(m_id.substr(1,m_length),1);
    allReactions.push_back(unfold);
}

void Specie::growIt(std::list<Reaction>& allReactions,Specie specie,
                    float alpha, std::string HorP, int maxLength){
                        Reaction growth(m_id,1,specie.m_id,0,alpha);
                        if (m_length<maxLength){
                            growth.addProduct(m_id+HorP,1);
                        }
                        allReactions.push_back(growth);
}

void Specie::catalyzeIt(std::list<Reaction>& allReactions,Specie specie,
                         float alpha, float eH, int maxLength){
    //how many H's are attracted to each other?
    int common;
    if (specie.m_folded && (not m_folded)){
//         std::cout << "other is folded " << std::endl;
        common = std::min(specie.m_catalyst.length(),m_substrate.length());
        float rate = exp(eH*common);
        Reaction catalysis(m_id,1,specie.m_id,1,rate);
        catalysis.addProduct(specie.m_id,1);
        if (m_length<maxLength){
            catalysis.addProduct(m_id+std::string("H"),1);
        }
        allReactions.push_back(catalysis);
    }
    else{
//         std::cout << "self is folded " << std::endl;
        common = std::min(m_catalyst.length(),specie.m_substrate.length());
        float rate = exp(eH*common);
        Reaction catalysis(m_id,1,specie.m_id,1,rate);
        catalysis.addProduct(m_id,1);
        if (specie.m_length<maxLength){
            catalysis.addProduct(specie.m_id+std::string("H"),1);
        }
        allReactions.push_back(catalysis);
    }
    if (common == 0){
        std::cout << "c" <<m_catalyst << std::endl;
        throw std::invalid_argument("common = 0");
    }
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
    float aH = configDict["monomerBirthH"].getFloat();
    float aP = configDict["monomerBirthP"].getFloat();
    int maxLength = configDict["maxLength"].getInt();
    float alpha = configDict["growth"].getFloat();
    float d = configDict["degradation"].getFloat();
    float k_unf = configDict["unfolding"].getFloat();
    float eH = configDict["hydrophobicEnergy"].getFloat();
    float dH = configDict["hydrolysisRate"].getFloat();
    float dAgg = configDict["aggregation"].getFloat();
    float aggPower = configDict["aggrDegree"].getFloat();
    //all the reactions two species can have
    std::list<Reaction> allReactions;
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
            if (m_native!=0){
                foldIt(allReactions,specie,eH,k_unf);
            }
            //it can grow
            growIt(allReactions,specie,alpha, std::string("H"),maxLength);
            growIt(allReactions,specie,alpha, std::string("P"),maxLength);
        }
        else{
            //it unfolds
            unfoldIt(allReactions,specie,k_unf);
        }
    }
    //binary reactions
    //if the other molecule is a catalyst 
    //and a given one isn't folded and is a substate
    else if (specie.m_catalyst != std::string("N") && 
            m_folded == false && 
            m_substrate != std::string("N")){
        catalyzeIt(allReactions,specie,alpha,eH,maxLength);
    }
    else if (m_catalyst != std::string("N") && 
            specie.m_folded == false && 
            specie.m_substrate != std::string("N")){
        catalyzeIt(allReactions,specie,alpha,eH,maxLength);
    }
    return allReactions;
}
Specie::~Specie(){
}
