#include "parametersLoader.h"

#include "inih/ini.h"
#include <iostream>
#include <cstdlib>
#include <cstring>

static int handler(void* user, const char* section, const char* name, const char* value){
    // The function which is called every time a new entry is read from the parameters INI file

    std::map<std::string,Parameter>* dict = (std::map<std::string,Parameter>*) user;

    std::cout << section << std::endl;
    if(strcmp(section, "kinetic model") == 0) // processing the "kinetic model" section entries
    {
        float tempval = std::stof(value); // TODO replace with type autodetection
        dict->emplace(name, tempval);
        return 0;
    }
    else // no other sections allowed
        std::cout << "Cannot recognize parameter INI file section " << section << std::endl;
    return 1;
}

void readConfig(std::map<std::string,Parameter>* dict, std::string filename){
    std::cout << "Reading parameters from " << filename << std::endl;
    if(ini_parse(filename.c_str(), handler, (void*) dict) < 0){
        std::cout << "Can't load parameters\n";
        exit(1);
    }
    return;
}

void showConfig(std::map<std::string,Parameter>* dictionary){
    std::cout << "Parameters: ";
    for(auto it=dictionary->begin(); it!=dictionary->end(); it++)
        std::cout << it->first << "=" << (it->second).getString() << " ";
    std::cout << std::endl;
    return;
}
