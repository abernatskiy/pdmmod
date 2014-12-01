#include "nativeListLoader.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <iterator>

std::map<std::string,std::string> readCatPatterns(std::string filename)
{
    std::map<std::string,std::string> catPatterns;
    std::string line;
    std::ifstream nativeList(filename);
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
    return catPatterns;
}

std::map<std::string,int> readWellDepths(std::string filename)
{
    std::map<std::string,int> wellDepths;
    std::string line;
    std::ifstream nativeList(filename);
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
    return wellDepths;
}
