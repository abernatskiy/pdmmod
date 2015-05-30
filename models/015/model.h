#ifndef __SPECIE_H
#define __SPECIE_H
#include <map>
#include <vector>
#include <string>
#include <list>
#include "parameter.h"
#include "reaction.h"

/*binary polymers
 * sequences grow on its own and never decay
 */

extern std::map<std::string,std::string> catPatterns;


class Specie
{
    /* A Specie can be:
     * - activated monomer
     * - unfolded polymer, including 1-mers
     * - folded polymer
     * - substrate: unfolded polymer with 'HH' in the end
     * - catalyst: folded polymer, if catalyst catPatterns[m_id]!= "N"
     * - complex: catalyst and substate bound together
     *      m_id = catalyst.m_id+"_"+substate.m_id
     */
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
    bool m_complex;
    
    //constants
    
    
    //methods
    std::list<Reaction> reactions(Specie specie);
    
    friend std::ostream& operator<<(std::ostream& os, const Specie& sp);
    // Methods
private:
    //imports either H* or P* 
    void importActive( std::list<Reaction>& allReactions,Specie other,
                       float impRate,std::string HorP);
    //degrades or aggregates molecule
    void degradeIt(std::list<Reaction>& allReactions,Specie specie,
                      float degrRate);
    void hydrolyseIt(std::list<Reaction>& allReactions,Specie specie,
                             float dH);
    void aggregateIt(std::list<Reaction>& allReactions,Specie specie,
                     float aggRate,int aggPower);
    void foldIt(std::list<Reaction>& allReactions,Specie specie,
           float eH, float k_unf);
    void unfoldIt(std::list<Reaction>& allReactions,Specie specie,
                  float k_unf);
    void formComplex(std::list<Reaction>& allReactions,Specie specie,
                     float alpha, float eH);
    
};

#endif // __SPECIE_H
