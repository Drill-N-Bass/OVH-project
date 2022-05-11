#!/usr/bin/env python
# coding: utf-8

# # About "OVH test raw db GUI"
# 
# This simple program will be used as a tool for preparing statistical analysis of set of data from disks.

# =============================================================================
# Each entry of the data set consists of following fields separated by ;
# character:
# 
#     datacenter
#     hostname
#     disk serial
#     disk age (in s)
#     total reads
#     total writes
#     average IO latency from 5 minutes (in ms)
#     total uncorrected read errors
#     total uncorrected write errors
# =============================================================================

# =============================================================================
# The proper solution (a script in Python) should output following
# information on the GUI's output window:
#     
# - Additional test that will compare the reference database to the selected one
# 
# - How many disks are in total and in each DC
# 
# - Which disk is the youngest/oldest one and what is its age (in days)
# 
# - What's the average disk age per DC (in days)
# 
# - How many read/write IO/s disks processes on average
# 
# - Find top 5 disks with lowest/highest average IO/s (reads+writes, print disks and their avg IO/s)
# 
# - Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter)
# 
# - There should also be tests that verify if parts of the script are processing data properly.
# 
# =============================================================================


# The functionalities:
# 1. The program will read selected file in raw format.
# 2. Then convert it to `Pandas` version.
# 3. Then it will check if the data is clean by comparing the data to reference data frame
# 4. Then it will display the output with all informations needed (mentioned in the solution part - above)
# 5. There will be a feature to save this output to txt file. 


# The first two steps will be done below:

# =============================================================================
# Part 1:
# Processing input data
# =============================================================================

import numpy as np
import pandas as pd

# Testing modules:
from pandas import testing as tm
from pandas.testing import assert_frame_equal

# Needed for display log with the error exeption function:
# https://realpython.com/the-most-diabolical-python-antipattern/
import logging

# Need for print an error message without printing a traceback and close the program when a condition is not met:
# https://stackoverflow.com/questions/17784849/print-an-error-message-without-printing-a-traceback-and-close-the-program-when-a
import sys

import tkinter as tk
import tkinter.font as font

# import filedialog module
from tkinter import filedialog

# https://stackoverflow.com/questions/33139451/print-big-words-on-console-using-python-bit-by-bit
#!pip install art
from art import *

# Let's go!

#global root
root = tk.Tk()
root.geometry("1770x870") # "1740x850"
root.columnconfigure(0, weight=3)
root.rowconfigure(0, weight=3)
# https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter/51592104
def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   

root.title('OVH test raw GUI')

content = tk.Frame(root)
content.configure(bg='LightCyan2')


content.columnconfigure(0, weight=8)
content.columnconfigure(1, weight=8)
content.columnconfigure(2, weight=8)
content.columnconfigure(3, weight=8)
content.columnconfigure(4, weight=8)

content.rowconfigure(0, weight=8)
content.rowconfigure(1, weight=8)
content.rowconfigure(2, weight=8)
content.rowconfigure(3, weight=8)
content.rowconfigure(4, weight=8)
content.rowconfigure(5, weight=8)
content.rowconfigure(6, weight=8)
content.rowconfigure(7, weight=8)
content.rowconfigure(8, weight=8)
content.rowconfigure(9, weight=8)

# =============================================================================
# Button's font pattern:
# =============================================================================

font_button_big = font.Font(family='Helvetica', size="11", weight='bold')
font_button_small = font.Font(family='Helvetica', size="10", weight='bold')

# =============================================================================
# Creating a "File Explorer" feature:
# =============================================================================

# https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
# Function for opening the
# file explorer window



def browseFiles():
    filename = (
            filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File in raw format",
                                          filetypes = (("Text files",
                                                        "*.raw*"),
                                                       ("all files",
                                                        "*.*")))
    )
    
    

    with open('reference_data/reference_data.raw', 'r') as file1:
        data_ovh_reference_version = pd.read_csv(
            file1,
            sep=";",
            header=None
        )
    
    # creating test file - which is not prefiltered for further analysis:
    with open(filename, 'r') as file2:
        data_ovh_test_case = pd.read_csv(
            file2,
            sep=";",
            header=None
        )
    
    col_names_list = [
    'data_ovhcenter', 
    'hostname', 
    'disk serial', 
    'disk age (in s)', 
    'total reads', 
    'total writes', 
    'average I O latency from 5 minutes (in ms)', 
    'total uncorrected read errors', 
    'total uncorrected write errors']

    # Camel sase for tittles in columns:
    col_names_list = [
        n.title().replace(' ', '') 
        for n in col_names_list
    ]
    # print(col) # test
    
    data_ovh_reference_version.columns = col_names_list
    data_ovh_test_case.columns = col_names_list
    
    # data_ovh_reference_version.head()
    
# =============================================================================
#     Testing modules:
# =============================================================================
    count_ok_test = 0
    
    
    # Test 1: Check that left and right Index are equal.
    
    data_ovh_reference_version_index = data_ovh_reference_version.index
    data_ovh_test_case_index = data_ovh_test_case.index
    
    try:
        tm.assert_index_equal(data_ovh_reference_version_index, data_ovh_test_case_index)
        test_output1 = "Test 1 - Check that left and right Index are equal: Test OK" 
        count_ok_test += 1
    except AssertionError as ae:
        sys.tracebacklimit = 0
        logging.exception(
            'Caught an error [in code used: except AssertionError]',
            '\n',
            'Check that left and right Indexes are equal. Comparison between the reference data frame and a new one.' + str(ae))
        test_output1 =(
                    'Test 1 - Check that left and right Index are equal:\n Caught an possible error [in code used: except AssertionError]'
                    + '\n'
                    + "Check that left and right Indexes are equal:\n Comparison between the reference data frame and a new one.\n They are not equal, but this fact doesn't block further analysis."
                    + str(ae)
                    )
    
     # print(tm.assert_index_equal(data_ovh_reference_version_index, data_ovh_test_case_index))
    
