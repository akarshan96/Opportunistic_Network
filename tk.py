# -*- coding: utf-8 -*-

import Tkinter as tk
import urllib2
import re
import pyaudio
import wave
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sms_twilio import *
import time

class One(tk.Tk):
    def __init__(self, *args, **kwargs):
        # initializing Tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        # defining the main container
        container = tk.Frame(self)
        container.update_idletasks()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # defining different frames
        self.frames = {}
        for F in ( PageOne, Message, questionaire, statistics, military, requirements, condition, send, StartPage, PageOneHindi, Message_Hindi, questionaire_Hindi):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.var = tk.StringVar()
        global var1
        var1 = tk.StringVar()
        var1.set("English")
        print var1.get()
        label = tk.Label(self, text="WELCOME / अभिवादन")
        label3 = tk.Label(self, text="Choose a language / एक भाषा चुनें")
        option = tk.OptionMenu(self, var1, "English", "हिंदी", command=lambda x: self.lang(var1,button1,label,button2,button3,button4))
        label.pack(pady=5, padx=5)
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=1)
            self.var.set("CONNECTED / इंटरनेट से जुड़े हुए है")
        except urllib2.URLError as err:
            self.var.set("NOT CONNECTED / इंटरनेट से जुड़े नहीं है")
        label2 = tk.Label(self, textvariable=self.var)
        label2.pack(pady=5, padx=5)
        button1 = tk.Button(self, text="Collect Messages", command=lambda : self.Collect(controller))
        button2 = tk.Button(self, text="Send Messages", command=lambda: controller.show_frame(send))
        button3 = tk.Button(self, text="Refresh", command=lambda: self.refresh())
        button4 = tk.Button(self, text="Statistics", command=lambda: controller.show_frame(statistics))
        label3.pack()
        option.pack()
        button1.pack()
        button2.pack()
        button4.pack()
        button3.pack()
    def lang(self,var,button1,label,button2,button3,button4):
        print var.get()
        if var.get().encode('utf-8')=="हिंदी":
            button1.config(text="संदेश लीजिए")
            button2.config(text="संदेश भेजे")
            button3.config(text="रेफ़्रेश ")
            button4.config(text="आँकड़े")
        else:
            button1.config(text="Collect Messages")
            button2.config(text="Send Messages")
            button3.config(text="Refresh")
            button4.config(text="Statistics")


    def refresh(self):
        try:
            urllib2.urlopen('http://216.58.192.142', timeout=1)
            self.var.set("CONNECTED / इंटरनेट से जुड़े हुए है")
        except urllib2.URLError as err:
            self.var.set("NOT CONNECTED / इंटरनेट से जुड़े नहीं है")
    def Collect(self,controller):
        if var1.get()=="English":
            controller.show_frame(PageOne)
        elif var1.get().encode('utf-8')=="हिंदी":
            controller.show_frame(PageOneHindi)
        else:
            controller.show_frame(PageOne)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Basic Information")
        label1 = tk.Label(self, text="Your Name")
        label2 = tk.Label(self, text="Recipient's Name")
        label3 = tk.Label(self, text="Recipient's Phone no.")
        label4 = tk.Label(self, text="Recipient's email")
        label5 = tk.Label(self, text="Additional info.")
        button1 = tk.Button(self, text="Submit", command=lambda: self.submit(controller))
        button2 = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        self.name1 = tk.Entry(self)
        self.name2 = tk.Entry(self)
        self.phone = tk.Entry(self)
        self.email = tk.Entry(self)
        self.info = tk.Entry(self)

        label.pack()
        label1.pack()
        self.name1.pack()
        label2.pack()
        self.name2.pack()
        label3.pack()
        self.phone.pack()
        label4.pack()
        self.email.pack()
        label5.pack()
        self.info.pack()
        button1.pack()
        button2.pack()

    def submit(self,controller):
        if self.name1.get() == "" or self.name2.get() == "":
            if self.phone.get()=="" and self.email.get()=="":
               popup_window("field(s) missing","One or more fields are missing","Okay")
        else:
            if self.phone.get() != "" and self.match_1() != True:
                popup_window("wrong phone no.", "phone no. is not of 10 digits","Okay")

            elif self.email.get() != "" and self.match_2() == False:

                popup_window("wrong email", "incorrect email id entered","Okay")
            else:

                controller.show_frame(Message)
                getters(self.name1.get(), self.name2.get(), self.phone.get(), self.email.get(), self.info.get())
                self.name1.delete(0,'end')
                self.name2.delete(0, 'end')
                self.phone.delete(0, 'end')
                self.email.delete(0,'end')
                self.info.delete(0,'end')


    def match_1(self):
        pattern = re.compile("[0-9]{10}")
        if pattern.match(self.phone.get()):
            return True
        else:
            return False

    def match_2(self):
        pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if pattern.match(self.email.get()):
            return True
        else:
            return False


