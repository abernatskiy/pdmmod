#!/usr/bin/python
import math

def wr(f,tab,line):
    return f.write('\t'*tab+line+'\n')

def filewriter(filename,modelName,numSpec,maxLength,collRate):#TODO
    f = open(filename,'w')
    wr(f,0,'<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    wr(f,0,'<sbml xmlns="http://www.sbml.org/sbml/level2/version4" level="2" version="4">')
    wr(f,0,'<model id="'+str(modelName)+'" name="model">')
    wr(f,1,'<listOfCompartments>')
    wr(f,2,'<compartment id="compartment_1" name="default" size="1" units="volume"/>')
    wr(f,1,'</listOfCompartments>')
    speciesWriter(f,numSpec,maxLength)
    parameterWriter(f,collRate)
    reactionsWriter(f,numSpec,collRate)
    wr(f,0,'</model>')
    wr(f,0,'</sbml>')
    f.close()
    print('File '+str(filename)+' is written')
    return None

def speciesWriter(f,numSpec,maxLength):#TEST
    wr(f,1,'<listOfSpecies>')
    globalCount = 0
    for i in range(1,(numSpec+1)):
        for j in range(1,maxLength+1):
            globalCount+=1
            wr(f,2,'<species compartment="compartment_1" '+
            'id="'+'species_'+str("%05d" %globalCount)+'"'+
            ' initialAmount="1"'+
            ' name="'+str("%04d" %i)+'_'+str(j)+'"/>')
    wr(f,1,'</listOfSpecies>')
    
    return None

def parameterWriter(f,collRate):#TEST
    wr(f,1,'<listOfParameters>')
    wr(f,2,'<parameter id="k" name="k" units="rate" value="'+str(collRate)+'"/>')
    wr(f,1,'</listOfParameters>')
    return None

def convToName(i,maxLength):
    rem = i%maxLength
    main = math.ceil(i/maxLength)
    if rem == 0:
        rem = maxLength
    name1=str("%04d" %main)+'_'+str(rem)
    return name1

def growIt(i,maxLength):
    rem = i%maxLength
    main = math.ceil(i/maxLength)
    iRet = i
    if rem == 0:
        rem = 1
        iRet = iRet-maxLength+1
    else:
        rem = rem+1
        iRet=iRet+1
    return str("%04d" %main)+'_'+str(rem),iRet
    

def reactionsWriter(f,numSpec,collRate):#TODO
    id =0
    wr(f,1,'<listOfReactions>')
    for i in range(1,(numSpec*maxLength+1)):
        name1=convToName(i,maxLength)
        for j in range(1,i+1):
            name2=convToName(j,maxLength)
            id+=1
            wr(f,2,'<reaction id="reaction_'+str("%06d" %id)+'" name="collision" reversible="false">')
            wr(f,3,'<listOfReactants>')
            if not i==j:
                wr(f,4,'<speciesReference name="'+
                    name1+'" species="species_'+
                    str("%05d" %i)+'" stoichiometry="1"/>')
                wr(f,4,'<speciesReference name="'+
                    name2+'" species="species_'+
                    str("%05d" %j)+'" stoichiometry="1"/>')
            else:
                wr(f,4,'<speciesReference name="'+
                    name1+'" species="species_'+
                    str("%05d" %i)+'" stoichiometry="2"/>')
            wr(f,3,'</listOfReactants>')
            wr(f,3,'<listOfProducts>')
            prod1, iRet = growIt(i,maxLength)
            prod2, jRet = growIt(j,maxLength)
            if not i==j:
                wr(f,4,'<speciesReference name="'+
                    prod1+'" species="species_'+
                    str("%05d" %iRet)+'" stoichiometry="1"/>')
                wr(f,4,'<speciesReference name="'+
                    prod2+'" species="species_'+
                    str("%05d" %jRet)+'" stoichiometry="1"/>')
            else:
                wr(f,4,'<speciesReference name="'+
                    prod1+'" species="species_'+
                    str("%05d" %iRet)+'" stoichiometry="2"/>')
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




#filename = 'b.sbml'
#numSpec = 3
#pop = 4
#collRate =0.5
#maxLength=2
#modelName = 'balls'

#filewriter(filename,modelName,numSpec,maxLength,collRate)
