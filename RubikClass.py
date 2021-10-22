import re
import time

import numpy as np
import matplotlib.pyplot as plt

import MotionClass


def MatrixBackConvert(A):
    m = len(A)
    R_Mat = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            R_Mat[i][j] = A[m - i - 1][m - j - 1]
    return R_Mat


def MatrixTurn(A, direction, ax):
    Mat = np.copy(A)
    m = len(Mat)
    n = len(Mat[0])
    R_Mat = np.zeros((m, n))
    if ax == 1:
        if direction == 'A':
            direction = 'T'
        elif direction == 'T':
            direction = 'A'

    if direction == 'A':
        # clock-wise rotate the matrix
        for i in range(m):
            for j in range(n):
                R_Mat[i][j] = Mat[m - j - 1][i]
    elif direction == 'T':
        # counter clock-wise rotate the matrix
        for i in range(m):
            for j in range(n):
                R_Mat[i][j] = Mat[j][n - i - 1]
    # print(R_Mat)
    return R_Mat


def MatrixVrtc(A, B, side, startP, endP):
    Mat1 = np.copy(A)
    Mat2 = np.copy(B)
    m = len(Mat1)
    if side == 'R':
        for i in range(m):
            for j in range(m - startP, m - endP - 1, -1):
                Mat1[i][j] = Mat2[i][j]
    elif side == 'L':
        for i in range(m):
            for j in range(startP - 1, endP):
                Mat1[i][j] = Mat2[i][j]
    return Mat1


def MatrixHrzt(A, B, side, startP, endP):
    Mat1 = np.copy(A)
    Mat2 = np.copy(B)
    m = len(Mat1)
    if side == 'D':
        for i in range(m - startP, m - endP - 1, -1):
            for j in range(m):
                Mat1[i][j] = Mat2[i][j]
    elif side == 'U':
        for i in range(startP - 1, endP):
            for j in range(m):
                Mat1[i][j] = Mat2[i][j]
    return Mat1


def MatrixCycl(A, B, side, startP, endP):
    Mat1 = np.copy(A)
    Mat2 = np.copy(B)
    m = len(Mat1)
    if side == 'F':
        for i in range(m - startP, m - endP - 1, -1):
            for j in range(m):
                Mat1[i][j] = Mat2[i][j]
    elif side == 'B':
        for i in range(startP - 1, endP):
            for j in range(m):
                Mat1[i][j] = Mat2[i][j]
    return Mat1


