from ..Base import Display
from ..Base.Display import DisplayBase
from tornado.web import Application
import tornado
from IPython.core.display import Javascript as JS
from IPython.core.display import display
from time import sleep
import os
import threading
import tempfile
import tornado.testing


class NBDisplay(Display.DisplayBase):

    _templateFile = "template.html"
    """

    
    """
    init = False
    app = None
    staticDir = None
    __uidCounter__ = 0
    port = None
    __cache__ = 20
    
    def name(self): 
        __doc__ = DisplayBase.name.__doc__
        return "NotebookDisplay"
        
    def __init__(self,size = (640,480),type_ = Display.DEFAULT,title = "SimpleCV",fit = Display.SCROLL,delay = .500):
        """
        **SUMMARY**
        
        Opens up a display in a window. 
        
        d = Display()
        
        **PARAMETERS**
        
        * *size* - the size of the diplay in pixels.
        
        * *type_* - unused tight now
            
        * *title* - the title bar on the display, if there exists one.
        
        * *fit* - unused right  now
        
        * *delay* - delay in seconds for which to wait to let the browser load the window
        
        
        **EXAMPLE**
        
        >>> display = Display(type_ = FULLSCREEN,fit = SCROLL)
        >>> img = Image('lenna')
        >>> img.save(dispay)
        
        """
        if( not NBDisplay.init):
            #check if a tornado server exists, if not , create one
            NBDisplay.init = True
            
            #dir in which images are stored
            NBDisplay.staticDir = tempfile.mkdtemp()
            NBDisplay.app = Application(static_path = NBDisplay.staticDir,
            
            #all images are accesses with the /diplay/
            static_url_prefix = "/display/")
            
            NBDisplay.port = tornado.testing.get_unused_port()
            NBDisplay.app.listen(NBDisplay.port)
            
            #start a thread for tornado
            threading.Thread(target=tornado.ioloop.IOLoop.instance().start).start()
            
        #the unique id for each Display
        self.__uid__ = NBDisplay.__uidCounter__
        NBDisplay.__uidCounter__ += 1

        
        # load the template HTML and replace params in it
        fn = os.path.dirname(__file__) + os.sep + NBDisplay._templateFile
        tmp = open(fn)
        raw_lines = tmp.readlines()
        tmp.close()
        lines = [line.replace('\n','') for line in raw_lines]
        template = ''.join(lines)
        template = template.replace('__port__',str(NBDisplay.port))
        template = template.replace('__cache__',str(NBDisplay.__cache__))
        
        options = {}
        options['width'],options['height'] = size
        options['code'] = template 
        options['title'] = title 
        options['id'] = self.getUID()
        
        
        #this pops up a window
        self.startStr = """
        window.disp%(id)s = window.open('','%(title)s','width=%(width)s,height=%(height)s')
        window.disp%(id)s.document.write("%(code)s")
        """ % options
        
        display(JS(self.startStr))
        
        #otherwise the browser complains if showImage is called right after this
        sleep(delay)
        
        
    def close(self):

        Display.DisplayBase.close(self)
        command = 'window.disp%d.close()' % (self.getUID() )
        display(JS(command))
    
    def showImage(self,img):
        """
        
        **SUMMARY**
        
        Show the image. 
        
        **PARAMETERS**
        
        * *img = a SimpleCV Image object to be displayed 
        
        **Example**
        >>> img = Image('lenna')
        >>> d = Display()
        >>> d.showImage(img)
        
        """
        
        # so that only the last few images are saved, newer ones over-write the old ones
        img.save(NBDisplay.staticDir + os.sep + str(img.getUID() % NBDisplay.__cache__) + '.png' )
        #print uid%10
        options = {}
        options['imageID'] = img.getUID()
        options['width'] = img.width
        options['height'] = img.height
        options['displayID'] = self.getUID()
        command = "window.disp%(displayID)s.show(%(imageID)s,%(width)s,%(height)s)" % options
        #print command
        #pass the id to javascript and do the rest there
        display(JS(command))

    def mousePosition(self):
        """
        **SUMMARY**
        
        Reutrns the mouse pointer potion as a tuple of (x,y), with respect to
        the image coordinates

        **RETURNS**
        
        An (x,y) mouse postion tuple .
        
        """
        pass
        
    def mousePositionRaw(self):
        """
        **SUMMARY**
        
        Reutrns the mouse pointer potion as a tuple of (x,y), with respect to
        the display coordinates
        
        **RETURNS**
        
        An (x,y) mouse postion tuple .
        
        """
        pass
    
    def leftDown(self):
        """
        **SUMMARY**
        
        Reutrns the position where the left mouse button last went down,None 
        if it didn't since the last time this fucntion was called
        
        **RETURNS**
        
        An (x,y) mouse postion tuple where the left mouse button went down.
        
        """

    def leftUp(self):
        """
        **SUMMARY**
        
        Reutrns the position where the left mouse button last went up,None 
        if it didn't since the last time this fucntion was called
        
        **RETURNS**
        
        An (x,y) mouse postion tuple where the left mouse button went up.
        
        """

    def rightDown(self):
        """
        **SUMMARY**
        
        Reutrns the position where the right mouse button last went down,None 
        if it didn't since the last time this fucntion was called
        
        **RETURNS**
        
        An (x,y) mouse postion tuple where the right mouse button went down.
        
        """
        
    def rightUp(self):
        """
        **SUMMARY**
        
        Reutrns the position where the right mouse button last went up,None 
        if it didn't since the last time this fucntion was called
        
        **RETURNS**
        
        An (x,y) mouse postion tuple where the right mouse button went up.
        
        """
        
    def middleDown(self):
        """
        **SUMMARY**
        
        Reutrns the position where the middle mouse button last went down,None 
        if it didn't since the last time this fucntion was called
        
        **RETURNS**
        
        An (x,y) mouse postion tuple where the middle mouse button went down.
        
        """
        
    def middleUp(self):
        """
        **SUMMARY**
        
        Reutrns the position where the middle mouse button last went up,None 
        if it didn't since the last time this fucntion was called
        
        **RETURNS**
        
        An (x,y) mouse postion tuple where the middle mouse button went up.
        
        """
        
    def getUID(self):
        return self.__uid__


