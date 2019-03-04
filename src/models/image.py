

'''
    Represents an image in our application. It's created with an OpenCV::imread image
    but it adds project oriented features

    Overloaded operators:
    - point in image

'''
class Image(object):

    base = None # We keep the original one to be able to reset
    '''
    This property is the original image as passed in the constructor

    /!\ This property should not be manipulated, use Image::image instead
    '''

    image = None
    """
    This property is the underlying OpenCV image that we can manipulate
    """

    def __init__(self, cv_image):
        if not bool(cv_image): print('[WARNING] Instanciated an empty image')

        self.base = cv_image
        self.image = self.base.copy()

    def reset(self):
        '''
        Resets the OpenCV image to its original version (as passed in the constructor)
        '''
        self.image = self.base.copy()

    def __contains__(self, point) -> bool:
        '''
        We consider the points to be zero indexed
        '''
        return point.x < self.width() - 1
            and point.y < self.height() - 1

    def size(self):
        return self.image.shape

    def width(self):
        return self.size()[1]

    def height(self):
        return self.size()[0]