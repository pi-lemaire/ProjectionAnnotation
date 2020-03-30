# ProjectionAnnotation
A very simple GUI to determine the homography matrix used to convert from a photography taken at an angle to an ortho-photo (typically, an aerial photography).

It is coded to work under a Python 3 environment.

To have it work, you need the following libraries:
- numpy
- opencv
- tkinter (should be already installed on most configurations)

The principle is that you annotate matching points from an image you want to register to another

First, you open 2 image files at the same time. 3 windows open, 2 that you can annotate, with the images you have loaded. A third one is there to show you how the computed projection matrix is performing. At first, the left half of this image is empty.

Then, you annotate corresponding landmarks from one image to another. Once you have annotated at least 4 points, the computed result is visible on the visualization window.

Annotating is performed using only the left button on the mouse. A single click adds a button. You can drag an existing point to change its position. Deleting a point is performed by double-clicking.
Be careful to respect the same points ordering between both images.

For a better precision, it is advised to annotate more than 4 points. Several robust methods are available (see keyboard shortcuts) to reject the points with .

Keyboard shortcuts:
- n: load a new set of images
- s: save the resulting homography matrix into a .json file
- l: set the robust method to LMEDS (at least half of the points consensus)
- r: set the robust method to RANSAC
- p: set the robust method to RHO-RANSAC
- 0: don't set a robust method (all points taken into account equally)