#     Test 2:
#     Checking dtypes of each column in both data frames:
    
    try:
        # Comparing same index in 2 lists:
        data_ovh_reference_version_dtypes_list =  list(data_ovh_reference_version.dtypes)
        data_ovh_test_case_dtypes_list = list(data_ovh_test_case.dtypes)

        res1 = [i == j for i, j in zip(data_ovh_reference_version_dtypes_list, data_ovh_test_case_dtypes_list)]

        #convert bools to strings:
        res12 = [str(i) for i in res1]

        # Finding an index of the faulty columns:

        list_of_faulty_dtypes = []

        for i in range(len(res12)):
            if res12[i] == 'False':
                list_of_faulty_dtypes.append(i)

        if not list_of_faulty_dtypes:
            test_output2 = "Test 2 - Checking dtypes of each column in both data frames: Test OK"
            count_ok_test += 1
        else:
            list_of_faulty_printed = [i for i in list(data_ovh_test_case.columns[list_of_faulty_dtypes])]
            list_of_faulty_printed_to_string = (' ' + '\n').join(map(str, list_of_faulty_printed))

            raise ValueError('columns ', data_ovh_test_case.columns[list_of_faulty_dtypes], 'are in wrong dtype format.') 
#            test_output2 = 'Test 2 - Checking dtypes of each column in both data frames: uncorrect dtype in column(s): ', list_of_faulty_printed
           
    except ValueError as ve:
        sys.tracebacklimit = 0
        logging.exception(
        'Caught an error [in code used: except AssertionError]',
        '\n',
        'Check that left and right Indexes are equal. Comparison between the reference data frame and a new one.'
            + str(ve)
        )
        test_output2 = ('Test 2 - Checking dtypes of each column in both data frames: uncorrect dtype in column(s): '
                        + '\n\n'
                        + list_of_faulty_printed_to_string
                        )
        
     # print(list(data_ovh_test_case.columns[list_of_faulty_dtypes]))
    
       
#     Test 3: Check for NaN under an entire DataFrame (there shouldn't be any):
        
        
    try:
        if data_ovh_test_case.isnull().values.any() == False:
            test_output3 = "Test 3 - Check for NaN under an entire DataFrame (there shouldn't be any missing values nor NaN's): Test OK"
            count_ok_test += 1
        else:
            raise ValueError(
                "Missing values in the data frame, of NaNs, were detected! Dataframe isn't prepared for further analysis!"
            )
    except ValueError as ve:
        sys.tracebacklimit = 0
        logging.exception(
            "Missing values in the data frame, of NaNs, were detected! Dataframe isn't prepared for further analysis!"
            + str(ve)
        )
     
        test_output3 = (
                "Test 3 - Check for NaN under an entire DataFrame (there shouldn't be any):\n Missing values in the data frame, of NaNs, were detected! Dataframe isn't prepared for further analysis!"
                + str(ve)
                )
        
    
    # Test 4: 
    # looking for correct strings in `Data_Ovhcenter` and `hostname` columns.
    
    
    mask = data_ovh_test_case['Data_Ovhcenter'].str.contains('^dc-').all()
    mask1 = data_ovh_test_case['Hostname'].str.contains('.storage.ovh$').all()
    mask2 = data_ovh_test_case['Hostname'].str.contains('^host').all()
    
    if mask != False and mask1 != False and mask2 != False:
        test_output4 = "Test 4 - looking for correct strings in `Data_Ovhcenter` and `hostname` columns:\n all ok with string consistency of the columns: 'Data_Ovhcenter' and 'Hostname'. Test: OK"
        count_ok_test += 1
    elif mask == False and mask1 != False and mask2 != False:
        test_output4 = "Test 4 - looking for correct strings in `Data_Ovhcenter` and `hostname` columns:\n Some string(s) in 'Data_Ovhcenter' column is/are corrupted. Clean the data before further processing"
    elif mask != False and (mask1 == False or mask2 == False):
        test_output4 = "Test 4 - looking for correct strings in `Data_Ovhcenter` and `hostname` columns:\n Some string(s) in 'Hostname' column is/are corrupted. Clean the data before further processing"
    else:
        test_output4 = "Test 4 - looking for correct strings in `Data_Ovhcenter` and `hostname` columns:\n Some string(s) in 'Data_Ovhcenter' and'Hostname' column is/are corrupted. Clean the data before further processing"



