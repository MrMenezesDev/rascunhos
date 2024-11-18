import pyscript 
import inspect
_P5_INSTANCE = pyscript.window

CLOSE = _P5_INSTANCE.CLOSE

importing_module = inspect.currentframe().f_back.f_globals['__name__']

def iniciar_animacao(setup, draw):
    setup()
    def animacao(*args):
        draw()
        _P5_INSTANCE.requestAnimationFrame(animacao)
    _P5_INSTANCE.requestAnimationFrame(animacao)

def vertex(*args):
    return _P5_INSTANCE.vertex(*args)

def no_stroke(*args):
    return _P5_INSTANCE.noStroke(*args)

def stroke_weight(*args):
    return _P5_INSTANCE.strokeWeight(*args)

def end_shape(*args):
    return _P5_INSTANCE.endShape(*args)

def begin_shape(*args):
    return _P5_INSTANCE.endShape(*args)

def requestAnimationFrame(*args):
    return _P5_INSTANCE.requestAnimationFrame(*args)

def alpha(*args):
    return _P5_INSTANCE.alpha(*args)

def blue(*args):
    return _P5_INSTANCE.blue(*args)

def brightness(*args):
    return _P5_INSTANCE.brightness(*args)

def color(*args):
    return _P5_INSTANCE.color(*args)

def green(*args):
    return _P5_INSTANCE.green(*args)

def hue(*args):
    return _P5_INSTANCE.hue(*args)

def lerpColor(*args):
    return _P5_INSTANCE.lerpColor(*args)

def lightness(*args):
    return _P5_INSTANCE.lightness(*args)

def red(*args):
    return _P5_INSTANCE.red(*args)

def saturation(*args):
    return _P5_INSTANCE.saturation(*args)

def background(*args):
    return _P5_INSTANCE.background(*args)

def clear(*args):
    __pragma__('noalias', 'clear')
    p5_clear = _P5_INSTANCE.clear(*args)
    __pragma__('alias', 'clear', 'py_clear')
    return p5_clear

def erase(*args):
    return _P5_INSTANCE.erase(*args)

def noErase(*args):
    return _P5_INSTANCE.noErase(*args)

def colorMode(*args):
    return _P5_INSTANCE.colorMode(*args)

def fill(*args):
    return _P5_INSTANCE.fill(*args)

def noFill(*args):
    return _P5_INSTANCE.noFill(*args)

def noStroke(*args):
    return _P5_INSTANCE.noStroke(*args)

def stroke(*args):
    return _P5_INSTANCE.stroke(*args)

def arc(*args):
    return _P5_INSTANCE.arc(*args)

def ellipse(*args):
    return _P5_INSTANCE.ellipse(*args)

def circle(*args):
    return _P5_INSTANCE.circle(*args)

def line(*args):
    return _P5_INSTANCE.line(*args)

def point(*args):
    return _P5_INSTANCE.point(*args)

def quad(*args):
    return _P5_INSTANCE.quad(*args)

def rect(*args):
    return _P5_INSTANCE.rect(*args)

def square(*args):
    return _P5_INSTANCE.square(*args)

def triangle(*args):
    return _P5_INSTANCE.triangle(*args)

def plane(*args):
    return _P5_INSTANCE.plane(*args)

def box(*args):
    return _P5_INSTANCE.box(*args)

def sphere(*args):
    return _P5_INSTANCE.sphere(*args)

def cylinder(*args):
    return _P5_INSTANCE.cylinder(*args)

def cone(*args):
    return _P5_INSTANCE.cone(*args)

def ellipsoid(*args):
    return _P5_INSTANCE.ellipsoid(*args)

def torus(*args):
    return _P5_INSTANCE.torus(*args)

def loadModel(*args):
    return _P5_INSTANCE.loadModel(*args)

def model(*args):
    return _P5_INSTANCE.model(*args)

def ellipseMode(*args):
    return _P5_INSTANCE.ellipseMode(*args)

def noSmooth(*args):
    return _P5_INSTANCE.noSmooth(*args)

def rectMode(*args):
    return _P5_INSTANCE.rectMode(*args)

def smooth(*args):
    return _P5_INSTANCE.smooth(*args)

def strokeCap(*args):
    return _P5_INSTANCE.strokeCap(*args)

def strokeJoin(*args):
    return _P5_INSTANCE.strokeJoin(*args)

