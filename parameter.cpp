#include "parameter.h"


Parameter::Parameter(){
    m_value=NULL;
}
//BOOL
Parameter::Parameter(bool value){
    bool* ptr = new bool;
    *ptr = value;
    m_valuePtr = (void *) ptr;
    m_type = 0;
}
bool Parameter::getBool(){
    bool* ptr = (bool*) m_valuePtr;
    //TODO Exceptions
    return *ptr;
}

//INT
Parameter::Parameter(int value){
    int* ptr = new int;
    *ptr = value;
    m_valuePtr = (void *) ptr;
    m_type = 1;
}
int Parameter::getBool(){
    int* ptr = (int*) m_valuePtr;
    //TODO Exceptions
    return *ptr;
}

//CASES
Parameter::~Parameter(){
    switch(m_type){
        case 0:
            bool* ptr = (bool*) m_valuePtr;
            delete ptr;
        case 1:
            int* ptr = (int *) m_valuePtr;
    }
}

std::string Parameter::getType(){
    switch(m_type){
        case 0:
            std::string typeValue = std::string("bool");
        case 1:
            std::string typeValue = std::string("int");
    }
    }
    
    return typeValue;
}



