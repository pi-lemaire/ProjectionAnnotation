#ifndef ORTHORECTIFY_H
#define ORTHORECTIFY_H


#include <opencv2/opencv.hpp>

#include <nlohmann/json.hpp>

#include <fstream>


const std::string _OrthoRectify_YAMLKey_ImgFileToRectify   = "ImgFileToRectify";
const std::string _OrthoRectify_YAMLKey_ImgFileToOrtho     = "ImgFileToOrtho";
const std::string _OrthoRectify_YAMLKey_OrthoMat           = "OrthoMat";
const std::string _OrthoRectify_YAMLKey_CoordsPtsToRectify = "CoordsPtsToRectify";
const std::string _OrthoRectify_YAMLKey_CoordsPtsOrtho     = "CoordsPtsOrtho";



class OrthoRectify
{
public:
    OrthoRectify();
    ~OrthoRectify();

    bool loadJSONFile(const std::string &fileName);

private:
    std::string imgRectifyFilename, imgOrthoFilename, parametersFilename;
    cv::Mat orthoParameters, imgRectifyMat, imgOrthoMat;
    std::vector<cv::Point2i> coordsRectify, coordsOrtho;
};


#endif // ORTHORECTIFY_H
