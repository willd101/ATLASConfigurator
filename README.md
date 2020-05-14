# ATLASConfigurator
Tool to configure ATLAS constants to specific car parameters automatically. The user defines their constants in a spreadsheet, the tool then reads this, and replaces/creates a txt file, also specified by the user, which can be read by ATLAS to define its default constants.

## Why is This Useful?
ATLAS is not built to handle constantly changing between different vehicles with different parameters, especially when the majority of the channels we want to view are calculated using functions written in ATLAS. Without this tool, the only options for swapping between vehicles is to:
* Create seperate workbooks and functions for each car, with the constants defined within each function.
* Manually edit or swap between dedicated constants files for each car.

With this tool, we can build a single set of functions that will work for all the cars you wish to analyse. Additionally, each constant is only defined once rather than in each function, making it much quicker and less error prone to adjust parameters that may change even for a single car (for example centre of mass or spring rates).

The use of Excel also lets you calculate constants in the same enviroment as where you will be storing them, and allows you to perform calculations once rather than everytime you load a new layer in ATLAS (e.g. calculating Centre of Mass from Corner Weights)

## Set Up/First Use
1. Save the .exe file anywhere that is practical for you (personally, mine is on my desktop)
1. Save the example spreadsheet/create your own somewhere practical (same directory or otherwise) and remember the path. More detail on how to format the spreadsheet is below.
1. Find out the path to your ATLAS constants file. To do this:
    * Open ATLAS
    * Go to Tools -> Options-> Functions
    * In the table, look under Constants + Defaults. The path is usually something like:
      `\Documents\McLaren Electronic Systems\ATLAS 9\Config\Constants.txt`
    
    *Note that you can point Atlas to a different txt file here if you wish (e.g. if you want to keep the txt file in the same location as the spreadsheet). You should never have to edit or open the txt file, but the option is there to move it if you really want to.*
    
1. Open the ATLASConfigurator.exe tool. The first time you do this, you will have to set the paths to your spreadsheet and constants file. To do this, paste the file paths in to the respective boxes at the top.
1. Click **Update Settings**. The tool will read the sheet names of the spreadsheet you have defined and update the list below.
1. Select the car for which you wish to configure ATLAS from the list, and click **Launch**.

## Formatting your Spreadsheet
The spreadsheet is where you can add and edit parameter values for each car. While it is easy to use, it is important to follow the correct formatting for the Tool to be able to read it correctly.

To add a constant, simply write its name and value in the next available row, ensuring you follow the rules below:

* **One sheet per car**
  * Each sheet in the spreadsheet file defines a different car. The sheet name is the car's name that will be picked up in the tool.
  * To add a new car, simply create a new sheet and name it appropriately.
  
* Follow the **Name | Value | Description** Format
  * The first 2 columnns are where you must define your constants.
    * Column 1: Constant's name as it will appear in ATLAS
    * Column 2: Constant's value. Leaving the value cell blank will mean that the constant is skipped by the tool and not written to the constants txt file.
    * I also tend to add a Column 3: Optional Description of the constant.
  * No data outside the first 2 columns will be read, so feel free to use the rest of the space for notes, calculations etc.
  
* **The First Row will not be read**
  * This row should be used for headings (e.g. Name | Value | Description)  

* Naming a sheet __*TEMPLATE*__ means it will **not** be read
  * Using a template sheet is useful to track constant's names across multiple cars, and if correctly named (all uppercase) this sheet will be ignored by the tool.