def strokeWeight(*args):
    return _P5_INSTANCE.strokeWeight(*args)

def bezier(*args):
    return _P5_INSTANCE.bezier(*args)

def bezierDetail(*args):
    return _P5_INSTANCE.bezierDetail(*args)

def bezierPoint(*args):
    return _P5_INSTANCE.bezierPoint(*args)

def bezierTangent(*args):
    return _P5_INSTANCE.bezierTangent(*args)

def curve(*args):
    return _P5_INSTANCE.curve(*args)

def curveDetail(*args):
    return _P5_INSTANCE.curveDetail(*args)

def curveTightness(*args):
    return _P5_INSTANCE.curveTightness(*args)

def curvePoint(*args):
    return _P5_INSTANCE.curvePoint(*args)

def curveTangent(*args):
    return _P5_INSTANCE.curveTangent(*args)

def beginContour(*args):
    return _P5_INSTANCE.beginContour(*args)

def beginShape(*args):
    return _P5_INSTANCE.beginShape(*args)

def bezierVertex(*args):
    return _P5_INSTANCE.bezierVertex(*args)

def curveVertex(*args):
    return _P5_INSTANCE.curveVertex(*args)

def endContour(*args):
    return _P5_INSTANCE.endContour(*args)

def endShape(*args):
    return _P5_INSTANCE.endShape(*args)

def quadraticVertex(*args):
    return _P5_INSTANCE.quadraticVertex(*args)

def vertex(*args):
    return _P5_INSTANCE.vertex(*args)

def cursor(*args):
    return _P5_INSTANCE.cursor(*args)

def frameRate(*args):
    return _P5_INSTANCE.frameRate(*args)

def noCursor(*args):
    return _P5_INSTANCE.noCursor(*args)

def fullscreen(*args):
    return _P5_INSTANCE.fullscreen(*args)

def pixelDensity(*args):
    return _P5_INSTANCE.pixelDensity(*args)

def displayDensity(*args):
    return _P5_INSTANCE.displayDensity(*args)

def getURL(*args):
    return _P5_INSTANCE.getURL(*args)

def getURLPath(*args):
    return _P5_INSTANCE.getURLPath(*args)

def getURLParams(*args):
    return _P5_INSTANCE.getURLParams(*args)

def preload(*args):
    return _P5_INSTANCE.preload(*args)

def setup(*args):
    return _P5_INSTANCE.setup(*args)

def draw(*args):
    return _P5_INSTANCE.draw(*args)

def remove(*args):
    return _P5_INSTANCE.remove(*args)

def noLoop(*args):
    return _P5_INSTANCE.noLoop(*args)

def loop(*args):
    return _P5_INSTANCE.loop(*args)

def push(*args):
    return _P5_INSTANCE.push(*args)

def redraw(*args):
    return _P5_INSTANCE.redraw(*args)

def resizeCanvas(*args):
    return _P5_INSTANCE.resizeCanvas(*args)

def noCanvas(*args):
    return _P5_INSTANCE.noCanvas(*args)

def createGraphics(*args):
    return _P5_INSTANCE.createGraphics(*args)

def blendMode(*args):
    return _P5_INSTANCE.blendMode(*args)

def setAttributes(*args):
    return _P5_INSTANCE.setAttributes(*args)

def applyMatrix(*args):
    return _P5_INSTANCE.applyMatrix(*args)

def resetMatrix(*args):
    return _P5_INSTANCE.resetMatrix(*args)

def rotate(*args):
    return _P5_INSTANCE.rotate(*args)

def rotateX(*args):
    return _P5_INSTANCE.rotateX(*args)

def rotateY(*args):
    return _P5_INSTANCE.rotateY(*args)

def rotateZ(*args):
    return _P5_INSTANCE.rotateZ(*args)

def scale(*args):
    return _P5_INSTANCE.scale(*args)

def shearX(*args):
    return _P5_INSTANCE.shearX(*args)

def shearY(*args):
    return _P5_INSTANCE.shearY(*args)

def translate(*args):
    return _P5_INSTANCE.translate(*args)

def createStringDict(*args):
    return _P5_INSTANCE.createStringDict(*args)

def createNumberDict(*args):
    return _P5_INSTANCE.createNumberDict(*args)

def append(*args):
    return _P5_INSTANCE.append(*args)

def arrayCopy(*args):
    return _P5_INSTANCE.arrayCopy(*args)

