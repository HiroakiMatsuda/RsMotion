#!/usr/bin/env python
#coding:utf-8
# ver. 1.21118
# (C) 2012 Matsuda Hiroaki

import Tkinter as Tk
import ConfigParser as Conf
import ScrolledText as St

class TkRsMotion():
    
    def __init__(self):
        self.root = Tk.Tk()
        self.root.option_add('*font', ('Helvetica', 10))
        self.root.title('RsMotion')

        self.servo_num, self.servo_data, icon_list = self.read_inifile('ini\gui.ini')
        self.set_img(icon_list)

        panedwindow = Tk.PanedWindow(self.root)
        panedwindow.pack(fill = Tk.BOTH, expand = True)
        

        frame_main = Tk.Frame(panedwindow)
        frame_text = Tk.Frame(panedwindow)
        frame_sys = Tk.LabelFrame(frame_main, text = 'All Servo Motor', labelanchor = Tk.NW)

        self.button_servo = Tk.Button(frame_sys, height = 24, image = self.img[0],
                                 bg = '#003366', command = lambda: self.all_servo_on())
        self.button_servo.pack(fill = Tk.BOTH)
 
        frame_sys.grid(column = 0, row = 0, sticky=Tk.W + Tk.E)

        self.text = St.ScrolledText(frame_text, width = 40)
        self.text.pack(expand = True, fill = Tk.BOTH)

        self.frame_servo = []
        self.position = []
        self.on_flag = {}
        self.all_flag = 0
        self.btn_img = {}
        self.slbar = {}
        self.label = {}

        for i in range(self.servo_num):
            self.position.append(Tk.IntVar())
            self.position[i].set(0)

            temp_id = self.servo_data[i][1]       
            self.on_flag[temp_id] = 0

            self.frame_servo.append(Tk.LabelFrame(frame_main, text = self.servo_data[i][0], labelanchor = Tk.NW))
            
            self.btn_img[temp_id] = Tk.Button(self.frame_servo[i], height = 24, image = self.img[0],
                                   command = lambda id = temp_id: self.servo_on(id), bg = '#003366')
            self.btn_img[temp_id].pack(side = Tk.LEFT)

            self.slbar[temp_id] = Tk.Scale(self.frame_servo[i], orient = 'h', from_ = self.servo_data[i][2],
                                           to = self.servo_data[i][3], variable = self.position[i],
                                           showvalue = False, length = 200,
                                          command = lambda x, id = temp_id: self.write_command(x, id))
            self.slbar[temp_id].pack(side = Tk.LEFT)
                        
            self.label[temp_id] = Tk.Label(self.frame_servo[i], textvariable = self.position[i] ,width = 4)
            self.label[temp_id].pack(side = Tk.LEFT)
            
            self.frame_servo[i].grid(column = self.servo_data[i][4], row = self.servo_data[i][5])

        # set main window
        panedwindow.add(frame_main)
        panedwindow.add(frame_text)

        
        # initialize sens data
        self.sens_data = []
        for i in range(self.servo_num):
            self.sens_data.append(['None', 'None', 'None', 'None', 'None', 'None', 'None'])

    def all_servo_on(self):
        if self.all_flag == 0:
            self.button_servo.configure(bg = '#339966')
            for i in range(self.servo_num):
                id = self.servo_data[i][1]
                self.out_port([1, id, 1])
                self.on_flag[id] = 1
                self.btn_img[id].configure(bg = '#339966')
            self.all_flag = 1
            
        elif self.all_flag == 1:
            self.button_servo.configure(bg = '#cc0033')
            for i in range(self.servo_num):
                id = self.servo_data[i][1]
                self.out_port([1, id, 0])
                self.on_flag[id] = 0
                self.btn_img[id].configure(bg = '#cc0033')
            self.all_flag = 0

    def servo_on(self, id):
        if self.on_flag[id] == 0:
            self.btn_img[id].configure(bg = '#339966')
            self.out_port([0, id, 1])
            self.on_flag[id] = 1
            
        elif self.on_flag[id] == 1:
            self.btn_img[id].configure(bg = '#cc0033')
            self.out_port([0, id, 0])
            self.on_flag[id] = 0

    def write_command(self, position, id):
        self.out_port([0, id, int(position), 10])
        self.write_text()
        
    def read_inifile(self, path):
        conf = Conf.SafeConfigParser()
        conf.read(path)
        servo_num = int(conf.get('SERVO', 'servo_num'))
        servo_data = []
        for i in range(servo_num):
            servo_temp = []
            servo_temp.append(conf.get('SERVO', 'id' + str(i + 1) + '_label'))
            servo_temp.append(int(conf.get('SERVO', 'id' + str(i + 1) + '_id')))
            servo_temp.append(int(conf.get('SERVO', 'id' + str(i + 1) + '_min')))
            servo_temp.append(int(conf.get('SERVO', 'id' + str(i + 1) + '_max')))
            servo_temp.append(int(conf.get('SERVO', 'id' + str(i + 1) + '_column')))
            servo_temp.append(int(conf.get('SERVO', 'id' + str(i + 1) + '_row')))
            servo_data.append(servo_temp)
        icon_list = []
        icon_list.append(conf.get('ICON', 'servo_on'))
        
        return servo_num, servo_data, icon_list

    def set_img(self, icon_list):
        self.img = []
        for i in range(len(icon_list)):
            self.img.append(Tk.PhotoImage(file = icon_list[i]))

    def set_icon(self, inifile):
        img = []
        for i in range(len(inifile[1])):
            img.append(Tk.PhotoImage(file = inifile[1][i][1]))
        return img

    def set_sens(self):
        sens =  self.in_port()
        for i in range(1, self.servo_num + 1):
            if len(sens) != 0:
                if i == sens[0]:
                    self.sens_data[i - 1] = sens

    def write_text(self):
        self.text_form = 'ID Pos Cur Vol Loa Tem\n'
        self.set_sens()
        for i in range(self.servo_num):
            self.text_form += '%s %s %s %s %s %s \n' %(i + 1, self.position[i].get(),
                                                       self.sens_data[i][2], self.sens_data[i][3],
                                                       self.sens_data[i][4], self.sens_data[i][5])
        self.text.delete('1.0', 'end')
        self.text.insert('end', self.text_form)

    def get_out_port(self, func):
        self.out_port = func

    def get_in_port(self, func):
        self.in_port = func
