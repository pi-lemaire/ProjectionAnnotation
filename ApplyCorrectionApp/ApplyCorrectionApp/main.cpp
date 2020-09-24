#include <iostream>
#include "InputParser.h"
#include "OrthoRectify.h"

#include <opencv2/opencv.hpp>


using namespace std;

int main(int argc, char *argv[])
{
    std::string parametersJsonFile, trackletsInputCsvFile, correctedTrackletsOutputCsvFile;

    InputParser input(argc, argv);


    parametersJsonFile = "/Volumes/LaCie/stationair/apps/code snippets/python homography calculator/2016-03-18_siteouvert_orion_1080p_24fps_maisoncarree_00001.MTS_id0_fr6811.png.json";
    trackletsInputCsvFile = "/Volumes/LaCie/stationair/GroundTruth/ExtractedFG/WholeSeq/2016-03-18_siteouvert_orion_1080p_24fps_maisoncarree_00001.MTS_Tracklets.csv";
    correctedTrackletsOutputCsvFile = "test.csv";

    if (input.cmdOptionExists("-params"))
    {
        parametersJsonFile = input.getCmdOption("-params");
    }
    if (input.cmdOptionExists("-trackletsIn"))
    {
        trackletsInputCsvFile = input.getCmdOption("-trackletsIn");
    }
    if (input.cmdOptionExists("-trackletsOut"))
    {
        correctedTrackletsOutputCsvFile = input.getCmdOption("-trackletsOut");
    }

    cout << "input file for parameters : " << parametersJsonFile << endl;
    cout << "tracklets input file : " << trackletsInputCsvFile << endl;
    cout << "corrected tracklets output file : " << correctedTrackletsOutputCsvFile << endl;

    OrthoRectify ortho;

    if (ortho.loadJSONFile(parametersJsonFile))
        cout << "success" << endl;
    else
        cout << "failure" << endl;

}