# =============================================================================
# Establish all pandas calculations:
# =============================================================================
    if count_ok_test == 4:
        data_ovh_test_case.shape
        
        
        # In[3]:
        
        
        data_ovh_test_case.info()
        
        
        # Our data in the `data_ovh_test_case` data frame has 25000 entries (rows). 
        # 
        # Three columns are object types and have strings. 
        # 
        # Six columns have `int64` - in our case integers.
        # 
        # 
        # ---------------------------------------------------------
        # 
        
        # In[4]:
        
        ##
        data_ovh_test_case.describe()
        
        
        # In[5]:
        
        
        data_ovh_test_case.describe(include='all')
        
        
        # In[6]:
        
        
        """
        with `.isnull()` function I can check a scalar or 
        array-like object and indicates whether values are missing 
        (NaN in numeric arrays, 
        None or NaN in object arrays, 
        NaT in datetimelike)
        
        with `.any()` function 
        I can check for any instance in the whole df
        """
        data_ovh_test_case.isnull().any()
        
        
        # ##### Data analysis and cleaning: conclusion
        # 
        # As the data looks consistent, as evidenced by the fact that:
        # - `data_ovh_test_case.isnull ()` showed that we do not have empty fields
        # - `data_ovh_test_case.describe (include = 'all')` and data_ovh_test_case.describe () showed that we do not have outliners
        # 
        # In fact, the data itself has errors, as evidenced by the fact that it has the columns `TotalUncorrectedReadErrors` and` otalUncorrectedWriteErrors`. However, these are errors that were foreseen by the creator of this database. As the values in the columns mentioned are also consistent, I can go to the next part.
        
        # 
        # --------------------------------------
        # Since some tasks can be solved faster than others, and the very fact of data analysis gives fragments of answers, let me focus on what comes effortlessly in the first place.
        # 
        # I'll start with the quests: 
        # - **"How many read/write IO/s disks processes on average"**
        # - **"Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter)"**
        # 
        # ----------
        # 
        
        # ### How many read/write IO/s disks processes on average:
        # 
        # In order to find out how many read / write IO / s disks processes on average I will use the `df.describe ()` method. Additionally, I will do it on the new data frame: `data_ovh_test_case_r_w_io_per_s_avg`, which will only contain the columns that are relevant for this task.
        
        # In[7]:
        
        
        """
        "How many read/write IO/s disks processes on average":
        """
        
        data_ovh_test_case_r_w_io_per_s_avg = data_ovh_test_case[
            ['TotalReads',
             'TotalWrites',
             'AverageIOLatencyFrom5Minutes(InMs)']
        ]
        
        data_ovh_test_case_r_w_io_per_s_avg.describe()
        
        
        # As we can see on avarage there is:
        # 
        # - For `TotalReads` **1.597572e+09**.
        # - For `TotalWrites` **6.403327e+08**.
        # - For **IO/s** in `AverageIoLatencyFrom5Minutes(InMs)` **14.503040** **Ms**.
        # 
        # ------------
        
        # ### Find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter):
        # 
        # In order to find disks which are most probably broken, i.e. have non-zero uncorrected errors (print disks and error counter) I will use boolean indexing.
        # 
        # As we can read on [geeksforgeeks.org](https://www.geeksforgeeks.org/boolean-indexing-in-pandas/):
        # 
        # *In boolean indexing, we will select subsets of data based on the actual values of the data in the DataFrame and not on their row / column labels or integer locations. In boolean indexing, we use a boolean vector to filter the data*
        
        # In[8]:
        
        
        """
        Find disks which are most probably broken, 
        i.e. have non-zero uncorrected errors (print disks and error counter):
        """
        
        data_ovh_test_case_errors_ture = (
            data_ovh_test_case['TotalUncorrectedReadErrors'] != 0
        )
        
        print(data_ovh_test_case_errors_ture.value_counts())
        print("\n", "\n")
        
        data_ovh_test_case_errors_tuwe = (
            data_ovh_test_case['TotalUncorrectedWriteErrors'] != 0
        )
        
        print(data_ovh_test_case_errors_tuwe.value_counts())
        
        
        # as we can see on 25,000 rows there are:
        # 
        # - For `TotalUncorrectedReadErrors`  **===> 2 errors**
        # - For `TotalUncorrectedWriteErrors` **===> 6 errors**
        
        # Disks that have `TotalUncorrectedReadErrors`:
        
        # In[9]:
        
        
        data_ovh_test_case[data_ovh_test_case_errors_ture][['DiskSerial', 'TotalUncorrectedReadErrors']]
        
        
        # Disks that have `TotalUncorrectedWriteErrors`:
        
        # In[10]:
        
        
        data_ovh_test_case[data_ovh_test_case_errors_tuwe][['DiskSerial', 'TotalUncorrectedWriteErrors']]
        
        
        # ### How many disks are in total and in each DC:
        # 
        # **How many disks are in each DC:**
        # 
        # Because I assume that all disk serials are unique I can solve this task by grouping `DC`: `Data_Ovhcenter` column. Using the `size()` function I can count the instances for all disks at once.
        
        # In[11]:
        
        
        """
        Just in case I will check do we have unique disk serials:
        """
        a = data_ovh_test_case['DiskSerial']
        a.is_unique
        
        
        # In[12]:
        
        
        """
        Because each disk that I can find, will always has a unique serial number
        I can check how many disks are in each DC using just `df.groupby()` with
        the `size()` function. 
        The `size()` function will point out serial instances for each DC group.
        """
        
        data_ovh_test_case_disks_per_DC = (
            data_ovh_test_case.groupby('Data_Ovhcenter')
            .size()
        )
        
        data_ovh_test_case_disks_per_DC = (
            data_ovh_test_case_disks_per_DC
            .sort_values(ascending=True)
        )
        
        data_ovh_test_case_disks_per_DC
        
        
        # #### Before we jump to a conclusion about this data:
        # 
        # At this point, I realized that I don't know - once again - what's the purpose of this analysis (fuzzy logic). If the output data is needed for further computing, processing etc. Then, it's fine, output data are enough. But if someone wants to analyse those data, then it would be better to present them in a more human-readable format. It is important because in this manner there is easier to understand data and find some hidden patterns. More about this can be found [here](https://en.wikipedia.org/wiki/Principles_of_grouping) and [here](https://en.wikipedia.org/wiki/Gestalt_psychology).
        # 
        # That's why I decided to implement plots using `Matplotlib` library.
        # 
        # ##### One more, "before", we start:
        # 
        # If I wanted to publish the data visualizations I create, I need to be mindful of people having [**colour blindness**](https://en.wikipedia.org/wiki/Color_blindness). Thankfully, there are colour palettes I can use that are friendly for people with colour blindness. One of them is called [Color Blind 10](http://tableaufriction.blogspot.com/2012/11/finally-you-can-use-tableau-data-colors.html) and was released by Tableau, the company that makes the data visualization platform of the same name.
        # 
        # **The Data-Ink concept** 
        # 
        # Data-ink is the non-erasable ink used for the presentation of data. If data-ink would be removed from the image, the graphic would lose the content. Non-Data-Ink is accordingly the ink that does not transport the information but is used for scales, labels and edges. The data-ink ratio is the proportion of Ink that is used to present actual data compared to the total amount of ink (or pixels) used in the entire display. 
        # 
        # Non-data ink includes any elements in the chart that don't directly display data points. This includes tick markers, tick labels, and legends. Data ink includes any elements that display and depending on the data points underlying the chart. In a line chart, the data-ink would primarily be the lines and in a scatter plot, the data-ink would primarily be in the markers. As I increase the data-ink ratio, I decrease non-data ink that can help a viewer understand certain aspects of the plots. I need to be mindful of this trade-off as I work on making the appearance of plots to tell a story because plots I create could end up telling the wrong story.
        # 
        # This principle was originally set forth by [Edward Tufte](https://en.wikipedia.org/wiki/Edward_Tufte), a pioneer in the field of data visualization. Tufte's first book, **The Visual Display of Quantitative Information**, is considered a bible among information designers.
        # 
        # 
        # ![SegmentLocal](data-ink.gif "Non-data ink")
        # 
        # “Graphical excellence is that which gives to the viewer the greatest number of ideas in the shortest time with the least ink in the smallest space.”
        #                                                                                                      Edward Tufte
        
        # In[13]:
        
        #
        # # let's do a plot:
        # fig1, ax = plt.subplots(figsize=(15,4))
        #
        # """
        # The axis is drawn as a unit, so the effective zorder for drawing
        # the grid is determined by the zorder of each axis,
        # not by the zorder of the Line2D objects comprising the grid.
        # Therefore, to set grid zorder, use set_axisbelow or,
        # for more control, call the set_zorder method of each axis.
        #
        # Inspiration from:
        # https://stackoverflow.com/questions/31506361/grid-zorder-seems-not-to-take-effect-matplotlib
        # """
        # ax.set_axisbelow(True)
        #
        # """
        # for the sake of using colours from the colour-blind page:
        # http://tableaufriction.blogspot.com/2012/11/finally-you-can-use-tableau-data-colors.html
        # I need to convert int to float between 0 and 1 for RGB values like 174.199.232 (blue colour).
        # The value 174.199.232 is from the mentioned page.
        # It is so because matplotlib needs it in such a format.
        #
        # Inspired from:
        # https://stackoverflow.com/questions/41643189/plotting-just-a-single-rgb-color-in-matplotlib
        # """
        # ax = data_ovh_test_case_disks_per_DC.plot.bar(
        #     fontsize=15,
        #     zorder=1,
        #     color=(174/255, 199/255, 232/255)
        # ) # 'zorder' is bar layaut order
        #
        # """
        # Below is a for loop for displaying values above their respective bars.
        #
        # Inspiration from:
        # https://stackoverflow.com/questions/63146552/how-do-i-display-these-values-above-their-respective-bars-on-this-bar-chart-with
        # """
        # for p in ax.patches:
        #     ax.annotate(s=p.get_height(),
        #                 xy=(p.get_x()+p.get_width()/2.,
        #                     p.get_height()
        #                    ),
        #                 ha='center',
        #                 va='center',
        #                 xytext=(0, 10),
        #                 textcoords='offset points')
        #
        #
        # ax.spines["right"].set_visible(False)
        # ax.spines["left"].set_visible(False)
        # ax.spines["top"].set_visible(False)
        # ax.spines["bottom"].set_visible(False)
        #
        # ax.set_title(
        #     'How many disks are in total and in each DC:',
        #     fontsize=50
        # )
        #
        # ax.set_xticklabels(
        #     data_ovh_test_case_disks_per_DC.index,
        #     rotation=34.56789,
        #     fontsize='xx-large'
        # ) # We will set xticklabels in angle to be easier to read)
        # # The labels are centred horizontally, so when we rotate them 34.56789°
        #
        # ax.grid(axis='y', zorder=0) # 'zorder' is bar layaut order
        #
        # plt.ylim([4500, 5300])
        #
        # plt.show()
        
        
        # As we can see:
        # - `dc-tug` has the lowest quantity of drives, having **4549** units
        # - `dc-tur` has the highest quantity of drives, having **5240** units
        # 
        # --------
        # 
        
        # **How many disks are in total:**
        # 
        # Because each disk that I can find, will always has a unique serial number, in consequence, row numbers will be equal to the number of disks. Besides the fact that at the beginning I compute it with `df.describe()` function. I will print below the 
        
        # In[14]:
        
        
        data_ovh_test_case_disks_per_DC.sum()
        
        
        # ----------------------
        # ### Which disk is the youngest/oldest one and what is its age (in days):
        # 
        # To solve this task I will use `pandas` Series.min and Series.max methods.
        # Because I need to know the output in days, instead of seconds, I will divide the output by 86400 which is 24 hours multiplied by 60 seconds multiplied by 60 minutes. I.e. seconds * minutes * hours = day.
        
        # In[15]:
        
        
        # #test:
        # print("data_ovh_test_case['DiskAge(InS)'].min() ====>", data_ovh_test_case['DiskAge(InS)'].min())
        
        youngest_drive_age = (
            data_ovh_test_case['DiskAge(InS)']
            .min() 
            / 86400 # conversion from sec to days
        )
        
        print(
            "`youngest_drive_age` has:",
            round(youngest_drive_age,4),
            "days"
        )
        
        
        # In[16]:
        
        
        # #test:
        # print("data_ovh_test_case['DiskAge(InS)'].max() ====> ", data_ovh_test_case['DiskAge(InS)'].max())
        
        oldest_drive_age = (
            data_ovh_test_case['DiskAge(InS)']
            .max()
            / 86400 # conversion from sec to days
        )
        
        print(
            "`oldest_drive_age` has:",
            round(oldest_drive_age, 4),
            "days"
        )
        
        
        # In[17]:
        
        
        youngest_drive_val = data_ovh_test_case['DiskAge(InS)'].min()
        oldest_drive_val = data_ovh_test_case['DiskAge(InS)'].max()
        
        youngest_drive = data_ovh_test_case.loc[
            data_ovh_test_case['DiskAge(InS)'] == youngest_drive_val,
            ['DiskSerial']
        ]
        
        oldest_drive = data_ovh_test_case.loc[
            data_ovh_test_case['DiskAge(InS)'] == oldest_drive_val,
            ['DiskSerial']
        ]
        
        younges_oldest_drives = pd.concat(
            [youngest_drive, oldest_drive],
            keys=['youngest drive', 'oldest drive'],
            names=['type', 'Index']
        )
        
        """
        At this point, it would be nice to have one index, 
        so I need to reshape the multi-index.
        
        Inspiration from:
        https://stackoverflow.com/questions/20110170/turn-pandas-multi-index-into-column
        """
        younges_oldest_drives = younges_oldest_drives.reset_index()  
        
        """
        I need to first `round()` values before I will convert them to `int`. 
        Without that the value will be rounded less accurate.
        """
        
        younges_oldest_days_list = [
            round(youngest_drive_age, 0),
            round(oldest_drive_age, 0)
        ]
        
        younges_oldest_drives['age (in days)'] = younges_oldest_days_list
        
        younges_oldest_drives['age (in days)'] = (
            younges_oldest_drives['age (in days)']
            .astype(int)
        )
        
        younges_oldest_drives
        
        
        # In[18]:
        
        
        print("2074 days it's", round(oldest_drive_age / 365, 2), "years")
        
        
        # As we can see, the difference between the youngest and the oldest disc is significant.
        # When averaging the result over the days, the difference between the disks is 2,074 days.
        # It's more than five and a half years: **5.68** years.
        # 
        # Youngest drive has index: `5899`, serial number: **`WHEJNKGW99`** and less than one day running.
        # 
        # Oldest drive has index: `14418 	`, serial number: **`HBWRKAXG18`** and `2074` days.
        
        # ### What's the average disk age per DC (in days)
        # 
        # This case is similar to previous: *How many disks are in total and in each DC*. I will use `df.groupby()` function too.
        # 
        # After that I will create a new **series** called `disk_avg_age` from this grouped **data frame** called `data_ovh_test_case_grouped`, I will use it for further computing with the `Series.mean()` function on 'DiskAge(InS)' column. 
        # 
        # Finally, `disk_avg_age` series will output the mean disk age, rounded with `round()` function and convert from seconds to days, thanks for my previous approach. 
        
        # In[19]:
        
        
        data_ovh_test_case_grouped = data_ovh_test_case.groupby('Data_Ovhcenter')
        
        # data_ovh_test_case_grouped.head() # Test
        
        disk_avg_age = round(
            data_ovh_test_case_grouped['DiskAge(InS)'].mean() / 86400,
            0
        ) # conversion from sec to days
        
        disk_avg_age = (
            disk_avg_age
            .sort_values(ascending=True)
            .astype(int)
        )
        
        disk_avg_age
        
        
        # In[20]:
        
        #
        # # let's do a plot:
        # fig2, ax = plt.subplots(figsize=(15,4))
        #
        # """
        # The axis is drawn as a unit, so the effective zorder for drawing
        # the grid is determined by the zorder of each axis,
        # not by the zorder of the Line2D objects comprising the grid.
        # Therefore, to set grid zorder, use set_axisbelow or,
        # for more control, call the set_zorder method of each axis.
        #
        # Inspiration from:
        # https://stackoverflow.com/questions/31506361/grid-zorder-seems-not-to-take-effect-matplotlib
        # """
        # ax.set_axisbelow(True)
        #
        # """
        # for the sake of using colours from the colour-blind page:
        # http://tableaufriction.blogspot.com/2012/11/finally-you-can-use-tableau-data-colors.html
        # I need to convert int to float between 0 and 1 for RGB values like 255.187.120 (orange colour).
        # The value 174.199.232 is from the mentioned page.
        # It is so because matplotlib needs it in such a format.
        #
        # Inspired from:
        # https://stackoverflow.com/questions/41643189/plotting-just-a-single-rgb-color-in-matplotlib
        # """
        # ax = disk_avg_age.plot.bar(
        #     fontsize=15,
        #     zorder=1,
        #     color=(255/255, 187/255, 120/255)
        # ) # 'zorder' is bar layaut order
        #
        #
        # """
        # Below is a for loop for displaying values above their respective bars.
        #
        # Inspiration from:
        # https://stackoverflow.com/questions/63146552/how-do-i-display-these-values-above-their-respective-bars-on-this-bar-chart-with
        # """
        # for p in ax.patches:
        #     ax.annotate(s=p.get_height(),
        #                 xy=(p.get_x()+p.get_width()/2.,
        #                     p.get_height()
        #                    ),
        #                 ha='center',
        #                 va='center',
        #                 xytext=(0, 10),
        #                 textcoords='offset points'
        #                )
        #
        # ax.spines["right"].set_visible(False)
        # ax.spines["left"].set_visible(False)
        # ax.spines["top"].set_visible(False)
        # ax.spines["bottom"].set_visible(False)
        #
        # ax.set_title(
        #     "What's the average disk age per DC (in days)",
        #     fontsize=50
        # )
        #
        # ax.set_xticklabels(
        #     data_ovh_test_case_disks_per_DC.index,
        #     rotation=34.56789,
        #     fontsize='xx-large'
        # ) # We will set xticklabels in angle to be easier to read)
        # # The labels are centred horizontally, so when we rotate them 34.56789°
        #
        # ax.grid(axis='y', zorder=0) # 'zorder' is bar layaut order
        #
        # plt.ylim([720, 745])
        #
        # plt.show()
        
        
        # ### Find the top 5 disks with the lowest/highest average IO/s (reads+writes, print disks and their avg IO/s):
        # 
        # For this task, I can use `nsmallest()` and `nlargest()` functions on `AverageIOLatencyFrom5Minutes(InMs)` column. Additionally, I will pass `5` argument inside each function, to find all the top 5 disks from both categories: highest and lowest.
        
        # In[21]:
        
        
        top_five_io_hi = (
            data_ovh_test_case['AverageIOLatencyFrom5Minutes(InMs)']
            .nlargest(5)
        )
        top_five_io_hi
        
        
        # In[22]:
        
        
        top_five_io_lo = (
            data_ovh_test_case['AverageIOLatencyFrom5Minutes(InMs)']
            .nsmallest(5)
        )
        top_five_io_lo
        
        
        # In[23]:
        
        
        """
        I will use `.index` method, 
        because without it I will lose index pre-column 
        which may be important for someone.
        """
        
        top_five_io_hi_df = (
            data_ovh_test_case.loc[top_five_io_hi.index]
            [[
                'TotalReads',
                'TotalWrites',
                'DiskSerial',
                'AverageIOLatencyFrom5Minutes(InMs)'
            ]]
        )
        
        top_five_io_hi_df
        
        
        # In[24]:
        
        
        """
        I will use `.index` method, 
        because without it I will lose index pre-column 
        which may be important for someone.
        """
        top_five_io_lo_df = (
            data_ovh_test_case.loc[top_five_io_lo.index]
            [[
                'TotalReads',
                'TotalWrites',
                'DiskSerial',
                'AverageIOLatencyFrom5Minutes(InMs)'
            ]]
        )    
        
        top_five_io_lo_df
        
        
        # `top_five_io_lo` doesn't seem to be correct because even ram doesn't have `0ms` latency. If I assume that `0` is an outliner then I need to drop all rows with the `0` value in `AverageIOLatencyFrom5Minutes(InMs)` to find the top 5 disks with the lowest average IO/s. **This issue has to be addressed because without information about disks specification I don't know for sure is 1ms a proper lowest value that should be set in boolean comparison.**
        #  
        # In the updated approach, I will chain the `where` method with the `lambda x: x > 0`, with that I will look for the smallest values using `nsmallest()`.
        # 
        # If disks documentation will point out that for example, the lowest possible latency is `10 ms`, then I will change `lambda x: x > 0` to `lambda x: x > 10`.
        # 
        # 
        # Finally, there should be addressed a question: is the fact of having `AverageIOLatencyFrom5Minutes(InMs)` == 0 isn't a hidden bug. Maybe those rows should be dropped? Maybe it should be addressed to some support or HQ? 
        # Also, it should be investigated what happens with those disks. [**Some `black box` and `white box` testing**](https://www.practitest.com/qa-learningcenter/resources/black-box-vs-white-box-testing/) may be required. 
        # 
        
        # In[25]:
        
        
        top_five_io_lo_no_zero = (
            data_ovh_test_case['AverageIOLatencyFrom5Minutes(InMs)']
            .where(lambda x: x > 0)
            .nsmallest(5)
        )
        
        top_five_io_lo_no_zero
        
        
        # In[26]:
        
        
        """
        I will use `.index` method, 
        because without it I will lose index pre-column 
        which may be important for someone.
        """
        top_five_io_lo_df = (
            data_ovh_test_case.loc[top_five_io_lo_no_zero.index]
            [[
                'TotalReads',
                'TotalWrites',
                'DiskSerial',
                'AverageIOLatencyFrom5Minutes(InMs)'
            ]]
        )
        
        top_five_io_lo_df
        
        
        # ##### Below a list of potential outliners with `AverageIOLatencyFrom5Minutes(InMs) == 0`:
        
        # In[27]:
        
        
        suspected_io_with_zero = (
            data_ovh_test_case[data_ovh_test_case['AverageIOLatencyFrom5Minutes(InMs)'] == 0]
        )
        
        suspected_io_with_zero.head()
        
        
        # In[28]:
        
        
        suspected_io_with_zero.size
        
        
        # In[29]:
        
        
        suspected_io_with_zero_table = pd.pivot_table(
            suspected_io_with_zero,
            values='DiskSerial',
            index='Data_Ovhcenter',
            aggfunc=np.size
        )
        
        suspected_io_with_zero_table
        
        
        # I found 378 instances where `['AverageIOLatencyFrom5Minutes(InMs)'] == 0`.
        # 
        # Most instances are located in `Data_Ovhcenter`: `dc-tur` but they are in each `Data_Ovhcenter`!
        
        # --------------------------- 
        # I found that the Average IO latency from 5 minutes(In Ms) is from 0 (or 1) to 36 `Ms`. 
        # 
        # It is possible that further investigation has to be made with outliers.
        
        # ### Final conclusions:
        # 
        # To present a bigger picture from this analysis, I will displat plots from several parts of this whole project.
        # 
        # I will also create a new data frame called `final_data_frame` with columns listed below:
        # - 'disk avg age(days)'
        # - 'data ovh disks per DC'
        # - 'top_five_io_lo_series_new'
        # - 'top_five_io_hi_series_new'
        # - 'data_ovh_test_case_disks_per_DC'
        # 
        # With all of that I will be able to see easily all the data.
        
        # In[30]:
        
        
        top_five_io_hi_df_new = (
            data_ovh_test_case.loc[top_five_io_hi_df.index]
            [['Data_Ovhcenter', 'AverageIOLatencyFrom5Minutes(InMs)']]
        )
        
        top_five_io_hi_df_new = (
            top_five_io_hi_df_new
            .set_index('Data_Ovhcenter')
        )
        
        """
        I can then use df.squeeze() to convert the DataFrame into a Series:
        """
        top_five_io_hi_series_new = top_five_io_hi_df_new.squeeze() 
        
        top_five_io_hi_series_new
        
        
        # In[31]:
        
        
        """
        let's groupby output:
        """
        top_five_io_hi_series_new = (
            top_five_io_hi_series_new
            .groupby(level=0)
            .mean()
        )
        
        top_five_io_hi_series_new
        
        
        # In[32]:
        
        
        top_five_io_lo_df_new = (
            data_ovh_test_case.loc[top_five_io_lo_df.index]
            [['Data_Ovhcenter', 'AverageIOLatencyFrom5Minutes(InMs)']]
        )
        
        top_five_io_lo_df_new = (
            top_five_io_lo_df_new
            .set_index('Data_Ovhcenter')
        )
        
        
        """
        I can then use df.squeeze() to convert the DataFrame into a Series:
        """
        top_five_io_lo_series_new = top_five_io_lo_df_new.squeeze() 
        
        top_five_io_lo_series_new
        
        
        # In[33]:
        
        
        """
        let's groupby output:
        """
        top_five_io_lo_series_new = (
            top_five_io_lo_series_new
            .groupby(level=0)
            .mean()
        )
        
        top_five_io_lo_series_new
        
        
        # In[34]:
        
        
        d = {
            'disk avg age(days)': disk_avg_age,
            'data ovh disks per DC': data_ovh_test_case_disks_per_DC,
            'top_five_io_lo_series_new': top_five_io_lo_series_new,
            'top_five_io_hi_series_new': top_five_io_hi_series_new,
            'data_ovh_test_case_disks_per_DC': data_ovh_test_case_disks_per_DC
        }
        
        final_data_frame = pd.DataFrame(data=d)
        final_data_frame
        
        #
        # # In[35]:
        #
        #
        # fig1
        #
        #
        # # In[36]:
        #
        #
        # fig2
        
        
        # From the collected data I can see that:
        # 
        # - `dc-tur` has the highest quantity of disks from all `Data_Ovhcenter`. It also has the oldest disks. 
        # 
        # 
        # - `dc-tug` has the lowest quantity of disks among all `Data_Ovhcenter`. It also has the youngest disks. Because the `dc-tug` is the youngest, I assume, that it's the reason why I don't have information about values in columns: `top_five_io_lo_series_new` and `top_five_io_hi_series_new`.
        # 
        # 
        # - `dc-bzy` has the highest latency in `top_five_io_hi_series_new`. That's odd because it's almost the youngest, so it's possible that there is a need for some revision in the whole system. Something might be wrong with efficiency there. I suggest doing some [**`black box` and `white box` testing**](https://www.practitest.com/qa-learningcenter/resources/black-box-vs-white-box-testing/). 
        
        # In[38]:
        
        
        """
        Thank you for your attention. 
        Below, an easter egg running in Jupyter Notebook 
        (using an open-source library that I wrote. More details at: https://pypi.org/project/get-gifNimage/ )
        """
        ##
        #
        # !pip install get-gifNimage  | grep -v 'already satisfied'
        #
        # import get_gifNimage
        # from get_gifNimage import get_gifNimage
        # get_gifNimage('https://media.giphy.com/media/W80Y9y1XwiL84/giphy.gif')
    

