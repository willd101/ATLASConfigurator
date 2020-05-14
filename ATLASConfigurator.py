########################################################################################################################
# This is a (relatively) simple application to allow the user to easily set different constants in ATLAS for different
# cars by editing a spreadsheet. This app will then read those values and format them in to the txt file ATLAS uses to
# define it's constants.
#######################################################################################################################
import os
from tkinter import *
import configparser
import xlrd  # pandas is kinda shit with pyinstaller to make exe so will read spreadsheets with this instead
import sys

# ----------------------------------------------------------------------------------------------------------------------
# First of all need to set file locations for spreadsheet and ATLAS File to be replaced. This is stored in an ini file.
# ini File is located in users appdata folder.
config = configparser.ConfigParser()  # Object to parse variables in ini file
# Work out where it should be and check if it exists. If not, make it's directory and add some defaults. Else read it.
iniDir = os.getenv('appdata') + '\\ATLASConfiguratorTool\\'
iniFullFile = iniDir + 'config.ini'
if not(os.path.isdir(iniDir)):
    os.mkdir(iniDir)
if not(os.path.isfile(iniFullFile)):
    config.add_section('FilePaths')
    config['FilePaths']['UserXLFile'] = 'Enter\\Path\\To\\Spreadsheet.xlsx'
    config['FilePaths']['ATLASConstants'] = 'Enter\\Path\\To\\ATLAS\\Constants.txt'
else:
    config.read(iniFullFile)

XLFile = config['FilePaths']['UserXLFile']
ATLASConstantFile = config['FilePaths']['ATLASConstants']

# ----------------------------------------------------------------------------------------------------------------------
# Now that we have those we can try to get a car list from the Excel File. Make it a function to use in the GUI too.


def get_car_choices(XLFn):
    """Attempts to return sheet names from Excel File, along with success/fail message to display in GUI."""
    try:
        XL = xlrd.open_workbook(XLFn)
        cars = XL.sheet_names()
        if cars.count('TEMPLATE'):  # If there is a template sheet, remove it
            cars.remove('TEMPLATE')
        msg = 'Loaded Successfully from Excel'
    except:
        cars = []
        msg = 'Could not load XL File'

    return cars, msg


[Cars, loadmsg] = get_car_choices(XLFile)

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Start Building the GUI : Boring set up stuff
root = Tk()
root.minsize(800, 400)
root.title("ATLAS Configurator")

# Set the app icon. Will be in different location between exe and py files
IconFile = 'images\\tyreClipArt.ico'
if getattr(sys, 'frozen', False):
    IconPath = sys._MEIPASS  #Temp folder set up by pyinstaller
else:
    IconPath = os.path.abspath('.') #
try:
    root.iconbitmap(os.path.join(IconPath, IconFile))
    print('Set icon to\n{}'.format(IconPath + '\\' + IconFile))
except:
    print("Could not find icon file from:\n{}\n".format((IconPath + '\\' +IconFile)) +
          "Hopefully you're running the source code, else I've fk'd up the exe distribution")

# Column 1 (Text boxes) will expand with window resizing
root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- File Location Text Boxes
XLLabel = Label(root, text='Excel File')
XLEntry = Entry(root)
XLEntry.insert(0, XLFile)
XLLabel.grid(row=0, column=0, sticky='E')
XLEntry.grid(row=0, column=1, sticky=W+E)

ATLASLabel = Label(root, text='ATLAS Constants File')
ATLASEntry = Entry(root)
ATLASEntry.insert(0, ATLASConstantFile)
ATLASLabel.grid(row=1, column=0, sticky='E')
ATLASEntry.grid(row=1, column=1, sticky=W+E)

# ----------------------------------------------------------------------------------------------------------------------
# Create an info message displaying if a Car List was found or not
XLMessageLabel = Label(root)


def UpdateLoadMessage(msg):
    """Updates message on screen with msg from get_car_choices"""
    XLMessageLabel['text'] = msg


UpdateLoadMessage(loadmsg)
XLMessageLabel.grid(row=3,columnspan=2)

# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------- Add the Main Selection List of Car Choices, and make it scrollable
CarListBox = Listbox(root, height=10)
for car in Cars:
    CarListBox.insert(END, car)
CarListBox.grid(row=5, columnspan=2)

CarLBScrollbar = Scrollbar(root)
CarListBox.config(yscrollcommand=CarLBScrollbar.set)
CarLBScrollbar.grid(row=5, column=2, sticky=N+S)
CarLBScrollbar.config(command=CarListBox.yview)

# -------------------------------------- Add Button above it to update List contents from XL file specified.
def UpdateListBox():
    """
    Updates based on User Inputs:
        global variables for file paths and "Cars" List
        ini File settings
        list in GUI
    """
    global XLFile, ATLASConstantFile, config, Cars

    XLFile = XLEntry.get()
    ATLASConstantFile = ATLASEntry.get()

    config['FilePaths']['UserXLFile'] = XLFile
    config['FilePaths']['ATLASConstants'] = ATLASConstantFile
    with open(iniFullFile, 'w') as f:
        config.write(f)

    CarListBox.delete(0, END)
    [Cars, msg] = get_car_choices(XLFile)
    for car in Cars:
        CarListBox.insert(END, car)
    UpdateLoadMessage(msg)


UpdateButton = Button(root, text='Update Settings', command=UpdateListBox)
UpdateButton.grid(row=4, columnspan=2)

# ----------------------------------------------------------------------------------------------------------------------
# Finally, create button that will overwrite ATLASConstantsFile with car specific config and then launch ATLAS


def ConfigureATLAS(Car, XLFn, ATLASConstantsFile):
    """
    read constants, format in to txt file, copy to ATLAS location
    """
    # Read Excel Sheet
    xlfile = xlrd.open_workbook(XLFn)
    sheet = xlfile.sheet_by_name(Car)
    data = {'Name': sheet.col_values(0)[1:], 'Value': sheet.col_values(1)[1:]}  # Row 1 contains headers
    for i, name in enumerate(data['Name']):
        print(name, data['Value'][i])

    # Format in to string for txt file by building up string line by line
    string = ''
    for i in range(len(data['Name'])):
        if not data['Value'][i] == '':  # xlrd will return empty string if the cell is empty.
            string = string + data['Name'][i] + '\t' + str(data['Value'][i]) \
                     + '\n'
        else:
            print('Skipping {}'.format(data['Name'][i]))

    f = open('Constants.txt', 'w+')
    f.write(string)
    f.close()

    # Replace Constants File + Open ATLAS
    if os.path.isfile(ATLASConstantsFile):
        os.remove(ATLASConstantsFile)
    os.rename('Constants.txt', ATLASConstantsFile)


def LaunchButtonProcess():
    # global XLFile, ATLASConstantFile
    IDCar = CarListBox.curselection()  # Returns tuple of currently selected list element
    ConfigureATLAS(Cars[IDCar[0]], XLFile, ATLASConstantFile)
    root.destroy()  # GUI needs to close before calling os.system(), as this command does not end until ATLAS is closed.
    print(('-' * 40) + '\nYou can now close this window, or it will close when ATLAS is closed')
    fail = os.system('ATLAS.exe')
    if fail:  # os.system returns 1 if it cannot complete the command. Most likely becuase ATLAS.exe is not found on
        # PATH. Therefore show a little popup msg explaining the situation.
        msg = 'ATLAS has been configured correctly, however subsequently could not be opened by the tool.\n' +\
            'Please open manually. To fix, ensure the file ATLAS.exe is on your system PATH'

        popup = Tk()
        popup.title('Could not open ATLAS')
        popup.iconbitmap(os.path.join(IconPath, IconFile))

        label = Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command=popup.destroy)
        B1.pack()

        popup.mainloop()


LaunchButton = Button(root, text='Launch', command=LaunchButtonProcess)
LaunchButton.grid(row=6, columnspan=2)

# ----------------------------------------------------------------------------------------------------------------------
# Launch the finished GUI
root.mainloop()

