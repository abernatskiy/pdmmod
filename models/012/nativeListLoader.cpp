#include "nativeListLoader.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <iterator>
#include <cstdlib>
#include <iostream>

/*DATA
 * catPattern -- string. (cases)
 * interp.:
 *  - if consists of 'H' and 'P' then represents a catalytic site of a given catalyst.
 *  - if it's 'N' then it means the sequence is NOT a catalyst
 *
 * catPatterns -- dict. {string: string}
 * interp. a dictionary from monomer sequence string to catalytic pattern string
 *
 * wellDepth -- dict. {string: int}
 * interp. a dictionary form monomer sequence string to potential well depth (energy of folded state)
 */


std::map<std::string,std::string> readCatPatterns(std::string filename)
{
    std::map<std::string,std::string> catPatterns;
    std::string line;
    std::ifstream nativeList(filename, std::ifstream::in);
    std::cout << "reading " << filename << std::endl;
    if(nativeList.is_open())
    {
        std::getline(nativeList, line); // ignoring the first line
                                        // TODO make normal comments support
        while(std::getline(nativeList, line))
        {
            std::istringstream iss(line);
            std::vector<std::string> tokens{std::istream_iterator<std::string>{iss}, std::istream_iterator<std::string>{}};

            catPatterns[tokens[0]] = tokens[2];
        }
        nativeList.close();
    }
    else
    {
        std::cout << "nativeListLoader.cpp: Cannot open the native list file " << filename << std::endl;
        exit(EXIT_FAILURE);
    }
    return catPatterns;
}

std::map<std::string,int> readWellDepths(std::string filename)
{
    std::map<std::string,int> wellDepths;
    std::string line;
    std::ifstream nativeList(filename, std::ifstream::in);
    if(nativeList.is_open())
    {
        std::getline(nativeList, line); // ignoring the first line
                                        // TODO make normal comments support
        while(std::getline(nativeList, line))
        {
            std::istringstream iss(line);
            std::vector<std::string> tokens{std::istream_iterator<std::string>{iss}, std::istream_iterator<std::string>{}};
            int wellDepth = std::stoi(tokens[1]);
            wellDepths[tokens[0]] = wellDepth;
        }
        nativeList.close();
    }
    else
    {
        std::cout << "nativeListLoader.cpp: Cannot open the native list file " << filename << std::endl;
        exit(EXIT_FAILURE);
    }
    return wellDepths;
}