# =============================================================================
# Let's put all outputs from above part to one object called 'final_output_pandas_analysis_or_post_mortem'
# =============================================================================


    # Data analysis output:
    
        final_output_pandas_analysis_or_post_mortem = (
                text2art("Panda's")
                + text2art("Analysis :")
                + '\n\n\n'
                + "What's the shape of DB:"
                +'\n\n'
                + str(data_ovh_test_case.shape)
                + '\n\n================================================================================\n'
                + "What's the shape of DB:"
                +'\n\n'
                + str(data_ovh_test_case.shape)
                + '\n\n================================================================================\n'
                + "Panda's `pd.describe()`:"
                +'\n\n'
                + str(data_ovh_test_case.describe())
                + '\n\n================================================================================\n'
                + "Any column has a missing values?"
                +'\n\n'
                + str(data_ovh_test_case.isnull().any())
                + '\n\n================================================================================\n'
                + "Find disks which are most probably broken, i.e. have non-zero uncorrected errors (str disks and error counter):"
                +'\n\n'
                + str(data_ovh_test_case_errors_tuwe.value_counts())
                + '\n\n================================================================================\n'
                + "Disks that have TotalUncorrectedReadErrors:"
                +'\n\n'
                + str(data_ovh_test_case[data_ovh_test_case_errors_ture][['DiskSerial', 'TotalUncorrectedReadErrors']])
                + '\n\n================================================================================\n'
                + "Disks that have TotalUncorrectedWriteErrors:"
                +'\n\n'
                + str(data_ovh_test_case[data_ovh_test_case_errors_tuwe][['DiskSerial', 'TotalUncorrectedWriteErrors']])
                + '\n\n================================================================================\n'
                + "How many disks are in total and in each DC:"
                +'\n\n'
                + str(data_ovh_test_case_disks_per_DC)
                + '\n\n================================================================================\n'
                + "Which disk is the youngest/oldest one and what is its age (in days)"
                +'\n\n'
                + str(younges_oldest_drives)
                +'\n\n'
                + "The oldest disk from output generated above has:"
                + "2074 days it's " +  str(round(oldest_drive_age / 365, 2)) +  " years"
                + '\n\n================================================================================\n'
                + "What's the average disk age per DC (in days)"
                +'\n\n'
                + str(disk_avg_age)
                + '\n\n================================================================================\n'
                + "Find the top 5 disks with the highest average IO/s (reads+ writes, str disks and their avg IO/s):"
                +'\n\n'
                + str(top_five_io_hi_df)
                + '\n\n================================================================================\n'
                + "Find the top 5 disks with the lowest average IO/s (reads+ writes, str disks and their avg IO/s):"
                +'\n\n'
                + str(top_five_io_lo_df)
                +'\n\n'
                + "Below a list of potential outliners with:\nAverageIOLatencyFrom5Minutes(InMs) == 0:"
                +'\n\n'
                + "1.Size"
                +'\n'
                + str(suspected_io_with_zero.size)
                +'\n'
                + "2. Instances per each `Data_Ovhcenter`"
                +'\n\n'
                + str(suspected_io_with_zero_table)
                + '\n\n================================================================================\n'
                + "Additional informations:"
                +'\n\n'
                + str(final_data_frame)
                 )
    else:
        final_output_pandas_analysis_or_post_mortem = (
                text2art("Post   Mortem :")
                + '\n\n\n'
                +"Due to an error in the test (s) with numbers from 2 to 4, no further analysis is possible.\n The data analyst should clean up and systematize the data before further analysis in Pandas."
                )



    # Change label contents
    text_box.insert(
            "0.0",
            'File Opened ready for further processing: '
            + '\n\n'
            + filename
            + '\n================================================================================\n'
            + test_output1
            + '\n\n================================================================================\n'
            + test_output2
            + '\n================================================================================\n'
            + test_output3
            + '\n\n================================================================================\n'
            + test_output4
            + '\n\n================================================================================\n'
            + final_output_pandas_analysis_or_post_mortem
            + '\n\n'
            )
    



