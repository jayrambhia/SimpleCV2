__version__ = '1.3.0'

from SimpleCV.base import *
from SimpleCV.Camera import *
from SimpleCV.Color import *
from SimpleCV.Display import *
from SimpleCV.Features import *
from SimpleCV.ImageClass import *
from SimpleCV.Stream import *
from SimpleCV.Font import *
from SimpleCV.ColorModel import *
from Display.Base.DrawingLayer import DrawingLayer
from SimpleCV.Segmentation import *
from SimpleCV.MachineLearning import *
from SimpleCV.LineScan import *
from SimpleCV.DFT import DFT
from Display.Gtk.Display import GtkDisplay
from Display.Base.Display import *

Display = GtkDisplay

if (__name__ == '__main__'):
    from SimpleCV.Shell import *
    main(sys.argv)
