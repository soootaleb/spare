# School Spacial Relations [![Build Status](https://travis-ci.com/soootaleb/spare.svg?branch=master)](https://travis-ci.com/soootaleb/spare)

This project aims to work on the fuzzy spacial relations

![GUI](https://i.ibb.co/1fsdnHL/Capture-d-e-cran-2019-05-12-a-00-59-55.png "SpaRe")

# Quickstart

Use python pipenv tool (install it with `pip install pipenv`) to install the dependencies.

```
$ pipenv shell
$ pipenv install
$ python src/main.py
```

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

### Histogram

The `Histogram` is a data structure representing a classical histogram in the case of our application. Thus, we added several elements like the two images associated with the histogram, the cardinal which represents the number of angles, and the associated descriptor.

  - `Histogram::set_cardinal` defines the number of angles in the histogram
  - `Histogram::set_descriptor` set the associated descriptor
  - `Histogram::normalize` will set all the values between 0 and 1
  - `Histogram::substract_minimum` will substract the minimum value of the histogram to all the values
  - `Histogram::save` will save the histogram using the serializer given in parameters

Here are th available properties

  - `Histogram::directions` will return a linear list of directions depending on the hisotgram cardinal

Some python methods are overloaded to allow

  - `Histogram[direction]` returns the value of the given direction
  - `Histogram[direction] = 26` sets the value of the given direction

### Descriptor

The `Descriptor` model is to be extended. The inheriting descriptors must implement three methods in order to be used. A descriptor is linked as 1-1 with a `Histogram`. The histogram is the data structure that allows the descriptor to evaluate the spacial relation.

`Descriptor::__init__` a descriptor can be constructed with two images call `reference` and `relative`. Each is a binary image that has only the reference object or the relative one.

Here are the base class methods.

  - `Descriptor::set_cardinal` will define the number of angle computed
  - `Descriptor::set_variance` will define the variance of the gaussian mask applied on the associated histogram.

Here are the methods to override when creating a descriptor.

  - `Descriptor::compute_direction(parallels: Segment[])` This method is responsible for computing a float value of description depending on a particular direction, which is represented by the scanning parallels. The method must accept those scanning parallels and return a float which describes "how much" the relative image is positioned in this direction. In other words, this method is responsible of formalizing the mathematical computation for a given direction. In again other words, this method computes a `Histogram` value for a given direction (angle).
  - `Descriptor::interpret` This method should generate the textual description of the descriptor. Using the `relations` property, and leverage some quantitative qualifer, the output should be a correctly syntaxed phrase describing the scene.

## Computing

## GUI

This project is not going to be deployed in production for any industry. Instead, our client described a certain interest in the possibility to have a tool to demonstrate the underlying mechanics. That’s why we opted for developing a graphical user interface that allows our client to easily show some results to any industrial that may be interested in the technology. The GUI (graphical user interface) has been developed using the Python programming language, and relies on PyQt as binding library to use the Qt graphical framework.

### Features (Variables & results)

In order to bring the most value to our application, we developed several types of features. The first one are the input features. They allow the user to interact with the algorithms in order to tune some parameters. The second one are the output features. It is the possibility to have a visual return of what’s happening and the associated results. More generally, one can change some values used by the underlying computations, and see the results in near real time. Finally, we implemented the possibility to export the data in a given configuration.
The input features are sliders that allow the user to tune some parameters. The variance slider allows to customize the shape of the mask we apply on the histograms in order to produce textual interpretation. One angular slider allows to set a direction in which a colored ray is displayed on the merged image. This old feature was one of the first implemented in order to make sure our Bresenham algorithm was behaving correctly. Checking the correct radio button will display all the parallels of a given ray in a direction. The other direction slider on the same level as the images is to move the relative object (the middle image) in order to observe in near real time the evolution of outputs depending on the relative position of the two objects. One slider allows to choose the number of angles (cardinal) in which the computations are done. Finally, the resize slider makes the images resized in order to fasten computations and observe the results of scaling.
The output set of features is comprised of 3 images, 3 histograms, and a sentence describing the scene. The images are binary images, which correspond to the image of the reference object, the one of the relative object, and and the third is the merge of the first two. That allows the user to see clearly the two evaluated images, and have a  result of the combined scene. The histograms show, for a given angle, the computed value by the associated descriptor. The textual description is using the associated relations and intensity qualifiers (a bit, totally, …) in order to produce a human readable sentence describing the scene. The color of the sentence is an indicator of how much the phrase is reliable or not.
Finally, the « save histogram » button exports the currently displayed histograms into a JSON or CSV file in order to reuse it later.

### Data manipulation (Structure & logic)

We wanted our application to serve as a proper base for further explorations and experimentations. For that, we developed it in a way that makes the application accessible to any researcher or open source participant. More that documenting and testing it, we designed our underlying code base to allow easy learning and update. By code base, we mainly talk about two axes that are structuring the whole application. On one hand, we designed a simple but powerful data structure and logic, that separate concerns and lets the developer add abstractions over the time. On the other hand, the software architecture has been thought to decouple the application logic (graphical components and user events) from the data and image manipulations.
The data structures are fundamentally structuring any software. Having it well designed for the business it addresses was for us an obligation in order to make the application flexible in the future. That’s why we decided to implement a list of models that represent — using OOP classes — the different objects our domain is using. As an atom, we have a Pixel. A list of Pixel is a Segment. An Image class is wrapping the classical matrix representing the pixels, the class Histogram offers an API to encapsulate histograms logic, and a Descriptor class can be extended in order to create new descriptors. Based on those simple classes, we can now develop our reasonings and logic around business oriented concerns (i.e relative to our approach of the research domain). Here are some examples of how our simple models extend the basic OpenCV structures and allows our problem to be solved more easily. The Segment class offers a Segment::angle method, that returns in degrees or radians the direction of the segment. This is fundamental since the whole approach relies on angles. Another example is the Image class. It exposes very specific methods like Image::ray or Image::parallels, that return a Segment corresponding in pixels in a given direction (and respectively a list of Segment that are parallel). One more good example is the Descriptor class. This class is meant to be inherited by specific descriptors, depending on their respective way to compute a value for a given angle. However, the base class handles several common behaviors like parameters tuning (e.g the variance of the mask), or the application of the mask on the computed values.
Now that we have a flexible data structure that clearly represents our problems, we developed the logic of computing our descriptions using the previously constructed API. Put simply, when the user performs an action like changing a slider’s value, we call adapted methods on created objects in order to perform the computation needed, and get the visual result by injecting the computed values in a graphical object. As an example, the Image class allows method chaining in order to perform multiple sequential transformations and computations. That’s how we can get a complete description of the scene by modifying our image by calling Image.reset().resize().rotate()... and on the other side call MyDescriptor.compute_histogram().describe()...
As a result, the application clearly draws a boundary between responsibilities of each model. Object models like Point or Segment are basic structures that can be leveraged when dealing with business computations, while more abstracted classes like Histogram or Descriptor can be extended and used as an API in order to get the interesting results. Each class can be updated in order to implement new methods, each algorithm can be optimized, innovative approaches can be implemented using several lines of code and the result is accessible visually in minutes.

### Performances & future ideas

Since this application has only test and discovery purpose, the computing performances have not been a priority. However, some steps have proven to be very long to achieve, especially when dealing with matrices and their potentially huge number of values (n^2). In this section, we detail what steps of our computing operations are long to process, how we optimized a part of them, and further options to make this application more robust and reliable.
Since Python is an interpreted language, its general performance will never be as good as a compiled C program. However, it turns out that many of the executed code in our application does compute in the order of milliseconds. In reality, the real bottleneck preventing our interface to be real time is the fact that some small actions are repeated for each point of our image matrix. More precisely, the Descriptor::parallels took more than 30 milliseconds to compute the parallels on a given angle. After optimizing the branching factor and the calls needed at each iteration, we came up with the method getting all the parallels in 2 milliseconds.
Furthermore, a good improvement that could be done is the integration of segments instead of point, meaning that in a segment of the image, at the scanning, we could instantly check if the reference object is present, or it’s relative. Doing so would have several advantages, the first would be to enable checking only in one direction, as the reverse operation would be that set of segments in the reverse order, whereas we actually have to check the image again in the opposite direction to get results in some descriptors (Angular Presence and Angular distance) as the count of the relative points starts when we have already seen reference. 
And it would enable to apply the algorithms of the descriptors to each sub-segment, enabling the descriptors to work on concaves objects whereas we only ensure it works on convex objects for now.
Finally, many mechanics are implemented using imperative Python programming. But several computations could be delegated to NumPy. For this, the iterative approach (for example to compare two Segment) must be replaced with a matrix approach (or list), in order to apply bitwise operations and NumPy matrix comparisons, which are implemented in compiled code and thus very faster.


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
