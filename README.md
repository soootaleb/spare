# School Spacial Relations

This project aims to work on the fuzzy spacial relations.

# Resources

  * [How to show an OpenCV image with PyQt](https://stackoverflow.com/questions/52869400/how-to-show-image-to-pyqt-with-opencv)

# To Do

Those lists are the atomic steps to accomplish in order to produce a graphical application
that allows the user to load two binary images with objects and display the associated F-histogram

change line generation order according to angle in bresenham_angle (in image.py)

merge two images into one for GUI

test if it's working on rectangular images

## Improvement idea

keep an image in RGB only for visual, have a grayscale / boolean matrix for interating on it
resize images to have less empty border in each image
reshape image in order to iterate on smaller images depending on size
create histogram based on 180 degrees

## Basic functions

  * ~~Implement the `bresenham` function~~
  * ~~Implement the `scan_linear` function to execute Bresenham on all parallels~~
  * ~~Implement the `scan_polar` function to execute Bresenham on all angles~~

## Process functions

  * Move image to binary
  * ~~Mount a data structure that represents the object after a full scan~~
  * ~~Implement a function to compute a histogram value given an angle and a relation~~
  * ~~Mount a data structure that represents the full histogram on 360°~~

## GUI functions

  * ~~Implement the image loading from a button~~ (may be twice for two images)
  * ~~Implement the images display~~
  * ~~Implement the histogram display - classic~~
  * Implement the histogram display - radial

# Progress

## 360° scanning

> Only to use starting point at (0, 0) in the image
  using only end point on the other side of the image (x = height, or y = height). By doing so, we ensure to have always  a segment that have the max lenght of the image, ensuring we can scan the whole image. For the other angles, we apply a rotation of a multiple of 90° on the image.

Instead, the first implementation relies on a more flexible Bresenham algorithm which works for 360 degrees. This was maybe a bit trickier than a simple `image.rotate(90)`, but the final software design is cleaner and will certainly be more adapted to the next steps and eventual researches.

## Graphical User Interface

> We think that our client will see more value if a visual rendering is displayed. This rendering must allow simple interactions in order to allow us to see what happens and eventualy ensure it's working.

As a first implementation, we decided to implement a simple window that allow user to load a fixed image, and use a slider to indicate the scanning direction. The visual output is the image, on which we colored the pixels visited by the scan. By moving the solider and eventually activate the linear scanning, we can observe how our algorithm can walk on all pixels by a defined direction.

We want to show our result in differents ways :
  * using histogram, representing polar result for each relation :
      * Showing histogram
      * histogram contain one relation
      * further relations added to the histogram
  
  * using natural langage

## Histogram generation

Angular histogram
