#ifndef __SPECIE_H
#define __SPECIE_H

#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

/*binary polymers
 * sequences grow on its own and never decay
 */




class Specie
{
public:
    std::string modelName;
    Specie(){};
    Specie(std::string id);
    ~Specie();
    
    //attributes
    std::string m_id;
    std::string m_catalyst;
    std::string m_substrate;
    bool m_product;
    int m_length;
    bool m_folded;
    int m_native;
    float m_hydrophobicity;
    bool m_active;
    
    //constants
    
    
    //methods
    std::list<Reaction> reactions(Specie specie);
    
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
    
private:
    //imports either H* or P* 
    void importHorP( std::list<Reaction>& allReactions,Specie other,
                       float impRate,std::string HorP);

    void degradeIt(std::list<Reaction>& allReactions,Specie specie,
              float degrRate);

    void aggregateIt(std::list<Reaction>& allReactions,Specie specie,
                      float aggRate,float aggPower);
    void hydrolyseIt(std::list<Reaction>& allReactions,Specie specie,
                     float dH);
    void foldIt(std::list<Reaction>& allReactions,Specie specie,
                        float eH, float k_unf);
    void unfoldIt(std::list<Reaction>& allReactions,Specie specie,
                  float k_unf);
    void growIt(std::list<Reaction>& allReactions,Specie specie,
                float alpha, std::string HorP, int maxLength);
    void catalyzeIt(std::list<Reaction>& allReactions,Specie specie,
                    float alpha, float eH,int maxLength);
};


#endif // __SPECIE_H
