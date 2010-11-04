import sys, pygame
from pygame.locals import *
from pygame import Rect
from xml import sax

#read the XML file
class Tileset:
    def __init__(self, file, tile_width, tile_height):
        image = pygame.image.load(file).convert_alpha()
        if not image:
            print "Error creating new Tileset: file %s not found" % file
        print "Tileset: " + str(tile_width) + " x " + str(tile_height)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles = []
        for line in xrange(image.get_height()/self.tile_height):
            for column in xrange(image.get_width()/self.tile_width):
                print "line : " + str(line) + "column " + str(column)
                pos = Rect(
                        column*self.tile_width,
                        line*self.tile_height,
                        self.tile_width,
                        self.tile_height )
                self.tiles.append(image.subsurface(pos))
        print 
    def get_tile(self, gid):
        return self.tiles[gid]

class TMXHandler(sax.ContentHandler):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.tile_width = 0
        self.tile_height = 0
        self.columns = 0
        self.lines  = 0
        self.properties = {}
        self.image = None
        self.tileset = None

    def startElement(self, name, attrs):
        # get most general map informations and create a surface
        if name == 'map':
            self.columns = int(attrs.get('width', None))
            self.lines  = int(attrs.get('height', None))
            self.tile_width = int(attrs.get('tilewidth', None))
            self.tile_height = int(attrs.get('tileheight', None))
            self.width = self.columns * self.tile_width
            self.height = self.lines * self.tile_height
            self.image = pygame.Surface([self.width, self.height]).convert()
        # create a tileset
        elif name=="image":
            source = attrs.get('source', None)
            self.tileset = Tileset(source, self.tile_width, self.tile_height)
        # store additional properties.
        elif name == 'property':
            self.properties[attrs.get('name', None)] = attrs.get('value', None)
        # starting counting
        elif name == 'layer':
            self.line = 0
            self.column = 0
        # get information of each tile and put on the surface using the tileset
        elif name == 'tile':
            gid = int(attrs.get('gid', None)) - 1
            if gid <0: gid = 0
            tile = self.tileset.get_tile(gid)
            pos = (self.column*self.tile_width, self.line*self.tile_height)
            self.image.blit(tile, pos)

            self.column += 1
            if(self.column>=self.columns):
                self.column = 0
                self.line += 1

    # just for debugging
    def endDocument(self):
        print self.width, self.height, self.tile_width, self.tile_height
        print self.properties
        print self.image
