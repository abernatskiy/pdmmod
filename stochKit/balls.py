#!/usr/bin/python


def filewriter(filename,numSpec,pop,collRate):
    f = open(filename,'w')
    f.write('<Model>\n') 
    f.write('\t<Description> balls with collision rate '+str(collRate)+' '+'</Description>\n')
    f.write('\t<NumberOfReactions>'+str(numSpec*(numSpec+1)/2)+'</NumberOfReactions>\n')
    f.write('\t<NumberOfSpecies>'+str(numSpec)+'</NumberOfSpecies>\n')
    f.write('\t<ParametersList>\n')
    parameterWriter(f,collRate)
    f.write('\t</ParametersList>\n')
    f.write('\t<ReactionsList>\n')
    reactionsWriter(f,numSpec,collRate)
    f.write('\t</ReactionsList>\n')
    f.write('\t<SpeciesList>\n')
    speciesWriter(f,numSpec,pop)
    f.write('\t</SpeciesList>\n')
    f.write('</Model>\n')
    f.close()
    print('File '+str(filename)+' is written')
    return None

def parameterWriter(File,collRate):#Add comments, test
    File.write('\t\t<Parameter>\n')
    File.write('\t\t\t<Id>c1</Id>\n')
    File.write('\t\t\t<Expression>'+str(collRate)+'</Expression>\n')
    File.write('\t\t</Parameter>\n')
    
    return None

def reactionsWriter(File,numSpec,collRate):#TODO
    id =0
    for i in range(1,numSpec+1):
        for j in range(1,i+1):
            id+=1
            File.write('\t\t<Reaction>\n')
            File.write('\t\t\t<Id>R'+str(id)+'</Id>\n')
            File.write('\t\t\t<Description>'+str("%04d" %i)+' + ' + str("%04d" %j)+' -> '+str("%04d" %i)+' + ' + str("%04d" %j)+' </Description>\n')
            File.write('\t\t\t<Type>mass-action</Type>\n')
            File.write('\t\t\t<Rate>c1</Rate>\n')
            File.write('\t\t\t<Reactants>\n')
            if i==j:
                File.write('\t\t\t<SpeciesReference id=\"'+str("%04d" %i)+'\" stoichiometry=\"2\"/>\n')
            else:
                File.write('\t\t\t<SpeciesReference id=\"'+str("%04d" %i)+'\" stoichiometry=\"1\"/>\n')
                File.write('\t\t\t<SpeciesReference id=\"'+str("%04d" %j)+'\" stoichiometry=\"1\"/>\n')
            File.write('\t\t\t</Reactants>\n')
            File.write('\t\t\t<Products>\n')
            if i==j:
                File.write('\t\t\t<SpeciesReference id=\"'+str("%04d" %i)+'\" stoichiometry=\"2\"/>\n')
            else:
                File.write('\t\t\t<SpeciesReference id=\"'+str("%04d" %i)+'\" stoichiometry=\"1\"/>\n')
                File.write('\t\t\t<SpeciesReference id=\"'+str("%04d" %j)+'\" stoichiometry=\"1\"/>\n')
            File.write('\t\t\t</Products>\n')
            File.write('\t\t</Reaction>\n')
    return None


def speciesWriter(File,numSpec,pop):
    for i in range(1,numSpec+1):
        File.write('\t\t<Species>\n')
        File.write('\t\t\t<Id>'+str("%04d" %i)+'</Id>\n')
        File.write('\t\t\t<Description>Species #'+str("%04d" %i)+'</Description>\n')
        File.write('\t\t\t<InitialPopulation>'+str(pop)+'</InitialPopulation>\n')
        File.write('\t\t</Species>\n')
    
    
    return None

#filename = 'b.xml'
#numSpec = 3
#pop = 4
#collRate =0.5

#filewriter(filename,numSpec,pop,collRate)
