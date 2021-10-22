import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time


def TransposeSlicesMatrix(Mat, N):
    reMat = [[None for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            reMat[i][j] = Mat[j][i]

    return reMat


def RotateSlicesMatrix(Mat, N, direction):
    reMat = [[None for i in range(N)] for j in range(N)]
    if direction == 1:
        # clock-wise rotate the matrix
        for i in range(N):
            for j in range(N):
                reMat[i][j] = Mat[N - j - 1][i]
    elif direction == -1:
        # counter clock-wise rotate the matrix
        for i in range(N):
            for j in range(N):
                reMat[i][j] = Mat[j][N - i - 1]
    return reMat


class Slice(object):
    def __init__(self, vertices, clr, num, face):
        self.vertices = vertices
        self.clr = clr
        self.num = num
        self.face = face


def slice_move(vert_init, stepArr):
    vert = np.copy(vert_init)
    for i in range(4):
        for j in range(3):
            vert[i][j] = vert_init[i][j] + stepArr[j]
    return vert


def Init_Slices_Obtain(vert_init, direction, N, clr, face):
    # obtain vertices from the initial piece of every face
    Vert_Mat = [[j for j in range(N)] for i in range(N)]
    a = 0
    b = 0
    count = 1
    for i in range(N * direction[0] + 1 - direction[0]):
        for j in range(N * direction[1] + 1 - direction[1]):
            for k in range(N * direction[2] + 1 - direction[2]):
                SliceVertices = slice_move(vert_init, [i, j, k])
                Vert_Mat[a][b] = Slice(SliceVertices, clr, count, face)
                b = b + 1
                if b % N == 0:
                    a = a + 1
                    b = 0
                count += 1
    return Vert_Mat


def verticesMatExtractArr(Vert_Mat, N):
    Vert_Arr = [None] * N * N
    for i in range(N):
        for j in range(N):
            Vert_Arr[i * N + j] = Vert_Mat[i][j].vertices
    return Vert_Arr


class RubikFace(object):
    def __init__(self, face, N):
        vert_init = []
        direction = []
        self.face = face
        self.N = N
        self.vert_Mat = [[None] * N] * N
        self.vert_Arr = [None] * N * N
        self.clr_Mat = [[None] * N] * N
        self.clrArr = [None] * N * N

        transpose_mat = None
        rotate_mat = None
        clr_init = 'k'
        if face == 'F':
            vert_init = [[self.N, 0, 0], [self.N, 1, 0], [self.N, 1, 1], [self.N, 0, 1]]
            direction = [0, 1, 1]
            clr_init = 'r'
            transpose_mat = [None]
            rotate_mat = [-1]
        elif face == 'D':
            vert_init = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
            direction = [1, 1, 0]
            clr_init = 'w'
            transpose_mat = ['T']
            rotate_mat = [-1]
        elif face == 'B':
            vert_init = [[0, 0, 0], [0, 1, 0], [0, 1, 1], [0, 0, 1]]
            direction = [0, 1, 1]
            clr_init = 'm'
            transpose_mat = ['T']
            rotate_mat = [None]
        elif face == 'U':
            vert_init = [[0, 0, self.N], [1, 0, self.N], [1, 1, self.N], [0, 1, self.N]]
            direction = [1, 1, 0]
            clr_init = 'y'
            transpose_mat = [None]
            rotate_mat = [None]
        elif face == 'L':
            vert_init = [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]]
            direction = [1, 0, 1]
            clr_init = 'b'
            transpose_mat = [None]
            rotate_mat = [-1]
        elif face == 'R':
            vert_init = [[0, self.N, 0], [0, self.N, 1], [1, self.N, 1], [1, self.N, 0]]
            direction = [1, 0, 1]
            clr_init = 'c'
            transpose_mat = ['T']
            rotate_mat = [1, 1]
        # obtain the vertices matrices from the initial slice, by generating step by step
        vertice_Mat = Init_Slices_Obtain(vert_init, direction, self.N, clr_init, face)

        # rotate the matrix that adapting the view of the screen
        for i in transpose_mat:
            if i:
                vertice_Mat = TransposeSlicesMatrix(vertice_Mat, self.N)
        for i in rotate_mat:
            if i:
                vertice_Mat = RotateSlicesMatrix(vertice_Mat, self.N, i)

        # set the vertices matrix to the class object
        self.vert_Mat = vertice_Mat
        self.vert_Arr = verticesMatExtractArr(self.vert_Mat, self.N)

        self.clrArr = [clr_init for i in range(N * N)]  # initial color of the pieces

    def face_update(self, clrMat):
        #  update the face color by the given color matrix
        # the color matrix contains numbers, we translate them here to unify the color of the rubik.
        self.clr_Mat = clrMat
        Arr = [None] * self.N * self.N
        count = 0
        for i in range(self.N):
            for j in range(self.N):
                if clrMat[i][j] % 10 == 1:
                    Arr[count] = 'r'
                elif clrMat[i][j] % 10 == 2:
                    Arr[count] = 'w'
                elif clrMat[i][j] % 10 == 3:
                    Arr[count] = 'm'
                elif clrMat[i][j] % 10 == 4:
                    Arr[count] = 'y'
                elif clrMat[i][j] % 10 == 5:
                    Arr[count] = 'b'
                elif clrMat[i][j] % 10 == 6:
                    Arr[count] = 'c'
                count += 1
        self.clrArr = [row[:] for row in Arr]


class Rubik3D(object):
    def __init__(self, N, RubikMatrix):
        # initial value
        self.RubikMatrix = RubikMatrix
        self.N = N
        self.Face_F = RubikFace('F', N)
        self.Face_D = RubikFace('D', N)
        self.Face_B = RubikFace('B', N)
        self.Face_U = RubikFace('U', N)
        self.Face_L = RubikFace('L', N)
        self.Face_R = RubikFace('R', N)

        self.update_clr(RubikMatrix)

        # 3D plot first configuration, draw the cubes, edges, initial colors.
        self.fig = plt.gcf()
        self.fig.clf()

        self.ax = self.fig.add_subplot(111, projection='3d')

        self.poly_F = Poly3DCollection(self.Face_F.vert_Arr)
        self.poly_F.set_facecolor(self.Face_F.clrArr)
        self.poly_F.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_F)

        self.poly_D = Poly3DCollection(self.Face_D.vert_Arr)
        self.poly_D.set_facecolor(self.Face_D.clrArr)
        self.poly_D.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_D)

        self.poly_B = Poly3DCollection(self.Face_B.vert_Arr)
        self.poly_B.set_facecolor(self.Face_B.clrArr)
        self.poly_B.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_B)

        self.poly_U = Poly3DCollection(self.Face_U.vert_Arr)
        self.poly_U.set_facecolor(self.Face_U.clrArr)
        self.poly_U.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_U)

        self.poly_L = Poly3DCollection(self.Face_L.vert_Arr)
        self.poly_L.set_facecolor(self.Face_L.clrArr)
        self.poly_L.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_L)

        self.poly_R = Poly3DCollection(self.Face_R.vert_Arr)
        self.poly_R.set_facecolor(self.Face_R.clrArr)
        self.poly_R.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_R)

    def update_clr(self, RubikMatrix):
        # update by initial input matrix
        self.Face_F.face_update(RubikMatrix.F)
        self.Face_D.face_update(RubikMatrix.D)
        self.Face_B.face_update(RubikMatrix.B)
        self.Face_U.face_update(RubikMatrix.U)
        self.Face_L.face_update(RubikMatrix.L)
        self.Face_R.face_update(RubikMatrix.R)

    def draw3DCube(self):
        self.poly_F.set_facecolor(self.Face_F.clrArr)
        self.poly_D.set_facecolor(self.Face_D.clrArr)
        self.poly_B.set_facecolor(self.Face_B.clrArr)
        self.poly_U.set_facecolor(self.Face_U.clrArr)
        self.poly_L.set_facecolor(self.Face_L.clrArr)
        self.poly_R.set_facecolor(self.Face_R.clrArr)

        self.ax = self.fig.gca()

        self.ax.set_xlim(0, self.N)
        self.ax.set_ylim(0, self.N)
        self.ax.set_zlim(0, self.N)
        # ax.set_facecolor('white')
        # plt.axis('off')
        self.ax.view_init(30, -30)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(0.5)

        return self.fig
