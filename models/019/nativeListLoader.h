#ifndef __NATIVE_LIST_LOADER_H
#define __NATIVE_LIST_LOADER_H

#include <string>
#include <map>

std::map<std::string,std::string> readCatPatterns(std::string filename);
std::map<std::string,int> readWellDepths(std::string filename);

#endif // __NATIVE_LIST_LOADER_H
