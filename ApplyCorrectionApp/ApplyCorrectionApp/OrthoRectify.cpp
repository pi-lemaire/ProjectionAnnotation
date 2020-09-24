#include "OrthoRectify.h"

using namespace cv;
using namespace std;


// for convenience
using json = nlohmann::json;





OrthoRectify::OrthoRectify()
{
    this->orthoParameters = Mat::eye(3,3,CV_64FC1);
}


OrthoRectify::~OrthoRectify()
{
    this->orthoParameters.release();
    this->imgRectifyMat.release();
    this->imgOrthoMat.release();
}




bool OrthoRectify::loadJSONFile(const std::string &fileName)
{
    std::ifstream inFile(fileName);

    if (!inFile.is_open())
        return false;

    json fileContent;
    inFile >> fileContent;

    if (fileContent.contains(_OrthoRectify_YAMLKey_ImgFileToRectify))
    {
        cout << "key " << _OrthoRectify_YAMLKey_ImgFileToRectify << " found" << endl;
        this->imgRectifyFilename = fileContent.at(_OrthoRectify_YAMLKey_ImgFileToRectify).get<std::string>();
        this->imgRectifyMat = imread(this->imgRectifyFilename);
    }
    if (fileContent.contains(_OrthoRectify_YAMLKey_ImgFileToOrtho))
    {
        cout << "key " << _OrthoRectify_YAMLKey_ImgFileToOrtho << " found" << endl;
        this->imgOrthoFilename = fileContent.at(_OrthoRectify_YAMLKey_ImgFileToOrtho).get<std::string>();
        this->imgOrthoMat = imread(this->imgOrthoFilename);
    }
    if (fileContent.contains(_OrthoRectify_YAMLKey_OrthoMat))
    {
        if (fileContent.at(_OrthoRectify_YAMLKey_OrthoMat).is_array())
        {
            cout << "key " << _OrthoRectify_YAMLKey_OrthoMat << " is an array" << endl;
            json matrixNode = fileContent.at(_OrthoRectify_YAMLKey_OrthoMat);

            vector<vector<double> > vecMatrix = matrixNode.get<vector<vector<double> > >();
            // cout << vecMatrix.size() << endl;

            // just consider that the matrix was well initialized and the object size is right
            for (size_t i=0; i<vecMatrix.size(); i++)
                for (size_t j=0; j<vecMatrix[i].size(); j++)
                    this->orthoParameters.at<double>(static_cast<int>(i),static_cast<int>(j)) = vecMatrix[i][j];

            cout << this->orthoParameters;
        }
        else
            cout << "key " << _OrthoRectify_YAMLKey_OrthoMat << " was not found to be an array" << endl;
    }




    if (fileContent.contains(_OrthoRectify_YAMLKey_CoordsPtsToRectify))
    {
        if (fileContent.at(_OrthoRectify_YAMLKey_CoordsPtsToRectify).is_array())
        {
            cout << "key " << _OrthoRectify_YAMLKey_CoordsPtsToRectify << " is an array" << endl;
            json RectifPoints = fileContent.at(_OrthoRectify_YAMLKey_CoordsPtsToRectify);

            vector<vector<int> > coords = RectifPoints.get<vector<vector<int> > >();
            cout << coords.size() << " points found" << endl;

            this->coordsRectify.clear();

            // just consider that the matrix was well initialized and the object size is right
            for (size_t i=0; i<coords.size(); i++)
            {
                this->coordsRectify.push_back( Point2i(coords[i][0], coords[i][1]));
                cout << "point " << this->coordsRectify[i] << " added" << endl;
            }

        }
        else
            cout << "key " << _OrthoRectify_YAMLKey_CoordsPtsToRectify << " was not found to be an array" << endl;
    }



    if (fileContent.contains(_OrthoRectify_YAMLKey_CoordsPtsOrtho))
    {
        if (fileContent.at(_OrthoRectify_YAMLKey_CoordsPtsOrtho).is_array())
        {
            cout << "key " << _OrthoRectify_YAMLKey_CoordsPtsOrtho << " is an array" << endl;
            json OrthoPoints = fileContent.at(_OrthoRectify_YAMLKey_CoordsPtsOrtho);

            vector<vector<int> > coords = OrthoPoints.get<vector<vector<int> > >();
            cout << coords.size() << " points found" << endl;

            this->coordsOrtho.clear();

            // just consider that the matrix was well initialized and the object size is right
            for (size_t i=0; i<coords.size(); i++)
            {
                this->coordsOrtho.push_back( Point2i(coords[i][0], coords[i][1]));
                cout << "point " << this->coordsOrtho[i] << " added" << endl;
            }

        }
        else
            cout << "key " << _OrthoRectify_YAMLKey_CoordsPtsOrtho << " was not found to be an array" << endl;
    }

    // cout << fileContent.dump(4) << endl;

    /*

    FileStorage fsR(fileName, FileStorage::READ);

    if (!fsR.isOpened())
        return false;

    this->parametersFilename = fileName;
    */

   /*
    const std::string _OrthoRectify_YAMLKey_ImgFileToRectify   = "ImgFileToRectify";
    const std::string _OrthoRectify_YAMLKey_ImgFileToOrtho     = "ImgFileToOrtho";
    const std::string _OrthoRectify_YAMLKey_OrthoMat           = "OrthoMat";
    const std::string _OrthoRectify_YAMLKey_CoordsPtsToRectify = "CoordsPtsToRectify";
    const std::string _OrthoRectify_YAMLKey_CoordsPtsOrtho     = "CoordsPtsOrtho";
    */


    /*
    if (!fsR[_OrthoRectify_YAMLKey_ImgFileToRectify].empty())
    {
        fsR[_OrthoRectify_YAMLKey_ImgFileToRectify] >> this->imgRectifyFilename;
        this->imgRectifyMat = imread(this->imgRectifyFilename);

        cout << "filename of the image that we wish to rectify : " << this->imgRectifyFilename << endl;
    }

    if (!fsR[_OrthoRectify_YAMLKey_ImgFileToOrtho].empty())
    {
        fsR[_OrthoRectify_YAMLKey_ImgFileToOrtho] >> this->imgOrthoFilename;
        this->imgOrthoMat = imread(this->imgOrthoFilename);

        cout << "filename of the ortho image file : " << this->imgOrthoFilename << endl;
    }

    if (!fsR[_OrthoRectify_YAMLKey_OrthoMat].empty())
        fsR[_OrthoRectify_YAMLKey_OrthoMat] >> this->imgOrthoMat;

    cout << "ortho matrix values : " << this->imgOrthoMat << endl;
    */

    return true;
}


// std::string imgRectifyFilename, imgOrthoFilename, parametersFilename;
// cv::Mat orthoParameters, imgRectifyMat, imgOrthoMat;





/*
self.perspImgFilename = str(data['ImgFileToRectify'])
self.orthoImgFilename = str(data['ImgFileToOrtho'])

#print(self.perspImgFilename)
#print(self.orthoImgFilename)

self.loadNewImageFiles()

self.resultOrthoMat = np.array(data['OrthoMat'])

self.listPointsRectify = []
tmpListPointsRectify = tuple(data['CoordsPtsToRectify'])
for t in tmpListPointsRectify:
    self.listPointsRectify.append(tuple(t))

self.listPointsOrtho = []
tmpListPointsOrtho = tuple(data['CoordsPtsOrtho'])
*/
