#include <iostream>
#include "output.h"

//TODO
std::string storePopulations(TotalPopulation tp){
    std::list<Population> currentPops = tp.m_listOfPopulations;
    
    return std::string("todo");
}

//TODO
int openFile(std::string filename){
    return 0;
}

//TODO
int closeFile(std::string filename){
    return 1;
}


//TODO
std::string writeToFile(float currTime, std::list<Population> currPops, std::string filename){
    std::cout << "pretending that writing into " << filename << " at time " << currTime << std::endl;
    return std::string(".");
}

//TODO
float getPrevStep(float stepLen, float prevStep, float currTime){
    int t = currTime - prevStep;
    if (stepLen == 0){
        prevStep=currTime;
    }
    else{
        if (t >= 1.f && t < 2.f){
            prevStep = prevStep + 1.f;
        }
        else if (t >= 2.f){
            prevStep = prevStep + floor(t);
        }
        else{
            prevStep = prevStep;
        }
    }
    return prevStep;
}

//TEST
std::string writeOrNotTo(float stepLen, TotalPopulation tp, float prevStep, std::string prevPops, std::string filename){
    //if stepLen = 0, no questions: write every stepLen
    int t = tp.m_t - prevStep;
    if (stepLen == 0){
        writeToFile(tp.m_t, tp.m_listOfPopulations, filename);
        prevPops = std::string("");
    }
    else{
        if (t >= 1.f && t < 2.f){
            prevPops = writeToFile(tp.m_t, tp.m_listOfPopulations, filename);
        }
        else if (t >= 2.f){
            for (int time= prevStep+1.f; time < prevStep+t; time = time + 1.f){
                writeToFile(time, prevPops, filename);
            }
            prevPops = writeToFile(tp.m_t, tp.m_listOfPopulations, filename);
        }
    }
    return prevPops;
}