def concat(*args):
    return _P5_INSTANCE.concat(*args)

def reverse(*args):
    return _P5_INSTANCE.reverse(*args)

def shorten(*args):
    return _P5_INSTANCE.shorten(*args)

def shuffle(*args):
    return _P5_INSTANCE.shuffle(*args)

def sort(*args):
    return _P5_INSTANCE.sort(*args)

def splice(*args):
    return _P5_INSTANCE.splice(*args)

def subset(*args):
    return _P5_INSTANCE.subset(*args)

def float(*args):
    return _P5_INSTANCE.float(*args)

def int(*args):
    return _P5_INSTANCE.int(*args)

def str(*args):
    return _P5_INSTANCE.str(*args)

def boolean(*args):
    return _P5_INSTANCE.boolean(*args)

def byte(*args):
    return _P5_INSTANCE.byte(*args)

def char(*args):
    return _P5_INSTANCE.char(*args)

def unchar(*args):
    return _P5_INSTANCE.unchar(*args)

def hex(*args):
    return _P5_INSTANCE.hex(*args)

def unhex(*args):
    return _P5_INSTANCE.unhex(*args)

def join(*args):
    return _P5_INSTANCE.join(*args)

def match(*args):
    return _P5_INSTANCE.match(*args)

def matchAll(*args):
    return _P5_INSTANCE.matchAll(*args)

def nf(*args):
    return _P5_INSTANCE.nf(*args)

def nfc(*args):
    return _P5_INSTANCE.nfc(*args)

def nfp(*args):
    return _P5_INSTANCE.nfp(*args)

def nfs(*args):
    return _P5_INSTANCE.nfs(*args)

def split(*args):
    return _P5_INSTANCE.split(*args)

def splitTokens(*args):
    return _P5_INSTANCE.splitTokens(*args)

def trim(*args):
    return _P5_INSTANCE.trim(*args)

def setMoveThreshold(*args):
    return _P5_INSTANCE.setMoveThreshold(*args)

def setShakeThreshold(*args):
    return _P5_INSTANCE.setShakeThreshold(*args)

def keyIsDown(*args):
    return _P5_INSTANCE.keyIsDown(*args)

def createImage(*args):
    return _P5_INSTANCE.createImage(*args)

def saveCanvas(*args):
    return _P5_INSTANCE.saveCanvas(*args)

def saveFrames(*args):
    return _P5_INSTANCE.saveFrames(*args)


def image_proxy(img):
    """
    Proxy to turn of transcypt when calling img.get/set methods
    """

    def _set(*args):
        __pragma__('noalias', 'set')
        value = img.set(*args)
        __pragma__('alias', 'set', 'py_set')
        return value

    def _get(*args):
        __pragma__('noalias', 'get')
        value = img.get(*args)
        __pragma__('alias', 'get', 'py_get')
        return value

    img.set = _set
    img.get = _get
    return img


def loadImage(*args):
    imageObj = _P5_INSTANCE.loadImage(*args)
    return image_proxy(imageObj)

def image(*args):
    return _P5_INSTANCE.image(*args)

def tint(*args):
    return _P5_INSTANCE.tint(*args)

def noTint(*args):
    return _P5_INSTANCE.noTint(*args)

def imageMode(*args):
    return _P5_INSTANCE.imageMode(*args)

def blend(*args):
    return _P5_INSTANCE.blend(*args)

def copy(*args):
    return _P5_INSTANCE.copy(*args)

def filter(*args):
    if len(args) > 1 and (args[0] is None or callable(args[0])):
        return PythonFunctions.filter(*args)
    else:
        return _P5_INSTANCE.filter(*args)

def get(*args):
    __pragma__('noalias', 'get')
    p5_get = _P5_INSTANCE.get(*args)
    __pragma__('alias', 'get', 'py_get')
    return p5_get

def loadPixels(*args):
    return _P5_INSTANCE.loadPixels(*args)

def set(*args):
    if len(args) <= 1:
        return PythonFunctions.set(*args)
    else:
        return _P5_INSTANCE.set(*args)

def updatePixels(*args):
    return _P5_INSTANCE.updatePixels(*args)

def loadJSON(*args):
    return _P5_INSTANCE.loadJSON(*args)

def loadStrings(*args):
    return _P5_INSTANCE.loadStrings(*args)

def loadTable(*args):
    return _P5_INSTANCE.loadTable(*args)

