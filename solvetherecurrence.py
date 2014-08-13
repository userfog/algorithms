import os
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

expo = {}

def die(string, ln):
  print(("Usage (%s): %s" % (ln, string)))
  sys.exit(1)

def mod1000(i):
  if i < 0:
    return i % -1000
  else:
    return i % 1000

class Matrix:
  def __init__(self, numRows, numColumns, initialValues):
    self.numRows = numRows
    self.numColumns = numColumns
    self.mat = self.CreateMat(initialValues)

  def CreateMat(self, initialValues):
    if initialValues == '':
      M = []
      for i in xrange(0, self.numRows):
        M.append([])
        for j in xrange(0, self.numColumns):
          M[i].append(0)
      return M
    else:
      return  [map(int, [b for b in a.strip().split(" ")]) for a in initialValues.split(';')]

  @staticmethod
  def MatrixMult(mat1, mat2):
    if not mat1.numColumns == mat2.numRows:
      die("Invalid Multiplication Cols not = Rows", 28)
    else:
      Res = Matrix(mat1.numRows, mat2.numColumns, '')
      for k in xrange(0, mat2.numRows):
        for j in xrange(0, mat2.numColumns):
          for i in xrange(0, mat1.numRows):
            Res.mat[i][j] = mod1000(Res.mat[i][j] + mat1.mat[i][k]*mat2.mat[k][j])
      return Res

  @staticmethod
  def MatrixExp(mat1, i):
    if i == 0:
      return expo[1]
    if i == 1:
      return expo[2]
    else:
      helper = expo[2]
      for x in xrange(1, i):
        helper = Matrix.MatrixMult(helper, helper)
      return helper

  def dump(self):
    print("Rows: %s Columns: %s" % (self.numRows, self.numColumns))
    for el in self.mat:
      print(el)

def main():
    A = map(int, raw_input().split())
    var_list = map(int, raw_input().split())
    coef_list = map(int, raw_input().split())

    if A[1] <= A[0]:
      var_list[A[1] - 1]

    # a_i = a_i-1 * c_0 + a_i-2 * c_1 + ... + a_i-k * c_k-1
    var_list.reverse()
    vectorStr = str(var_list).strip('[]').replace(',', ';')
    if A[0] == 1:
      matStr = str(coef_list).strip('[]').replace(',', '')
    else:
      matStr = str(coef_list).strip('[]').replace(',', '') + ';'

    for i in xrange(0, A[0] - 1):
      l = [0]*A[0]
      l[i] = 1
      if i == A[0] - 2:
        matStr = matStr + str(l).strip('[]').replace(',', '')
      else:
        matStr = matStr + str(l).strip('[]').replace(',', '') + ';'

    a = Matrix(A[0], 1, vectorStr)
    b = Matrix(A[0], A[0], matStr)
    n = A[1] - (A[0] - 1)
    expo[1] = b
    expo[2] = Matrix.MatrixMult(b,b)
    l = list(bin(n))[2:]
    l.reverse()
    c = []
    for i in xrange(0, len(l)):
      if int(l[i]) == 1:
        c.append(Matrix.MatrixExp(b, i))
    for el in c:
      a = Matrix.MatrixMult(el, a)

    print(a.mat[0][0])


if __name__=="__main__":
    main()
