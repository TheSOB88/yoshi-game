import pygame, os, random, pygame.draw as draw
from pygame.locals import *

import piece
Piece = piece.Piece



class Board:
    matrix = []#[[0]*12]*8
    colorMatrix = []#[[None]*12]*8
    width, height = 8, 12
    
    def __init__( self ):
        matrix = [None] * self.height
        colorMatrix = [None] * self.height
        for j in range(0, self.height):
            matrix[j] = [0] * self.width
            colorMatrix[j] = [None] * self.width
        self.matrix = matrix
        self.colorMatrix = colorMatrix
        
    def addPiece( self, piece ):
        iCap = piece.getWidth() ##2 if piece.x < 7 else 1
        jCap = piece.getHeight() ##2 if piece.y < 11 else 1
        for i in range(0, iCap):
            x = piece.x + i
            for j in range(0, jCap):
                y = piece.y + j
                pieceTri = piece.matrix[j][i]
                if pieceTri:
                    selfTri = self.matrix[y][x]
                    newTri = Piece.addTri( pieceTri, selfTri )
                    self.matrix[y][x] = newTri
                    if pieceTri == newTri:
                        self.colorMatrix[y][x] = piece.color
                    else:
                        if pieceTri == 2 or pieceTri == 3:
                            self.colorMatrix[y][x] = ( self.colorMatrix[y][x], piece.color )
                        else:
                            self.colorMatrix[y][x] = ( piece.color, self.colorMatrix[y][x] )
    
    '''Check boundaries, reset piece's pos, add piece if necessary.
       Returns what has been done to the piece'''
    def checkBoundaries( self, piece ):
        if piece.x < 0:
            piece.x = 0
            print( 'fix x' )
        elif piece.x + piece.getWidth() > self.width:
            piece.x = piece.oldX
            print( 'fix x' )
        if piece.y + piece.getHeight() > self.height:
            piece.x = piece.oldX
            piece.y = piece.oldY
            print( "add piece" )
            return True
            
        iCap = piece.getWidth() 
        jCap = piece.getHeight()
        for i in range(0, iCap):
            x = piece.x + i
            for j in range(0, jCap):
                y = piece.y + j
                pieceTri = piece.matrix[j][i]
                selfTri = self.matrix[y][x]
                if pieceTri and selfTri and Piece.addTri( pieceTri, selfTri ) == -1:
                    piece.x = piece.oldX
                    piece.y = piece.oldY
                    return True
                    
        return False
                
    def removeLine( self, line ):
        for y in reversed( range( 1, line + 1 ) ):
            for x in range( 0, 8 ):
                self.matrix[y][x] = self.matrix[y-1][x] 
                self.colorMatrix[y][x] = self.colorMatrix[y-1][x] 
        self.matrix[0] = [0]*width
        self.colorMatrix[0] = [None]*width
        
    #check if there are lines to remove
    def update( self ):
        for y in range(0,12):
            x = -1
            broke = False
            while not broke:
                x += 1
                if x == 8 or (self.matrix[y][x] != 5 and self.matrix[y][x] != 6):
                    broke = True
            if not broke:
                self.removeLine( y )
                
    def draw( self, surface ):
        for y in range( 0, self.height ):
            for x in range( 0, self.width ):
                Piece.drawTriangle( surface, self.colorMatrix[y][x], self.matrix[y][x], x, y )
                