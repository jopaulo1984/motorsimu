"""
misc
====

Autor: João Paulo F da Silva
Versão: v1.0

Módulo que contém classes e funções muito usadas.

"""

import math

class Vector2d:
    
    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @x.setter
    def x(self, value):
        self.__x = value
    
    @y.setter
    def y(self, value):
        self.__y = value
    
    def set_point(self, x, y):
        self.__x = x
        self.__y = y
    
    def get_point(self):
        return self.__x, self.__y
    
    def get_mod(self):
        return math.sqrt((self.__x ** 2) + (self.__y ** 2))
    
    def get_polar(self):
        return self.get_mod(), self.get_teta()
    
    def get_complex(self):
        return self.__x, self.__y
    
    def get_teta(self):
        mod = self.get_mod()
        if mod == 0: return 0
        return math.acos(self.__x / mod)
    
    def __add__(self, A):
        if type(A) is not Vector2d:
            raise Exception("Não é possível somar vetor com escalar")
        
        return Vector2d(self.x + A.x, self.y + A.y)
    
    def __mul__(self, value):
        if type(value) is int or type(value) is float:        
            return Vector2d(self.x * value, self.y * value)
        elif type(value) is Vector2d:
            mres = self.get_mod() * value.get_mod()
            teta = self.get_teta() + value.get_teta()
            return Vector2d(mres * math.cos(teta), mres * math.sin(teta))
        else:
            raise Exception("Só é permitido multiplicar vetor com números reais ou com outro vetor 2d.")
    
    def __rmul__(self, value):
        return self * value
    
    def __truediv__(self, value):
        if type(value) is int or type(value) is float:        
            return Vector2d(self.x / value, self.y / value)
        elif type(value) is Vector2d:
            mres = self.get_mod() / value.get_mod()
            teta = self.get_teta() - value.get_teta()
            return Vector2d(mres * math.cos(teta), mres * math.sin(teta))
        else:
            raise Exception("Só é permitido dividir vetor com números reais ou com outro vetor 2d.")
    
    def __str__(self):
        return "{x:%0.2f, y:%0.2f}" % self.get_complex()
#
