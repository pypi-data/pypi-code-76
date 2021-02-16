"""
Daniel Vogler
cdtimer - countdown timer
"""

import tkinter as tk
from tkinter import *
from tkinter import filedialog

import os

import warnings
warnings.filterwarnings("ignore", message="play FAIL sox: Sorry, there is no default audio device configured")


class CDTimer(tk.Frame):


    ### initialize
    def __init__(self,master):

        self.definitions()
        app.geometry(self.window_resolution)
        app.configure(bg=self.color_background)

        tk.Frame.__init__(self, master)
        self.master = master
        self.app_running = False
        self.sound_on = False
        self.idx = 0
        self.gui()


    ### construct window
    def gui(self):

        ### enter and set time
        self.entry = Entry(self.master, width=8, font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, relief="flat", justify='center')
        self.submit_button = Button(self.master, text="Set time", font=(self.font_type, self.font_size_button), fg=self.font_color_text, bg=self.color_background, borderwidth=0, highlightthickness=0, command = self.set_total_time )

        ### set sound frequency
        self.entry_sound = Entry(self.master, width=8, font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, relief="flat", justify='center')
        self.set_sound_button = Button(self.master, text="Set sound", font=(self.font_type, self.font_size_button), fg=self.font_color_text, bg=self.color_background, borderwidth=0, highlightthickness=0, command = self.set_sound )

        ### time display
        self.time_display = Label(self.master, text="00:00:00", font=(self.font_type, self.font_size_time_display), borderwidth=2, fg=self.font_color_time_display, bg=self.color_background)
        ### timetable display
        self.timetable_display = Label(self.master, text="", font=(self.font_type, self.font_size_tt_display), borderwidth=2, fg=self.font_color_tt_display, bg=self.color_background)
        ### set time display
        self.interval_display = Label(self.master, text="", font=(self.font_type, self.font_size_tt_display), borderwidth=2, fg=self.font_color_tt_display, bg=self.color_background)
        ### next timetable display
        self.next_timetable_display = Label(self.master, text="", font=(self.font_type, int(self.font_size_tt_display*0.5)), borderwidth=2, fg=self.font_color_tt_display, bg=self.color_background)

        ### turn sound ON/OFF
        self.sound_button = Button(self.master, text="Sound OFF", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.sound)
        ### start countdown button
        self.start_button = Button(self.master, text="Start", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.start)
        ### next and last button
        self.next_button = Button(self.master, text="Next", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.next)
        self.last_button = Button(self.master, text="Last", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.last)
        ### close window button
        self.close_button = Button(self.master, text="Close", font=(self.font_type, self.font_size_button), bg=self.color_background, fg=self.font_color_text, borderwidth=0, highlightthickness=0, command=self.master.quit)

        ### browse for timetable file
        self.browse_file = Button(self.master,text = "Browse Files", bg=self.color_background, fg=self.font_color_text,command = self.browse_files)
        self.browse_file.place(relx=0.5, rely=0.1, anchor=CENTER)
        ### layout - set time
        self.entry.place(relx=0.12, rely=0.1, anchor=CENTER)
        self.submit_button.place(relx=0.12, rely=0.2, anchor=CENTER)
        ### layout - set sound frequency
        self.entry_sound.place(relx=0.88, rely=0.1, anchor=CENTER)
        self.set_sound_button.place(relx=0.88, rely=0.2, anchor=CENTER)
        ### layout time/timetable
        self.time_display.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.timetable_display.place(relx=0.5, rely=0.65, anchor=CENTER)
        self.interval_display.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.next_timetable_display.place(relx=0.5, rely=0.95, anchor=CENTER)
        ### layout - sound on/off
        #self.sound_button.place(relx=0.7, rely=0.1, anchor=CENTER)
        self.start_button.place(relx=0.5, rely=0.2, anchor=CENTER)
        #self.close_button.place(relx=0.7, rely=0.9, anchor=CENTER)


    ### get time from entry field
    def set_total_time(self):

        self.total_time = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        parsed_time = self.entry.get().split(":")

        if len(parsed_time) == 1:
            self.seconds = int(parsed_time[-1])
        elif len(parsed_time) == 2:
            self.seconds = int(parsed_time[-1])
            self.minutes = int(parsed_time[-2])
        elif len(parsed_time) == 3:
            self.seconds = int(parsed_time[-1])
            self.minutes = int(parsed_time[-2])
            self.hours = int(parsed_time[-3])

        self.set_time = self.seconds + self.minutes*60 + self.hours*3600
        self.time = self.set_time
        print("Set time:", self.set_time)

        self.update_time_display()

        self.interval_display.configure(text='', fg=self.font_color_time_display)
        self.timetable_display.configure(text='', fg=self.font_color_tt_display)
        self.next_timetable_display.configure(text='', fg=self.font_color_tt_display)


        return self.set_time


    ### parse to hhmmss
    def time_format(self, time):

        seconds = time % 60
        minutes = ( time // 60 ) % 60
        hours = time // 3600

        time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

        return time_string


    ### browse timetable files
    def browse_files(self):

        self.tt_file = filedialog.askopenfilename(initialdir = "./",title = "Select a File",filetypes =[("CSV files", ".csv")])
        self.timetable_construction()


    ### update time display
    def update_time_display(self):

        self.time_string = self.time_format(self.time)

        if (self.set_time - self.time) % self.sound_frequency == 0 and (self.set_time - self.time) != 0 and self.sound_on:
            self.play_sound(self.sound_duration, 600)

        self.time_display.configure(text=self.time_string, fg = self.font_color_time_display)


    ### update timetable display
    def update_timetable_display(self):

        ### string for timetable display
        tt_string = str(self.tt_list[self.idx][0]+" "+self.tt_list[self.idx][1]+" #"+ self.tt_list[self.idx][2])
        ### update timetable display
        self.timetable_display.configure(text=tt_string, fg=self.font_color_tt_display)
        ### update next timetable display
        if self.idx < self.tt_list[-1][6]:
            tt_next_string = str(self.tt_list[self.idx+1][0]+" "+self.tt_list[self.idx+1][1]+" #"+ self.tt_list[self.idx+1][2])
            self.next_timetable_display.configure(text=tt_next_string, fg=self.font_color_tt_display)
        else:
            self.next_timetable_display.configure(text="Finished", fg=self.color_end)


    ### update interval time
    def update_interval_time(self):
        ### format interval time to hh:mm:ss
        self.interval_time_string = str(self.time_format(self.interval_time))
        ### check if hh can be omitted
        if self.interval_time_string.startswith("00:"):
            self.interval_time_string = self.interval_time_string[3:]

        self.interval_display.configure(text=self.interval_time_string, fg=self.font_color_time_display)


    ### start countdown
    def start(self):

        self.start_button.configure(text="Stop", command=lambda: self.stop())
        self.play_sound(self.sound_duration, 600)

        self.app_running = True
        self.update_time()


    ### next interval
    def next(self):

        if self.tt_loaded:
            self.idx += 1
            self.time = self.set_time - self.tt_list[self.idx][5]
            self.interval_time = self.tt_list[self.idx][3]
            ### update displays
            self.update_time_display()
            self.update_timetable_display()
            self.update_interval_time()


    ### last interval
    def last(self):

        if self.tt_loaded:
            self.idx -= 1
            self.time = self.set_time - self.tt_list[self.idx][5]
            self.interval_time = self.tt_list[self.idx][3] 
            ### update displays
            self.update_time_display()
            self.update_timetable_display()
            self.update_interval_time()


    ### turn sound on and off
    def sound(self):

        if self.sound_on:
            self.sound_button.configure(text="Sound OFF")
            self.sound_on = False

        elif self.sound_on == False:
            self.sound_button.configure(text="Sound ON")
            self.sound_on = True
            self.play_sound(self.sound_duration, 600)


    ### set sound signal frequency
    def set_sound(self):

        self.sound_frequency = int(self.entry_sound.get())


    ### play sound
    def play_sound(self, duration, frequency):
        if self.sound_on:
            os.system('play -n synth %s sin %s' % (duration, frequency))


    ### update time
    def update_time(self):

        if self.app_running:
            if self.time <= 0:
                self.time_display.configure(text="Finished", fg=self.color_end)
                self.start_button.configure(text="Start")
                ### time out timetable display
                self.tt_loaded = False

                if self.sound_on:
                    self.play_sound(1.0, 600)

            else:
                self.time -= 1
                self.time_display.configure(text=self.update_time_display())
                self.after(1000, self.update_time)

            ### check if new timetable interval is reached
            if self.tt_loaded:

                self.interval_time -= 1

                if (self.set_time - self.time) in self.tt_set_time:
                    ### find correct set for time stamp
                    self.idx = self.tt_set_time.index(self.set_time - self.time)
                    ### set time
                    self.interval_time = self.interval_time_total = self.tt_list[self.idx][3]
                    ### update timetable displays
                    self.update_timetable_display()
                    ###
                    self.play_sound(self.sound_duration, 600)

                self.update_interval_time()


    ### pause countdown
    def stop(self):

        self.start_button.configure(text="Start", command=lambda: self.start())
        self.app_running = False
        self.update_time


    ### read in timetable file
    def timetable_construction(self):

        from construct_timetable import read_timetable_file

        self.tt_loaded = True

        try:
            self.tt_file
        except NameError:
            print("No timetable file defined")
        else:
            print("Reading:", self.tt_file)
            ### construct time timetable
            self.tt_list, self.tt_set_time, self.set_time = read_timetable_file(self.tt_file)
            self.time = self.set_time
            ### update time display
            self.update_time_display()
            ### current set
            tt_string = str(self.tt_list[0][0]+" "+self.tt_list[0][1]+" #"+ self.tt_list[0][2])
            tt_next_string = str(self.tt_list[1][0]+" "+self.tt_list[1][1]+" #"+ self.tt_list[1][2])
            self.interval_time = self.tt_list[0][3]
            ### update interval display
            self.interval_time_string = str(self.time_format(self.interval_time))
            if self.interval_time_string.startswith("00:"):
                self.interval_time_string = self.interval_time_string[3:]
            self.interval_display.configure(text=self.interval_time_string, fg=self.font_color_time_display)
            ### update timetable display
            self.timetable_display.configure(text=tt_string, fg=self.font_color_tt_display)
            self.next_timetable_display.configure(text=tt_next_string, fg=self.font_color_tt_display)

        ### display next button
        self.next_button.place(relx=0.8, rely=0.8, anchor=CENTER)
        self.last_button.place(relx=0.2, rely=0.8, anchor=CENTER)


    ### definitions
    def definitions(self):
        self.color_background = "black"
        self.color_end = "green"
        self.font_color_time_display = "red"
        self.font_color_tt_display = "blue"
        self.font_color_text = "white"
        self.font_size_time_display = 175
        self.font_size_tt_display = 80
        self.font_size_button = 40
        self.button_borderwidth = 5
        self.window_resolution = "2500x1400"
        self.font_type = "Helvetica"
        self.sound_frequency = 3600
        self.sound_duration = 0.2
        self.tt_loaded = False


if __name__ == "__main__":
    app = Tk()
    my_gui = CDTimer(app)
    app.title("Countdown timer")
    app.mainloop()