button_explore = tk.Button(
                        content,
                        text = "Browse Files",
                        command = browseFiles,
                        width=20,
                        height=3,
                        bg=from_rgb((23,175,231)),
                        fg="black",
                        font=font_button_small
                        )
# =============================================================================
# making "analyze the data" button
# =============================================================================
"""
I will change the data frame into a string,
then separate each line and I will add an interline for better visibility.
"""

currency_table = [1,2,3,4,5,6]
string_currency_table = currency_table


def show_text_from_entry_all_curr(): # https://www.youtube.com/watch?v=ITaDE9LLEDY
    output_text = text_box.insert(
            "0.0", output_currency_table)
    print(output_text)
    
    return None

button_all_curr = tk.Button(
    content,
    command=show_text_from_entry_all_curr,
    text="analyze the data ",
    width=20,
    height=2,
    bg=from_rgb((23,175,231)),
    fg="black",
    font=font_button_small
    )



# =============================================================================
# making "test data consistency " button
# =============================================================================
def show_text_from_entry(): # https://www.youtube.com/watch?v=ITaDE9LLEDY
    output_text = text_box.insert(
            "0.0",
            "Currency exchange rate PLN/EUR:\n\n" +
            "Broker buy: " +
            str(float(currency_table.loc[0]["broker buy"])) +
            " PLN" +
            "\nBroker Sell: " +
            str(float(currency_table.loc[0]["broker sell"])) +
            " PLN"
            )
    print(output_text)
    return None