class PageOneHindi(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="मूलभूत जानकारी")
        label1 = tk.Label(self, text="आपका नाम")
        label2 = tk.Label(self, text="प्राप्तकर्ता का नाम")
        label3 = tk.Label(self, text="प्राप्तकर्ता का फोन नंबर")
        label4 = tk.Label(self, text="प्राप्तकर्ता की ई - मेल")
        label5 = tk.Label(self, text="अतिरिक्त जानकारी")
        button1 = tk.Button(self, text="जमा करें", command=lambda: self.submit(controller))
        button2 = tk.Button(self, text="वापस", command=lambda: controller.show_frame(StartPage))

        self.name1 = tk.Entry(self)
        self.name2 = tk.Entry(self)
        self.phone = tk.Entry(self)
        self.email = tk.Entry(self)
        self.info = tk.Entry(self)

        label.pack()
        label1.pack()
        self.name1.pack()
        label2.pack()
        self.name2.pack()
        label3.pack()
        self.phone.pack()
        label4.pack()
        self.email.pack()
        label5.pack()
        self.info.pack()
        button1.pack()
        button2.pack()
    def submit(self,controller):
        if self.name1.get() == "" or self.name2.get() == "":
            if self.phone.get()=="" and self.email.get()=="":
                popup_window("अनुपस्थित", "लापता एक या एक से अधिक क्षेत्र","ठीक है")
        else:
            if self.phone.get() != "" and self.match_1() != True:
                popup_window("ग़लत फ़ोन नंबर","फोन नंबर 10 अंकों का नहीं है","ठीक है")
            elif self.email.get() != "" and self.match_2() == False:
                popup_window("गलत ई-मेल आईडी", "गलत ई-मेल आईडी दर्ज किया","ठीक है")
            else:

                controller.show_frame(Message_Hindi)
                getters(self.name1.get(), self.name2.get(), self.phone.get(), self.email.get(), self.info.get())
                self.name1.delete(0, 'end')
                self.name2.delete(0, 'end')
                self.phone.delete(0, 'end')
                self.email.delete(0, 'end')
                self.info.delete(0, 'end')
    def match_1(self):
        pattern = re.compile("[0-9]{10}")
        if pattern.match(self.phone.get()):
            return True
        else:
            return False

    def match_2(self):
        pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if pattern.match(self.email.get()):
            return True
        else:
            return False


