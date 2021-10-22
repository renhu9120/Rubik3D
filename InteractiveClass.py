import datetime
import os
import re
import tkinter
from tkinter import messagebox

import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import DisplayClass
import RubikClass
from tkinter.filedialog import askopenfilename


class RubikInteractive(object):
    def __init__(self, N):
        self.N = N
        self.stepNum = 0
        root = tkinter.Tk()
        root.wm_title("Rubik Cube")
        self.SuccessFlag = True

        container_frame = tkinter.Frame(root)
        container_frame.grid(row=1)

        # setting the windows size
        # root.geometry("600x400")

        # figure preparation
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.view_init(30, -30)
        self.ax.set_xlim(0, self.N)
        self.ax.set_ylim(0, self.N)
        self.ax.set_zlim(0, self.N)

        # Rubik definition
        self.rbk = RubikClass.RubikMatrix(N)
        self.rbk3D = DisplayClass.Rubik3D(N, self.rbk)

        # canvas in the figure definition
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0)
        # toolbar = NavigationToolbar2Tk(self.canvas, root)
        # toolbar.update()
        # self.canvas.get_tk_widget().grid(row=1)

        # 3D plot first configuration, draw the cubes, edges, initial colors.
        self.poly_F = Poly3DCollection(self.rbk3D.Face_F.vert_Arr)
        self.poly_F.set_facecolor(self.rbk3D.Face_F.clrArr)
        self.poly_F.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_F)

        self.poly_D = Poly3DCollection(self.rbk3D.Face_D.vert_Arr)
        self.poly_D.set_facecolor(self.rbk3D.Face_D.clrArr)
        self.poly_D.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_D)

        self.poly_B = Poly3DCollection(self.rbk3D.Face_B.vert_Arr)
        self.poly_B.set_facecolor(self.rbk3D.Face_B.clrArr)
        self.poly_B.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_B)

        self.poly_U = Poly3DCollection(self.rbk3D.Face_U.vert_Arr)
        self.poly_U.set_facecolor(self.rbk3D.Face_U.clrArr)
        self.poly_U.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_U)

        self.poly_L = Poly3DCollection(self.rbk3D.Face_L.vert_Arr)
        self.poly_L.set_facecolor(self.rbk3D.Face_L.clrArr)
        self.poly_L.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_L)

        self.poly_R = Poly3DCollection(self.rbk3D.Face_R.vert_Arr)
        self.poly_R.set_facecolor(self.rbk3D.Face_R.clrArr)
        self.poly_R.set_edgecolor("black")
        self.ax.add_collection3d(self.poly_R)

        # button "Motion" and "Entry"
        self.motion_input = tkinter.StringVar()

        def _motion_submit():
            self.stepNum += 1
            self.SuccessFlag = False
            list_mtn_str = self.motion_input.get()
            mtn_list = re.split(r'[-;,\s]\s*', list_mtn_str)
            self.motion_input.set("")
            for mtn in mtn_list:
                # update the rubik{
                flag = self.rbk.MatrixStep(mtn)
                # self.Update_Rubik()
                # till now cannot show multiple steps in 3D motion, don't know why, #
                # so in order to save time, just show at the end of the loop
                # }
                if flag == -1:  # input check
                    messagebox.showerror("Error", "Wrong motion input!")
                    return
                if self.rbk.SuccessCheck():  # completion check
                    self.SuccessFlag = True
                    print("Success!")
            self.Update_Rubik()

        Motion_label = tkinter.Label(master=container_frame, text="Motion: ")
        Motion_label.grid(row=1, column=0)
        Motion_entry = tkinter.Entry(master=container_frame,
                                     textvariable=self.motion_input,
                                     font=('calibre', 10, 'normal'))
        Motion_entry.grid(row=1, column=1)
        Motion_enter_btn = tkinter.Button(master=container_frame, text="Enter", command=_motion_submit)
        Motion_enter_btn.grid(row=1, column=2)

        # button "reset view"
        def _view_reset():
            self.ax.view_init(30, -30)
            self.canvas.draw()
            root.focus_set()

        reset_view_btn = tkinter.Button(master=container_frame, text="Reset View", command=_view_reset)
        reset_view_btn.grid(row=1, column=3)

        # button "shuffle"
        def _shuffle():
            if not self.SuccessFlag:
                shuffle_Qsn = messagebox.askquestion("Form", "Do you want to Shuffle")
                if shuffle_Qsn == "no":
                    return

            self.rbk.MatrixShuffle()
            self.Update_Rubik()
            self.SuccessFlag = False
            print("Shuffle Complete!")

        shuffle_btn = tkinter.Button(master=container_frame, text="Shuffle", command=_shuffle)
        shuffle_btn.grid(row=2, column=1)

        # button "shuffle"
        def _save_current():
            cur_time = datetime.datetime.now()
            name_str = str(cur_time.year) + str(cur_time.month) + str(cur_time.day) + str(cur_time.hour) + str(
                cur_time.minute) + str(cur_time.second)
            tkinter.Tk().withdraw()
            filename = tkinter.filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")],
                                                            defaultextension=".txt",
                                                            initialfile="R" + name_str + ".txt",
                                                            title="Save current game",
                                                            initialdir=os.getcwd())
            if filename == "":
                return

            order_str = str(self.N) + "\n"  # write in the order first

            # write in the matrix which is the main part
            saveMat = np.concatenate((self.rbk.F, self.rbk.D, self.rbk.B, self.rbk.U, self.rbk.L, self.rbk.R))
            save_str = '\n'.join(','.join('%d' % x for x in y) for y in saveMat)
            # print(save_str)

            mat_write = open(filename, "a")
            mat_write.write(order_str)
            mat_write.write(save_str)
            mat_write.close()

        shuffle_btn = tkinter.Button(master=container_frame, text="Save", command=_save_current)
        shuffle_btn.grid(row=2, column=2)

        # button "shuffle"
        def _load_current():
            tkinter.Tk().withdraw()
            filename = tkinter.filedialog.askopenfilename(filetypes=[("txt file", ".txt")],
                                                          title="Load game",
                                                          initialdir=os.getcwd())
            if filename == "":
                return
            mat_read = open(filename, "r")
            mat_info = mat_read.readlines()
            mat_read.close()

            print(mat_info[0])
            self.N = int(mat_info[0])

            Mat = [[0 for j in range(self.N)] for i in range(self.N * 6)]
            for i in range(0, len(mat_info) - 1):  # translate the string matrix back to rubik matrix
                # Rubik definition
                mat_str = mat_info[i + 1]
                mat_split = mat_str.split(',')
                j = 0
                for s in mat_split:
                    Mat[i][j] = int(s)
                    j = j + 1

            # reload the rubik and the figure class
            self.rbk = RubikClass.RubikMatrix(self.N)
            self.rbk3D = DisplayClass.Rubik3D(self.N, self.rbk)
            self.rbk.MatrixLoad(Mat)

            # update the whole figure
            self.ax.set_xlim(0, self.N)
            self.ax.set_ylim(0, self.N)
            self.ax.set_zlim(0, self.N)
            self.Update_Rubik()

        shuffle_btn = tkinter.Button(master=container_frame, text="Load", command=_load_current)
        shuffle_btn.grid(row=2, column=3)

        # button "Quit"
        def _quit():
            print("Total step number:", self.stepNum)
            root.quit()  # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        quit_btn = tkinter.Button(master=container_frame, text="Quit", command=_quit)
        quit_btn.grid(row=2, column=4)

        # key "Enter" press event
        def _enter_press(event):
            _motion_submit()

        root.bind('<Return>', _enter_press)

        # key "Arrow" press
        def _arrow_press(event):
            self.stepNum += 1
            cur_focus = root.focus_get().winfo_name()  # get the current focus.
            if cur_focus == "!entry":
                return  # If it is in the entry, then do nothing when press arrows.
            direction = ''
            face = ''
            if event.keysym == "Up":
                direction = 'T'
                face = 'L'
            elif event.keysym == "Down":
                direction = 'A'
                face = 'L'
            elif event.keysym == "Left":
                direction = 'A'
                face = 'U'
            elif event.keysym == "Right":
                direction = 'T'
                face = 'U'
            mtn = direction + str(self.N) + face  # up arrow can be seen as the counter clockwise left side all layers
            self.rbk.MatrixStep(mtn)
            self.Update_Rubik()

        root.bind('<Up>', _arrow_press)
        root.bind('<Down>', _arrow_press)
        root.bind('<Left>', _arrow_press)
        root.bind('<Right>', _arrow_press)

        # key "brace" press
        def _brace_press(event):
            cur_focus = root.focus_get().winfo_name()  # get the current focus.
            if cur_focus == "!entry":
                return  # If it is in the entry, then do nothing when press arrows.
            direction = ''
            self.stepNum += 1
            brace_key = event.char
            if brace_key == "[":
                direction = 'T'
            elif brace_key == "]":
                direction = 'A'
            if brace_key == "[" or brace_key == "]":
                mtn = direction + str(self.N) + 'F'
                self.rbk.MatrixStep(mtn)
                self.Update_Rubik()

        root.bind('<Key>', _brace_press)

        tkinter.mainloop()
        # If you put root.destroy() here, it will cause an error if the window is
        # closed with the window manager.

    def Update_Rubik(self):
        # update rubik by updating the data and then draw again the canvas
        self.rbk3D = DisplayClass.Rubik3D(self.N, self.rbk)
        self.poly_F.set_facecolor(self.rbk3D.Face_F.clrArr)
        self.poly_D.set_facecolor(self.rbk3D.Face_D.clrArr)
        self.poly_B.set_facecolor(self.rbk3D.Face_B.clrArr)
        self.poly_U.set_facecolor(self.rbk3D.Face_U.clrArr)
        self.poly_L.set_facecolor(self.rbk3D.Face_L.clrArr)
        self.poly_R.set_facecolor(self.rbk3D.Face_R.clrArr)
        self.canvas.draw()