class RubikMatrix(object):
    def __init__(self, Dim):
        # initialize the variables
        self.N = Dim
        self.UnFoldMat = np.zeros((4 * Dim, 3 * Dim))
        self.F = [[(i + j * Dim + 1) * 10 + 1 for i in range(Dim)] for j in range(Dim)]
        self.D = [[(i + j * Dim + 1) * 10 + 2 for i in range(Dim)] for j in range(Dim)]
        self.B = [[(i + j * Dim + 1) * 10 + 3 for i in range(Dim)] for j in range(Dim)]
        self.U = [[(i + j * Dim + 1) * 10 + 4 for i in range(Dim)] for j in range(Dim)]
        self.L = [[(i + j * Dim + 1) * 10 + 5 for i in range(Dim)] for j in range(Dim)]
        self.R = [[(i + j * Dim + 1) * 10 + 6 for i in range(Dim)] for j in range(Dim)]

    def MatrixUnFold(self):
        # to Unfold the cube into a flat matrix containing all 6 sides of the cube
        MatRow = np.concatenate((self.L, self.F, self.R), axis=1)
        MatCol = np.concatenate((self.D, self.B, self.U), axis=0)
        for i in range(self.N):
            for j in range(3 * self.N):
                self.UnFoldMat[i][j] = MatRow[i][j]
        for i in range(self.N, 4 * self.N):
            for j in range(self.N, 2 * self.N):
                self.UnFoldMat[i][j] = MatCol[i - self.N][j - self.N]

    def MatrixFold(self):
        # Fold the large matrix into formatted matrices, in order to use later
        # self.F = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                self.F[i][j] = self.UnFoldMat[i][self.N + j]
        for i in range(self.N):
            for j in range(self.N):
                self.D[i][j] = self.UnFoldMat[self.N + i][self.N + j]
        for i in range(self.N):
            for j in range(self.N):
                self.B[i][j] = self.UnFoldMat[2 * self.N + i][self.N + j]
        for i in range(self.N):
            for j in range(self.N):
                self.U[i][j] = self.UnFoldMat[3 * self.N + i][self.N + j]
        for i in range(self.N):
            for j in range(self.N):
                self.L[i][j] = self.UnFoldMat[i][j]
        for i in range(self.N):
            for j in range(self.N):
                self.R[i][j] = self.UnFoldMat[i][2 * self.N + j]

    def MatrixStep(self, mtn_str):
        # First analyze the motion string and translate it into 'Motion Class'
        if mtn_str:
            mtn = MotionClass.RubikMotion(mtn_str)
            if mtn.trans_motion == -1:
                return -1
        else:  # if the motion is empty, then ignore, otherwise report -1 when wrong
            return
        # mtn.MotionShow()

        if mtn.motion_D == "A":
            if mtn.motion_S == "U":
                # horizontal motion, influence L,F,R,B and 'U' rotate of 90 degrees
                temp = np.copy(self.F)
                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

                self.F = MatrixHrzt(self.F, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixHrzt(self.R, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixHrzt(self.B, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixHrzt(self.L, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

            elif mtn.motion_S == "D":
                # horizontal motion, influence L,F,R,B and 'D' rotate of 90 degrees
                temp = np.copy(self.F)
                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

                self.F = MatrixHrzt(self.F, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixHrzt(self.L, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixHrzt(self.B, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixHrzt(self.R, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

            elif mtn.motion_S == "R":
                # horizontal motion, influence F,D,B,U and 'R' rotate of 90 degrees
                temp = np.copy(self.F)

                self.F = MatrixVrtc(self.F, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixVrtc(self.D, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixVrtc(self.B, self.U, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.U = MatrixVrtc(self.U, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

            elif mtn.motion_S == "L":
                # horizontal motion, influence F,D,B,U and 'L' rotate of 90 degrees
                temp = np.copy(self.F)

                self.F = MatrixVrtc(self.F, self.U, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.U = MatrixVrtc(self.U, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixVrtc(self.B, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixVrtc(self.D, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

            elif mtn.motion_S == "F":
                # horizontal motion, influence U,R,D,L and 'F' rotate of 90 degrees
                temp = np.copy(self.U)

                self.L = MatrixTurn(self.L, mtn.motion_D, 0)  # when U is seen as the origin, then L and R should be
                self.R = MatrixTurn(self.R, mtn.motion_D, 1)  # rotate 90 degrees toward it
                self.D = MatrixBackConvert(self.D)  # when U is seen as the origin, D is seen as bottom

                self.U = MatrixCycl(self.U, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixCycl(self.L, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixCycl(self.D, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixCycl(self.R, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.D = MatrixBackConvert(self.D)
                self.L = MatrixTurn(self.L, mtn.motion_D, 1)
                self.R = MatrixTurn(self.R, mtn.motion_D, 0)
            elif mtn.motion_S == "B":
                # horizontal motion, influence L,F,R,B
                # horizontal motion, influence U,R,D,L and 'F' rotate of 90 degrees
                temp = np.copy(self.U)

                self.B = MatrixBackConvert(self.B)
                self.L = MatrixTurn(self.L, mtn.motion_D, 0)  # when U is seen as the origin, then L and R should be
                self.R = MatrixTurn(self.R, mtn.motion_D, 1)  # rotate 90 degrees toward it
                self.D = MatrixBackConvert(self.D)  # when U is seen as the origin, D is seen as bottom

                self.U = MatrixCycl(self.U, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixCycl(self.R, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixCycl(self.D, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixCycl(self.L, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.D = MatrixBackConvert(self.D)
                self.L = MatrixTurn(self.L, mtn.motion_D, 1)
                self.R = MatrixTurn(self.R, mtn.motion_D, 0)
                self.B = MatrixBackConvert(self.B)

        elif mtn.motion_D == "T":
            if mtn.motion_S == "U":
                # horizontal motion, influence L,F,R,B and 'U' rotate of 90 degrees
                temp = np.copy(self.F)
                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

                self.F = MatrixHrzt(self.F, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixHrzt(self.L, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixHrzt(self.B, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixHrzt(self.R, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

            elif mtn.motion_S == "D":
                # horizontal motion, influence L,F,R,B and 'D' rotate of 90 degrees
                temp = np.copy(self.F)
                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

                self.F = MatrixHrzt(self.F, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixHrzt(self.R, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixHrzt(self.B, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixHrzt(self.L, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.B = MatrixBackConvert(self.B)  # the backside of the cube is upside down in the motion

            elif mtn.motion_S == "R":
                # horizontal motion, influence F,D,B,U and 'R' rotate of 90 degrees
                temp = np.copy(self.F)

                self.F = MatrixVrtc(self.F, self.U, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.U = MatrixVrtc(self.U, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixVrtc(self.B, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixVrtc(self.D, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

            elif mtn.motion_S == "L":
                # horizontal motion, influence F,D,B,U and 'L' rotate of 90 degrees
                temp = np.copy(self.F)

                self.F = MatrixVrtc(self.F, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixVrtc(self.D, self.B, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.B = MatrixVrtc(self.B, self.U, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.U = MatrixVrtc(self.U, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

            elif mtn.motion_S == "F":
                # horizontal motion, influence U,R,D,L and 'F' rotate of 90 degrees
                temp = np.copy(self.U)

                self.L = MatrixTurn(self.L, mtn.motion_D, 1)  # when U is seen as the origin, then L and R should be
                self.R = MatrixTurn(self.R, mtn.motion_D, 0)  # rotate 90 degrees toward it
                self.D = MatrixBackConvert(self.D)  # when U is seen as the origin, D is seen as bottom

                self.U = MatrixCycl(self.U, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixCycl(self.R, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixCycl(self.D, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixCycl(self.L, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.D = MatrixBackConvert(self.D)
                self.L = MatrixTurn(self.L, mtn.motion_D, 0)
                self.R = MatrixTurn(self.R, mtn.motion_D, 1)
            elif mtn.motion_S == "B":
                # horizontal motion, influence L,F,R,B
                # horizontal motion, influence U,R,D,L and 'F' rotate of 90 degrees
                temp = np.copy(self.U)

                self.B = MatrixBackConvert(self.B)
                self.L = MatrixTurn(self.L, mtn.motion_D, 1)  # when U is seen as the origin, then L and R should be
                self.R = MatrixTurn(self.R, mtn.motion_D, 0)  # rotate 90 degrees toward it
                self.D = MatrixBackConvert(self.D)  # when U is seen as the origin, D is seen as bottom

                self.U = MatrixCycl(self.U, self.L, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.L = MatrixCycl(self.L, self.D, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.D = MatrixCycl(self.D, self.R, mtn.motion_S, mtn.motion_B, mtn.motion_E)
                self.R = MatrixCycl(self.R, temp, mtn.motion_S, mtn.motion_B, mtn.motion_E)

                self.D = MatrixBackConvert(self.D)
                self.L = MatrixTurn(self.L, mtn.motion_D, 0)
                self.R = MatrixTurn(self.R, mtn.motion_D, 1)
                self.B = MatrixBackConvert(self.B)

        if mtn.motion_B == 1:
            if mtn.motion_S == "U":
                self.U = MatrixTurn(self.U, mtn.motion_D, 0)
            elif mtn.motion_S == "D":
                self.D = MatrixTurn(self.D, mtn.motion_D, 0)
            elif mtn.motion_S == "R":
                self.R = MatrixTurn(self.R, mtn.motion_D, 0)
            elif mtn.motion_S == "L":
                self.L = MatrixTurn(self.L, mtn.motion_D, 0)
            elif mtn.motion_S == "F":
                self.F = MatrixTurn(self.F, mtn.motion_D, 0)
            elif mtn.motion_S == "B":
                self.B = MatrixTurn(self.B, mtn.motion_D, 0)

        if mtn.motion_E == self.N:
            if mtn.motion_S == "U":
                self.D = MatrixTurn(self.D, mtn.motion_D, 1)
            elif mtn.motion_S == "D":
                self.U = MatrixTurn(self.U, mtn.motion_D, 1)
            elif mtn.motion_S == "R":
                self.L = MatrixTurn(self.L, mtn.motion_D, 1)
            elif mtn.motion_S == "L":
                self.R = MatrixTurn(self.R, mtn.motion_D, 1)
            elif mtn.motion_S == "F":
                self.B = MatrixTurn(self.B, mtn.motion_D, 1)
            elif mtn.motion_S == "B":
                self.F = MatrixTurn(self.F, mtn.motion_D, 1)

    def MatrixMutiStep(self, list_mtn_str):
        mtn_list = re.split(r'[-;,\s]\s*', list_mtn_str)
        for mtn in mtn_list:
            self.MatrixStep(mtn)
            # self.MatrixShow()

    def MatrixShuffle(self):
        list_mtn_str = MotionClass.RadonMotionGenerator(self.N)
        mtn_list = re.split(r'[-;,\s]\s*', list_mtn_str)
        for mtn in mtn_list:
            self.MatrixStep(mtn)

    def MatrixShow(self):
        self.MatrixUnFold()
        Mat = self.UnFoldMat
        clr = ''
        fig = plt.gcf()
        fig.clf()
        for i in range(4 * self.N):
            for j in range(3 * self.N):
                if Mat[i][j] != 0:
                    if Mat[i][j] % 10 == 1:
                        clr = 'r'
                    elif Mat[i][j] % 10 == 2:
                        clr = 'c'
                    elif Mat[i][j] % 10 == 3:
                        clr = 'm'
                    elif Mat[i][j] % 10 == 4:
                        clr = 'y'
                    elif Mat[i][j] % 10 == 5:
                        clr = 'b'
                    elif Mat[i][j] % 10 == 6:
                        clr = 'k'
                    plt.text(0.5 + j, 4 * self.N - 0.5 - i, str(int(Mat[i][j])), verticalalignment="center",
                             horizontalalignment="center", color=clr)
        ax = fig.gca()
        ax.set_xticks(np.arange(0, 3 * self.N + 1, 1))
        ax.set_yticks(np.arange(0, 4 * self.N + 1, 1))
        plt.grid()
        plt.show()

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.5)

    def SuccessCheck(self):
        f1 = MatrixSameCheck(MatrixElementsReminder(self.F))
        f2 = MatrixSameCheck(MatrixElementsReminder(self.D))
        f3 = MatrixSameCheck(MatrixElementsReminder(self.B))
        f4 = MatrixSameCheck(MatrixElementsReminder(self.U))
        f5 = MatrixSameCheck(MatrixElementsReminder(self.L))
        f6 = MatrixSameCheck(MatrixElementsReminder(self.R))
        if f1 + f2 + f3 + f4 + f5 + f6 == 6:
            return True
        return False

    def MatrixLoad(self, Mat):
        # reload the matrix from the input list of matrices, order F,D,B,U,L,R
        if len(Mat) != self.N and len(Mat[0]) != self.N:
            print("Dimension doesn't match!")
            return -1
        Mat = np.array(Mat)
        self.F = Mat[0:self.N, :]
        self.D = Mat[self.N:self.N * 2, :]
        self.B = Mat[self.N * 2:self.N * 3, :]
        self.U = Mat[self.N * 3:self.N * 4, :]
        self.L = Mat[self.N * 4:self.N * 5, :]
        self.R = Mat[self.N * 5:self.N * 6, :]


def MatrixElementsReminder(Mat):
    m = len(Mat)
    n = len(Mat[0])
    R_Mat = np.copy(Mat)
    for i in range(m):
        for j in range(n):
            R_Mat[i][j] = Mat[i][j] % 10
    return R_Mat


def MatrixSameCheck(Mat):
    m = len(Mat)
    n = len(Mat[0])
    for i in range(m):
        for j in range(n):
            if Mat[0][0] != Mat[i][j]:
                return -1
    return 1