def loadXML(*args):
    return _P5_INSTANCE.loadXML(*args)

def loadBytes(*args):
    return _P5_INSTANCE.loadBytes(*args)

def httpGet(*args):
    return _P5_INSTANCE.httpGet(*args)

def httpPost(*args):
    return _P5_INSTANCE.httpPost(*args)

def httpDo(*args):
    return _P5_INSTANCE.httpDo(*args)

def createWriter(*args):
    return _P5_INSTANCE.createWriter(*args)

def save(*args):
    return _P5_INSTANCE.save(*args)

def saveJSON(*args):
    return _P5_INSTANCE.saveJSON(*args)

def saveStrings(*args):
    return _P5_INSTANCE.saveStrings(*args)

def saveTable(*args):
    return _P5_INSTANCE.saveTable(*args)

def day(*args):
    return _P5_INSTANCE.day(*args)

def hour(*args):
    return _P5_INSTANCE.hour(*args)

def minute(*args):
    return _P5_INSTANCE.minute(*args)

def millis(*args):
    return _P5_INSTANCE.millis(*args)

def month(*args):
    return _P5_INSTANCE.month(*args)

def second(*args):
    return _P5_INSTANCE.second(*args)

def year(*args):
    return _P5_INSTANCE.year(*args)

def createVector(*args):
    return _P5_INSTANCE.createVector(*args)

def abs(*args):
    return _P5_INSTANCE.abs(*args)

def ceil(*args):
    return _P5_INSTANCE.ceil(*args)

def constrain(*args):
    return _P5_INSTANCE.constrain(*args)

def dist(*args):
    return _P5_INSTANCE.dist(*args)

def exp(*args):
    return _P5_INSTANCE.exp(*args)

def floor(*args):
    return _P5_INSTANCE.floor(*args)

def lerp(*args):
    return _P5_INSTANCE.lerp(*args)

def log(*args):
    return _P5_INSTANCE.log(*args)

def mag(*args):
    return _P5_INSTANCE.mag(*args)

def map(*args):
    if len(args) > 1 and callable(args[0]):
        return PythonFunctions.map(*args)
    else:
        return _P5_INSTANCE.map(*args)


def max(*args):
    return _P5_INSTANCE.max(*args)

def min(*args):
    return _P5_INSTANCE.min(*args)

def norm(*args):
    return _P5_INSTANCE.norm(*args)

def pow(*args):
    return _P5_INSTANCE.pow(*args)

def round(*args):
    return _P5_INSTANCE.round(*args)

def sq(*args):
    return _P5_INSTANCE.sq(*args)

def sqrt(*args):
    return _P5_INSTANCE.sqrt(*args)

def noise(*args):
    return _P5_INSTANCE.noise(*args)

def noiseDetail(*args):
    return _P5_INSTANCE.noiseDetail(*args)

def noiseSeed(*args):
    return _P5_INSTANCE.noiseSeed(*args)

def randomSeed(*args):
    return _P5_INSTANCE.randomSeed(*args)

def random(*args):
    return _P5_INSTANCE.random(*args)

def randomGaussian(*args):
    return _P5_INSTANCE.randomGaussian(*args)

def acos(*args):
    return _P5_INSTANCE.acos(*args)

def asin(*args):
    return _P5_INSTANCE.asin(*args)

def atan(*args):
    return _P5_INSTANCE.atan(*args)

def atan2(*args):
    return _P5_INSTANCE.atan2(*args)

def cos(*args):
    return _P5_INSTANCE.cos(*args)

def sin(*args):
    return _P5_INSTANCE.sin(*args)

def tan(*args):
    return _P5_INSTANCE.tan(*args)

def degrees(*args):
    return _P5_INSTANCE.degrees(*args)

def radians(*args):
    return _P5_INSTANCE.radians(*args)

def angleMode(*args):
    return _P5_INSTANCE.angleMode(*args)

def textAlign(*args):
    return _P5_INSTANCE.textAlign(*args)

def textLeading(*args):
    return _P5_INSTANCE.textLeading(*args)

def textSize(*args):
    return _P5_INSTANCE.textSize(*args)

def textStyle(*args):
    return _P5_INSTANCE.textStyle(*args)

def textWidth(*args):
    return _P5_INSTANCE.textWidth(*args)

def textAscent(*args):
    return _P5_INSTANCE.textAscent(*args)

def textDescent(*args):
    return _P5_INSTANCE.textDescent(*args)