button_pln_eur = tk.Button(
    content,
    command=show_text_from_entry,
    text="test data consistency ",
    width=20,
    height=2,
    bg=from_rgb((23,175,231)),
    fg="black",
    font=font_button_small
    )




# =============================================================================
# delete button: It will delete the output from `text_box`
# =============================================================================

def delete_output():
    text_box.delete("0.0", tk.END)
    return None
delete_button = tk.Button(
    content,
    command=delete_output,
    text="Delete output text",
    width=20,
    height=3,
    bg="red",
    fg="black",
    font=font_button_big
    )

# =============================================================================
# making "exit window" button
# =============================================================================

# =============================================================================
def quit_app():
    # get data from entry
    output_text = text_box.get("1.0",'end-1c')
    with open('OVH_log.txt', 'w') as f:  # open file in write mode
        f.write(output_text)
        # the entered data else write nothing (note that this will overwrite everything in the file)
    content.quit()  # or use `exit()` depending on what you need

# https://stackoverflow.com/questions/68807822/tkinter-how-to-detect-checkbutton-when-gui-starts?noredirect=1#comment121631633_68807822
root.protocol('WM_DELETE_WINDOW', quit_app) # this protocol
# is triggered when user presses the "X" button in the top right corner of window
 
 
exit_button = tk.Button(
        content, 
        text='Save to txt and quit', 
        command=quit_app,
        width=30,
        height=3,
        bg=from_rgb((213,60,60)),
        fg="black",
        font=font_button_big
        )
