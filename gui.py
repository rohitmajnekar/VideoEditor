from functools import reduce
from tkinter import *
from tkinter import filedialog as fd, filedialog
from main import EditVideo
from os import path

bg_color ='#2196F3'
color_success = '#FF3D00'
FILE_NAME = ""
color_secondary = '#2196F3'

root  = Tk()
root.title("VideoEditor")
root.configure(bg = bg_color)
root.geometry('500x600')

menubar = Menu(root)
root.config(menu = menubar)


Header = Frame(root)
Header.grid(row=0, column=0,sticky=EW)
top = Label(Header, text='Enter your Cut Timings')
top.pack(fill=X)

select_video_text = StringVar()
video_duration = StringVar()
select_video_text.set("No video Selected")
selectedVideo = Label(Header, text='No video Selected', textvariable = select_video_text)
selectedVideo.pack(side=LEFT)
Label(Header, textvariable=video_duration).pack(side=LEFT)



Add_Cut_Box = Frame(root, bg= color_secondary)
Add_Cut_Box.grid(row=1, column=0)
Label(Add_Cut_Box, text= 'HH',bg= color_secondary).grid(row=0, column=1, padx=20)
Label(Add_Cut_Box, text= 'MM',bg= color_secondary).grid(row=0, column=2, padx=20)
Label(Add_Cut_Box, text= 'SS',bg= color_secondary).grid(row=0, column=3, padx=20)

fromL = Label(Add_Cut_Box, text='From',bg= color_secondary)
fromL.grid(row=1, column=0)

HH = Entry(Add_Cut_Box,width=8)
HH.grid(row=1, column=1, padx=10)
MM = Entry(Add_Cut_Box,width=8)
MM.grid(row=1, column=2, padx=10)
SS = Entry(Add_Cut_Box,width=8)
SS.grid(row=1, column=3, padx=10)

ToL = Label(Add_Cut_Box, text='To',bg= color_secondary)
ToL.grid(row=3, column=0)

HH2 = Entry(Add_Cut_Box,width=8)
HH2.grid(row=3, column=1, padx=10)
MM2 = Entry(Add_Cut_Box,width=8)
MM2.grid(row=3, column=2, padx=10)
SS2 = Entry(Add_Cut_Box,width=8)
SS2.grid(row=3, column=3, padx=10)


def addNewTiming():

    if len(HH.get()) == 0:
        HH.insert(0, '00')
    if len(MM.get()) == 0:
        MM.insert(0, '00')
    if len(SS.get()) == 0:
        SS.insert(0, '00')
    if len(HH2.get()) == 0:
        HH2.insert(0, '00')
    if len(MM2.get()) == 0:
        MM2.insert(0, '00')
    if len(SS2.get()) == 0:
        SS2.insert(0, '00')

    listbox.insert(0,(HH.get()+":"+MM.get()+":"+SS.get(), HH2.get()+":"+MM2.get()+":"+SS2.get() ))

    # reset timings
    HH.delete(0, len(HH.get()))
    MM.delete(0, len(MM.get()))
    SS.delete(0, len(SS.get()))
    # 2
    HH2.delete(0, len(HH2.get()))
    MM2.delete(0, len(MM2.get()))
    SS2.delete(0, len(SS2.get()))


Add_button = Button(Add_Cut_Box, text = "Add", command =addNewTiming , bg = '#b19cd9', fg = 'white',borderwidth =0)
Add_button.grid(row=1, column=4, padx=20, rowspan=3)

Result_Frame = Frame(root)
Result_Frame.grid(row=2, column=0)
scrollbar = Scrollbar(Result_Frame, bg = '#413C3C')
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(Result_Frame, height=20, width=80,  yscrollcommand=scrollbar.set, selectmode=EXTENDED)
scrollbar.config(command=listbox.yview)


# Functions
def onMouseWheel(event):
    scrollbar.config(command = listbox.yview)

def deleteTiming():
    try:
        listbox.delete(getActiveidx())
    except:
        print("error")
def getActiveidx():
    item= listbox.get(ACTIVE)
    return listbox.get(0, 'end').index(item)

def editTiming():
    try:

        timing = listbox.get(getActiveidx())
        HH.insert(0, timing[0][0:2])
        MM.insert(0, timing[0][3:5])
        SS.insert(0, timing[0][6:8])

        HH2.insert(0, timing[1][0:2])
        MM2.insert(0, timing[1][3:5])
        SS2.insert(0, timing[1][6:8])
        deleteTiming()
    except:
        print('error')

def openFile():
    global FILE_NAME, editorObj
    FILE_NAME = fd.askopenfilename()
    select_video_text.set('Video: "'+ str(path.basename(FILE_NAME))+ "\"")
    editorObj = EditVideo(FILE_NAME)
    video_duration.set('Duration : "' + secondsToStr(editorObj.getDuration())+ "\"")


def startEditing():
    list = listbox.get(0, 'end')
    editorObj.editVideo(list, TITLE_NAME.get(), FOLDER_NAME,isBoosted.get())

def openFolder():
    global FOLDER_NAME
    FOLDER_NAME = filedialog.askdirectory()
    folderLoc.insert(0, FOLDER_NAME)

def secondsToStr(t):
    return "%02d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(round(t*1000),),1000,60,60])

# Taskbar
submenu = Menu(menubar,tearoff = 0)
menubar.add_cascade(label = 'File', menu = submenu)
submenu.add_command(label = 'Open Folder', command = openFile)


# Delete
Button_Frame = Frame(root, bg = bg_color)
Button_Frame.grid(row=3, column=0, pady=5)

DeleteButton = Button(Button_Frame, text = 'Delete', command=deleteTiming, bg = '#BB2124', fg = 'white',borderwidth =0)
DeleteButton.pack(side= LEFT, padx= 10)
EditButton = Button(Button_Frame, text = '-Edit-', command=editTiming, bg = '#F0AD4E', fg = 'white',borderwidth =0)
EditButton.pack(side = LEFT, padx = 10)

Final_Frame = Frame(root, bg = bg_color )
Final_Frame.grid(row=4, column=0, pady=5)
Label(Final_Frame, text='FileName:',bg= color_secondary).grid(row=0, column=0, padx=4)
TITLE_NAME = Entry(Final_Frame)
TITLE_NAME.grid(row=0, column=1)
Label(Final_Frame, text='Output:', width=7,bg= color_secondary).grid(row=1, column=0, padx=4, pady=3, sticky=W)
folderLoc = Entry(Final_Frame)
folderLoc.grid(row=1, column=1)
Ouput_button = Button(Final_Frame, text = 'open', command=openFolder, bg = 'grey', fg = 'white',borderwidth =0)
Ouput_button.grid(row=1, column=3, padx=3)
isBoosted = IntVar()
checkButton = Checkbutton(Final_Frame, text='Boost volumen into 2x',bg= color_secondary,variable = isBoosted, onvalue = True, offvalue = False)
checkButton.grid(row=2, column=0, columnspan=2, sticky=EW, padx=3)
StartButton = Button(Final_Frame, text = 'Start',width=26, height=2, command=startEditing, bg = color_success, fg = 'white',borderwidth =0)
StartButton.grid(row=3, column=0, pady=8, columnspan=2)


listbox.pack()
root.mainloop()