def loadFont(*args):
    return _P5_INSTANCE.loadFont(*args)

def text(*args):
    return _P5_INSTANCE.text(*args)

def textFont(*args):
    return _P5_INSTANCE.textFont(*args)

def orbitControl(*args):
    return _P5_INSTANCE.orbitControl(*args)

def debugMode(*args):
    return _P5_INSTANCE.debugMode(*args)

def noDebugMode(*args):
    return _P5_INSTANCE.noDebugMode(*args)

def ambientLight(*args):
    return _P5_INSTANCE.ambientLight(*args)

def directionalLight(*args):
    return _P5_INSTANCE.directionalLight(*args)

def pointLight(*args):
    return _P5_INSTANCE.pointLight(*args)

def lights(*args):
    return _P5_INSTANCE.lights(*args)

def loadShader(*args):
    return _P5_INSTANCE.loadShader(*args)

def createShader(*args):
    return _P5_INSTANCE.createShader(*args)

def shader(*args):
    return _P5_INSTANCE.shader(*args)

def resetShader(*args):
    return _P5_INSTANCE.resetShader(*args)

def normalMaterial(*args):
    return _P5_INSTANCE.normalMaterial(*args)

def texture(*args):
    return _P5_INSTANCE.texture(*args)

def textureMode(*args):
    return _P5_INSTANCE.textureMode(*args)

def textureWrap(*args):
    return _P5_INSTANCE.textureWrap(*args)

def ambientMaterial(*args):
    return _P5_INSTANCE.ambientMaterial(*args)

def specularMaterial(*args):
    return _P5_INSTANCE.specularMaterial(*args)

def shininess(*args):
    return _P5_INSTANCE.shininess(*args)

def camera(*args):
    return _P5_INSTANCE.camera(*args)

def perspective(*args):
    return _P5_INSTANCE.perspective(*args)

def ortho(*args):
    return _P5_INSTANCE.ortho(*args)

def createCamera(*args):
    return _P5_INSTANCE.createCamera(*args)

def setCamera(*args):
    return _P5_INSTANCE.setCamera(*args)

def select(*args):
    return _P5_INSTANCE.select(*args)

def selectAll(*args):
    return _P5_INSTANCE.selectAll(*args)

def removeElements(*args):
    return _P5_INSTANCE.removeElements(*args)

def changed(*args):
    return _P5_INSTANCE.changed(*args)

def input(*args):
    return _P5_INSTANCE.input(*args)

def createDiv(*args):
    return _P5_INSTANCE.createDiv(*args)

def createP(*args):
    return _P5_INSTANCE.createP(*args)

def createSpan(*args):
    return _P5_INSTANCE.createSpan(*args)

def createImg(*args):
    return _P5_INSTANCE.createImg(*args)

def createA(*args):
    return _P5_INSTANCE.createA(*args)

def createSlider(*args):
    return _P5_INSTANCE.createSlider(*args)

def createButton(*args):
    return _P5_INSTANCE.createButton(*args)

def createCheckbox(*args):
    return _P5_INSTANCE.createCheckbox(*args)

def createSelect(*args):
    return _P5_INSTANCE.createSelect(*args)

def createRadio(*args):
    return _P5_INSTANCE.createRadio(*args)

def createColorPicker(*args):
    return _P5_INSTANCE.createColorPicker(*args)

def createInput(*args):
    return _P5_INSTANCE.createInput(*args)

def createFileInput(*args):
    return _P5_INSTANCE.createFileInput(*args)

def createVideo(*args):
    return _P5_INSTANCE.createVideo(*args)

def createAudio(*args):
    return _P5_INSTANCE.createAudio(*args)

def createCapture(*args):
    return _P5_INSTANCE.createCapture(*args)

def createElement(*args):
    return _P5_INSTANCE.createElement(*args)

def createCanvas(*args):
    canvas = _P5_INSTANCE.createCanvas(*args)

    global width, height
    width = _P5_INSTANCE.width
    height = _P5_INSTANCE.height

    return canvas


def pop(*args):
    __pragma__('noalias', 'pop')
    p5_pop = _P5_INSTANCE.pop(*args)
    __pragma__('alias', 'pop', 'py_pop')
    return p5_pop


# Processing Python or Java mode compatibility aliases
size = createCanvas
popMatrix = pop
popStyle = pop
pushMatrix = push
pushStyle = push