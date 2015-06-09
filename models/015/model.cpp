#include <map>
#include <string>
#include <iostream>
#include <math.h>
#include <algorithm> // std::min
#include <stdexcept>
#include "parameter.h"
#include "model.h"
/* hp-model "hp--hydrolysis-phobicCut-3species-interactions" #015
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
#include <exception>


extern std::map<std::string,Parameter> configDict;
/* HP-model-specific global variables */
// extern std::map<std::string,std::string> catPatterns;
extern std::map<std::string,int> wellDepths;



Specie::Specie(std::string id){
    /* A Specie can be:
     * - activated monomer
     * - unfolded polymer, including 1-mers
     * - folded polymer
     * - substrate: unfolded polymer with 'HH' in the end
     * - catalyst: folded polymer, if catalyst catPatterns[m_id]!= "N"
     * - complex: catalyst and substate bound together
     *   m_id = catalyst.m_id+"_"+substate.m_id
     */
    modelName = std::string("hp-full-hydrolysis-phobicCut");
    m_complex = false;
    m_active = false;
    m_catalyst = std::string("N");
    m_substrate = std::string("N");
    m_product = false;
    m_id = id; //HP sequence
    //define emptyness
    if (m_id==""){}
    //if id is one letter
    else if(m_id.length()==1){}
    //if id has * -- it's activated
    else if (m_id==std::string("H*") || m_id==std::string("P*")){
        m_length = 1;
        m_active = true;
        m_substrate = std::string("N");
        m_product = false;
        m_folded = false;
        m_complex = false;
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
        //if id has '_' it's a 2 molecules complex
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
        //if it's a complex of folder and non-folder
        if (m_id.find(std::string("_")) != std::string::npos){
            m_folded = false;
            m_length = 0;
            m_catalyst = std::string("N");
            m_substrate =std::string("N");
            m_native = 0;
            m_complex = true;
        }
        else{
            m_folded = true;
            //so the length of the sequence is shorter than m_id by 1.
            m_length = m_id.length()-1;
            //it can be a catalyst
            //if it's a catalyst we'll get a catPattern, if not we'll get "N" as m_catalyst
            m_catalyst = catPatterns[m_id.substr(1,m_length+1)];
            m_native = wellDepths.find(m_id.substr(1,m_length+1)) -> second;
            if (m_catalyst.length() == 0){
                std::cout << "is catPattern empty in model.cpp?" << std::endl;
                std::cout<< catPatterns["HHPHPH"] << std::endl;
                std::cout << "is configDict empty in model.cpp?" << std::endl;
                std::cout<< configDict["unfolding"].getFloat() << std::endl;
                for (std::map<std::string,std::string>::iterator it=catPatterns.begin(); it!=catPatterns.end(); ++it)
                    std::cout << "element " <<it->first << " => " << it->second << '\n';
//                 throw std::invalid_argument("pattern isn't found in the catPattern dict: "+m_id+" "+m_id.substr(1,m_length+1));
            }
        }
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
void Specie::importActive(std::list<Reaction>& allReactions,Specie specie,
                           float impRate,std::string HorP){
    Reaction importIt(m_id, 0, specie.m_id, 0, impRate);
    importIt.addProduct(HorP+std::string("*"),1);
    allReactions.push_back(importIt);
}

void Specie::degradeIt(std::list<Reaction>& allReactions,Specie specie,
                          float degrRate){
    Reaction degradation(m_id,1,specie.m_id,0,degrRate);
    allReactions.push_back(degradation);
    }

void Specie::make2mer(std::list<Reaction>& allReactions,Specie specie,
                    float alpha){
    Reaction getHH(m_id,1,specie.m_id,0,alpha);
    getHH.addProduct((std::string("H")+m_id.substr(0,1)),1);
    allReactions.push_back(getHH);
    
    Reaction getPH(m_id,1,specie.m_id,0,alpha);
    getPH.addProduct((std::string("P")+m_id.substr(0,1)),1);
    allReactions.push_back(getPH);
    }
    
void Specie::aggregateIt(std::list<Reaction>& allReactions,Specie specie,
                     float aggRate,int aggPower){
    if (aggPower==0){
        if (m_hydrophobicity >=0.8){
            Reaction aggregation(m_id,1,specie.m_id,0,aggRate);
            allReactions.push_back(aggregation);
        }
    }
    else{
        Reaction aggregation(m_id,1,specie.m_id,0,
                         aggRate*pow(m_hydrophobicity,aggPower)*m_length);
        allReactions.push_back(aggregation);
    }
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
    if (m_native!=0){
        Reaction fold(m_id,1,specie.m_id,0,k_unf*exp(eH*m_native));
        fold.addProduct(std::string("f")+m_id,1);
        allReactions.push_back(fold);
    }
}

void Specie::unfoldIt(std::list<Reaction>& allReactions,Specie specie,
                    float k_unf){
    Reaction unfold(m_id,1,specie.m_id,0,k_unf);
    unfold.addProduct(m_id.substr(1,m_length),1);
    allReactions.push_back(unfold);
}

void Specie::growIt(std::list<Reaction>& allReactions,Specie specie,
                    float alpha, int maxLength){//BUG!
    Reaction growth(m_id,1,specie.m_id,1,alpha);
    if (m_active && specie.m_length<maxLength){
        std::cout << "self is active " << std::endl;
        growth.addProduct(specie.m_id+m_id.substr(0,1),1);
        allReactions.push_back(growth);
    }
    else{
        std::cout << "other is active " << std::endl;
        if (m_length<maxLength){
        growth.addProduct(m_id+specie.m_id.substr(0,1),1);
        allReactions.push_back(growth);
        }
    }
}

void Specie::formComplex(std::list<Reaction>& allReactions,Specie specie,
                         float alpha, float eH){
    //how many H's are attracted to each other?
    int common;
    if (specie.m_folded && (not m_folded)){
        std::cout << "other is folded " << std::endl;
        common = std::min(specie.m_catalyst.length(),m_substrate.length());
        float rate = exp(eH*common);
        Reaction complexFormation(m_id,1,specie.m_id,1,rate);
        complexFormation.addProduct(specie.m_id+std::string("_")+m_id,1);
        allReactions.push_back(complexFormation);
    }
    else{
        std::cout << "self is folded " << std::endl;
        common = std::min(m_catalyst.length(),specie.m_substrate.length());
        float rate = exp(eH*common);
        Reaction complexFormation(m_id,1,specie.m_id,1,rate);
        complexFormation.addProduct(m_id+std::string("_")+specie.m_id,1);
        allReactions.push_back(complexFormation);
    }
    if (common == 0){
        throw std::invalid_argument("common = 0");
    }
}
//         //catalyst always stays
//         catGrowth.addProduct(specie.m_id,1);
//         if (m_length<maxLength){
//             catGrowth.addProduct(m_id+std::string("H"),1);
//         }
//         allReactions.push_back(catGrowth);

//Defining reactions here
std::list<Reaction> Specie::reactions(Specie specie){
    /* Nothing can:
     * - create Activated monomer (imp.) :implemented 
     * Activated monomer can:
     * - interact with Unfolded polymer in Growth reaction: (imp.)
     * - interact with Unfolded polymer in FalseGrowth reaction 
     *      if Unfolded polymer is maxLength long: (imp.)
     * - interact with Complex in Catalysis reaction(TODO) 
     * - interact with Complex in FalseCatalysis reaction
     *      if substate part of Complex is maxLength long: (TODO) 
     * - transform into 2mer 
     *      (this is interactinon with 1mers, 
     *      but we assume 1 mers are const concentration): (imp.)
     * Unfolded polymer (including 1mers and substrates) can:
     * - interact with activated monomer in Growth reaction (imp.)
     * - interact with activated monomer in FalseGrowth reaction
     *      if it's maxLength long (imp.)
     * - hydrolyze (imp.)
     * - degrade (imp.)
     * - aggregate if condtions met (imp.)
     * - fold (TEST)
     * Substrate is Unfolded polymer + it can:
     * - interact with Catalyst to form Complex (imp.)
     * Folded polymer (including catalysts) can:
     * - unfold (imp.)
     * - degrade (imp.)
     * Catalyst is Folded polymer + it can:
     * - interact with Substrate to form Complex (imp.)
     * Complex can:
     * - degrade (imp.TEST)
     * - interact with Activated monomer in Catalysis reaction (TODO)
     * - interact with Activated monomer in FalseCatalysis reaction
     *      if substate part of Complex is maxLength long: (TODO) 
     */

//    std::cout << "CALL " << m_id << ".reactions(" << specie.m_id << "), RETURNED:\n";

    //parameters
    float aH = configDict["monomerBirthH"].getFloat();
    float aP = configDict["monomerBirthP"].getFloat();     
    int maxLength = configDict["maxLength"].getInt();
     float alpha = configDict["growth"].getFloat();
    float d = configDict["unfoldedDegradation"].getFloat();
//     float dF = configDict["foldedDegradation"].getFloat();
    float k_unf = configDict["unfolding"].getFloat();
    float eH = configDict["hydrophobicEnergy"].getFloat();
    float dH = configDict["hydrolysisRate"].getFloat();
    float dAgg = configDict["aggregation"].getFloat();
    int aggPower = configDict["aggrDegree"].getInt();
    //all the reactions two species can have
    std::list<Reaction> allReactions;
    // 'H' and 'P' monomers are being produced from activated monomers, concentration of which is const.
    if (m_id==std::string("")){
        if (specie.m_id==std::string("")){
            importActive(allReactions,specie,aH,std::string("H"));
            importActive(allReactions,specie,aP,std::string("P"));
        }
    }
    //monomolecular reactions
    else if (m_id == specie.m_id && m_active){
        make2mer(allReactions,specie,alpha);
    }
    else if (m_id == specie.m_id && (not m_active)){
         //it degrades
        degradeIt(allReactions,specie,d);
    
        //if it's not folded
        if (m_folded == false){//BUG need to get read of complexes here
            //hydrolysis of any bond can happen
            hydrolyseIt(allReactions,specie,dH);
            //it can aggregate
            aggregateIt(allReactions,specie,dAgg,aggPower);
            //and might fold BUG what if m_native = 0
            foldIt(allReactions,specie,eH,k_unf);
        }
        //if specie is folded
        else{
            //it unfolds
            unfoldIt(allReactions,specie,k_unf);
        }
    }
    //if the other molecule is a catalyst and a given one isn't folded and a substate
    else if (specie.m_catalyst != std::string("N") && m_folded == false && 
        m_substrate.find(std::string("HH"))!= std::string::npos){
        std::cout << "other is folded " << std::endl;
        formComplex(allReactions,specie,alpha,eH);
    }
    //if a given molecule is a catalyst and the other molecule isn't folded and a substate TODO HERE
    else if (m_catalyst != std::string("N") && specie.m_folded == false && 
        specie.m_substrate.find(std::string("HH")) != std::string::npos){
        formComplex(allReactions,specie,alpha,eH);
    }
    else if (m_active && (specie.m_folded==false && specie.m_active==false)){
        growIt(allReactions,specie,alpha,maxLength);
    }
    else if ((m_folded==false && m_active==false) && specie.m_active==true){
        growIt(allReactions,specie,alpha,maxLength);
    }

//    for(auto it=allReactions.begin(); it != allReactions.end(); it++)
//        std::cout << (*it) <<std::endl;

    return allReactions;
}
Specie::~Specie(){
}
