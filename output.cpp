#include "output.h"

extern std::map<std::string,Parameter> configDict;

//TODO
std::string storePopulations(TotalPopulation* tp){
    std::stringstream ss;
    for (auto pops_it = tp->m_listOfPopulations.begin(); pops_it != tp->m_listOfPopulations.end(); pops_it++)
    {
        if( pops_it->m_specie.m_id != "" ){
            ss << pops_it->m_specie.m_id << " " << pops_it->m_n << ",";
        }
    }
    return ss.str();
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

void writeHeaderToFile(TotalPopulation* tp, int argc, char** argv, std::ofstream* myfile){

    std::string modelName = (((tp->m_listOfPopulations).begin())->m_specie).modelName;
    (*myfile) << "# Model: " << modelName << std::endl;
    (*myfile) << "#";
    for(auto it = configDict.begin(); it != configDict.end(); it++)
        (*myfile) << " " << it->first << "=" << (it->second).getString();
    (*myfile) << std::endl;
    (*myfile) << "# Command line:";
    for(int i=0; i<argc; i++)
        (*myfile) << " " << std::string(argv[i]);
    (*myfile) << std::endl;
    return;
}

//TODO
void writeToFile(std::string strPops, float time, std::ofstream* myfile){
    std::cout << "writing to a file at time " << time  << std::endl;

    (*myfile) << time << ",";
    (*myfile) << strPops <<"\n";

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
std::string writeOrNotTo(float stepLen, TotalPopulation* tp, float prevStep, std::string prevPops, std::ofstream* myfile){
    //if stepLen = 0, no questions: write every stepLen
    int t = (tp->m_t) - prevStep;
    if (stepLen == 0){
        writeToFile(storePopulations(tp),tp->m_t, myfile);
        prevPops = std::string("");
    }
    else{
        if (t >= stepLen && t < 2.f*stepLen){
            prevPops = storePopulations(tp);
            writeToFile(prevPops,tp->m_t, myfile);
        }
        else if (t >= 2.f*stepLen){
            std::cout << "prevStep is " << prevStep << std::endl;
            std::cout << "stepLen is " <<stepLen << std::endl;
            for (float time= prevStep+stepLen; time < prevStep+t; time = time + stepLen){
                std::cout << "time is " << time << std::endl;
                writeToFile(prevPops, time, myfile);
            }
            prevPops = storePopulations(tp);
            writeToFile(prevPops,tp->m_t, myfile);
        }
    }
    return prevPops;
}
