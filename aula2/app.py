# class Circulo():
#   PI = 3.14159
#   def __init__(self, r):
#     self.raio = r
#     self.__volume = 12
  
#   @property
#   def volume(self):
#     return self.__volume
  
#   @volume.setter
#   def volume(self, novoVolume):
#     self.__volume = novoVolume if novoVolume > 100 else novoVolume

#   @classmethod
#   def calcular_volume(cls, a, b):
#     pass

#   ## este metodo calcula seila
#   @staticmethod
#   def calc():
#     pass

# c1 = Circulo(3)
# c2 = Circulo(3)
# c1.PI = 0
# c1.volume = 20

# print(c1.volume)

# def funcao_nomal(a, b):
#   print("asasas")


class Iracional():
  def comer(self):
    print("comer Iracional")


class Animal():
  DADO = 123
  def __init__(self, t):
    self.tamanho = t
    self.membros = 6
  
  def comer(self):
    print("comer animal")

  @classmethod
  def olha(cls):
    print(cls.DADO)

class Cachoro(Iracional, Animal):
  pass

class Gato(Iracional, Animal):
  pass

p1 = Cachoro(0.40)
# p1.comer()
c1 = Gato(0.20)
# c1.comer()

def faz_comer(obj):
  obj.comer()

faz_comer(p1)
faz_comer(c1)

p1.olha()
c1.olha()

class Poligono():
  def calcular_area(self, a):
    print("meu primeiro metodo")

  @classmethod
  def calcular_area(cls, *e):
    print("meu segundo metodo")

poli = Poligono()

poli.calcular_area(5,0,8,65,6,9,0)
