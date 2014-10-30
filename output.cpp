#include <fstream>
#include "output.h"

//TODO
std::string storePopulations(TotalPopulation tp){
    std::list<Population> currentPops = tp.m_listOfPopulations;
    std::string x = "Populations";
    return x;
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



//TODO
std::string writeToFile(std::string strPops, float time, std::ofstream myfile){
    std::cout << "pretending that writing into a file at time " << time  << std::endl;
    
    myfile << time << "/";
    myfile << strPops <<"\n";
    
    return std::string(".");
}

//TODO
float getPrevStep(float stepLen, float prevStep, float currTime){
    int t = currTime - prevStep;
    if (stepLen == 0){
        prevStep=currTime;
    }
    else{
        if (t >= stepLen && t < 2.f*stepLen){
            prevStep = prevStep + 1.f;
        }
        else if (t >= 2.f*stepLen){
            prevStep = prevStep + floor(t);
        }
        else{
            prevStep = prevStep;
        }
    }
    return prevStep;
}

//TEST
std::string writeOrNotTo(float stepLen, TotalPopulation tp, float prevStep, std::string prevPops, std::ofstream myfile){
    //if stepLen = 0, no questions: write every stepLen
    int t = tp.m_t - prevStep;
    if (stepLen == 0){
        writeToFile(storePopulations(tp),tp.m_t, myfile);
        prevPops = std::string("");
    }
    else{
        if (t >= stepLen && t < 2.f*stepLen){
            prevPops = writeToFile(storePopulations(tp),tp.m_t, myfile);
        }
        else if (t >= 2.f*stepLen){
            std::cout << "prevStep is " << prevStep << std::endl;
            std::cout << "stepLen is " <<stepLen << std::endl;
            for (float time= prevStep+stepLen; time < prevStep+t; time = time + stepLen){
                std::cout << "time is " << time << std::endl;
                writeToFile(prevPops, time, myfile);
            }
            prevPops = writeToFile(storePopulations(tp),tp.m_t, myfile);
            
        }
    }
    return prevPops;
}