class Message(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global flag
        flag = 0
        label = tk.Label(self, text="Enter the message")
        self.msg = tk.Text(self, height=15, width=50, bg="#B7CEEC")
        record = tk.Button(self, text="Record Message(30 secs)", command=lambda: self.status_change(status))
        submit = tk.Button(self, text="Submit", command=lambda: self.validate(controller))
        status = tk.Label(self, text="", bd=1, relief="sunken", anchor="w")
        label.pack()
        self.msg.pack()
        record.pack()
        submit.pack()
        status.pack(side="bottom", fill="x")


    def record(self):
        listy = setters()
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 10
        if listy[2]=="" and listy[3]!="":
            WAVE_OUTPUT_FILENAME = ""+str(listy[3])+".wav"
        elif listy[3]=="" and listy[2]!="":
            WAVE_OUTPUT_FILENAME = "" + str(listy[2]) + ".wav"
        else:
            WAVE_OUTPUT_FILENAME = "" + str(listy[3]) + ".wav"

        print (WAVE_OUTPUT_FILENAME)
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        popup_window("Done","The message is recorded","Okay")
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def validate(self,controller):
            controller.show_frame(questionaire)
            self.msg.delete(0,'end')
    def status_change(self,status):
        status.config(text="Recorded")
        time.sleep(1)
        self.record()


class Message_Hindi(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="संदेश दर्ज करें")
        self.msg = tk.Text(self, height=15, width=50, bg="#B7CEEC")
        record = tk.Button(self, text="रिकार्ड संदेश (30 सेकेंड)", command=self.record)
        submit = tk.Button(self, text="जमा करें", command=lambda: self.validate(controller))
        label.pack()
        self.msg.pack()
        record.pack()
        submit.pack()

    def record(self):
        listy = setters()
        CHUNK = 1024
        FORMAT = pyaudio.paInt16  # paInt8
        CHANNELS = 2
        RATE = 44100  # sample rate
        RECORD_SECONDS = 30
        if listy[2]=="" and listy[3]!="":
            WAVE_OUTPUT_FILENAME = ""+str(listy[3])+".wav"
        elif listy[3]=="" and listy[2]!="":
            WAVE_OUTPUT_FILENAME = "" + str(listy[2]) + ".wav"
        else:
            WAVE_OUTPUT_FILENAME = "" + str(listy[3]) + ".wav"

        print (WAVE_OUTPUT_FILENAME)
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("recording")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)  # 2 bytes(16 bits) per channel
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.popup()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    def popup(self):
        popup = tk.Tk()
        popup.wm_title("समाप्त")
        label = tk.Label(popup, text="संदेश दर्ज की गई है", pady=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(popup, text="ठीक है", command=popup.destroy)
        button.pack()
        popup.mainloop()

    def validate(self,controller):
            controller.show_frame(questionaire_Hindi)
            self.msg.delete(0,'end`')


class questionaire(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="QUESTIONNAIRE")
        condition = tk.Label(self, text="What is the present condition at ground zero?(0-SEVERE,10-GOOD)")
        con = tk.Scale(self, from_=0, to=10, orient="horizontal")
        needs = tk.Label(self, text="Basic amenities that you require ?")
        self.var1 = tk.IntVar()
        need1 = tk.Checkbutton(self, text="Food",variable=self.var1)
        self.var2 = tk.IntVar()
        need2 = tk.Checkbutton(self, text="Water", variable=self.var2)
        self.var3 = tk.IntVar()
        need3 = tk.Checkbutton(self, text="Medicines", variable=self.var3)
        self.var = tk.IntVar()
        mil = tk.Label(self, text="Military response and aid in the area ?")
        R1 = tk.Radiobutton(self, text="Satisfactory", variable=self.var, value=1)
        R2 = tk.Radiobutton(self, text="Unsatisfactory", variable=self.var, value=2)
        R3 = tk.Radiobutton(self, text="NIL", variable=self.var, value=3)
        button = tk.Button(self, text="Submit", command=lambda: controller.show_frame(StartPage))
        label.pack(anchor="w")
        condition.pack(anchor="w")
        con.pack(anchor="w")
        needs.pack(anchor="w")
        need1.pack(anchor="w")
        need2.pack(anchor="w")
        need3.pack(anchor="w")
        mil.pack(anchor="w")
        R1.pack(anchor="w")
        R2.pack(anchor="w")
        R3.pack(anchor="w")
        button.pack()


class questionaire_Hindi(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="प्रश्नावली")
        condition = tk.Label(self, text=" वर्तमान स्थिति क्या है? (0-गंभीर, 10-उपयुक्त)")
        con = tk.Scale(self, from_=0, to=10, orient="horizontal")
        needs = tk.Label(self, text="आपकी आवश्यकता अभी क्या है?")
        self.var1 = tk.IntVar()
        need1 = tk.Checkbutton(self, text="भोजन",variable=self.var1)
        self.var2 = tk.IntVar()
        need2 = tk.Checkbutton(self, text="पानी", variable=self.var2)
        self.var3 = tk.IntVar()
        need3 = tk.Checkbutton(self, text="दवाई", variable=self.var3)
        self.var = tk.IntVar()
        mil = tk.Label(self, text="सैन्य प्रतिक्रिया और इस क्षेत्र में सहायता?")
        R1 = tk.Radiobutton(self, text="संतोषजनक", variable=self.var, value=1)
        R2 = tk.Radiobutton(self, text="असंतोषजनक", variable=self.var, value=2)
        R3 = tk.Radiobutton(self, text="कुछ नहीं", variable=self.var, value=3)
        button = tk.Button(self, text="जमा करें", command=lambda: controller.show_frame(StartPage))
        label.pack(anchor="w")
        condition.pack(anchor="w")
        con.pack(anchor="w")
        needs.pack(anchor="w")
        need1.pack(anchor="w")
        need2.pack(anchor="w")
        need3.pack(anchor="w")
        mil.pack(anchor="w")
        R1.pack(anchor="w")
        R2.pack(anchor="w")
        R3.pack(anchor="w")
        button.pack()


class statistics(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Stats and Trends")
        button1 = tk.Button(self, text="Condition's Report", command= lambda: controller.show_frame(condition))
        button2 = tk.Button(self, text="Requirements Trends", command= lambda: controller.show_frame(requirements))
        button3 = tk.Button(self, text="Military Response Review", command= lambda: controller.show_frame(military))
        button4 = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        label.pack()
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()


class military(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="Pie chart representing Military Response")
        button = tk.Button(self, text="Back", command= lambda: controller.show_frame(statistics))
        f = plt.figure(figsize=(4,2.5), dpi=98, facecolor='white')
        plt.rcParams['font.size'] = 9.0
        labels = 'satisfactory', 'unsatisfactory', 'nil'
        sizes = [30, 45, 25]
        colors = ['#00C69C', '#00E28E', '#00FF80']
        explode = (0, 0, 0.3)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=150)
        plt.axis('equal')
        canvas = FigureCanvasTkAgg(f, self)
        label.pack()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.show()
        button.pack()


class requirements(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bar Graph representing Basic Requirements")
        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(statistics))
        f = plt.figure(figsize=(4, 2.5), dpi=98, facecolor='white')
        ax = f.add_subplot(111)
        data = (20, 35, 30)
        ind = numpy.arange(3)
        width = .5
        rects1 = ax.bar(ind, data, width)
        ax.set_xticks(ind + width - 0.25)
        ax.set_xticklabels(('food', 'water', 'medicines'))
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        label.pack()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        button.pack()


class condition(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button = tk.Button(self, text="Back", command=lambda: controller.show_frame(statistics))
        f = plt.figure(figsize=(4, 2.5), dpi=98, facecolor='white')
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8,9,10],[20,15,12,23,21,17,20,19,16,17])
        a.set_ylabel("no. of people", fontsize=12)
        a.set_xlabel("condition scale", fontsize=12)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        button.pack()


class send(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,text="Select a method")
        button1 = tk.Button(self,text="SMS",command=lambda : send_sms("+918826722169"))
        button2 = tk.Button(self,text="Email", command=lambda : send_email("akarshan.gandotra@gmail.com"))
        button3 = tk.Button(self,text="Back", command=lambda : controller.show_frame(StartPage))
        label.pack()
        button1.pack()
        button2.pack()
        button3.pack()


def getters(name1,name2,phone,email,additonal):
    global list
    list = []
    list.append(name1)
    list.append(name2)
    list.append(phone)
    list.append(email)
    list.append(additonal)
    print(list)


def setters():
    new_list =list
    return new_list


def popup_window(title,label,button_text):
    popup = tk.Tk()
    popup.wm_title(title)
    label = tk.Label(popup, text=label, pady=10)
    label.pack(side="top", fill="x", pady=10)
    button = tk.Button(popup, text=button_text, command=popup.destroy)
    button.pack()
    popup.mainloop()

app = One()
app.title("Opportunistic Network Interface / अवसरवादी नेटवर्क इंटरफेस")
app.mainloop()
