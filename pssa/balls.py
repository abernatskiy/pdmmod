#!/usr/bin/python

def wr(f,tab,line):
    return f.write('\t'*tab+line+'\n')

def filewriter(filename,modelName,numSpec,pop,collRate):#TODO
    f = open(filename,'w')
    wr(f,0,'<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    wr(f,0,'<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">')
    wr(f,0,'<model id="'+str(modelName)+'" name="model">')
    wr(f,1,'<listOfCompartments>')
    wr(f,2,'<compartment id="compartment_1" name="default" size="1" units="volume"/>')
    wr(f,1,'</listOfCompartments>')
    speciesWriter(f,numSpec,pop)
    parameterWriter(f,collRate)
    reactionsWriter(f,numSpec,collRate)
    wr(f,0,'</model>')
    wr(f,0,'</sbml>')
    #f.close()
    print('File '+str(filename)+' is written')
    return None

def speciesWriter(f,numSpec,pop):#TEST
    wr(f,1,'<listOfSpecies>')
    for i in range(1,numSpec+1):
        wr(f,2,'<species compartment="compartment_1" '+
           'id="'+'species_'+str("%05d" %i)+'"'+
           ' initialAmount="'+str(pop)+'"'+
           ' name="'+str("%05d" %i)+'"/>')
    wr(f,1,'</listOfSpecies>')
    
    return None

def parameterWriter(f,collRate):#TEST
    wr(f,1,'<listOfParameters>')
    wr(f,2,'<parameter id="k" name="k" units="rate" value="'+str(collRate)+'"/>')
    wr(f,1,'</listOfParameters>')
    return None

def reactionsWriter(f,numSpec,collRate):#TODO
    id =0
    wr(f,1,'<listOfReactions>')
    for i in range(1,numSpec+1):
        for j in range(1,i+1):
            id+=1
            wr(f,2,'<reaction id="reaction_'+str("%06d" %id)+'" name="collision" reversible="false">')
            wr(f,3,'<listOfReactants>')
            if not i==j:
                wr(f,4,'<speciesReference name="'+
                    str("%05d" %i)+'" species="species_'+
                    str("%05d" %i)+'" stoichiometry="1"/>')
                wr(f,4,'<speciesReference name="'+
                    str("%05d" %j)+'" species="species_'+
                    str("%05d" %j)+'" stoichiometry="1"/>')
            else:
                wr(f,4,'<speciesReference name="'+
                    str("%05d" %i)+'" species="species_'+
                    str("%05d" %i)+'" stoichiometry="2"/>')
            wr(f,3,'</listOfReactants>')
            wr(f,3,'<listOfProducts>')
            if not i==j:
                wr(f,4,'<speciesReference name="'+
                    str("%05d" %i)+'" species="species_'+
                    str("%05d" %i)+'" stoichiometry="1"/>')
                wr(f,4,'<speciesReference name="'+
                    str("%05d" %j)+'" species="species_'+
                    str("%05d" %j)+'" stoichiometry="1"/>')
            else:
                wr(f,4,'<speciesReference name="'+
                    str("%05d" %i)+'" species="species_'+
                    str("%05d" %i)+'" stoichiometry="2"/>')
            wr(f,3,'</listOfProducts>')
            wr(f,3,'<kineticLaw>')
            wr(f,4,'<math xmlns="http://www.w3.org/1998/Math/MathML">')
            wr(f,5,'<apply>')
            wr(f,6,'<times/>')
            wr(f,6,'<ci>k</ci>')
            wr(f,6,'<cn type="real">1.0</cn>')
            wr(f,5,'</apply>')
            wr(f,4,'</math>')
            wr(f,3,'</kineticLaw>')
            wr(f,2,'</reaction>')
    wr(f,1,'</listOfReactions>')
    return None



if __name__ == "__main__":
    filename = 'b.sbml'
    numSpec = 3
    pop = 4
    collRate =0.5
    modelName = 'balls'
    filewriter(filename,modelName,numSpec,pop,collRate)