# =============================================================================
# =============================================================================
# creating a text box for output:
# =============================================================================

text_box_description = tk.Label(
        content,
        text="Output:",
        foreground="forest green",
        background=from_rgb((30,81,100)),
        width=70,
        height=1,
        font=font.Font(family='Helvetica', size="12", weight='bold')
        )

text_box = tk.Text(
        content,
        width=80,
        height=40,
        bg=from_rgb((38,15,2)),
        fg="gainsboro"
        )

# =============================================================================
# making image button
# https://blog.furas.pl/python-tkinter-how-to-load-display-and-replace-image-on-label-button-or-canvas-gb.html
# https://pythonexamples.org/python-pillow-show-display-image/
# https://pythonexamples.org/python-pillow-resize-image/
# =============================================================================
#from PIL import ImageTk, Image
# https://stackoverflow.com/questions/38180388/tkinter-how-to-insert-an-image-to-a-text-widget
# https://stackoverflow.com/questions/35924690/tkinter-image-wont-show-up-in-new-window

def add_image():
    toplevel_about = tk.Toplevel()
#    toplevel_about.columnconfigure(0, weight=2)
    toplevel_about.title('About')
    canvas = tk.Canvas(toplevel_about, width = 1000, height = 650)
#    canvas.grid(sticky="S"+"N"+"E"+"W")
#    canvas.columnconfigure(0, weight=3)
    canvas.pack(expand = tk.YES, fill = tk.BOTH)
    img1 = tk.PhotoImage(file = 'Pictures\picture1.png')
                                #image not visual
    canvas.create_image(50, 10, image = img1, anchor = tk.NW)
    #assigned the gif1 to the canvas object
    canvas.img1 = img1
    canvas.create_text(500,530,fill="darkblue",font="Times 20 italic bold",
                        text="OVH test raw db GUI v. 0.0.1\n\n" +
                        "Author: Paweł Pedryc\n pawelpedryc@gmail.com")
    
