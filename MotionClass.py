import random
import re


def MotionTranslate(mtn):
    # initialize
    motion_D = ''  # direction of the motion
    motion_E = 0  # the beginning point of the motion
    motion_S = ''  # the side of the motion
    motion_B = 0  # the end point of the motion
    trans_motion = ''

    # eliminate all the spaces from the motion input
    mtn = mtn.replace(" ", "")
    if MotionCheck(mtn) == -1:
        return -1
    MotionLen = len(mtn)
    if MotionLen == 1:
        # this is the skip-form of input
        motion_D = 'A'  # direction of the motion
        motion_E = 1  # the beginning point of the motion
        motion_S = mtn  # the side of the motion
        motion_B = 1  # the end point of the motion
    elif MotionLen == 2:
        # this is the skip-form of input
        if str.isdigit(mtn[0]):
            motion_D = 'A'  # direction of the motion
            motion_E = int(mtn[0])  # the end point of the motion
        elif str.isalpha(mtn[0]):
            motion_D = mtn[0]  # direction of the motion
            motion_E = 1  # the end point of the motion
        motion_S = mtn[1]  # the side of the motion
        motion_B = 1  # the beginning point of the motion
    elif MotionLen == 3:
        if str.isdigit(mtn[0]):
            motion_D = 'A'  # direction of the motion
            motion_E = int(mtn[0])  # the end point of the motion
            motion_S = mtn[1]  # the side of the motion
            motion_B = int(mtn[2])  # the beginning point of the motion
        elif str.isalpha(mtn[0]):
            motion_D = mtn[0]  # direction of the motion
            motion_E = int(mtn[1])  # the end point of the motion
            motion_S = mtn[2]  # the side of the motion
            motion_B = 1  # the beginning point of the motion
    elif MotionLen == 4:
        motion_D = mtn[0]  # direction of the motion
        motion_E = int(mtn[1])  # the end point of the motion
        motion_S = mtn[2]  # the side of the motion
        motion_B = int(mtn[3])  # the beginning point of the motion
    trans_motion = motion_D + str(motion_E) + motion_S + str(motion_B)
    return trans_motion


def MotionCheck(mtn):
    # This function is not complete yet
    # Eliminate the apparent wrong motion
    direction = "AT"
    face = "FBDULR"
    num = "12345679890"

    check_str = direction + face + num
    for s in mtn:
        if s not in check_str:
            return -1


def RadonMotionGenerator(N):
    num = random.randint(5, 50)
    motion_Arr = ''
    motion = ''
    for i in range(num):
        # decide direction, clockwise or counter-clockwise
        direction = ''
        if random.random() > 0.5:
            direction = 'A'
        else:
            direction = 'T'

        # decide face, F,D,B,U,L,R
        face_rand = random.randint(0, 100)
        face = ''
        if face_rand % 6 == 0:
            face = 'F'
        elif face_rand % 6 == 1:
            face = 'D'
        elif face_rand % 6 == 2:
            face = 'B'
        elif face_rand % 6 == 3:
            face = 'U'
        elif face_rand % 6 == 4:
            face = 'L'
        elif face_rand % 6 == 5:
            face = 'R'

        # decide lines, starting point and end point
        L1 = random.randint(1, N)
        L2 = random.randint(1, N)

        sp = min(L1, L2)
        ep = max(L1, L2)

        # combine the motion
        motion = direction + str(ep) + face + str(sp)
        motion_Arr += motion + ';'
    # print(motion_Arr)
    return motion_Arr


class RubikMotion(object):
    def __init__(self, MotionStr):
        self.motion = MotionStr.upper()  # to eliminate the case of the input letters
        self.trans_motion = MotionTranslate(self.motion)
        if self.trans_motion != -1:
            self.motion_D = self.trans_motion[0]  # direction of the motion
            self.motion_E = int(self.trans_motion[1])  # end line of the motion
            self.motion_S = self.trans_motion[2]  # face of the motion
            self.motion_B = int(self.trans_motion[3])  # start line of the motion

    def MotionShow(self):
        print(self.trans_motion)


def BasisMotionGenerator(N):
    # This function generates all the effective motions as rubik's motion basis;
    # There are equivalent motions that are ignored here to make it easier, for example, d = (N-1)U1, L=(N-1)R1;
    # Besides, a rubik turns all lines means a rotate, there is nothing changed actually;
    # Moreover, counter clockwise 'T' is also treated by '90 * 3', a '90 * 4' is also a rotate.
    BasisSides = ['F', 'L', 'U']
    BasisMotions = []
    # This generates only different motion of a rubik
    for s in BasisSides:
        for i in range(1, N + 1):
            for j in range(i, N):
                motion = 'A' + str(j) + s + str(i)  # standard input of the motion basis
                BasisMotions.append(motion)

    # This generate the different turns as 90 * 1, 90*2, 90*3='T' which is counter clockwise
    BasisMotionList = []
    for s in BasisMotions:
        for i in range(3):
            motions = ""
            for j in range(i, 3):
                motions += s + ';'
            BasisMotionList.append(motions)
    return BasisMotionList


def MotionReverse(list_mtn_str):
    # exchange 'A' and 'T' as reverse motion
    list_mtn_str = list_mtn_str.upper()
    list_mtn_str = list_mtn_str.replace('A', 'Q')
    list_mtn_str = list_mtn_str.replace('T', 'A')
    list_mtn_str = list_mtn_str.replace('Q', 'T')

    mtn_list = re.split(r'[-;,\s]\s*', list_mtn_str)
    for s in mtn_list:
        if not s:
            mtn_list.remove("")  # remove empty
            break

    mtn_list.reverse()  # reverse motion order to make it back

    list_mtn_str = ";".join(mtn_list)
    return list_mtn_str
