#include <stdio.h>
#include <stdexcept>
#include "parameter.h"


Parameter::Parameter(){
    printf("strings goes here\n");
    m_valuePtr=NULL;
}
//BOOL
Parameter::Parameter(bool value){
    bool* ptr = new bool;
    *ptr = value;
    m_valuePtr = (void *) ptr;
    m_type = 0;
    printf("boolean created %s\n", value ? "true" : "false");
}
bool Parameter::getBool(){
    bool* ptr = (bool*) m_valuePtr;
    if (m_type != 0){
        throw std::invalid_argument("Parameter is not of type Bool");
    }
    return *ptr;
}

//INT
Parameter::Parameter(int value){
    int* ptr = new int;
    *ptr = value;
    m_valuePtr = (void *) ptr;
    m_type = 1;
    printf("int created: %d\n", value);
}
int Parameter::getInt(){
    int* ptr = (int*) m_valuePtr;
    if (m_type != 1){
        throw std::invalid_argument("Parameter is not of type Int");
    }
    return *ptr;
}

//FLOAT
Parameter::Parameter(float value){
    float* ptr = new float;
    *ptr = value;
    m_valuePtr = (void *) ptr;
    m_type = 2;
    
}
float Parameter::getFloat(){
    float* ptr = (float*) m_valuePtr;
    if (m_type != 2){
        throw std::invalid_argument("Parameter is not of type Float");
    }
    return *ptr;
}

//CASES
Parameter::~Parameter(){
    switch(m_type){
        case 0:{
            bool* ptr = (bool*) m_valuePtr;
            printf("bool deleted\n");
            delete ptr;
            break;
        }
        case 1:{
            int* ptr = (int *) m_valuePtr;
            printf("int deleted\n");
            delete ptr;
            break;
        }
        case 2:{
            float* ptr = (float *) m_valuePtr;
            printf("float deleted\n");
            delete ptr;
            break;
        }
        default:{
            throw std::invalid_argument("unknown type happened");
            break;
        }
    }
}

std::string Parameter::getType(){
    std::string typeValue;
    switch(m_type){
        case 0:{
            typeValue = std::string("bool");
            break;
        }
        case 1:{
            typeValue = std::string("int");
            break;
        }
        case 2:{
            typeValue = std::string("float");
            break;
        }
        default:{
            typeValue = std::string("unknown");
            break;
        }
    }
    
    return typeValue;
}



