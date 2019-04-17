# School Spacial Relations

This project aims to work on the fuzzy spacial relations

# Features

The project is composed of a graphical user interface that allows one to interact with the application. It allows you to change the parameters and easily observe the impact on the histograms, used by the descriptors to describe the scene.

The description is colored corresponding to a sort of _quality_ of the result. It means that when the phrase is red, the program understands that the description is not really relevant. On the other hand a green label will indicate a strong faith in what is written.

Here are the different parameters you can play with in the graphical user interface.

  - Displaying the result of bresenham algorithm (move the angle slider)
    - On ray
    - All parallels
  - Change the angle in which apply the bresenham algorithm
  - Change the variance of the mask (a gaussian curve) applied on the descriptor
  - Save the current histogram values (in csv or json files)
  - Rotate the `relative` image
  - Change the number of computed angles on the histogram
  - Resize the images
  - Switch between polar & classic histogram

The labels will help you understand the roles of the buttons and sliders.

# Starting

This project has been developped using the Python 3 language. The need dependencies for python are
  
  - pyqt5
  - matplotlib
  - opencv-python

Those libraries may need system libraries like Qt or different other dev dependencies.

When the dependencies are met, simply execute `python src/main.py` in order to start the program. The GUI should pop on your screen.

# Architecture

This section describes how the software is developped in order to allow further extensions. The general approach is like an MVC application

The models represent data structures manipulated by the computations around the project. The view part is not really isolated but is mainly encapsulated in the `app.py#Application#init_ui` method. The controller part is in the rest of the `Application` class using callbacks on the buttons clicked (`@pyQtSlot()`)

In general, the system has been kept easy to extend and customize by relying on a simple yet powerful data model.

## Models

The models are classicaly composed of `Points` in a bigger `Image` which is mainly a numpy matrix (from opencv). Those `Points` are also part of a `Segment` model in order to manipulate the rays which are the main component of our approach. Also, a `Descriptor` combined the relations and is based on a `Histogram`

### Point

The `Point` class is very simple yet used pretty much everywhere. It ensures that that constructed point `Point(x, y)` is given `x > 0 && y > 0`. It also implements how to print a point in the console, and overrides the `==` operator.

### Segment

A `Segment` inherits from the python `list`.

  - It has a random color to observe it visualy
  - You can `Segment::append` a `Point`, only if the given point is next to the last one of the segment and not already in.
  - `Point::horizontal` and `Point::vertical` return booleans
  - You can access points like python lists with `Segment[Point]` or `Segment[3]` or any iterable with at leats two values (tuple, etc).
  - You can get the angle of a segment (defaults to degrees but can be obtained by radians)

### Image

The `Image` class is used to add features on the classical `cv.Image`. This class implements _method chaining_ which allows one to chain methods in order to apply multiple modifications like

```python
img = Image('my_image.png') \
    .resize(1/6) \
    .rotate(90)
```

#### Loading

You can load an image (in memory) by passing a file name in the constructor. The file must be in the `Image::IMAGES_DIR` directory, which defaults to the `images` folder at the root of this project.

Additionaly, you can choose to load the image in binary or in color with the associated parameter.

> Images are classical `cv.Mat` objects. When loading a binary image, the constructor will transform all positive values (like 255) to 1. This allows potential bitwise operations and potential optimisations.

You can also load an image which is already in memory (like a `cv.Mat`). When the first parameter `fname` is recognized as is, the matrix is loaded instead of the file.

#### Manipulating

First, it's important to note that manipulations are not done on the original image. In order to allow a `Image::reset` function or simply to allow lazy modification, the constructor creates a copy of the original image with `self.image.copy()`. This allows to not load the image each time we want it fresh, what is often necessary with the graphical rendering.

#### Operations

Here are the operations available on the `Image` class.

  - `Image::resize` using `cv.resize`, the factor must be < 1 if you want to make it smaller
  - `Image::rotate` you must pass angle by degrees
  - `Image::merge` merges the given image with the current instance and **returns a new Image instance**
  - `Image::ray` returns a `Segment` corresponding to the image points in a given direction. All points are existing in the image.
  - `Image::parallels` returns the parallel `Segment`s in a given direction. All points are in the image.
  - `Image::draw` will set the points of the `Segment` in color in the corresponding image. The color is defined randomly by the segment.
  - `Image::reset` will reset the image as it was loaded from the original file

You also can access some properties on the image

  - `Image::max_dimension` returns an int giving the max dimension (with or hight)
  - `Image::with` and `Image::height` return an int giving the value of the corresponding dimension
  - `Image::center` returns a `Point` which represents the central point of the image.

Finaly an `Image` overloads classical python methods like

  - `in` operator, you can check if a given `Point` is in an image with `Point in Image`
  - Index access like lists, you can access points with `Image[Point]` or `Image[x, y]` or `Image[(x, y)]`
  - String representation

### Descriptor

### Histogram

## Computing

## GUI

# Resources

  * [How to show an OpenCV image with PyQt](https://stackoverflow.com/questions/52869400/how-to-show-image-to-pyqt-with-opencv)

# To Do

  * Those lists are the atomic steps to accomplish in order to produce a graphical application
  * that allows the user to load two binary images with objects and display the associated F-histogram

  * ~~change line generation order according to angle in bresenham_angle (in image.py)~~
  * use pythagore theorem to get the lenght of the rays

  * ~~merge two images into one for GUI~~
  * ~~merge the images into 2 differents color channels~~

  * Get rid of resizing images each time, and reload image in case of resizing factor changing using openCV enumeration of resizing on load.
  * test if it's working on rectangular images

## Improvement idea

  * ~~keep an image in RGB only for visual, have a grayscale / boolean matrix for interating on it~~
  * ~~resize images to have less empty border in each image~~
  * check if the 2 images are the same size, and if not, resize according to an option (add on top left ? right ?... etc)
  * ~~reshape image in order to iterate on smaller images~~
  * reshape images depending on their initial size
  * ~~create histogram based on 180 degrees~~(actually a really bad idea)

## Basic functions

  * ~~Implement the `bresenham` function~~
  * ~~Implement the `scan_linear` function to execute Bresenham on all parallels~~
  * ~~Implement the `scan_polar` function to execute Bresenham on all angles~~

## Process functions

  * Move image to binary (kind of useless to do so)
  * ~~Mount a data structure that represents the object after a full scan~~
  * ~~Implement a function to compute a histogram value given an angle and a relation~~
  * ~~Mount a data structure that represents the full histogram on 360°~~

## GUI functions

  * Implement the image loading from a button (may be twice for two images)
  * ~~Implement the images display~~
  * ~~Implement the histogram display - classic~~
  * ~~Implement the histogram display - radial~~

  * Create a debug mode, which can show the inner functions, and in exploit mode, only show : merged images, description
  * Add more functions that move the objects, for testing purpose

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
      * ~~Showing histogram~~
      * ~~Histogram contains one relation~~
      * ~~Histogram contains several relation, with colors to differentiate them~~
      * add a color-based legend of the different relations
  
  * ~~using natural langage~~

## Histogram generation

  * ~~Angular histogram~~
  * ~~Overlapping histogram~~