# canvas + grid: https://stackoverflow.com/questions/20149483/python-canvas-and-grid-tkinter

button_about = tk.Button(
    content,
    command=add_image,
    text="About",
    width=8,
    height=1,
    bg="red",
    fg="black",
    font=font.Font(family='Helvetica', size="14", weight='bold')
    )

# =============================================================================
# Main grid:x
# =============================================================================

content.grid(column=0, row=0)
#frame.grid(column=0, row=0, columnspan=3, rowspan=6)
text_box_description.grid(column=0, row=0)
text_box.grid(column=0, row=1, rowspan=10)



# =============================================================================
# # create a Scrollbar and associate it with `text_box`:
# =============================================================================


# Vertical (y) Scroll Bar
scroll = tk.Scrollbar(content)
# scroll bar remember position after "scroll":
text_box.config(yscrollcommand=scroll.set) 
scroll.config(command=text_box.yview)

scroll.grid(column=0, row=1, rowspan=10, sticky="N"+"S"+"E")
# Configure the scrollbars
scroll.config(command=text_box.yview)

button_explore.grid(column=1, row=7)
delete_button.grid(column=1, row=8)

button_about.grid(column=4, row=0, sticky=(tk.E))
exit_button.grid(column=3, row=10, columnspan=4, sticky=(tk.N))


root.mainloop()

root.withdraw()


