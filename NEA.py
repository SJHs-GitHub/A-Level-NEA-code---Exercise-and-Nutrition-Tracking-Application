##### due to the nature of this program, there is a lot of code that needs to be repeated (mainly for gui, databases, primary keys etc).
#### If the functionality of a section of code has been explained once,
### it will not be repeated, due to the time constraints on this project.
## annotations are done from start of code and down from there, so if something isn't explained, it's because it has been done above.

#importing all the modules I need
#to run will require sys, sqlite3, time, tkinter, matplotlib.
import sys
import sqlite3
import time
from datetime import datetime
from tkinter import *
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#sets up the root window for the GUI to be presented in.
root = Tk()
root.title("Nutrition Tracker")
root.configure(background = "azure")
root.geometry("480x640")
root.resizable(width=False, height=False)

#this function creates/re-creates tables for the factory reset procedure.
def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:    #connects to db as defined by the parameter.
        db.execute("PRAGMA foreign_keys = ON")  #turns foreign keys on.
        cursor = db.cursor()    #defines the cursor in terms of open db (to traverse, add, delete, return records etc.)
        cursor.execute("select name from sqlite_master where name =?", (table_name,))   #selects the tablename from the database (if exists)
        result = cursor.fetchall()  #returns result

        keep_table = True
        if len(result) == 1:    #if the table exists this is true.   
            response = "Y"      
            if response.upper() == 'Y':     
                keep_table = False      #sets variable to false so will be recreated.
                print("The table", table_name, "will be recreated. All data will be lost.")
                cursor.execute("drop table if exists {0}".format(table_name))   #drops the table so it can recreated in a second.              
                db.commit()   #commits changes to db.
            else:
                print("The existing table was kept.")
        else:       #if table does not exist....
            keep_table = False
        if not keep_table:
            cursor.execute(sql)   #execute sql to create the table (from parameter), if table does not exist or user wants to recreate it. 
            db.commit()     #commit changes to db

#as lots of database commands and jargon are repeated, any that have already been explained will not in future.

#function to create tables in user_details db.
def create_db_UserDetails():
    db_name = "User_Details.db"     
    #################################################################
    #defines the table to be created in terms of the sql commands that will create it, with the column name followed by the datatype.
    sql = """create table UserAccountDetails
             (UserKeyID text,
             UserEmail text,
             UserPassword text,
             Primary key(UserKeyID))""" #defines the userKeyID as being the primary key.

    create_table(db_name, "UserAccountDetails", sql)  #passes the sql to create_table() to create the new table.
    #################################################################
    sql = """create table UserPersonalDetails
             (DateTimeID text,
             UserKeyID text,
             UserFName text,
             UserSName text,
             UserDOB text,
             UserHeight float,
             UserWeight float,
             UserHR integer,
             UserBF float,
             UserArmCirc float,
             UserWaistCirc float,
             UserLegCirc float,
             UserChestCirc float,
             UserCalfCirc float,
             Date text,
             Time text,
             Primary key(DateTimeID),
             Foreign key(UserKeyID) references UserAccountDetails(UserKeyID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "UserPersonalDetails", sql)

    userKeyIDFile = open("NEA_UserKeyID.txt", "w")   #opens the file where the primary key for the userKeyID is stored.
    userKeyIDFile.write('0')        #resets it to 0.
    userKeyIDFile.close         #closes file.

#function to create tables in food db.
def create_db_Food():
    db_name = "Food.db"
    #################################################################
    sql = """create table UserKey
             (UserKeyID text,
             Primary key(UserKeyID))"""
    create_table(db_name, "UserKey", sql)
    #################################################################
    sql = """create table Food
             (FoodID text,
             FoodName text,
             Carb_Pro_Fat text,
             StndrdWeight float,
             FoodCals integer,
             FoodCarb float,
             FoodProtein float,
             FoodFat float,
             FoodCarb_gram float,
             FoodProtein_gram float,
             FoodFat_gram float,
             Primary key(FoodID))"""
    create_table(db_name, "Food", sql)
    #################################################################
    sql = """create table Meal
             (MealID text,
             MealName text,
             MealCals integer,
             MealCarb float,
             MealProtein float,
             MealFat float,
             Primary key(MealID))"""
    create_table(db_name, "Meal", sql)
    #################################################################
    sql = """create table FoodMeal
             (MealID text,
             FoodID text,
             StndrdWeight float,
             FoodCals integer,
             FoodCarb float,
             FoodProtein float,
             FoodFat float,
             Primary key(MealID, FoodID),
             Foreign key(MealID) references Meal(MealID) ON DELETE CASCADE ON UPDATE CASCADE,
             Foreign key(FoodID) references Food(FoodID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    #in this table, the two foreign keys are referenced by referring to their original defined tables where they are primary keys.
    #they are set to cascade, so if anything changes in their original table, they are updated/deleted here also.
    create_table(db_name, "FoodMeal", sql)
    #################################################################
    sql = """create table Protein
             (FoodID text,
             FoodName text,
             Carb_Pro_Fat text,
             StndrdWeight float,
             FoodCals integer,
             FoodCarb float,
             FoodProtein float,
             FoodFat float,
             FoodCarb_gram float,
             FoodProtein_gram float,
             FoodFat_gram float,
             Primary key(FoodID),
             Foreign key(FoodID) references Food(FoodID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "Protein", sql)
    #################################################################
    sql = """create table Fat
             (FoodID text,
             FoodName text,
             Carb_Pro_Fat text,
             StndrdWeight float,
             FoodCals integer,
             FoodCarb float,
             FoodProtein float,
             FoodFat float,
             FoodCarb_gram float,
             FoodProtein_gram float,
             FoodFat_gram float,
             Primary key(FoodID),
             Foreign key(FoodID) references Food(FoodID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "Fat", sql)
    #################################################################
    sql = """create table Carb
             (FoodID text,
             FoodName text,
             Carb_Pro_Fat text,
             StndrdWeight float,
             FoodCals integer,
             FoodCarb float,
             FoodProtein float,
             FoodFat float,
             FoodCarb_gram float,
             FoodProtein_gram float,
             FoodFat_gram float,
             Primary key(FoodID),
             Foreign key(FoodID) references Food(FoodID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "Carb", sql)
    #################################################################
    sql = """create table DailyFoodLog
             (LogID text,
             Date text,
             TotalCals integer,
             TotalCarb float,
             TotalProtein float,
             TotalFat float,
             CalsRemaining integer,
             CarbRemaining float,
             FatRemaining float,
             ProteinRemaining float,
             Primary key(LogID))"""
    create_table(db_name, "DailyFoodLog", sql)
    #################################################################
    sql = """create table FoodLog
             (FoodLogID text,
             LogID text,
             FoodID text,
             Time text,
             FoodName text,
             FoodServ float,
             FoodCals integer,
             FoodCarb float,
             FoodProtein float,
             FoodFat float,
             Primary key(FoodLogID),
             Foreign key(LogID) references DailyFoodLog(LogID) ON DELETE CASCADE ON UPDATE CASCADE,
             Foreign key(FoodID) references Food(FoodID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "FoodLog", sql)
    #################################################################
    sql = """create table MealLog
             (MealLogID text,
             LogID text,
             MealID text,
             Time text,
             MealName text,
             MealServ float,
             MealCals integer,
             MealCarb float,
             MealProtein float,
             MealFat float,
             Primary key(MealLogID),
             Foreign key(LogID) references DailyFoodLog(LogID) ON DELETE CASCADE ON UPDATE CASCADE,
             Foreign key(MealID) references Meal(MealID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "MealLog", sql)

    foodIDFile = open("NEA_FoodID.txt", "w") #opens the file where the primary key for the foodID is stored.
    foodIDFile.write('0') #resets it to 0.
    foodIDFile.close #closes file.

    mealIDFile = open("NEA_MealID.txt", "w") #opens the file where the primary key for the mealID is stored.
    mealIDFile.write('0') #resets it to 0.
    mealIDFile.close #closes file.

    dailyFoodLogIDFile = open("NEA_DailyFoodLogID.txt", "w") #opens the file where the primary key for the dailyFoodLogID is stored.
    dailyFoodLogIDFile.write('0') #resets it to 0.
    dailyFoodLogIDFile.close #closes file.

    foodLogIDFile = open("NEA_FoodLogID.txt", "w")  #opens the file where the primary key for the foodLogID is stored.
    foodLogIDFile.write('0') #resets it to 0.
    foodLogIDFile.close #closes file.

    mealLogIDFile = open("NEA_MealLogID.txt", "w")  #opens the file where the primary key for the mealLogID is stored.
    mealLogIDFile.write('0') #resets it to 0.
    mealLogIDFile.close #closes file.
    

def create_db_Exercise():
    db_name = "Exercise.db"
    #################################################################
    sql = """create table UserKey
             (UserKeyID text,
             Primary key(UserKeyID))"""
    create_table(db_name, "UserKey", sql)
    #################################################################
    sql = """create table Exercise
             (ExerciseID text,
             ExerciseName text,
             MuscleGroup text,
             Weight float,
             Reps integer,
             Sets integer,
             CalsBurned integer,
             Primary key(ExerciseID))"""
    create_table(db_name, "Exercise", sql)
    #################################################################
    sql = """create table WorkoutPlans
             (WorkoutID text,
             WorkoutName text,
             WorkoutCalsBurned integer,
             Primary key(WorkoutID))"""
    create_table(db_name, "WorkoutPlans", sql)
    #################################################################
    sql = """create table ExerciseWorkout
             (WorkoutID text,
             ExerciseID text,
             ExerciseName text,
             MuscleGroup text,
             Weight float,
             Reps integer,
             Sets integer,
             CalsBurned integer,
             Primary key(WorkoutID, ExerciseID),
             Foreign key(WorkoutID) references WorkoutPlans(WorkoutID) ON DELETE CASCADE ON UPDATE CASCADE,
             Foreign key(ExerciseID) references Exercise(ExerciseID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "ExerciseWorkout", sql)
    #################################################################
    sql = """create table DailyExerciseLog
             (LogID text,
             Date text,
             TotalCalsBurned integer,
             CalsRemaining integer,
             Primary key(LogID))"""
    create_table(db_name, "DailyExerciseLog", sql)
    #################################################################
    sql = """create table ExerciseExerciseLog
             (ExerciseLogID text,
             LogID text,
             ExerciseID text,
             Time text,
             ExerciseName text,
             Weight float,
             Reps integer,
             Sets integer,
             CalsBurned integer,
             Primary key(ExerciseLogID),
             Foreign key(LogID) references DailyExerciseLog(LogID) ON DELETE CASCADE ON UPDATE CASCADE,
             Foreign key(ExerciseID) references Exercise(ExerciseID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "ExerciseExerciseLog", sql)
    #################################################################
    sql = """create table WorkoutExerciseLog
             (WorkoutLogID text,
             LogID text,
             WorkoutID text,
             Time text,
             WorkoutName text,
             CalsBurned integer,
             Primary key(WorkoutLogID),
             Foreign key(LogID) references DailyExerciseLog(LogID) ON DELETE CASCADE ON UPDATE CASCADE,
             Foreign key(WorkoutID) references WorkoutPlans(WorkoutID) ON DELETE CASCADE ON UPDATE CASCADE)"""
    create_table(db_name, "WorkoutExerciseLog", sql)

    exerciseIDFile = open("NEA_ExerciseID.txt", "w") #opens the file where the primary key for the exerciseID is stored.
    exerciseIDFile.write('0') #resets it to 0.
    exerciseIDFile.close #closes file.

    workoutIDFile = open("NEA_WorkoutID.txt", "w") #opens the file where the primary key for the workoutID is stored.
    workoutIDFile.write('0') #resets it to 0.
    workoutIDFile.close #closes file.

    dailyExerciseLogIDFile = open("NEA_DailyExerciseLogID.txt", "w") #opens the file where the primary key for the dailyExerciseID is stored.
    dailyExerciseLogIDFile.write('0') #resets it to 0.
    dailyExerciseLogIDFile.close #closes file.

    exerciseLogIDFile = open("NEA_ExerciseLogID.txt", "w")  #opens the file where the primary key for the exerciseLogID is stored.
    exerciseLogIDFile.write('0') #resets it to 0.
    exerciseLogIDFile.close #closes file.

    workoutLogIDFile = open("NEA_WorkoutLogID.txt", "w") #opens the file where the primary key for the workoutLogID is stored.
    workoutLogIDFile.write('0') #resets it to 0.
    workoutLogIDFile.close #closes file.

#--------------------------------------------------------------------
#function to select all the items in a table.
def selectAllItems(db_name, sql):
    with sqlite3.connect(db_name) as db:
        db.execute("PRAGMA foreign_keys = ON")
        cursor = db.cursor()
        cursor.execute(sql)   
        items = cursor.fetchall()    
        return items    #returns the items (all items in table) to the fucntion that called this one.

#function that is same as previous, but instead of just selecting all items, selects multiple items that meet certain criteria, as defined by the sql and values parameters.
def selectAllItems2(db_name, sql, values):
    with sqlite3.connect(db_name) as db:
        db.execute("PRAGMA foreign_keys = ON")
        cursor = db.cursor()
        cursor.execute(sql, (values,))   #executes in qmark form, where the values replace question marks that were used instead of attributes and values in the sql.
        items = cursor.fetchall()    
        return items

#selects one item from the table that meets the certain criteria in sql and values.
def selectItem(db_name, sql, values):   
    with sqlite3.connect(db_name) as db:
        db.execute("PRAGMA foreign_keys = ON")
        cursor = db.cursor()
        cursor.execute(sql, (values,))   
        item = cursor.fetchone()   
        return item

#function to insert a new record into the table, based off of sql and values defining what to insert, and where.
def insertItem(db_name, sql, values):   
    with sqlite3.connect(db_name) as db:
        db.execute("PRAGMA foreign_keys = ON")
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()

#updates a record in the table based upon sql and values.
def updateItem(db_name, sql, values):         
    with sqlite3.connect(db_name) as db:
        db.execute("PRAGMA foreign_keys = ON")
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        
#deletes a record in the db based off of sql and the values passed.
def deleteItem(db_name, sql, values):
    with sqlite3.connect(db_name) as db:
        db.execute("PRAGMA foreign_keys = ON")
        cursor = db.cursor()
        cursor.execute(sql, (values,))
        db.commit()


# MERGE SORT----------------------------------------------------------
# this function is the merge sort algorithm. It is used to display to the user the amounts of protein, fat and carb of foods in their respective databases, in order.
# the purpose of this is so the user can see the amounts of macronutrients in foods easily (as they are ordered),
# so they can choose an item of food which has the desired amount of a macronutrient easily (to fit their daily targets).
def mergeSort(dataList):
    if len(dataList) > 1:
        #here the list is split in two in the middle. Then recursion is used for this function to call itself, with each half being split again and again,
        #until there are n lists with one element in each when recursion stops.
        #the recursion then unwinds (as length = 1 when two items get merged) to build the lists back up in sorted order,
        #performing the necessary actions below to sort them into correct order as it does so.
        midpoint = len(dataList)//2   
        leftList = dataList[:midpoint]
        rightList = dataList[midpoint:]
        mergeSort(leftList)
        mergeSort(rightList)

        x = 0
        y = 0
        z = 0

        while x < len(leftList) and y < len(rightList):  #repeat until one of the lists has been fully merged.
            if leftList[x] < rightList[y]:   #add x to list if x < y.
                dataList[z] = leftList[x]
                x = x + 1   #increment x, so next time next item in list is compared.
            else:  #else if y is greater append y to list.
                dataList[z] = rightList[y]
                y = y + 1  #increment y, so next time next item in list is compared.

            z = z + 1   #increases position in the merged list, as up to the current position is in order.

        while x < len(leftList):   #if rightList has all been added to dataList, but not all of leftList
            dataList[z] = leftList[x]   #add it to the merged list.
            x = x + 1
            z = z + 1

        while y < len(rightList):  #if leftList has all been aded to datalist, but not all of rightList
            dataList[z] = rightList[y]  #add it to the merged list.
            y = y + 1
            z = z + 1

    return(dataList)


#---------------------------------------------------------------------
# class object which is part of gui, to display data.
class DisplayPage:
    def __init__(self, master, returned):   #constructor to instantiate object's attributes

        self.returned = returned    #the parameter now becomes an attribute of the object.

        self.otherFrame = Frame(master)     #defines the frame (for all other GUI elements to be placed in) as an attribute of object.
        self.otherFrame.pack(side=TOP)  #packs it in to the root (places it), with side= defining where.

        self.displayLabel = Label(self.otherFrame, text = self.returned, fg = "white", bg = "sky blue", width = 200, height = 2)    #defines a label object to go into the frame, to display the 'returned' information.
        self.displayLabel.pack(side=TOP)  #packs it into the frame.
        self.displayLabel.config(font=("Calibri", 12))  #sets font to calibri and fontsize to 12.

        self.homeButton = Button(self.otherFrame, text = "Home", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.home)   #defines a button object to go into the frame. cont. below
        self.homeButton.pack(side = TOP)                                                                                                    #When pressed runs function as defined by 'command =' (below)
        self.homeButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

        print("\n\n", self.returned,"\n\n")  # prints information to the shell also.

    #home function, that is called by pressing 'home button'
    def home(self):
        self.otherFrame.destroy()  #destroys the frame (so gui page no longer visible)
        x = Starter(root)  #calls the new page's class to create the new page as an object.
        s.top = s.top-1   #makes the top of the stack object = the top -1 (to correct for the +1 earlier (was just discovered during development to be necessary to make the code work,
                          #as if not there was an error if you went to another object and then pressed 'back' - by adding 1 earlier and removing 1 when going to new page it worked correctly for all scenarios))
        s.push(stack, Starter, maxSize, noItems, top)   #pushes the new gui object onto stack and updates object.
        

    def back(self):
        if s.top < 1:   #if the current top object is the first in the stack, you cannot go back so prints message.
            print("Cannot perform operation, no back pages.")
        else:   
            LOL = s.back(stack, top)   #calls stack object's back function to return previous page's object
            self.otherFrame.destroy()  #destroys current frame.
            x = LOL(root)   #calls returned back object to present in GUI.
            
    def forward(self):
        if s.top+1 >= s.noItems: #if the top+1 (as top starts at 0) = the number of items in the list, there are no forward pages.
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)  #calls stack object's forward function to return forward page's object
            self.otherFrame.destroy()  #destroys current frame.
            x = xD(root)  #calls returned forward object to present in GUI.



class DeletePage:
    def __init__(self, master, records, table, column_name, db_name):  #constructor for class

        #defines class' attributes.
        self.records = records
        self.table = table
        self.column_name = column_name
        self.db_name = db_name

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=TOP)

        self.displayLabel = Label(self.otherFrame, text = "Please Enter the Name/Date of the Record to Delete:", fg = "white", bg = "sky blue", width = 200, height = 2)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.displayLabel2 = Label(self.otherFrame, text = self.records, fg = "white", bg = "sky blue", width = 200, height = 2)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 16))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)  #defines an entry object.
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.delete)  #binds it to the 'delete' function below.

        self.selectButton = Button(self.otherFrame, text = "Delete", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.delete)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def delete(self):
        # defines all necessary variables for this function.
        realRecords = []
        name = self.entry1.get()  #get() command sets the variable = what the user input to the as defined above entry.
        length = len(self.records)
        counter = 0
        counter2 = 0
        valid = False

        #runs this if statement the table parameter is the UserPersonalDetails
        if self.table == "UserPersonalDetails":
            if length == 1:  #if there is only one record in the UserPersonaldetails table, it will not delete it and will instead destroy current frame and recall the object to the GUI.
                print("\n\nCannot delete final record as it contains important sign-up information.")
                self.otherFrame.destroy()
                x = DeletePage(root, self.records, self.table, self.column_name, self.db_name)
                valid = False #sets valid to false so no more code is run in this function
                
            else:
                # tests all the records to see if they are all the same date. If they are valid stays false and no more code runs, else valid becomes true and the desired record(s) are deleted.
                for i in range(0, length):
                    test = self.records[counter2][0]
                    if test == name:
                        counter2+=1
                    else:
                        valid = True
                        break
                if valid == False:
                    print("Only one date left in the database, and cannot delete these records as they contain vital information.")
                        
        else:
            # if the table isnt UserPersonalDetails, it is set to true.
            valid = True
        
        if valid == True:
            for i in range(0, length):
                realRecords.append(self.records[counter][0])  #appends just the names/dates to the new list so you have a list of names/dates (as opposed to a list of tuples, as returned by call to db).
                counter += 1
            if name not in realRecords:     #if desired name/date is not in records, the entry is invalid and the error message is avoided by not executing the sql and just re-creating the object.
                print("Invalid Entry")
                self.otherFrame.destroy()
                x = DeletePage(root, self.records, self.table, self.column_name, self.db_name)
            else:
                sql = "delete from %s WHERE %s=?" % (self.table, self.column_name) #else deletes the item using the previously defined function and appropraite sql using % and qmark formats to sub in values.
                values = (name)
                deleteItem(self.db_name, sql, values)

                self.otherFrame.destroy()
                x = Starter(root)
                s.top = s.top-1
                s.push(stack, Starter, maxSize, noItems, top)
                

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)

        
        
        
        

class UserInsertPageUPD:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM)

        self.displayLabel = Label(self.otherFrame, text = 'New Height (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.entry)

        self.displayLabel2 = Label(self.otherFrame, text = 'New Weight (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.entry2 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry2.pack(side = TOP)
        self.entry2.configure(font=("Calibri", 12))
        self.entry2.bind(self.entry)

        self.displayLabel3 = Label(self.otherFrame, text = 'New Heartrate (bpm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))

        self.entry3 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry3.pack(side = TOP)
        self.entry3.configure(font=("Calibri", 12))
        self.entry3.bind(self.entry)

        self.displayLabel4 = Label(self.otherFrame, text = 'New Body Fat Percentage (%)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel4.pack(side=TOP) 
        self.displayLabel4.config(font=("Calibri", 12))

        self.entry4 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry4.pack(side = TOP)
        self.entry4.configure(font=("Calibri", 12))
        self.entry4.bind(self.entry)

        self.displayLabel5 = Label(self.otherFrame, text = 'New Arm Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel5.pack(side=TOP) 
        self.displayLabel5.config(font=("Calibri", 12))

        self.entry5 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry5.pack(side = TOP)
        self.entry5.configure(font=("Calibri", 12))
        self.entry5.bind(self.entry)

        self.displayLabel6 = Label(self.otherFrame, text = 'New Waist Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel6.pack(side=TOP) 
        self.displayLabel6.config(font=("Calibri", 12))

        self.entry6 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry6.pack(side = TOP)
        self.entry6.configure(font=("Calibri", 12))
        self.entry6.bind(self.entry)

        self.displayLabel7 = Label(self.otherFrame, text = 'New Leg Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel7.pack(side=TOP) 
        self.displayLabel7.config(font=("Calibri", 12))

        self.entry7 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry7.pack(side = TOP)
        self.entry7.configure(font=("Calibri", 12))
        self.entry7.bind(self.entry)

        self.displayLabel8 = Label(self.otherFrame, text = 'New Chest Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel8.pack(side=TOP) 
        self.displayLabel8.config(font=("Calibri", 12))

        self.entry8 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry8.pack(side = TOP)
        self.entry8.configure(font=("Calibri", 12))
        self.entry8.bind(self.entry)

        self.displayLabel9 = Label(self.otherFrame, text = 'New Calf Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel9.pack(side=TOP) 
        self.displayLabel9.config(font=("Calibri", 12))

        self.entry9 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry9.pack(side = TOP)
        self.entry9.configure(font=("Calibri", 12))
        self.entry9.bind(self.entry)

        self.selectButton = Button(self.otherFrame, text = "Add Item", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.entry)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))



    def entry(self):
        db_name = "User_Details.db"
        UserKeyID = USERKEYID #USERKEYID is a global variable that is never changed (a constant then i guess) and represents the UserKeyID of the current user.
        # selects the required fields from the previous UserPersonaldetails entry (hence why cannot delete all entries to this table).
        userKeyIDtemp = selectItem("User_Details.db", "select UserKeyID from UserAccountDetails where UserKeyID =?", (UserKeyID))
        userKeyID = userKeyIDtemp[0] #returns a tuple so by doing this you get the information you want, and not other pasrt of tuple.
        userFNametemp = selectItem("User_Details.db", "select UserFName from UserPersonalDetails where UserKeyID =?", (userKeyID))
        userFName = userFNametemp[0]
        userSNametemp = selectItem("User_Details.db", "select UserSName from UserPersonalDetails where UserKeyID =?", (userKeyID))
        userSName = userSNametemp[0]
        userDOBtemp = selectItem("User_Details.db", "select UserDOB from UserPersonalDetails where UserKeyID =?", (userKeyID))
        userDOB = userDOBtemp[0]

        #gets all the data from user entries.
        userHeighttemp = self.entry1.get()
        userWeighttemp = self.entry2.get()
        userHRtemp = self.entry3.get()
        userBFtemp = self.entry4.get()
        userArmCirctemp = self.entry5.get()
        userWaistCirctemp = self.entry6.get()
        userLegCirctemp = self.entry7.get()
        userChestCirctemp = self.entry8.get()
        userCalfCirctemp = self.entry9.get()
        invalid = False
        # makes a new list and appends all the user input items that will need to be floats.
        check1 = []
        check1.append(userHeighttemp)
        check1.append(userWeighttemp)
        check1.append(userBFtemp)
        check1.append(userArmCirctemp)
        check1.append(userWaistCirctemp)
        check1.append(userLegCirctemp)
        check1.append(userChestCirctemp)
        check1.append(userCalfCirctemp)
        z = 0
        # below is defensive programming for the user inputs.
        # checks all items to see if they can be floats (ie are not strings or boolean etc).
        # if they are all valid, invalid stays False so code can proceed.
        # if they are not all valid floats, invalid = True so code stops execution befrore it breaks, frame is destroyed and page is recalled with message saying why.
        for i in range(len(check1)):
            try:
                float(check1[z])
            except ValueError:
                self.otherFrame.destroy()
                invalid = True
            z = z+1

        # checks this to see if it is an integer, as that is the appropriate data type.
        try:
            int(userHRtemp)
        except ValueError:
            self.otherFrame.destroy()
            invalid = True

        #if anything was invalid datatype, recalls the page object, and prints that input was invalid. 
        if invalid == True:
            print("Input was invalid. Please re-enter information.")
            x = UserInsertPageUPD(root)

        else:
            #if wasn't invalid, transfers the inputs to their correct datatypes.
            userHeight = float(userHeighttemp)        
            userWeight = float(userWeighttemp)
            userHR = int(userHRtemp)
            userBF = float(userBFtemp)
            userArmCirc = float(userArmCirctemp)
            userWaistCirc = float(userWaistCirctemp)
            userLegCirc = float(userLegCirctemp)
            userChestCirc = float(userChestCirctemp)
            userCalfCirc = float(userCalfCirctemp)

            now = datetime.now() #gets time and date from imported module and sets it = to this object.
            date = ("%s/%s/%s" % (now.day, now.month, now.year))   #sets the date using % formatting and getting attributes from now object.
            now = datetime.now()
            time = ("%s:%s:%s" % (now.hour, now.minute, now.second))  #does same with time.
            dateTimeIDtemp = date+time
            dateTimeID = str(dateTimeIDtemp)
            sql = "insert into UserPersonalDetails (DateTimeID, UserKeyID, UserFName, UserSName, UserDOB, UserHeight, UserWeight, UserHR, UserBF, UserArmCirc, UserWaistCirc, UserLegCirc, UserChestCirc, UserCalfCirc, Date, Time) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (dateTimeID, userKeyID, userFName, userSName, userDOB, userHeight, userWeight, userHR, userBF, userArmCirc, userWaistCirc, userLegCirc, userChestCirc, userCalfCirc, date, time)
            insertItem(db_name, sql, values) #inserts the new record using all information provided.
            self.otherFrame.destroy()
            x = Starter(root)  #goes back to home page.
            s.push(stack, Starter, maxSize, noItems, top)
            

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)


class UserInsertPageFood:
    def __init__(self, master):

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM)

        self.displayLabel = Label(self.otherFrame, text = 'Name', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.entry)

        self.displayLabel2 = Label(self.otherFrame, text = 'Carb/Protein/Fat', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.entry2 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry2.pack(side = TOP)
        self.entry2.configure(font=("Calibri", 12))
        self.entry2.bind(self.entry)

        self.displayLabel3 = Label(self.otherFrame, text = 'Standard Weight Consumed(g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))

        self.entry3 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry3.pack(side = TOP)
        self.entry3.configure(font=("Calibri", 12))
        self.entry3.bind(self.entry)

        self.displayLabel5 = Label(self.otherFrame, text = 'Calories', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel5.pack(side=TOP) 
        self.displayLabel5.config(font=("Calibri", 12))

        self.entry5 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry5.pack(side = TOP)
        self.entry5.configure(font=("Calibri", 12))
        self.entry5.bind(self.entry)

        self.displayLabel6 = Label(self.otherFrame, text = 'Carb (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel6.pack(side=TOP) 
        self.displayLabel6.config(font=("Calibri", 12))

        self.entry6 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry6.pack(side = TOP)
        self.entry6.configure(font=("Calibri", 12))
        self.entry6.bind(self.entry)

        self.displayLabel7 = Label(self.otherFrame, text = 'Protein (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel7.pack(side=TOP) 
        self.displayLabel7.config(font=("Calibri", 12))

        self.entry7 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry7.pack(side = TOP)
        self.entry7.configure(font=("Calibri", 12))
        self.entry7.bind(self.entry)

        self.displayLabel8 = Label(self.otherFrame, text = 'Fat (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel8.pack(side=TOP) 
        self.displayLabel8.config(font=("Calibri", 12))

        self.entry8 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry8.pack(side = TOP)
        self.entry8.configure(font=("Calibri", 12))
        self.entry8.bind(self.entry)

        self.displayLabel9 = Label(self.otherFrame, text = 'Carb per gram (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel9.pack(side=TOP) 
        self.displayLabel9.config(font=("Calibri", 12))

        self.entry9 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry9.pack(side = TOP)
        self.entry9.configure(font=("Calibri", 12))
        self.entry9.bind(self.entry)

        self.displayLabel10 = Label(self.otherFrame, text = 'Protein per gram (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel10.pack(side=TOP) 
        self.displayLabel10.config(font=("Calibri", 12))

        self.entry10 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry10.pack(side = TOP)
        self.entry10.configure(font=("Calibri", 12))
        self.entry10.bind(self.entry)

        self.displayLabel11 = Label(self.otherFrame, text = 'Fat per gram (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel11.pack(side=TOP) 
        self.displayLabel11.config(font=("Calibri", 12))

        self.entry11 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry11.pack(side = TOP)
        self.entry11.configure(font=("Calibri", 12))
        self.entry11.bind(self.entry)

        self.selectButton = Button(self.otherFrame, text = "Add Item", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.entry)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def entry(self):
        invalid = False
        # gets all user inputs from entries
        foodName = self.entry1.get()
        carbProFat = self.entry2.get()
        stndrdWeight = self.entry3.get()
        foodCals = self.entry5.get()
        foodCarb = self.entry6.get()
        foodProtein = self.entry7.get()
        foodFat = self.entry8.get()
        foodCarbGram = self.entry9.get()
        foodProGram = self.entry10.get()
        foodFatGram = self.entry11.get()

        #this block of code reads current ID of what you are entering, and then increements it by 1 for next input.
        foodIDFile = open("NEA_FoodID.txt", "r")  # opens required file in read mode.
        foodID = foodIDFile.readline()  #reads what is there.
        x = int(foodID)  #makes it an integer (so can be incremented, as beforewas string).
        nextFoodID = x+1  #increments.
        foodIDFile.close()  #closes file.
        foodIDFile = open("NEA_FoodID.txt", "w")   #opens file again but in write mode (so previous entry is gone).
        x = str(nextFoodID)  #so it writes next id in it as a string
        foodIDFile.write(x)  #writes it
        foodIDFile.close   #closes it.

        #defensive coding for the inputs, same process as before, adding items to lists for checking that the user entered appropriate datatypes
        #each list for different DT) and making sure they actually entered data.
        #this means they can't break the code and cause it to crash.
        check1 = []
        check1.append(foodName)
        check1.append(carbProFat)
        check1.append(stndrdWeight)
        check1.append(foodCals)
        check1.append(foodCarb)
        check1.append(foodProtein)
        check1.append(foodFat)
        check1.append(foodCarbGram)
        check1.append(foodProGram)
        check1.append(foodFatGram)

        check2 = []
        check2.append(stndrdWeight)
        check2.append(foodCarb)
        check2.append(foodProtein)
        check2.append(foodFat)
        check2.append(foodCarbGram)
        check2.append(foodProGram)
        check2.append(foodFatGram)

        #checking if they entered nothing for an input. If they did invalid is set to true and they have to re-enter information.
        z = 0
        for i in range(len(check1)):
            if len(check1[z]) == 0:
                self.otherFrame.destroy()
                invalid = True
            else:
                z = z+1

        #checking if the inputs which need to be floats are actually floats.
        z = 0
        for i in range(len(check2)):
            try:
                float(check2[z])
            except ValueError:
                self.otherFrame.destroy()
                invalid = True
            z = z+1

        #checking it is an int.
        z = 0
        try:
            int(foodCals)
        except ValueError:
            self.otherFrame.destroy()
            invalid = True

        #if there was at least one invalid input, recreates page object after destroying last, so can renter.
        if invalid == True:
            print("Input was invalid. Please re-enter information.")
            x = UserInsertPageFood(root)
        
        # if they were all valid insert appropriate record into the food database.
        else:
            sql = "insert into Food (FoodID, FoodName, Carb_Pro_Fat, StndrdWeight, FoodCals, FoodCarb, FoodProtein, FoodFat, FoodCarb_gram, FoodProtein_gram, FoodFat_gram) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (foodID, foodName, carbProFat, stndrdWeight, foodCals, foodCarb, foodProtein, foodFat, foodCarbGram, foodProGram, foodFatGram)
            insertItem("Food.db", sql, values)
            if carbProFat.upper() == 'CARB': #if its a carb, insert same thing into carb.
                sql = "insert into Carb (FoodID, FoodName, Carb_Pro_Fat, StndrdWeight, FoodCals, FoodCarb, FoodProtein, FoodFat, FoodCarb_gram, FoodProtein_gram, FoodFat_gram) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (foodID, foodName, carbProFat, stndrdWeight, foodCals, foodCarb, foodProtein, foodFat, foodCarbGram, foodProGram, foodFatGram)
                insertItem("Food.db", sql, values)
            elif carbProFat.upper() == 'PROTEIN': #if protein, insert intp protein.
                sql = "insert into Protein (FoodID, FoodName, Carb_Pro_Fat, StndrdWeight, FoodCals, FoodCarb, FoodProtein, FoodFat, FoodCarb_gram, FoodProtein_gram, FoodFat_gram) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (foodID, foodName, carbProFat, stndrdWeight, foodCals, foodCarb, foodProtein, foodFat, foodCarbGram, foodProGram, foodFatGram)
                insertItem("Food.db", sql, values)
            elif carbProFat.upper() == 'FAT': #if its a fat insert into fat.
                sql = "insert into Fat (FoodID, FoodName, Carb_Pro_Fat, StndrdWeight, FoodCals, FoodCarb, FoodProtein, FoodFat, FoodCarb_gram, FoodProtein_gram, FoodFat_gram) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (foodID, foodName, carbProFat, stndrdWeight, foodCals, foodCarb, foodProtein, foodFat, foodCarbGram, foodProGram, foodFatGram)
                insertItem("Food.db", sql, values)
                
            self.otherFrame.destroy() 
            x = Starter(root)
            s.push(stack, Starter, maxSize, noItems, top)
            

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)


class UserInsertPageMeal2:
    def __init__(self, master, foods, weights):

        self.foods = foods
        self.weights = weights

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = 'Enter name of Meal', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.complete)

        self.finishButton = Button(self.otherFrame, text = "Add Meal", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.complete)
        self.finishButton.pack(side = TOP)
        self.finishButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))
        
        

    def complete(self):
        totalMealCals = 0
        totalMealCarb = 0
        totalMealProtein = 0
        totalMealFat = 0

        #same process as before getting primary key ID and updating it for next input.
        mealIDFile = open("NEA_MealID.txt", "r")
        mealID = mealIDFile.readline()
        x = int(mealID)
        nextMealID = x+1
        mealIDFile.close()
        mealIDFile = open("NEA_MealID.txt", "w")
        x = str(nextMealID)
        mealIDFile.write(x)
        mealIDFile.close
        
        z = 0
        invalid = False
        mealName = self.entry1.get()

        #this for loop runs for every food to be added to the meal.
        for i in range(len (self.foods)):
            db_name = "Food.db"
            food = self.foods[z]
            weight = float(self.weights[z])

            sql = "select StndrdWeight from Food where FoodName=?"   #gets standard weight from its food record.
            tempStndrdWeight = selectItem(db_name, sql, food)
            if tempStndrdWeight == None:   #if food doesnt exist this is true, and so tells the user which food they entered is invalid, and goes back to previous page so they can renter.
                print("Food name", (z+1), "is Invalid")
                self.otherFrame.destroy()
                invalid = True  #so code from this function stops execution.
                break
            else:
                tempStndrdWeight2 = tempStndrdWeight[0]
                stndrdWeight = float(tempStndrdWeight2)   #makes it a float so it can be used in mathematical sums.

                #selects all the values for the food that are needed to be added to the meal from the food database.
                sql = "select FoodCals from Food where FoodName=?"
                tempFoodCals = selectItem(db_name, sql, food)
                foodCals = tempFoodCals[0]
                
                sql = "select FoodCarb from Food where FoodName=?"
                tempFoodCarb = selectItem(db_name, sql, food)
                foodCarb = tempFoodCarb[0]

                sql = "select FoodProtein from Food where FoodName=?"
                tempFoodProtein = selectItem(db_name, sql, food)
                foodProtein = tempFoodProtein[0]

                sql = "select FoodFat from Food where FoodName=?"
                tempFoodFat = selectItem(db_name, sql, food)
                foodFat = tempFoodFat[0]

                ratio = weight/stndrdWeight   #creates the ration of the weight the user wants to what is the standard weight.
                #adjusts calories and macros accordingly.
                newCals = ratio*foodCals
                newCarb = ratio*foodCarb
                newProtein = ratio*foodProtein
                newFat = ratio*foodFat

                #adds new cals and macros to the meal totals.
                totalMealCals += newCals
                totalMealCarb += newCarb
                totalMealProtein += newProtein
                totalMealFat += newFat

                z += 1
        if invalid == False:
            # if all inputs are valid insert the appropriate values into the meal db.
            sql = "insert into Meal (MealID, MealName, MealCals, MealCarb, MealProtein, MealFat) values (?, ?, ?, ?, ?, ?)"
            values = (mealID, mealName, totalMealCals, totalMealCarb, totalMealProtein, totalMealFat)
            insertItem(db_name, sql, values)

            z = 0

            #insert the appropriate values into the foodmeal table for each food in this meal.
            for i in range(len (self.foods)):
                db_name = "Food.db"
                food = self.foods[z]
                weight = float(self.weights[z])

                #select needed values from food db.
                sql = "select FoodID from Food where FoodName=?"
                tempFoodID = selectItem(db_name, sql, food)
                foodID = tempFoodID[0]

                sql = "select StndrdWeight from Food where FoodName=?"
                tempStndrdWeight = selectItem(db_name, sql, food)
                tempStndrdWeight2 = tempStndrdWeight[0]
                stndrdWeight = float(tempStndrdWeight2)

                sql = "select FoodCals from Food where FoodName=?"
                tempFoodCals = selectItem(db_name, sql, food)
                foodCals = tempFoodCals[0]

                sql = "select FoodCarb from Food where FoodName=?"
                tempFoodCarb = selectItem(db_name, sql, food)
                foodCarb = tempFoodCarb[0]

                sql = "select FoodProtein from Food where FoodName=?"
                tempFoodProtein = selectItem(db_name, sql, food)
                foodProtein = tempFoodProtein[0]

                sql = "select FoodFat from Food where FoodName=?"
                tempFoodFat = selectItem(db_name, sql, food)
                foodFat = tempFoodFat[0]

                #work out values for the food in this meal.
                ratio = weight/stndrdWeight
                newCals = ratio*foodCals
                newCarb = ratio*foodCarb
                newProtein = ratio*foodProtein
                newFat = ratio*foodFat

                #convert to strings so can be entered.
                enterCals = str(newCals)
                enterCarb = str(newCarb)
                enterProtein = str(newProtein)
                enterFat = str(newFat)

                #insert the values.
                sql = "insert into FoodMeal (MealID, FoodID, StndrdWeight, FoodCals, FoodCarb, FoodProtein, FoodFat) values (?, ?, ?, ?, ?, ?, ?)"
                values = (mealID, foodID, weight, enterCals, enterCarb, enterProtein, enterFat)
                insertItem(db_name, sql, values)

                z +=1

            self.otherFrame.destroy()        
            x = Starter(root)
            s.top = s.top-1
            s.push(stack, Starter, maxSize, noItems, top)

        if invalid == True:
            # if invalid is true return to beginning of adding a meal process.
            x = UserInsertPageMeal(root, [], [])

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)


        
class UserInsertPageMeal:
    def __init__(self, master, foods, weights):

        self.foods = foods
        self.weights = weights

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = 'Enter name of Food to add to Meal', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.addAnother)

        self.displayLabel2 = Label(self.otherFrame, text = 'Please enter weight (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.displayLabel3 = Label(self.otherFrame, text = 'Weight (g)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))

        self.entry3 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry3.pack(side = TOP)
        self.entry3.configure(font=("Calibri", 12))
        self.entry3.bind(self.addAnother)        

        self.anotherButton = Button(self.otherFrame, text = "Add Another Food", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.addAnother)
        self.anotherButton.pack(side = TOP)
        self.anotherButton.config(font=("Calibri", 12))

        self.finishButton = Button(self.otherFrame, text = "Finish", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.finish)
        self.finishButton.pack(side = TOP)
        self.finishButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))
        

    def addAnother(self):
        invalid = False
        weightCheck = self.entry3.get()
        # checks if the input weight is a float (and hence a valid weight) defensive programming. if it isnt invalid = True
        #(so stops execution before error message), and recalls page with nothing in foods or weights.
        try:
            float(weightCheck)
        except ValueError:
            print("Invalid input, resetting inputs")
            self.otherFrame.destroy()
            invalid = True
            
        if invalid == True:
            x = UserInsertPageMeal(root, [], [])

        #if inputs are valid, checks to see if the food they want to add to the meal has already been added before.
        #Defensive programming to stop having multiple primary keys the same,
        #as primary key is made of foodID and mealID, so if same food added to same meal multiple times, breaks unique constraint.
        if invalid == False:
            tempFood = self.entry1.get()
            if tempFood in self.foods:
                print("Already in Meal, please choose again")
                self.otherFrame.destroy()
                x = UserInsertPageMeal(root, self.foods, self.weights)
            else: #recalls page with updated self.foods and self.weights parameters for what was just added.
                self.foods.append(self.entry1.get())
                self.weights.append(self.entry3.get())
                self.otherFrame.destroy()
                x = UserInsertPageMeal(root, self.foods, self.weights)


    def finish(self):
        invalid = False
        weightCheck = self.entry3.get()
        # checks if the input weight is a float (and hence a valid weight) defensive programming. if it isnt invalid = True
        #(so stops execution before error message), and recalls page with nothing in foods or weights.
        try:
            float(weightCheck)
        except ValueError:
            print("Invalid input, resetting inputs")
            self.otherFrame.destroy()
            invalid = True

        if invalid == True:
            x = UserInsertPageMeal(root, [], [])

        #if inputs are valid, checks to see if the food they want to add to the meal has already been added before.
        #Defensive programming to stop having multiple primary keys the same,
        #as primary key is made of foodID and mealID, so if same food added to same meal multiple times, breaks unique constraint.
        if invalid ==False:
            tempFood = self.entry1.get()
            if tempFood in self.foods:
                print("Already in Meal, please choose again")
                self.otherFrame.destroy()
                x = UserInsertPageMeal(root, self.foods, self.weights)
            else: #proceeds to final part of adding meal on page 2 (above).
                self.foods.append(self.entry1.get())
                self.weights.append(self.entry3.get())
                self.otherFrame.destroy()
                x = UserInsertPageMeal2(root, self.foods, self.weights)
                

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)

        
                                        



#this class is called to display the dailyfoodlog and what is in it. Nothing new to it.
class DailyFoodLogViewer:
    def __init__(self, master, dailyFoodLog, foodLogRecords, mealLogRecords):
        
        self.frame1 = Frame(master)
        self.frame1.pack(side=LEFT)

        self.frame2 = Frame(master)
        self.frame2.pack(side=RIGHT)

        self.frame3 = Frame(master)
        self.frame3.pack(side=RIGHT)

        self.dailyFoodLog = dailyFoodLog
        self.foodLogRecords = foodLogRecords
        self.mealLogRecords = mealLogRecords

        self.displayLabel0 = Label(self.frame1, text = "Daily Totals:", fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel0.pack(side=TOP) 
        self.displayLabel0.config(font=("Calibri", 12))

        self.displayLabel = Label(self.frame1, text = self.dailyFoodLog, fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))
        
        self.displayLabel2 = Label(self.frame1, text = "Food Eaten Today:", fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.displayLabel3 = Label(self.frame1, text = self.foodLogRecords, fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))
        
        self.displayLabel4 = Label(self.frame1, text = "Meals Eaten Today:", fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel4.pack(side=TOP) 
        self.displayLabel4.config(font=("Calibri", 12))

        self.displayLabel5 = Label(self.frame1, text = self.mealLogRecords, fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel5.pack(side=TOP) 
        self.displayLabel5.config(font=("Calibri", 12))

        self.homeButton = Button(self.frame1, text = "Home", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.home)
        self.homeButton.pack(side = BOTTOM)
        self.homeButton.config(font=("Calibri", 12))

        self.backButton = Button(self.frame1, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.frame1, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

        print("\n\n", self.dailyFoodLog,"\n\n")
        print("\n\n", self.foodLogRecords,"\n\n")
        print("\n\n", self.mealLogRecords,"\n\n")

    def home(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        x = Starter(root)
        s.top = s.top-1
        s.push(stack, Starter, maxSize, noItems, top)
        

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()
            x = xD(root)


   

class DailyFoodLogViewDay:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = "Enter date (d/m/yyyy, dd/mm/yyyy etc.)", fg = "white", bg = "sky blue", width = 31, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry.pack(side = TOP)
        self.entry.configure(font=("Calibri", 12))
        self.entry.bind(self.view)        

        self.continueButton = Button(self.otherFrame, text = "View", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.view)
        self.continueButton.pack(side = TOP)
        self.continueButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def view(self):
        s.top = s.top+1
        #this function is ran if there has been no food entered on that day
        def noFood():
            DEFAULT = 'None'
            mealLogID = []
            sql = "select MealLogID from MealLog where LogID=?"
            values = (logID)
            mealLogIDtemp = selectAllItems2(db_name, sql, values)  #the id's returned are the mealLog id's for that logID (day)
            test = str(mealLogIDtemp)
            if test == '[]':   #if nothing is returned (ie no meals today), the viewer page is called with 'None' in the place where food and meals should be.
                    self.otherFrame.destroy()
                    x = DailyFoodLogViewer(root, dailyFoodLog, DEFAULT, DEFAULT)
                    
            else:
                #else append the meal log IDs. Then get the first and last log id numbers.
                #make current log and id = to the first log id, and make them both integers (so can be compared as numbers).
                mealLogID.append(mealLogIDtemp)
                firstLogID = mealLogID[0][0][0]
                tempLastLogID = mealLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                mealLogRecords = []
                # this is all done so the below runs the correct number of times (as many as there are logs for that day).
                while currentLogID <= lastLogID:
                    sql = "select Time, MealName, MealServ, MealCals, MealCarb, MealProtein, MealFat from MealLog where MealLogID=?"
                    values = currentLogID
                    mealLogRecord = selectItem(db_name, sql, values)
                    #the record is added to the list of records, which, when finished, is what is displayed to the user.
                    mealLogRecords.append(mealLogRecord)
                    currentLogID += 1

                self.otherFrame.destroy()
                x = DailyFoodLogViewer(root, dailyFoodLog, DEFAULT, mealLogRecords)
        invalid = False
        DEFAULT = "None"
        no_food = False

        date = self.entry.get()
        
        sql = "select Date, TotalCals, TotalCarb, TotalProtein, TotalFat, CalsRemaining, CarbRemaining, FatRemaining, ProteinRemaining from DailyFoodLog where Date=?"
        values = (date)
        db_name = "Food.db"
        dailyFoodLog = selectItem(db_name, sql, values)
        # if this is none it means no record with that date could be found, so it handles the error and recalls the page.
        if dailyFoodLog == None:
            print("Invalid date")
            self.otherFrame.destroy()
            invalid = True
        else:
            #selects appropraite logID for that day.
            sql = "select LogID from DailyFoodLog where Date=?"
            tempLogID = selectItem(db_name, sql, values)
            logID = tempLogID[0]
            
            foodLogID = []
            sql = "select FoodLogID from FoodLog where LogID=?"
            values = (logID)
            foodLogIDtemp = selectAllItems2(db_name, sql, values) #the id's returned are the foodLog id's for that logID (day)
            test = str(foodLogIDtemp)
            if test == '[]':  #if nothing is returned (ie no food today), no_food becomes true so the correct function is called later.
                noFood()
                no_food = True
            else:
                #else append the food log IDs. Then get the first and last log id numbers.
                #make current log and id = to the first log id, and make them both integers (so can be compared as numbers).
                foodLogID.append(foodLogIDtemp)
                firstLogID = foodLogID[0][0][0]
                tempLastLogID = foodLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                foodLogRecords = []
                # this is all done so the below runs the correct number of times (as many as there are logs for that day).
                while currentLogID <= lastLogID:
                    sql = "select Time, FoodName, FoodServ, FoodCals, FoodCarb, FoodProtein, FoodFat from FoodLog where FoodLogID=?"
                    values = (currentLogID)
                    foodLogRecord = selectItem(db_name, sql, values)
                    #the record is added to the list of records, which, when finished, is what is displayed to the user.
                    foodLogRecords.append(foodLogRecord)
                    currentLogID += 1

        #if there is food and food entries were valid
        if no_food == False and invalid == False:
            mealLogID = []
            sql = "select MealLogID from MealLog where LogID=?"
            values = (logID)
            mealLogIDtemp = selectAllItems2(db_name, sql, values)  #the id's returned are the mealLog id's for that logID (day)
            test = str(mealLogIDtemp)
            if test == '[]':  #if nothing is returned (ie no meals today), the viewer page is called with 'None' in the place where meals should be.
                    self.otherFrame.destroy()
                    x = DailyFoodLogViewer(root, dailyFoodLog, foodLogRecords, DEFAULT)
            else:
                #else append the meal log IDs. Then get the first and last log id numbers. make current log and id = to the first log id, and make them both integers (so can be compared as numbers).
                mealLogID.append(mealLogIDtemp)
                firstLogID = mealLogID[0][0][0]
                tempLastLogID = mealLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                mealLogRecords = []
                # this is all done so the below runs the correct number of times (as many as there are logs for that day).
                while currentLogID <= lastLogID:
                    sql = "select Time, MealName, MealServ, MealCals, MealCarb, MealProtein, MealFat from MealLog where MealLogID=?"
                    values = currentLogID
                    mealLogRecord = selectItem(db_name, sql, values)
                    #the record is added to the list of records, which, when finished, is what is displayed to the user.
                    mealLogRecords.append(mealLogRecord)
                    currentLogID += 1

                self.otherFrame.destroy()
                x = DailyFoodLogViewer(root, dailyFoodLog, foodLogRecords, mealLogRecords)

        if invalid == True:
            #if it's invalid call the page again.
            x = DailyFoodLogViewDay(root)
            s.top = s.top-1

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
        



class DailyFoodLogAddFood:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = "Enter Food to Add", fg = "white", bg = "sky blue", width = 21, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry.pack(side = TOP)
        self.entry.configure(font=("Calibri", 12))
        self.entry.bind(self.add)

        self.displayLabel2 = Label(self.otherFrame, text = "Enter Portion (number of x normal portion)", fg = "white", bg = "sky blue", width = 41, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.entry2 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry2.pack(side = TOP)
        self.entry2.configure(font=("Calibri", 12))
        self.entry2.bind(self.add)      

        self.addButton = Button(self.otherFrame, text = "Add", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.add)
        self.addButton.pack(side = TOP)
        self.addButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def add(self):
        invalid = False
        
        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))
        foodName = self.entry.get()
        tempPortion = self.entry2.get()
        #if not float, print invalid and recall the page. defensive programming.
        try:
            float(tempPortion)
        except ValueError:
            print("Invalid Input, resetting inputs")
            self.otherFrame.destroy()
            invalid = True
            
            
        if invalid == False:
            portion = float(tempPortion)
            db_name = "Food.db"
            sql = "select FoodID, FoodCals, FoodCarb, FoodProtein, FoodFat from Food where FoodName=?"
            values = (foodName)
            foodVals = selectItem(db_name, sql, values)

            #runs if nothing is returned (ie  input food does not exist in food db). defensive programming.
            if foodVals == None:
                print("Invalid Entry")
                self.otherFrame.destroy()
                invalid = True

            else:
                # sets inputs to correct data types and multiplies them by portion to work out correct amounts.
                foodID = foodVals[0]
                tempFoodCals = foodVals[1]
                tempFoodCals2 = int(tempFoodCals)
                foodCalsNearlyThere = tempFoodCals2*portion
                foodCals = int(foodCalsNearlyThere)
                tempFoodCarb = foodVals[2]
                tempFoodCarb2 = float(tempFoodCarb)
                foodCarb = (tempFoodCarb2*portion)
                tempFoodProtein = foodVals[3]
                tempFoodProtein2 = float(tempFoodProtein)
                foodProtein = tempFoodProtein2*portion
                tempFoodFat = foodVals[4]
                tempFoodFat2 = float(tempFoodFat)
                foodFat = tempFoodFat2*portion


                #selects all the fields needed from the dailyfoodlog record so can update with new values.
                sql = "select TotalCals, TotalCarb, TotalProtein, TotalFat, CalsRemaining, CarbRemaining, FatRemaining, ProteinRemaining from DailyFoodLog where Date=?"
                values = (date)
                beforeAddVals = selectItem(db_name, sql, values)
                tempBeforeCals = beforeAddVals[0]
                beforeCals = int(tempBeforeCals)
                tempBeforeCarb = beforeAddVals[1]
                beforeCarb = float(tempBeforeCarb)
                tempBeforeProtein = beforeAddVals[2]
                beforeProtein = float(tempBeforeProtein)
                tempBeforeFat = beforeAddVals[3]
                beforeFat = float(tempBeforeFat)
                tempBeforeCalsRem = beforeAddVals[4]
                beforeCalsRem = int(tempBeforeCalsRem)
                tempBeforeCarbRem = beforeAddVals[5]
                beforeCarbRem = float(tempBeforeCarbRem)
                tempBeforeFatRem = beforeAddVals[6]
                beforeFatRem = float(tempBeforeFatRem)
                tempBeforeProteinRem = beforeAddVals[7]
                beforeProteinRem = float(tempBeforeProteinRem)

                #calculating new values
                newCals = beforeCals + foodCals
                newCarb = beforeCarb + foodCarb
                newProtein = beforeProtein + foodProtein
                newFat = beforeFat + foodFat
                newCalsRem = beforeCalsRem - foodCals
                newCarbRem = beforeCarbRem - foodCarb
                newFatRem = beforeFatRem - foodFat
                newProteinRem = beforeProteinRem - foodProtein
                
                #updating db's.
                sql = "update DailyFoodLog set TotalCals=?, TotalCarb=?, TotalProtein=?, TotalFat=?, CalsRemaining=?, CarbRemaining=?, FatRemaining=?, ProteinRemaining=?"
                values = (newCals, newCarb, newProtein, newFat, newCalsRem, newCarbRem, newFatRem, newProteinRem)
                updateItem(db_name, sql, values)

                db_name = "Exercise.db"
                sql = "update DailyExerciseLog set CalsRemaining=?"
                values = (newCalsRem,)
                updateItem(db_name, sql, values)

                

                
                db_name = "Food.db"
                sql = "select LogID from DailyFoodLog where date=?"
                values = (date)
                tempLogID = selectItem(db_name, sql, values)
                logID = tempLogID[0]
                
                #gets primary key of foodLogID and increments for next time.
                foodLogIDFile = open("NEA_FoodLogID.txt", "r")
                foodLogID = foodLogIDFile.readline()
                x = int(foodLogID)
                nextFoodLogID = x+1
                foodLogIDFile.close()
                foodLogIDFile = open("NEA_FoodLogID.txt", "w")
                x = str(nextFoodLogID)
                foodLogIDFile.write(x)
                foodLogIDFile.close

                now = datetime.now()
                time = ("%s:%s" % (now.hour, now.minute))
                
                #inserts new data into foodLog
                sql = "insert into FoodLog (FoodLogID, LogID, FoodID, Time, FoodName, FoodServ, FoodCals, FoodCarb, FoodProtein, FoodFat) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (foodLogID, logID, foodID, time, foodName, portion, foodCals, foodCarb, foodProtein, foodFat)
                insertItem(db_name, sql, values)


                self.otherFrame.destroy()
                x = Starter(root)
                s.push(stack, Starter, maxSize, noItems, top)

        #if any input data was incorrect, will run this instead of running db related code.
        if invalid == True:
            x = DailyFoodLogAddFood(root)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
            





class DailyFoodLogAddMeal:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = "Enter Meal to Add", fg = "white", bg = "sky blue", width = 21, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry.pack(side = TOP)
        self.entry.configure(font=("Calibri", 12))
        self.entry.bind(self.add)

        self.displayLabel2 = Label(self.otherFrame, text = "Enter Portion (number of x normal portion)", fg = "white", bg = "sky blue", width = 41, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.entry2 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry2.pack(side = TOP)
        self.entry2.configure(font=("Calibri", 12))
        self.entry2.bind(self.add)      

        self.addButton = Button(self.otherFrame, text = "Add", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.add)
        self.addButton.pack(side = TOP)
        self.addButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def add(self):
        invalid = False
        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))
        mealName = self.entry.get()
        tempPortion = self.entry2.get()

        #if not float, print invalid and recall the page. defensive programming.
        try:
            float(tempPortion)
        except ValueError:
            print("Invalid Input, resetting inputs")
            self.otherFrame.destroy()
            invalid = True

        if invalid == False:
            portion = float(tempPortion)
            db_name = "Food.db"
            sql = "select MealID, MealCals, MealCarb, MealProtein, MealFat from Meal where MealName=?"
            values = (mealName)
            mealVals = selectItem(db_name, sql, values)
            
            #runs if nothing is returned (ie  input meal does not exist in meal db). defensive programming.
            if mealVals == None:
                print("Invalid Entry")
                self.otherFrame.destroy()
                invalid = True

            else:
                # sets returned values to correct data types and multiplies them by portion to work out correct amounts.
                mealID = mealVals[0]
                tempMealCals = mealVals[1]
                tempMealCals2 = int(tempMealCals)
                mealCals = tempMealCals2*portion
                tempMealCarb = mealVals[2]
                tempMealCarb2 = float(tempMealCarb)
                mealCarb = (tempMealCarb2*portion)
                tempMealProtein = mealVals[3]
                tempMealProtein2 = float(tempMealProtein)
                mealProtein = tempMealProtein2*portion
                tempMealFat = mealVals[4]
                tempMealFat2 = float(tempMealFat)
                mealFat = tempMealFat2*portion
                

                #selects all the fields needed from the dailyfoodlog record so can update with new values.
                sql = "select TotalCals, TotalCarb, TotalProtein, TotalFat, CalsRemaining, CarbRemaining, FatRemaining, ProteinRemaining from DailyFoodLog where Date=?"
                values = (date)
                beforeAddVals = selectItem(db_name, sql, values)
                tempBeforeCals = beforeAddVals[0]
                beforeCals = int(tempBeforeCals)
                tempBeforeCarb = beforeAddVals[1]
                beforeCarb = float(tempBeforeCarb)
                tempBeforeProtein = beforeAddVals[2]
                beforeProtein = float(tempBeforeProtein)
                tempBeforeFat = beforeAddVals[3]
                beforeFat = float(tempBeforeFat)
                tempBeforeCalsRem = beforeAddVals[4]
                beforeCalsRem = int(tempBeforeCalsRem)
                tempBeforeCarbRem = beforeAddVals[5]
                beforeCarbRem = float(tempBeforeCarbRem)
                tempBeforeFatRem = beforeAddVals[6]
                beforeFatRem = float(tempBeforeFatRem)
                tempBeforeProteinRem = beforeAddVals[7]
                beforeProteinRem = float(tempBeforeProteinRem)

                #calculating new values
                newCals = beforeCals + mealCals
                newCarb = beforeCarb + mealCarb
                newProtein = beforeProtein + mealProtein
                newFat = beforeFat + mealFat
                newCalsRem = beforeCalsRem - mealCals
                newCarbRem = beforeCarbRem - mealCarb
                newFatRem = beforeFatRem - mealFat
                newProteinRem = beforeProteinRem - mealProtein 

                #updating db's.
                sql = "update DailyFoodLog set TotalCals=?, TotalCarb=?, TotalProtein=?, TotalFat=?, CalsRemaining=?, CarbRemaining=?, FatRemaining=?, ProteinRemaining=?"
                values = (newCals, newCarb, newProtein, newFat, newCalsRem, newCarbRem, newFatRem, newProteinRem)
                updateItem(db_name, sql, values)

                sql = "update DailyExerciseLog set CalsRemaining=?"
                values = (newCalsRem,)
                db_name = "Exercise.db"
                updateItem(db_name, sql, values)
                


                db_name = "Food.db"
                sql = "select LogID from DailyFoodLog where date=?"
                values = (date)
                tempLogID = selectItem(db_name, sql, values)
                logID = tempLogID[0]

                #gets primary key of mealLogID and increments for next time.
                mealLogIDFile = open("NEA_MealLogID.txt", "r")
                mealLogID = mealLogIDFile.readline()
                x = int(mealLogID)
                nextMealLogID = x+1
                mealLogIDFile.close()
                mealLogIDFile = open("NEA_MealLogID.txt", "w")
                x = str(nextMealLogID)
                mealLogIDFile.write(x)
                mealLogIDFile.close

                now = datetime.now()
                time = ("%s:%s" % (now.hour, now.minute))
                
                #inserts new data into mealLog
                sql = "insert into MealLog (MealLogID, LogID, MealID, Time, MealName, MealServ, MealCals, MealCarb, MealProtein, MealFat) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                values = (mealLogID, logID, mealID, time, mealName, portion, mealCals, mealCarb, mealProtein, mealFat)
                insertItem(db_name, sql, values)


                self.otherFrame.destroy()
                x = Starter(root)
                s.push(stack, Starter, maxSize, noItems, top)
    
        #if any input data was incorrect, will run this instead of running db related code.
        if invalid == True:
            x = DailyFoodLogAddMeal(root)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
            
        
        
        


class FoodLogHub:
    def __init__(self, master):

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.viewTodayButton = Button(self.otherFrame, text = "View Today", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.viewToday)
        self.viewTodayButton.pack(side = TOP)
        self.viewTodayButton.config(font=("Calibri", 12))

        self.viewDayButton = Button(self.otherFrame, text = "View a Date", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.viewDay)
        self.viewDayButton.pack(side = TOP)
        self.viewDayButton.config(font=("Calibri", 12))

        self.insertMealButton = Button(self.otherFrame, text = "Add Meal", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.addMeal)
        self.insertMealButton.pack(side = TOP)
        self.insertMealButton.config(font=("Calibri", 12))

        self.insertFoodButton = Button(self.otherFrame, text = "Add Food", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.addFood)
        self.insertFoodButton.pack(side = TOP)
        self.insertFoodButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    #this function is the same as the DailyFoodLogViewDay above, just without the user inputs and hence without the error checking due to that.
    def viewToday(self):
        s.top = s.top+1
        def noFood():
            DEFAULT = 'None'
            mealLogID = []
            sql = "select MealLogID from MealLog where LogID=?"
            values = (logID)
            mealLogIDtemp = selectAllItems2(db_name, sql, values)
            test = str(mealLogIDtemp)
            if test == '[]':
                    self.otherFrame.destroy()
                    x = DailyFoodLogViewer(root, dailyFoodLog, DEFAULT, DEFAULT)
                    
            else:
                mealLogID.append(mealLogIDtemp)
                firstLogID = mealLogID[0][0][0]
                tempLastLogID = mealLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                mealLogRecords = []
                while currentLogID <= lastLogID:
                    sql = "select Time, MealName, MealServ, MealCals, MealCarb, MealProtein, MealFat from MealLog where MealLogID=?"
                    values = currentLogID
                    mealLogRecord = selectItem(db_name, sql, values)
                    if mealLogRecord is None:
                        raise ValueError("Not Found")
                        break
                    else:
                        mealLogRecords.append(mealLogRecord)
                        currentLogID += 1

                self.otherFrame.destroy()
                x = DailyFoodLogViewer(root, dailyFoodLog, DEFAULT, mealLogRecords)
        
        DEFAULT = "None"
        no_food = False

        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))
        
        sql = "select Date, TotalCals, TotalCarb, TotalProtein, TotalFat, CalsRemaining, CarbRemaining, FatRemaining, ProteinRemaining from DailyFoodLog where Date=?"
        values = (date)
        db_name = "Food.db"
        dailyFoodLog = selectItem(db_name, sql, values)
        sql = "select LogID from DailyFoodLog where Date=?"
        tempLogID = selectItem(db_name, sql, values)
        logID = tempLogID[0]
        
        foodLogID = []
        sql = "select FoodLogID from FoodLog where LogID=?"
        values = (logID)
        foodLogIDtemp = selectAllItems2(db_name, sql, values)
        test = str(foodLogIDtemp)
        if test == '[]':
            noFood()
            no_food = True
        else:
            foodLogID.append(foodLogIDtemp)
            firstLogID = foodLogID[0][0][0]
            tempLastLogID = foodLogID[0][-1][0]
            lastLogID = int(tempLastLogID)
            currentLogID = int(firstLogID)
            foodLogRecords = []
            while currentLogID <= lastLogID:
                sql = "select Time, FoodName, FoodServ, FoodCals, FoodCarb, FoodProtein, FoodFat from FoodLog where FoodLogID=?"
                values = (currentLogID)
                foodLogRecord = selectItem(db_name, sql, values)
                if foodLogRecord is None:
                    raise ValueError("Not Found")
                    break
                else:
                    foodLogRecords.append(foodLogRecord)
                    currentLogID += 1

        if no_food == False:
            mealLogID = []
            sql = "select MealLogID from MealLog where LogID=?"
            values = (logID)
            mealLogIDtemp = selectAllItems2(db_name, sql, values)
            test = str(mealLogIDtemp)
            if test == '[]':
                    self.otherFrame.destroy()
                    x = DailyFoodLogViewer(root, dailyFoodLog, foodLogRecords, DEFAULT)
            else:
                mealLogID.append(mealLogIDtemp)
                firstLogID = mealLogID[0][0][0]
                tempLastLogID = mealLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                mealLogRecords = []
                while currentLogID <= lastLogID:
                    sql = "select Time, MealName, MealServ, MealCals, MealCarb, MealProtein, MealFat from MealLog where MealLogID=?"
                    values = currentLogID
                    mealLogRecord = selectItem(db_name, sql, values)
                    if mealLogRecord is None:
                        raise ValueError("Not Found")
                        break
                    else:
                        mealLogRecords.append(mealLogRecord)
                        currentLogID += 1

                self.otherFrame.destroy()
                x = DailyFoodLogViewer(root, dailyFoodLog, foodLogRecords, mealLogRecords)

    def viewDay(self):
        self.otherFrame.destroy()
        x = DailyFoodLogViewDay(root)
        s.push(stack, DailyFoodLogViewDay, maxSize, noItems, top)

    def addMeal(self):
        self.otherFrame.destroy()
        x = DailyFoodLogAddMeal(root)
        s.push(stack, DailyFoodLogAddMeal, maxSize, noItems, top)

    def addFood(self):
        self.otherFrame.destroy()
        x = DailyFoodLogAddFood(root)
        s.push(stack, DailyFoodLogAddFood, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
        
        
        

#very closely related to UserInsertPageFood, error checking methods very closely related and how they work is similar
#(just diffrent variables etc depending on what is input to respective db's).
class UserInsertPageExercise:
    def __init__(self, master):

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = 'Exercise Name', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.entry)

        self.displayLabel2 = Label(self.otherFrame, text = 'Muscle Group', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.entry2 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry2.pack(side = TOP)
        self.entry2.configure(font=("Calibri", 12))
        self.entry2.bind(self.entry)

        self.displayLabel3 = Label(self.otherFrame, text = 'Weight (kg)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))

        self.entry3 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry3.pack(side = TOP)
        self.entry3.configure(font=("Calibri", 12))
        self.entry3.bind(self.entry)

        self.displayLabel4 = Label(self.otherFrame, text = 'Reps', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel4.pack(side=TOP) 
        self.displayLabel4.config(font=("Calibri", 12))

        self.entry4 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry4.pack(side = TOP)
        self.entry4.configure(font=("Calibri", 12))
        self.entry4.bind(self.entry)

        self.displayLabel5 = Label(self.otherFrame, text = 'Sets', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel5.pack(side=TOP) 
        self.displayLabel5.config(font=("Calibri", 12))

        self.entry5 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry5.pack(side = TOP)
        self.entry5.configure(font=("Calibri", 12))
        self.entry5.bind(self.entry)

        self.displayLabel6 = Label(self.otherFrame, text = 'Calories Burned', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel6.pack(side=TOP) 
        self.displayLabel6.config(font=("Calibri", 12))

        self.entry6 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry6.pack(side = TOP)
        self.entry6.configure(font=("Calibri", 12))
        self.entry6.bind(self.entry)

        self.selectButton = Button(self.otherFrame, text = "Add Item", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.entry)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))


    def entry(self):
        invalid = False
        #getting user inputs.
        exerciseName = self.entry1.get()
        muscleGroup = self.entry2.get()
        weight = self.entry3.get()
        reps = self.entry4.get()
        sets = self.entry5.get()
        calsBurned = self.entry6.get()

        #getting primary key ID and incrementing.
        exerciseIDFile = open("NEA_ExerciseID.txt", "r")
        exerciseID = exerciseIDFile.readline()
        x = int(exerciseID)
        nextExerciseID = x+1
        exerciseIDFile.close()
        exerciseIDFile = open("NEA_ExerciseID.txt", "w")
        x = str(nextExerciseID)
        exerciseIDFile.write(x)
        exerciseIDFile.close


        check1 = []
        check1.append(exerciseName)
        check1.append(muscleGroup)
        check1.append(weight)
        check1.append(reps)
        check1.append(sets)
        check1.append(calsBurned)

        check2 = []
        check2.append(reps)
        check2.append(sets)
        check2.append(calsBurned)
        

        #usual error checking as seen above, checking if inputs are empty, and are of correct datatypes.
        # if anything is not as is wanted, invalid becomes true and execution of this function is halted and the page object is recreated for the user.
        z = 0
        for i in range(len(check1)):
            if len(check1[z]) == 0:
                self.otherFrame.destroy()
                invalid = True
            else:
                z = z+1

        z = 0
        for i in range(len(check2)):
            try:
                int(check2[z])
            except ValueError:
                self.otherFrame.destroy()
                invalid = True
            z = z+1

        z = 0
        try:
            float(weight)
        except ValueError:
            self.otherFrame.destroy()
            invalid = True
        
        if invalid == True:
            print("Input was invalid. Please re-enter information.")
            x = UserInsertPageExercise(root)

        
        else:
            #inserting necessary information into exercise db.
            sql = "insert into Exercise (ExerciseID, ExerciseName, MuscleGroup, Weight, Reps, Sets, CalsBurned) values (?, ?, ?, ?, ?, ?, ?)"
            values = (exerciseID, exerciseName, muscleGroup, weight, reps, sets, calsBurned)
            insertItem("Exercise.db", sql, values)

            self.otherFrame.destroy()
            x = Starter(root)
            s.push(stack, Starter, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
            

#very similar to UserInsertPageMeal2
class UserInsertPageWorkoutPlans2:
    def __init__(self, master, exercises):

        self.exercises = exercises

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = 'Enter name of Workout Plan', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.complete)

        self.finishButton = Button(self.otherFrame, text = "Add Workout Plan", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.complete)
        self.finishButton.pack(side = TOP)
        self.finishButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))
        

    def complete(self):
        #gets workoutID and increments for next time.
        workoutIDFile = open("NEA_WorkoutID.txt", "r")
        workoutID = workoutIDFile.readline()
        x = int(workoutID)
        nextWorkoutID = x+1
        workoutIDFile.close()
        workoutIDFile = open("NEA_WorkoutID.txt", "w")
        x = str(nextWorkoutID)
        workoutIDFile.write(x)
        workoutIDFile.close
        
        z = 0
        invalid = False
        totalWorkoutCals = 0
        workoutName = self.entry1.get()
        
        #runs as many times as there are exercises, and selects the cals burned for each exercise and sums them together to get total cals burned.
        for i in range(len (self.exercises)):
            db_name = "Exercise.db"
            exercise = self.exercises[z]

            sql = "select CalsBurned from Exercise where ExerciseName=?"
            tempCals = selectItem(db_name, sql, exercise)

            #defensive programming - if exercise doesn't exist halt current program execution by making invalid true, and re-calling the page later if invalid is true.
            if tempCals == None:  
                print("Exercise", (z+1), "doesn't exist")
                self.otherFrame.destroy()
                invalid = True
                break
            else:
                tempCals2 = tempCals[0]
                calsBurned = float(tempCals2)

                totalWorkoutCals += calsBurned

                z += 1
        if invalid == False:
            # if all inputs are valid insert the appropriate values into the workoutplans db.
            sql = "insert into WorkoutPlans (WorkoutID, WorkoutName, WorkoutCalsBurned) values (?, ?, ?)"
            values = (workoutID, workoutName, totalWorkoutCals)
            insertItem(db_name, sql, values)

            z = 0

            #insert the appropriate values into the foodmeal table for each food in this meal.
            for i in range(len (self.exercises)):
                db_name = "Exercise.db"
                exercise = self.exercises[z]

                #select needed values from exercise db.
                sql = "select ExerciseID from Exercise where ExerciseName=?"
                tempExerciseID = selectItem(db_name, sql, exercise)
                exerciseID = tempExerciseID[0] #as tuple is returned.

                sql = "select MuscleGroup from Exercise where ExerciseName=?"
                tempMuscleGroup = selectItem(db_name, sql, exercise)
                muscleGroup = tempMuscleGroup[0]

                sql = "select Weight from Exercise where ExerciseName=?"
                tempWeight = selectItem(db_name, sql, exercise)
                weight = tempWeight[0]

                sql = "select Reps from Exercise where ExerciseName=?"
                tempReps = selectItem(db_name, sql, exercise)
                reps = tempReps[0]

                sql = "select Sets from Exercise where ExerciseName=?"
                tempSets = selectItem(db_name, sql, exercise)
                sets = tempSets[0]

                sql = "select CalsBurned from Exercise where ExerciseName=?"
                tempCals = selectItem(db_name, sql, exercise)
                tempCals2 = tempCals[0]
                calsBurned = float(tempCals2)

                #insert the values.
                sql = "insert into ExerciseWorkout (WorkoutID, ExerciseID, ExerciseName, MuscleGroup, Weight, Reps, Sets, CalsBurned) values (?, ?, ?, ?, ?, ?, ?, ?)"
                values = (workoutID, exerciseID, exercise, muscleGroup, weight, reps, sets, calsBurned)
                insertItem(db_name, sql, values)

                z += 1


            self.otherFrame.destroy()        
            x = Starter(root)
            s.top = s.top-1
            s.push(stack, Starter, maxSize, noItems, top)

        if invalid == True:
            # if invalid is true return to beginning of adding a workoutplan process.
            x = UserInsertPageWorkoutPlans(root, [])

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
            

#very similar once again to UserInsertPageMeal
class UserInsertPageWorkoutPlans:
    def __init__(self, master, exercises):

        self.exercises = exercises

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = 'Enter name of Exercise to add to Workout Plan', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.addAnother)

        self.anotherButton = Button(self.otherFrame, text = "Add Another Exercise", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.addAnother)
        self.anotherButton.pack(side = TOP)
        self.anotherButton.config(font=("Calibri", 12))

        self.finishButton = Button(self.otherFrame, text = "Finish", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.finish)
        self.finishButton.pack(side = TOP)
        self.finishButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def addAnother(self):
        tempExercise = self.entry1.get()
        #if inputs are valid, checks to see if the exercise they want to add to the workout has already been added before.
        #Defensive programming to stop having multiple primary keys the same,
        #as primary key is made of exerciseID and workoutID, so if same exercise added to same workout multiple times, breaks unique constraint.
        if tempExercise in self.exercises:
            print("Already in Workout Plan, please choose again")
            self.otherFrame.destroy()
            x = UserInsertPageWorkoutPlans(root, self.exercises)
        else:
            self.exercises.append(self.entry1.get())
            self.otherFrame.destroy()
            x = UserInsertPageWorkoutPlans(root, self.exercises)

    def finish(self):
        tempExercise = self.entry1.get()
        #if inputs are valid, checks to see if the exercise they want to add to the workout has already been added before.
        #Defensive programming to stop having multiple primary keys the same,
        #as primary key is made of exerciseID and workoutID, so if same exercise added to same workout multiple times, breaks unique constraint.
        if tempExercise in self.exercises:
            print("Already in Workout Plan, please choose again")
            self.otherFrame.destroy()
            x = UserInsertPageWorkoutPlans(root, self.exercises)
        else:
            self.exercises.append(self.entry1.get())
            self.otherFrame.destroy()
            x = UserInsertPageWorkoutPlans2(root, self.exercises)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)




#this class is called to display the dailyexerciselog and what is in it. Nothing new to it.
class DailyExerciseLogViewer:
    def __init__(self, master, dailyExerciseLog, exerciseLogRecords, workoutLogRecords):
        
        self.frame1 = Frame(master)
        self.frame1.pack(side=LEFT)

        self.frame2 = Frame(master)
        self.frame2.pack(side=RIGHT)

        self.frame3 = Frame(master)
        self.frame3.pack(side=RIGHT)

        self.dailyExerciseLog = dailyExerciseLog
        self.exerciseLogRecords = exerciseLogRecords
        self.workoutLogRecords = workoutLogRecords

        self.displayLabel0 = Label(self.frame1, text = "Daily Totals:", fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel0.pack(side=TOP) 
        self.displayLabel0.config(font=("Calibri", 12))

        self.displayLabel = Label(self.frame1, text = self.dailyExerciseLog, fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))
        
        self.displayLabel2 = Label(self.frame1, text = "Exercise(s) Performed Today:", fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.displayLabel3 = Label(self.frame1, text = self.exerciseLogRecords, fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))
        
        self.displayLabel4 = Label(self.frame1, text = "Workout(s) Completed Today:", fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel4.pack(side=TOP) 
        self.displayLabel4.config(font=("Calibri", 12))

        self.displayLabel5 = Label(self.frame1, text = self.workoutLogRecords, fg = "white", bg = "sky blue", width = 66, height = 1)
        self.displayLabel5.pack(side=TOP) 
        self.displayLabel5.config(font=("Calibri", 12))

        self.homeButton = Button(self.frame1, text = "Home", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.home)
        self.homeButton.pack(side = BOTTOM)
        self.homeButton.config(font=("Calibri", 12))

        self.backButton = Button(self.frame1, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.frame1, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

        print("\n\n", self.dailyExerciseLog,"\n\n")
        print("\n\n", self.exerciseLogRecords,"\n\n")
        print("\n\n", self.workoutLogRecords,"\n\n")

    def home(self):
        self.frame1.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        x = Starter(root)
        s.top = s.top-1
        s.push(stack, Starter, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.frame1.destroy()
            self.frame2.destroy()
            self.frame3.destroy()
            x = xD(root)




class DailyExerciseLogViewDay:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = "Enter date (d/m/yyyy, dd/mm/yyyy etc.)", fg = "white", bg = "sky blue", width = 31, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry.pack(side = TOP)
        self.entry.configure(font=("Calibri", 12))
        self.entry.bind(self.view)        

        self.continueButton = Button(self.otherFrame, text = "View", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.view)
        self.continueButton.pack(side = TOP)
        self.continueButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def view(self):
        s.top = s.top+1
        #this function is ran if there has been no exercise entered on that day
        def noExercise():
            DEFAULT = 'None'
            workoutLogID = []
            sql = "select WorkoutLogID from WorkoutExerciseLog where LogID=?"
            values = (logID)
            workoutLogIDtemp = selectAllItems2(db_name, sql, values) #the id's returned are the workoutLog id's for that logID (day)
            test = str(workoutLogIDtemp)
            if test == '[]':   #if nothing is returned (ie no workouts today), the viewer page is called with 'None' in the place where exercise and workouts should be.
                    self.otherFrame.destroy()
                    x = DailyExerciseLogViewer(root, dailyExerciseLog, DEFAULT, DEFAULT)
                    
            else:
                #else append the workout log IDs. Then get the first and last log id numbers.
                #make current log and id = to the first log id, and make them both integers (so can be compared as numbers).
                workoutLogID.append(workoutLogIDtemp)
                firstLogID = workoutLogID[0][0][0]
                tempLastLogID = workoutLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                workoutLogRecords = []
                # this is all done so the below runs the correct number of times (as many as there are logs for that day).
                while currentLogID <= lastLogID:
                    sql = "select Time, WorkoutName, CalsBurned from WorkoutExerciseLog where WorkoutLogID=?"
                    values = currentLogID
                    workoutLogRecord = selectItem(db_name, sql, values)
                    #the record is added to the list of records, which, when finished, is what is displayed to the user.
                    workoutLogRecords.append(workoutLogRecord)
                    currentLogID += 1

                self.otherFrame.destroy()
                x = DailyExerciseLogViewer(root, dailyExerciseLog, DEFAULT, workoutLogRecords)
        invalid = False
        DEFAULT = "None"
        no_exercise = False

        date = self.entry.get()
        
        sql = "select Date, TotalCalsBurned, CalsRemaining from DailyExerciseLog where Date=?"
        values = (date)
        db_name = "Exercise.db"
        dailyExerciseLog = selectItem(db_name, sql, values)
        # if this is none it means no record with that date could be found, so it handles the error and recalls the page.
        if dailyExerciseLog == None:
            print("Invalid Date")
            self.otherFrame.destroy()
            invalid = True
        else:
            #selects appropraite logID for that day.
            sql = "select LogID from DailyExerciseLog where Date=?"
            tempLogID = selectItem(db_name, sql, values)
            logID = tempLogID[0]
            
            exerciseLogID = []
            sql = "select ExerciseLogID from ExerciseExerciseLog where LogID=?"
            values = (logID)
            exerciseLogIDtemp = selectAllItems2(db_name, sql, values)  #the id's returned are the exerciseLog id's for that logID (day)
            test = str(exerciseLogIDtemp)
            if test == '[]':  #if nothing is returned (ie no exercise today), no_exercise becomes true so the correct function is called later.
                noExercise()
                no_exercise = True
            else:
                #else append the exercise log IDs. Then get the first and last log id numbers.
                #make current log and id = to the first log id, and make them both integers (so can be compared as numbers).
                exerciseLogID.append(exerciseLogIDtemp)
                firstLogID = exerciseLogID[0][0][0]
                tempLastLogID = exerciseLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                exerciseLogRecords = []
                # this is all done so the below runs the correct number of times (as many as there are logs for that day).
                while currentLogID <= lastLogID:
                    sql = "select Time, ExerciseName, Weight, Reps, Sets, CalsBurned from ExerciseExerciseLog where ExerciseLogID=?"
                    values = (currentLogID)
                    exerciseLogRecord = selectItem(db_name, sql, values)
                    #the record is added to the list of records, which, when finished, is what is displayed to the user.
                    exerciseLogRecords.append(exerciseLogRecord)
                    currentLogID += 1

        #if there is exercise and exercise entries were valid
        if no_exercise == False and invalid == False:
            workoutLogID = []
            sql = "select WorkoutLogID from WorkoutExerciseLog where LogID=?"
            values = (logID)
            workoutLogIDtemp = selectAllItems2(db_name, sql, values) #the id's returned are the workoutLog id's for that logID (day)
            test = str(workoutLogIDtemp)
            if test == '[]':  #if nothing is returned (ie no workouts today), the viewer page is called with 'None' in the place where workouts should be.
                    self.otherFrame.destroy()
                    x = DailyExerciseLogViewer(root, dailyExerciseLog, exerciseLogRecords, DEFAULT)
            else:
                #else append the workout log IDs. Then get the first and last log id numbers.
                #make current log and id = to the first log id, and make them both integers (so can be compared as numbers).
                workoutLogID.append(workoutLogIDtemp)
                firstLogID = workoutLogID[0][0][0]
                tempLastLogID = workoutLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                workoutLogRecords = []
                # this is all done so the below runs the correct number of times (as many as there are logs for that day).
                while currentLogID <= lastLogID:
                    sql = "select Time, WorkoutName, CalsBurned from WorkoutExerciseLog where WorkoutLogID=?"
                    values = currentLogID
                    workoutLogRecord = selectItem(db_name, sql, values)
                    #the record is added to the list of records, which, when finished, is what is displayed to the user.
                    workoutLogRecords.append(workoutLogRecord)
                    currentLogID += 1

                self.otherFrame.destroy()
                x = DailyExerciseLogViewer(root, dailyExerciseLog, exerciseLogRecords, workoutLogRecords)
                
        if invalid == True:
            #if it's invalid call the page again.
            x = DailyExerciseLogViewDay(root)
            s.top = s.top-1

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)



class DailyExerciseLogAddExercise:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = "Enter Exercise to Add", fg = "white", bg = "sky blue", width = 21, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry.pack(side = TOP)
        self.entry.configure(font=("Calibri", 12))
        self.entry.bind(self.add) 

        self.addButton = Button(self.otherFrame, text = "Add", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.add)
        self.addButton.pack(side = TOP)
        self.addButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def add(self):
        invalid = False
        
        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))
        exerciseName = self.entry.get()
        db_name = "Exercise.db"
        sql = "select ExerciseID, MuscleGroup, Weight, Reps, Sets, CalsBurned from Exercise where ExerciseName=?"
        values = (exerciseName)
        exerciseVals = selectItem(db_name, sql, values)
        
        #if nothing is returned entry is invalid so execution is halted and page is called again.
        if exerciseVals == None:
            print("Invalid Entry")
            self.otherFrame.destroy()
            invalid = True
            
        else:
            exerciseID = exerciseVals[0]
            muscleGroup = exerciseVals[1]
            weight = exerciseVals[2]
            reps = exerciseVals[3]
            sets = exerciseVals[4]
            calsBurned = exerciseVals[5]

            
            #selects all the fields needed from the dailyexerciselog record so can update with new values.
            sql = "select TotalCalsBurned, CalsRemaining from DailyExerciseLog where date=?"
            values = (date)
            beforeValues = selectItem(db_name, sql, values)
            tempBeforeCalsBurned = beforeValues[0]
            beforeCalsBurned = int(tempBeforeCalsBurned)
            tempBeforeCalsRem = beforeValues[1]
            beforeCalsRem = int(tempBeforeCalsRem)

            #calculating new values.
            newCalsBurned = beforeCalsBurned + calsBurned
            newCalsRem = beforeCalsRem + calsBurned

            #updating db's
            sql = "update DailyExerciseLog set TotalCalsBurned=?, CalsRemaining=?"
            values = (newCalsBurned, newCalsRem)
            updateItem(db_name, sql, values)

            sql = "update DailyFoodLog set CalsRemaining=?"
            values = (newCalsRem,)
            db_name = "Food.db"
            updateItem(db_name, sql, values)

            

            
            db_name = "Exercise.db"
            sql = "select LogID from DailyExerciseLog where date=?"
            values = (date)
            tempLogID = selectItem(db_name, sql, values)
            logID = tempLogID[0]
            
            #gets primary key of exerciseLogID and increments for next time.
            exerciseLogIDFile = open("NEA_ExerciseLogID.txt", "r")
            exerciseLogID = exerciseLogIDFile.readline()
            x = int(exerciseLogID)
            nextExerciseLogID = x+1
            exerciseLogIDFile.close()
            exerciseLogIDFile = open("NEA_ExerciseLogID.txt", "w")
            x = str(nextExerciseLogID)
            exerciseLogIDFile.write(x)
            exerciseLogIDFile.close

            now = datetime.now()
            time = ("%s:%s" % (now.hour, now.minute))
            
            #inserts new data into exerciselog.
            sql = "insert into ExerciseExerciseLog (ExerciseLogID, LogID, ExerciseID, Time, ExerciseName, Weight, Reps, Sets, CalsBurned) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (exerciseLogID, logID, exerciseID, time, exerciseName, weight, reps, sets, calsBurned)
            insertItem(db_name, sql, values)


            self.otherFrame.destroy()
            x = Starter(root)
            s.push(stack, Starter, maxSize, noItems, top)

        #if any input data was incorrect, will run this instead of running db related code.
        if invalid == True:
            x = DailyExerciseLogAddExercise(root)
            

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)







class DailyExerciseLogAddWorkout:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.displayLabel = Label(self.otherFrame, text = "Enter Workout to Add", fg = "white", bg = "sky blue", width = 21, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry.pack(side = TOP)
        self.entry.configure(font=("Calibri", 12))
        self.entry.bind(self.add)

        self.addButton = Button(self.otherFrame, text = "Add", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.add)
        self.addButton.pack(side = TOP)
        self.addButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def add(self):
        invalid = False
        
        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))
        workoutName = self.entry.get()
        db_name = "Exercise.db"
        sql = "select WorkoutID, WorkoutCalsBurned from WorkoutPlans where WorkoutName=?"
        values = (workoutName)
        workoutVals = selectItem(db_name, sql, values)

        #if nothing is returned means exercise doesn't exist, so doesn't run rest of code. defensive programming.
        if workoutVals == None:
            print("Invalid Entry")
            self.otherFrame.destroy()
            invalid = True

        else:
            #sets to correct data types
            workoutID = workoutVals[0]
            tempWorkoutCalsBurned = workoutVals[1]
            workoutCalsBurned = int(tempWorkoutCalsBurned)
            

            #selects all the fields needed from the dailyexerciselog record so can update with new values.
            sql = "select TotalCalsBurned, CalsRemaining from DailyExerciseLog where date=?"
            values = (date)
            beforeValues = selectItem(db_name, sql, values)
            tempBeforeCalsBurned = beforeValues[0]
            beforeCalsBurned = int(tempBeforeCalsBurned)
            tempBeforeCalsRem = beforeValues[1]
            beforeCalsRem = int(tempBeforeCalsRem)

            #calculating new values
            newCalsBurned = beforeCalsBurned + workoutCalsBurned
            newCalsRem = beforeCalsRem + workoutCalsBurned
            
            #updating db's.
            sql = "update DailyExerciseLog set TotalCalsBurned=?, CalsRemaining=?"
            values = (newCalsBurned, newCalsRem)
            updateItem(db_name, sql, values)

            sql = "update DailyFoodLog set CalsRemaining=?"
            values = (newCalsRem,)
            db_name = "Food.db"
            updateItem(db_name, sql, values)

            
            db_name = "Exercise.db"
            sql = "select LogID from DailyExerciseLog where date=?"
            values = (date)
            tempLogID = selectItem(db_name, sql, values)
            logID = tempLogID[0]
            
            #gets primary key of workoutLogID and increments for next time.
            workoutLogIDFile = open("NEA_WorkoutLogID.txt", "r")
            workoutLogID = workoutLogIDFile.readline()
            x = int(workoutLogID)
            nextWorkoutLogID = x+1
            workoutLogIDFile.close()
            workoutLogIDFile = open("NEA_WorkoutLogID.txt", "w")
            x = str(nextWorkoutLogID)
            workoutLogIDFile.write(x)
            workoutLogIDFile.close

            now = datetime.now()
            time = ("%s:%s" % (now.hour, now.minute))
            
            #inserts new data into workoutExerciseLog
            sql = "insert into WorkoutExerciseLog (WorkoutLogID, LogID, WorkoutID, Time, WorkoutName, CalsBurned) values (?, ?, ?, ?, ?, ?)"
            values = (workoutLogID, logID, workoutID, time, workoutName, workoutCalsBurned)
            insertItem(db_name, sql, values)


            self.otherFrame.destroy()
            x = Starter(root)
            s.push(stack, Starter, maxSize, noItems, top)
            
        #if any input data was incorrect, will run this instead of running db related code.
        if invalid == True:
            x = DailyExerciseLogAddWorkout(root)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)
    
        
        

class ExerciseLogHub:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.viewTodayButton = Button(self.otherFrame, text = "View Today", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.viewToday)
        self.viewTodayButton.pack(side = TOP)
        self.viewTodayButton.config(font=("Calibri", 12))

        self.viewDayButton = Button(self.otherFrame, text = "View a Date", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.viewDay)
        self.viewDayButton.pack(side = TOP)
        self.viewDayButton.config(font=("Calibri", 12))

        self.insertMealButton = Button(self.otherFrame, text = "Add Workout", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.addWorkout)
        self.insertMealButton.pack(side = TOP)
        self.insertMealButton.config(font=("Calibri", 12))

        self.insertFoodButton = Button(self.otherFrame, text = "Add Exercise", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.addExercise)
        self.insertFoodButton.pack(side = TOP)
        self.insertFoodButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))
    
    #this function is the same as the DailyExerciseLogViewDay above, just without the user inputs and hence without the error checking due to that.
    def viewToday(self):
        s.top = s.top+1

        def noExercise():
            DEFAULT = 'None'
            workoutLogID = []
            sql = "select WorkoutLogID from WorkoutExerciseLog where LogID=?"
            values = (logID)
            workoutLogIDtemp = selectAllItems2(db_name, sql, values)
            test = str(workoutLogIDtemp)
            if test == '[]':
                    self.otherFrame.destroy()
                    x = DailyExerciseLogViewer(root, dailyExerciseLog, DEFAULT, DEFAULT)
                    
            else:
                workoutLogID.append(workoutLogIDtemp)
                firstLogID = workoutLogID[0][0][0]
                tempLastLogID = workoutLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                workoutLogRecords = []
                while currentLogID <= lastLogID:
                    sql = "select Time, WorkoutName, CalsBurned from WorkoutExerciseLog where WorkoutLogID=?"
                    values = currentLogID
                    workoutLogRecord = selectItem(db_name, sql, values)
                    if workoutLogRecord is None:
                        raise ValueError("Not Found")
                        break
                    else:
                        workoutLogRecords.append(workoutLogRecord)
                        currentLogID += 1

                self.otherFrame.destroy()
                x = DailyExerciseLogViewer(root, dailyExerciseLog, DEFAULT, workoutLogRecords)
        
        DEFAULT = "None"
        no_exercise = False

        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))
        
        sql = "select Date, TotalCalsBurned, CalsRemaining from DailyExerciseLog where Date=?"
        values = (date)
        db_name = "Exercise.db"
        dailyExerciseLog = selectItem(db_name, sql, values)
        sql = "select LogID from DailyExerciseLog where Date=?"
        tempLogID = selectItem(db_name, sql, values)
        logID = tempLogID[0]
        
        exerciseLogID = []
        sql = "select ExerciseLogID from ExerciseExerciseLog where LogID=?"
        values = (logID)
        exerciseLogIDtemp = selectAllItems2(db_name, sql, values)
        test = str(exerciseLogIDtemp)
        if test == '[]':
            noExercise()
            no_exercise = True
        else:
            exerciseLogID.append(exerciseLogIDtemp)
            firstLogID = exerciseLogID[0][0][0]
            tempLastLogID = exerciseLogID[0][-1][0]
            lastLogID = int(tempLastLogID)
            currentLogID = int(firstLogID)
            exerciseLogRecords = []
            while currentLogID <= lastLogID:
                sql = "select Time, ExerciseName, Weight, Reps, Sets, CalsBurned from ExerciseExerciseLog where ExerciseLogID=?"
                values = (currentLogID)
                exerciseLogRecord = selectItem(db_name, sql, values)
                if exerciseLogRecord is None:
                    raise ValueError("Not Found")
                    break
                else:
                    exerciseLogRecords.append(exerciseLogRecord)
                    currentLogID += 1

        if no_exercise == False:
            workoutLogID = []
            sql = "select WorkoutLogID from WorkoutExerciseLog where LogID=?"
            values = (logID)
            workoutLogIDtemp = selectAllItems2(db_name, sql, values)
            test = str(workoutLogIDtemp)
            if test == '[]':
                    self.otherFrame.destroy()
                    x = DailyExerciseLogViewer(root, dailyExerciseLog, exerciseLogRecords, DEFAULT)
            else:
                workoutLogID.append(workoutLogIDtemp)
                firstLogID = workoutLogID[0][0][0]
                tempLastLogID = workoutLogID[0][-1][0]
                lastLogID = int(tempLastLogID)
                currentLogID = int(firstLogID)
                workoutLogRecords = []
                while currentLogID <= lastLogID:
                    sql = "select Time, WorkoutName, CalsBurned from WorkoutExerciseLog where WorkoutLogID=?"
                    values = currentLogID
                    workoutLogRecord = selectItem(db_name, sql, values)
                    if workoutLogRecord is None:
                        raise ValueError("Not Found")
                        break
                    else:
                        workoutLogRecords.append(workoutLogRecord)
                        currentLogID += 1

                self.otherFrame.destroy()
                x = DailyExerciseLogViewer(root, dailyExerciseLog, exerciseLogRecords, workoutLogRecords)

    def viewDay(self):
        self.otherFrame.destroy()
        x = DailyExerciseLogViewDay(root)
        s.push(stack, DailyExerciseLogViewDay, maxSize, noItems, top)
    
    def addWorkout(self):
        self.otherFrame.destroy()
        x = DailyExerciseLogAddWorkout(root)
        s.push(stack, DailyExerciseLogAddWorkout, maxSize, noItems, top)

    def addExercise(self):
        self.otherFrame.destroy()
        x = DailyExerciseLogAddExercise(root)
        s.push(stack, DailyExerciseLogAddExercise, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)

        
        


        

class SelectPage:
    def __init__(self, master, table):

        self.table = table

        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP, pady=20)

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.titleFrame, text = 'Please enter the name/date of the item you would like to search for', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 12))

        self.nameEntry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.nameEntry.pack(side = TOP)
        self.nameEntry.configure(font=("Calibri", 12))
        self.nameEntry.bind(self.entry)

        self.selectButton = Button(self.otherFrame, text = "Search", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.entry)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def entry(self):
        itemName = self.nameEntry.get()
        invalid = False
        #depending on the name of the table that was passed through as a parameter, it will choose the sql to match the table.

        if self.table == "User Account Details":
            sql = "select * from UserAccountDetails where UserPassword=?"
            db_name = "User_Details.db"

        if self.table == "User Personal Details":
            sql = "select * from UserPersonalDetails where Date=?"
            db_name = "User_Details.db"

        if self.table == "Food":
            sql = "select * from Food where FoodName=?"
            db_name = "Food.db"

        if self.table == "Meal":
            sql = "select * from Meal where MealName=?"
            db_name = "Food.db"

        if self.table == "Protein":
            sql = "select * from Protein where FoodName=?"
            db_name = "Food.db"

        if self.table == "Fat":
            sql = "select * from Fat where FoodName=?"
            db_name = "Food.db"

        if self.table == "Carb":
            sql = "select * from Carb where FoodName=?"
            db_name = "Food.db"

        if self.table == "Daily Food Log":
            sql = "select * from DailyFoodLog where Date=?"
            db_name = "Food.db"

        if self.table == "Exercise":
            sql = "select * from Exercise where ExerciseName=?"
            db_name = "Exercise.db"

        if self.table == "Workout Plans":
            sql = "select * from WorkoutPlans where WorkoutName=?"
            db_name = "Exercise.db"

        if self.table == "Daily Exercise Log":
            sql = "select * from DailyExerciseLog where Date=?"
            db_name = "Exercise.db"

        returned = selectItem(db_name, sql, itemName) # if name doesn't exist, re-calls function and tells user it was an invalid input.
        if returned == None:
            print("Invalid Entry")
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            invalid = True
        else:
            #else passes to the display page which will display the returned records.
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = DisplayPage(root, returned)
        if invalid == True:
            x = SelectPage(root, self.table)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = xD(root)
            

class dbEditHub:
    def __init__(self, master, table):

        self.table = table

        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP, pady=20)

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.titleFrame, text = 'Please select what you would like to do', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.selectAllButton = Button(self.otherFrame, text = "Select All Items", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectAll)
        self.selectAllButton.pack(side = TOP)
        self.selectAllButton.config(font=("Calibri", 12))

        self.selectButton = Button(self.otherFrame, text = "Select An Item", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.select)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))

        self.insertButton = Button(self.otherFrame, text = "Add a New Item", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.insert)
        self.insertButton.pack(side = TOP)
        self.insertButton.config(font=("Calibri", 12))

        self.deleteButton = Button(self.otherFrame, text = "Delete an Item", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.delete)
        self.deleteButton.pack(side = TOP)
        self.deleteButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def selectAll(self):
        #if the use chooses to select all, the sql (and what is returned) is decided by what the user chose to do on the previous page of the program,
        #as this selects what self.table is.
        
        if self.table == "User Personal Details":
            sql = "select * from UserPersonalDetails"
            db_name = "User_Details.db"

        if self.table == "Food":
            sql = "select * from Food"
            db_name = "Food.db"

        if self.table == "Meal":
            sql = "select * from Meal"
            db_name = "Food.db"


        if self.table == "Exercise":
            sql = "select * from Exercise"
            db_name = "Exercise.db"

        if self.table == "Workout Plans":
            sql = "select * from WorkoutPlans"
            db_name = "Exercise.db"

        returned =(selectAllItems(db_name, sql))
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = DisplayPage(root, returned)


    def select(self):
        #calls select page (see above).
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = SelectPage(root, self.table)


    def insert(self):
        #dependent on what the user has selected, the page they visit next is called here.
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        if self.table == "User Personal Details":
            x = UserInsertPageUPD(root)
            s.top = s.top-1
            s.push(stack, UserInsertPageUPD, maxSize, noItems, top)

        if self.table == "Food":
            x = UserInsertPageFood(root)
            s.top = s.top-1
            s.push(stack, UserInsertPageFood, maxSize, noItems, top)

        if self.table == "Meal":
            foods = []
            weights = []
            x = UserInsertPageMeal(root, foods, weights)

        if self.table == "Exercise":
            x = UserInsertPageExercise(root)
            s.top = s.top-1
            s.push(stack, UserInsertPageExercise, maxSize, noItems, top)

        if self.table == "Workout Plans":
            exercises = []
            x = UserInsertPageWorkoutPlans(root, exercises)


    def delete(self):
        #sets variables as according to what the user chose before, then passes these variables through to the delete page.
        if self.table == "User Personal Details":
            sql = "select Date from UserPersonalDetails"
            db_name = "User_Details.db"
            column_name = "Date"
            self.table = "UserPersonalDetails"
            
        if self.table == "Food":
            sql = "select FoodName from Food"
            db_name = "Food.db"
            column_name = "FoodName"

        if self.table == "Meal":
            sql = "select MealName from Meal"
            db_name = "Food.db"
            column_name = "MealName"

        if self.table == "Exercise":
            sql = "select ExerciseName from Exercise"
            db_name = "Exercise.db"
            column_name = "ExerciseName"

        if self.table == "Workout Plans":
            sql = "select WorkoutName from WorkoutPlans"
            db_name = "Exercise.db"
            column_name = "WorkoutName"
            self.table = "WorkoutPlans"

        records =(selectAllItems(db_name, sql))

        self.titleFrame.destroy()
        self.otherFrame.destroy()

        x = DeletePage(root, records, self.table, column_name, db_name)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = xD(root)

            

class ExerciseProgressViewer:
    def __init__(self, master, attribute):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.attribute = attribute

        invalid = False
        #selects the data to be displayed.
        db_name = "Exercise.db"
        sql = "select Weight from Exercise where ExerciseName=?"
        values = (self.attribute)
        data = selectAllItems2(db_name, sql, values)
        #checking the input exercise was valid.
        if data == []:
            print("Invalid Entry")
            self.otherFrame.destroy()
            invalid = True
        else:
            #appends all returned items to lists and separates them from their initial tuple states (for y axis).
            length = len(data)
            count1 = 0
            initialYList = []
            for i in range(0, length):
                initialYList.append(data[count1][0])
                count1 += 1
                    
            yList = []
            y = 0
            for i in range(0, length):
                yList.append(initialYList[y])
                y += 1
                
            #creates a list of values that increments in 1, up to as many as there are y values (for x axis, which is always time).
            x = 1
            xList = []
            for i in range(0, length):
                xList.append(x)
                x += 1

            figure = Figure(figsize=(5,5), dpi=100)   #creates a figure (graph) to display data.
            a = figure.add_subplot(111)   #creates a subplot for data.
            a.plot(xList, yList)   #define axes.
            a.set_title(self.attribute, fontsize = 14)   #define title.
            a.set_ylabel("Weight", fontsize = 12)   #define y title.
            a.set_xlabel("Time", fontsize = 12)    #define x title.

            canvas = FigureCanvasTkAgg(figure, master=self.otherFrame)    #creates a canvas (for figure to go on) which is in the GUI frame.
            canvas.get_tk_widget().pack()   #packs canvas.
            canvas.draw()    #draws graph.

            self.homeButton = Button(self.otherFrame, text = "Home", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.home)
            self.homeButton.pack(side = BOTTOM)
            self.homeButton.config(font=("Calibri", 12))

            self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
            self.backButton.pack(side = LEFT)
            self.backButton.config(font=("Calibri", 12))

            self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
            self.forwardButton.pack(side = RIGHT)
            self.forwardButton.config(font=("Calibri", 12))


        if invalid == True:
            # if data is invalid goes back to start of process.
            x = ExerciseProgress(root)
            s.top = s.top-1

    def home(self):
        self.otherFrame.destroy()
        x = Starter(root)
        s.top = s.top-1
        s.push(stack, Starter, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)



#nothing new in this, just transferring data to see above page.
class ExerciseProgress:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.otherFrame, text = 'Please enter name of exercise to display', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.nameEntry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.nameEntry.pack(side = TOP)
        self.nameEntry.configure(font=("Calibri", 12))
        self.nameEntry.bind(self.graph)

        self.graphButton = Button(self.otherFrame, text = "Graph", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.graph)
        self.graphButton.pack(side = TOP)
        self.graphButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))


    def graph(self):        
        attribute = self.nameEntry.get()
        self.otherFrame.destroy()
        x = ExerciseProgressViewer(root, attribute)
        s.top = s.top+1

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)




class Exercise:
    def __init__(self, master):
        
        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP, pady=20)

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.titleFrame, text = 'Please select where you would like to go', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.exerciseButton = Button(self.otherFrame, text = "Exercise Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.exercise)
        self.exerciseButton.pack(side = TOP)
        self.exerciseButton.config(font=("Calibri", 12))

        self.workoutPlansButton = Button(self.otherFrame, text = "Workout Plans Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.workoutPlans)
        self.workoutPlansButton.pack(side = TOP)
        self.workoutPlansButton.config(font=("Calibri", 12))

        self.progressButton = Button(self.otherFrame, text = "View Exercise Progress", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.progress)
        self.progressButton.pack(side = TOP)
        self.progressButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    #this is the page where the use decides where they want to go in the program next (with regard to exercise).
    #depending on the button they press (and therefore the method they choose) is where they go next in the program, and what they do.
    def exercise(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        table = "Exercise"
        x = dbEditHub(root, table)
        s.top = s.top+1

    def workoutPlans(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        table = "Workout Plans"
        x = dbEditHub(root, table)
        s.top = s.top+1

    def progress(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = ExerciseProgress(root)
        s.push(stack, ExerciseProgress, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = xD(root)
        
        


class carbProFatHub:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.carb1Button = Button(self.otherFrame, text = "Select All Carbs", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectAllCarbs)
        self.carb1Button.pack(side = TOP)
        self.carb1Button.config(font=("Calibri", 12))

        self.carb2Button = Button(self.otherFrame, text = "Select A Carb", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectCarb)
        self.carb2Button.pack(side = TOP)
        self.carb2Button.config(font=("Calibri", 12))

        self.pro1Button = Button(self.otherFrame, text = "Select All Proteins", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectAllProteins)
        self.pro1Button.pack(side = TOP)
        self.pro1Button.config(font=("Calibri", 12))

        self.pro2Button = Button(self.otherFrame, text = "Select A Protein", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectProtein)
        self.pro2Button.pack(side = TOP)
        self.pro2Button.config(font=("Calibri", 12))

        self.fat1Button = Button(self.otherFrame, text = "Select All Fats", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectAllFats)
        self.fat1Button.pack(side = TOP)
        self.fat1Button.config(font=("Calibri", 12))

        self.fat2Button = Button(self.otherFrame, text = "Select A Fat", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.selectFat)
        self.fat2Button.pack(side = TOP)
        self.fat2Button.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    #this page facilitates both the use of the merge sort algorithmn and the calling of the display page to display database data,
    #or the select page where the user can choose the record they want to display.
    def selectAllCarbs(self):
        sql = "select * from Carb"
        db_name = "Food.db"
        returned = selectAllItems(db_name, sql)
        self.otherFrame.destroy()
        x = DisplayPage(root, returned) #calls display page to display data in GUI.
        s.top = s.top+1
        counter = 0
        carbList = []
        for i in range(0, len(returned)): #this for loop appends the value of carb for each food returned from the db to the list.
            carbList.append(returned[counter][5])
            counter+=1
        listReturned = mergeSort(carbList)  #the list is then merge sorted, to produce a list of the amount of carbs in foods in the db, from least to most.
        print("Grams of Carbs in foods in the database (ascending order):")
        print(listReturned)

    def selectCarb(self):
        self.otherFrame.destroy()
        table = "Carb"
        x = SelectPage(root, table)
        s.top = s.top+1

    def selectAllProteins(self):
        sql = "select * from Protein"
        db_name = "Food.db"
        returned = selectAllItems(db_name, sql)
        self.otherFrame.destroy()
        x = DisplayPage(root, returned) #calls display page to display data in GUI.
        s.top = s.top+1
        counter = 0
        proteinList = []
        for i in range(0, len(returned)): #this for loop appends the value of protein for each food returned from the db to the list.
            proteinList.append(returned[counter][6])
            counter+=1
        listReturned = mergeSort(proteinList) #the list is then merge sorted, to produce a list of the amount of protein in foods in the db, from least to most.
        print("Grams of Protein in foods in the database (ascending order):")
        print(listReturned)

    def selectProtein(self):
        self.otherFrame.destroy()
        table = "Protein"
        x = SelectPage(root, table)
        s.top = s.top+1

    def selectAllFats(self):
        sql = "select * from Fat"
        db_name = "Food.db"
        returned = selectAllItems(db_name, sql)
        self.otherFrame.destroy()
        x = DisplayPage(root, returned) #calls display page to display data in GUI.
        s.top = s.top+1
        counter = 0
        fatList = []
        for i in range(0, len(returned)):  #this for loop appends the value of fat for each food returned from the db to the list.
            fatList.append(returned[counter][7])
            counter+=1
        listReturned = mergeSort(fatList) #the list is then merge sorted, to produce a list of the amount of fat in foods in the db, from least to most.
        print("Grams of Fat in foods in the database (ascending order):")
        print(listReturned)

    def selectFat(self):
        self.otherFrame.destroy()
        table = "Fat"
        x = SelectPage(root, table)
        s.top = s.top+1

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)



class Food:
    def __init__(self, master):
        
        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP, pady=20)

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.titleFrame, text = 'Please select where you would like to go', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.foodButton = Button(self.otherFrame, text = "Food Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.food)
        self.foodButton.pack(side = TOP)
        self.foodButton.config(font=("Calibri", 12))

        self.mealButton = Button(self.otherFrame, text = "Meal Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.meal)
        self.mealButton.pack(side = TOP)
        self.mealButton.config(font=("Calibri", 12))

        self.carbProFatButton = Button(self.otherFrame, text = "Carb/Pro/Fat Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.carbProFat)
        self.carbProFatButton.pack(side = TOP)
        self.carbProFatButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

        #this is the page where the use decides where they want to go in the program next (with regard to food).
        #depending on the button they press (and therefore the method they choose) is where they go next in the program, and what they do.

    def food(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        table = "Food"
        x = dbEditHub(root, table)
        s.top = s.top+1

    def meal(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        table = "Meal"
        x = dbEditHub(root, table)
        s.top = s.top+1

    def carbProFat(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = carbProFatHub(root)
        s.push(stack, carbProFatHub, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = xD(root)

#this class follows the exact same principle as the above ExerciseProgressViewer, where everything is explained. (please see above class)
#only difference is that the data selected is from the User Details db.
class PersonalProgressViewer:
    def __init__(self, master, attribute):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.attribute = attribute

        db_name = "User_Details.db"
        sql = "select Date from UserPersonalDetails"
        dates = selectAllItems(db_name, sql)
        length = len(dates)
        x = 1
        xList = []
        for i in range(0, length):
            xList.append(x)
            x += 1
        sql = "select %s from UserPersonalDetails" % (self.attribute)
        data = selectAllItems(db_name, sql)
        count1 = 0
        initialYList = []
        for i in range(0, length):
            initialYList.append(data[count1][0])
            count1 += 1
            
        yList = []
        y = 0
        for i in range(0, length):
            yList.append(initialYList[y])
            y += 1

        figure = Figure(figsize=(5,5), dpi=100)
        a = figure.add_subplot(111)
        a.plot(xList, yList)
        a.set_title(self.attribute, fontsize = 14)
        a.set_ylabel(self.attribute, fontsize = 12)
        a.set_xlabel("Time", fontsize = 12)

        canvas = FigureCanvasTkAgg(figure, master=self.otherFrame)
        canvas.get_tk_widget().pack()
        canvas.draw()

        self.homeButton = Button(self.otherFrame, text = "Home", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.home)
        self.homeButton.pack(side = BOTTOM)
        self.homeButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))


    def home(self):
        self.otherFrame.destroy()
        x = Starter(root)
        s.top = s.top-1
        s.push(stack, Starter, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)




class PersonalProgress:
    def __init__(self, master):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        columns = ["UserHeight", "UserWeight", "UserHR", "UserBF", "UserArmCirc", "UserWaistCirc", "UserLegCirc", "UserChestCirc", "UserCalfCirc"]

        self.titleLabel = Label(self.otherFrame, text = 'Please enter attribute to display', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.titleLabel2 = Label(self.otherFrame, text = columns, fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel2.pack(side=TOP) 
        self.titleLabel2.config(font=("Calibri", 8))

        self.nameEntry = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.nameEntry.pack(side = TOP)
        self.nameEntry.configure(font=("Calibri", 12))
        self.nameEntry.bind(self.graph)

        self.graphButton = Button(self.otherFrame, text = "Graph", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.graph)
        self.graphButton.pack(side = TOP)
        self.graphButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

    def graph(self):
        columns = ["UserHeight", "UserWeight", "UserHR", "UserBF", "UserArmCirc", "UserWaistCirc", "UserLegCirc", "UserChestCirc", "UserCalfCirc"]
        attribute = self.nameEntry.get()
        #error handling to make sure the input attribute is a real one.
        if attribute not in columns:
            print("Invalid Attribute")
            self.otherFrame.destroy()
            x = PersonalProgress(root)
        else:
            self.otherFrame.destroy()
            x = PersonalProgressViewer(root, attribute)
            s.top = s.top+1

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.otherFrame.destroy()
            x = xD(root)


    
    
class UserDetails:
    def __init__(self, master):
        
        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP, pady=20)

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.titleFrame, text = 'Please select what you would like to do', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.reCreateButton = Button(self.otherFrame, text = "Factory Reset", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.reCreate)
        self.reCreateButton.pack(side = TOP)
        self.reCreateButton.config(font=("Calibri", 12))

        self.userAccountDetailsButton = Button(self.otherFrame, text = "View User Account Details", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.userAccountDetails)
        self.userAccountDetailsButton.pack(side = TOP)
        self.userAccountDetailsButton.config(font=("Calibri", 12))

        self.userPersonalDetailsButton = Button(self.otherFrame, text = "User Personal Details Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.userPersonalDetails)
        self.userPersonalDetailsButton.pack(side = TOP)
        self.userPersonalDetailsButton.config(font=("Calibri", 12))

        self.progressButton = Button(self.otherFrame, text = "View Personal Progress", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.progress)
        self.progressButton.pack(side = TOP)
        self.progressButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))



    def reCreate(self):
        # if they choose to, all databases are recreated using above defined functions so they are empty, and the hash table is put back into null format, with '-' in every position.
        #the root (GUI) is destroyed and execution stopped.
        response = input("Are you sure you want to factory reset? (Y/N) ")
        if response.upper() == 'Y':
            create_db_UserDetails()
            create_db_Food()
            create_db_Exercise()
            hashTableFile = open("NEA_hash_file_test.txt", "w")
            for i in range(0, 13):
                hashTableFile.write('- \n')
            hashTableFile.close()
            print("All User Accounts Have been Deleted")
            global root
            root.destroy()
            sys.exit()
        else:
            pass
        
    #these below methods dictate where the program goes, depending on the button the user presses.
    #they just called other objects (pages) or set up variables to pass to these objects which are called.
    def userAccountDetails(self):
        db_name = "User_Details.db"
        sql = "select * from UserAccountDetails"
        accountDetails = selectAllItems(db_name, sql)
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = DisplayPage(root, accountDetails)
        s.top = s.top+1

    def userPersonalDetails(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        table = "User Personal Details"
        x = dbEditHub(root, table)
        s.top = s.top+1

    def progress(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = PersonalProgress(root)
        s.push(stack, PersonalProgress, maxSize, noItems, top)


    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = LOL(root)  
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = xD(root)

        


class Starter:
    def __init__(self, master):
        
        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP, pady=20)

        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM, pady=20)

        self.titleLabel = Label(self.titleFrame, text = 'Please choose the area of the program to visit', fg = "white", bg = "sky blue", width = 200, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 16))

        self.helpButton = Button(self.otherFrame, text = "How To Use", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.help)
        self.helpButton.pack(side = TOP)
        self.helpButton.config(font=("Calibri", 12))

        self.exerciseLogButton = Button(self.otherFrame, text = "ExerciseLog Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.exerciseLog)
        self.exerciseLogButton.pack(side = TOP)
        self.exerciseLogButton.config(font=("Calibri", 12))

        self.foodLogButton = Button(self.otherFrame, text = "FoodLog Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.foodLog)
        self.foodLogButton.pack(side = TOP)
        self.foodLogButton.config(font=("Calibri", 12))

        self.userDetailsButton = Button(self.otherFrame, text = "User Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.userDetails)
        self.userDetailsButton.pack(side = TOP)
        self.userDetailsButton.config(font=("Calibri", 12))

        self.exerciseButton = Button(self.otherFrame, text = "Exercise Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.exercise)
        self.exerciseButton.pack(side = TOP)
        self.exerciseButton.config(font=("Calibri", 12))

        self.foodButton = Button(self.otherFrame, text = "Food Hub", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.food)
        self.foodButton.pack(side = TOP)
        self.foodButton.config(font=("Calibri", 12))

        self.backButton = Button(self.otherFrame, text = "<--", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.back)
        self.backButton.pack(side = LEFT)
        self.backButton.config(font=("Calibri", 12))

        self.forwardButton = Button(self.otherFrame, text = "-->", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.forward)
        self.forwardButton.pack(side = RIGHT)
        self.forwardButton.config(font=("Calibri", 12))

       

    #to help the user understand how to function works, if the 'how to use' button is pressed this will be printed to tell them how it works.
    def help(self):
        print("""
            How To Use:\n
            It is highly recommended that before first use the program is factory reset.\n\n
            After signing up, you are presented with the home screen.
            This is the main hub of the program, and everything can be reached from here.
            As you have already found out, the 'How To Use' button takes you here.
            The 'ExerciseLog Hub' Button will take you to the Exercise Log hub, where you can use all the features of the Exercise Log.
            The 'FoodLog Hub' button works in the same way, but with regard to your Daily Food Log.
            The 'User Hub' Button takes you to the User Hub, where you can view and update information on yourself.
            The 'Exercise Hub' button takes you to the exercise hub.
            The 'Food Hub' button takes you to the food hub.
            The '<--' button takes you back to previous pages; once you've gone backwards, the '-->' forwards button takes you to more recent pages.\n\n\n
            How the Program Should be Used (with regard to the FoodLog):
            From the home screen press 'Food Hub'.
            This takes you to the Food Hub.
            From here, press the 'Food Hub' button.
            Now you can choose what you would like to do (either adding new foods or viewing or deleting foods previously entered into this database).
            If you press 'Add a New Item' you can add the properties of a particular food (i.e. whether it is a carb, protein, or a fat), name it, and when you press 'Add Item', it will be added to the database.
            You can now select (or delete) it from the database from the Food Hub.
            You can now also add it to meals.
            From the Food Hub if you press 'Meal Hub', you have the same options as you do with 'Food Hub'.
            If you press 'Add New Item' you can choose previously entered foods to add to a meal!
            (along with the portion of the food in that meal relative to the given portion size in food).
            By adding foods to meals (e.g. adding food chicken and  food rice to meal chicken and rice), they become a lot easier to add to the Foodlog, as you need only add one item!
            The Carb/Pro/Fat Hub button allows you to view foods that have been defined as such when entered into 'Food', independently from the others.
            This makes it easier to choose what protein you may want to have with a meal for instance, or if you need some more fat that day, you can view possible options already in the database!
            When you have entered some meals and foods, you can add them to the FoodLog!
            To do this, from the Home Page, press FoodLog Hub, and then either add meal, or add food.
            Input what you would like to add, and it gets added to the foodLog!
            Now go to the foodLog hub and press view today to see how it affects your daily calories and macros!
            You can also use the 'View a Date' button to view a specific date in the past.\n\n\n
            How the Program Should be Used (with regard to the ExerciseLog):
            It works very much the same as the section above for the foodLog.
            When you click onto the 'Exercise Hub' button, you will go to the exercise hub.
            From here, press 'Exercise Hub'.
            You will be presented with a page where you can select an exercise to view, select them all, delete one, or add a new one.
            Press Add a New Item, enter the relevant information, and add the exercise to the exercise database.
            You can now add this exercise to a workout.
            From the exercise hub, press workout plans.
            You will be presented with a page where you can select a workout to view, select them all, delete one, or insert a new one.
            Press insert and enter the exercises you want to insert to this plan.
            Once finished, you can add exercises and workouts to the ExerciseLog.
            From the home page, press exerciseLog and and then either add exercise, or add workout.
            Input what you want to add, then it is added to your exerciseLog for the day!
            You can now view today's exerciseLog, or a previous day's from the exercise log hub!\n\n\n
            UserHub:
            From here you can view the user account details, your personal details, and view your personal progress over different body attributes!
            You can update your personal details from here to show your progress.\n\n\n
            Viewing Progress:
            For both your personal progress and your exercise progress, you can view graphs to display this progression.
            By clicking the Personal Progress button, you are presented with a page which will tell you which attributes can be displayed.
            Choose one and click enter, and a graph of how this attribute has changed over time (based upon what has been input into User Personal Details) will be displayed.
            The same goes for exercise progress, except you enter the exercise you want (from what you have entered in Exercise).
        """)

    #these functions just call other objects (pages) to be displayed to the user based upon which button they press.
    def userDetails(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = UserDetails(root)
        s.push(stack, UserDetails, maxSize, noItems, top)

    def food(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = Food(root)
        s.push(stack, Food, maxSize, noItems, top)

    def exercise(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = Exercise(root)
        s.push(stack, Exercise, maxSize, noItems, top)

    def exerciseLog(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = ExerciseLogHub(root)
        s.push(stack, ExerciseLogHub, maxSize, noItems, top)

    def foodLog(self):
        self.titleFrame.destroy()
        self.otherFrame.destroy()
        x = FoodLogHub(root)
        s.push(stack, FoodLogHub, maxSize, noItems, top)

    def back(self):
        if s.top < 1:
            print("Cannot perform operation, no back pages.")
        else:
            LOL = s.back(stack, top)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = LOL(root)
            
    def forward(self):
        if s.top+1 >= s.noItems:
            print("Cannot perform operation, no forward pages.")
        else:
            xD = s.forward(stack, top, noItems)
            self.titleFrame.destroy()
            self.otherFrame.destroy()
            x = xD(root)


class SignUpUPD:
    def __init__(self, master, userKeyID):
        self.otherFrame = Frame(master)
        self.otherFrame.pack(side=BOTTOM)

        self.userKeyID = userKeyID

        self.displayLabel0 = Label(self.otherFrame, text = 'Please Enter Your Details Below', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel0.pack(side=TOP) 
        self.displayLabel0.config(font=("Calibri", 12))

        self.displayLabel99 = Label(self.otherFrame, text = 'First Name', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel99.pack(side=TOP) 
        self.displayLabel99.config(font=("Calibri", 12))

        self.entry99 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry99.pack(side = TOP)
        self.entry99.configure(font=("Calibri", 12))
        self.entry99.bind(self.entry)

        self.displayLabel98 = Label(self.otherFrame, text = 'Surname', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel98.pack(side=TOP) 
        self.displayLabel98.config(font=("Calibri", 12))

        self.entry98 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry98.pack(side = TOP)
        self.entry98.configure(font=("Calibri", 12))
        self.entry98.bind(self.entry)

        self.displayLabel97 = Label(self.otherFrame, text = 'Date of Birth (d/m/yyyy, dd/mm/yyyy etc.)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel97.pack(side=TOP) 
        self.displayLabel97.config(font=("Calibri", 12))

        self.entry97 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry97.pack(side = TOP)
        self.entry97.configure(font=("Calibri", 12))
        self.entry97.bind(self.entry)

        self.displayLabel = Label(self.otherFrame, text = 'Height (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel.pack(side=TOP) 
        self.displayLabel.config(font=("Calibri", 12))

        self.entry1 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry1.pack(side = TOP)
        self.entry1.configure(font=("Calibri", 12))
        self.entry1.bind(self.entry)

        self.displayLabel2 = Label(self.otherFrame, text = 'Weight (kg)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel2.pack(side=TOP) 
        self.displayLabel2.config(font=("Calibri", 12))

        self.entry2 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry2.pack(side = TOP)
        self.entry2.configure(font=("Calibri", 12))
        self.entry2.bind(self.entry)

        self.displayLabel3 = Label(self.otherFrame, text = 'Heartrate (bpm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel3.pack(side=TOP) 
        self.displayLabel3.config(font=("Calibri", 12))

        self.entry3 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry3.pack(side = TOP)
        self.entry3.configure(font=("Calibri", 12))
        self.entry3.bind(self.entry)

        self.displayLabel4 = Label(self.otherFrame, text = 'Body Fat Percentage (%)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel4.pack(side=TOP) 
        self.displayLabel4.config(font=("Calibri", 12))

        self.entry4 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry4.pack(side = TOP)
        self.entry4.configure(font=("Calibri", 12))
        self.entry4.bind(self.entry)

        self.displayLabel5 = Label(self.otherFrame, text = 'Arm Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel5.pack(side=TOP) 
        self.displayLabel5.config(font=("Calibri", 12))

        self.entry5 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry5.pack(side = TOP)
        self.entry5.configure(font=("Calibri", 12))
        self.entry5.bind(self.entry)

        self.displayLabel6 = Label(self.otherFrame, text = 'Waist Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel6.pack(side=TOP) 
        self.displayLabel6.config(font=("Calibri", 12))

        self.entry6 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry6.pack(side = TOP)
        self.entry6.configure(font=("Calibri", 12))
        self.entry6.bind(self.entry)

        self.displayLabel7 = Label(self.otherFrame, text = 'Leg Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel7.pack(side=TOP) 
        self.displayLabel7.config(font=("Calibri", 12))

        self.entry7 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry7.pack(side = TOP)
        self.entry7.configure(font=("Calibri", 12))
        self.entry7.bind(self.entry)

        self.displayLabel8 = Label(self.otherFrame, text = 'Chest Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel8.pack(side=TOP) 
        self.displayLabel8.config(font=("Calibri", 12))

        self.entry8 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry8.pack(side = TOP)
        self.entry8.configure(font=("Calibri", 12))
        self.entry8.bind(self.entry)

        self.displayLabel9 = Label(self.otherFrame, text = 'Calf Circumference (cm)', fg = "white", bg = "sky blue", width = 200, height = 1)
        self.displayLabel9.pack(side=TOP) 
        self.displayLabel9.config(font=("Calibri", 12))

        self.entry9 = Entry(self.otherFrame, bg = 'sky blue', width = 16)
        self.entry9.pack(side = TOP)
        self.entry9.configure(font=("Calibri", 12))
        self.entry9.bind(self.entry)

        self.selectButton = Button(self.otherFrame, text = "Continue", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.entry)
        self.selectButton.pack(side = TOP)
        self.selectButton.config(font=("Calibri", 12))




    def entry(self):
        db_name = "User_Details.db"
        #gets the user inputs.
        userFNametemp = self.entry99.get()
        userSNametemp = self.entry98.get()
        userDOBtemp = self.entry97.get()
        userHeighttemp = self.entry1.get()
        userWeighttemp = self.entry2.get()
        userHRtemp = self.entry3.get()
        userBFtemp = self.entry4.get()
        userArmCirctemp = self.entry5.get()
        userWaistCirctemp = self.entry6.get()
        userLegCirctemp = self.entry7.get()
        userChestCirctemp = self.entry8.get()
        userCalfCirctemp = self.entry9.get()
        invalid = False
        #appends them to lists depending on datatype.
        check1 = []
        check1.append(userHeighttemp)
        check1.append(userWeighttemp)
        check1.append(userBFtemp)
        check1.append(userArmCirctemp)
        check1.append(userWaistCirctemp)
        check1.append(userLegCirctemp)
        check1.append(userChestCirctemp)
        check1.append(userCalfCirctemp)
        check2 = []
        check2.append(userFNametemp)
        check2.append(userSNametemp)
        check2.append(userDOBtemp)
        #checks if the ones whoch are supposed to be floats are actually floats.
        z = 0
        for i in range(len(check1)):
            try:
                float(check1[z])
            except ValueError:
                self.otherFrame.destroy()
                invalid = True
            z = z+1

        #does the same with the integer
        try:
            int(userHRtemp)
        except ValueError:
            self.otherFrame.destroy()
            invalid = True

        z = 0

        #checks these have not been left blank by the user.
        for i in range(len(check2)):
            if len(check2[z]) == 0:
                self.otherFrame.destroy()
                invalid = True
            else:
                z = z+1
            
        if invalid == True:
            #if any inputs were invalid, runs this to avoid the code breaking, by reproducing the screen the user sees instead of running the next code.
            print("Input was invalid. Please re-enter information.")
            x = SignUpUPD(root, self.userKeyID)

        else:
            #defines them as their correct data types.
            userHeight = float(userHeighttemp)        
            userWeight = float(userWeighttemp)
            userHR = int(userHRtemp)
            userBF = float(userBFtemp)
            userArmCirc = float(userArmCirctemp)
            userWaistCirc = float(userWaistCirctemp)
            userLegCirc = float(userLegCirctemp)
            userChestCirc = float(userChestCirctemp)
            userCalfCirc = float(userCalfCirctemp)
            userFName = str(userFNametemp)
            userSName = str(userSNametemp)
            userDOB = str(userDOBtemp)
            
            now = datetime.now()
            date = ("%s/%s/%s" % (now.day, now.month, now.year))
            now = datetime.now()
            time = ("%s:%s:%s" % (now.hour, now.minute, now.second))
            dateTimeIDtemp = date+time
            dateTimeID = str(dateTimeIDtemp)
            #inserts record into userPersonalDetails table.
            sql = "insert into UserPersonalDetails (DateTimeID, UserKeyID, UserFName, UserSName, UserDOB, UserHeight, UserWeight, UserHR, UserBF, UserArmCirc, UserWaistCirc, UserLegCirc, UserChestCirc, UserCalfCirc, Date, Time) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (dateTimeID, self.userKeyID, userFName, userSName, userDOB, userHeight, userWeight, userHR, userBF, userArmCirc, userWaistCirc, userLegCirc, userChestCirc, userCalfCirc, date, time)
            insertItem(db_name, sql, values)
            self.otherFrame.destroy()
            x = Starter(root)
            s.push(stack, Starter, maxSize, noItems, top)

            
    

def instantiate_dailyLogs():
    sql = "select Date from DailyFoodLog where Date=?"
    
    now = datetime.now()
    date = ("%s/%s/%s" % (now.day, now.month, now.year))

    values = (date)

    foodLogDate = selectItem("Food.db", sql, values)

    #this will run if there is no record for today's date in the database, causing a new daily log record to be required.
    if foodLogDate == None:
        sql = "insert into DailyFoodLog (LogID, Date, TotalCals, TotalCarb, TotalProtein, TotalFat, CalsRemaining, CarbRemaining, FatRemaining, ProteinRemaining) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        
        #primary key IDs
        logIDFile = open("NEA_DailyFoodLogID.txt", "r")
        logID = logIDFile.readline()
        x = int(logID)
        nextLogID = x+1
        logIDFile.close()
        logIDFile = open("NEA_DailyFoodLogID.txt", "w")
        x = str(nextLogID)
        logIDFile.write(x)
        logIDFile.close

        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))

        #instantiates daily totals
        totalCals = 0
        totalCarb = 0
        totalProtein = 0
        totalFat = 0
        calsRemaining = 2000
        carbRemaining = 200
        fatRemaining = 50
        proteinRemaining = 200

        #inserts new record.
        values = (logID, date, totalCals, totalCarb, totalProtein, totalFat, calsRemaining, carbRemaining, fatRemaining, proteinRemaining)
        db_name = "Food.db"
        insertItem(db_name, sql, values)



        sql = "insert into DailyExerciseLog (LogID, Date, TotalCalsBurned, CalsRemaining) values (?, ?, ?, ?)"

        #primary key IDs
        logIDFile = open("NEA_DailyExerciseLogID.txt", "r")
        logID = logIDFile.readline()
        x = int(logID)
        nextLogID = x+1
        logIDFile.close()
        logIDFile = open("NEA_DailyExerciseLogID.txt", "w")
        x = str(nextLogID)
        logIDFile.write(x)
        logIDFile.close

        now = datetime.now()
        date = ("%s/%s/%s" % (now.day, now.month, now.year))

        #instantiates daily totals.
        totalCalsBurned = 0
        calsRemaining = 2000

        #inserts new record.
        values = (logID, date, totalCalsBurned, calsRemaining)
        db_name = "Exercise.db"
        insertItem(db_name, sql, values)

    else:
        #if not, there is nothing needed to be done so it can pass
        pass


   



# this is the stack.
# it functions much like a pure, theoretical queue does, except it has one additional attribute (self.noItems).
# during development it has changed from a stack to a queue as a queue works far better
# (as it allows you to implement the forwards button, as the stack would only allow for the back button).
# stack would only allow for back button as when you go back the page you were on would be popped, meaning you could not return to it.
# That is not the case with a queue, as data is not removed until it is full.
# when full, data was then removed from the front of the queue, which is how a queue works and hence making queue the superior abstract data type.
# The names of the class and attributes were not changed, as it would be highly confusing to try and change it throughout the program,
# and so instead of changing the names of the class and the attributes of the class, I only changed the way it was implemented.
# (hence why it is still called stack, and uses top etc, which are used for a stack, and not for a queue) however the way it works has been changed to be of a queue.
# the 'top' is now a pointer to the 'end' of the queue (not the true end of items, but as far as the queue is concerned, it is the end),
# maxSize is the maximum size of the queue, and stack is now a queue.
# items are removed from the front of the queue and added to the 'end'.
# 'push' adds items to the 'end' of the queue. The method 'pop' is defunct -
# it is no longer used in this code, as items are now removed from the front (but was included anyway for completeness).
# peek returns the item at the end of the queue.
# It logically behaves like a queue, but with stack terminology.
# Below how the queue works is described. It is described in terms of the stack (as that is how the code is defined) but is about the queue.
# The purpose of it is to traverse through previously visited pages, by peeking at different points in the stack.
# The stack itself is a list, the maxSize is the maximum number of items that can be added to it, the noItems is the number of items in the stack,
# and the top is the position of the page currently displayed to the user.
# New viewed pages get added to the top (which starts at 0).
# When a page gets added, top is incremented by 1, so is noItems. The object is added to that index of top in the stack.
# If noItems = maxSize, the objects at indexes up to and including the top get moved down by 1 place - 'stack[i] = stack[i+1]'. This removes the first item (hence making it a queue).
class Stack:
    def __init__(self, stack, top, maxSize, noItems):
        self.stack = stack
        self.top = top
        self.maxSize = maxSize
        self.noItems = noItems

    def isEmpty(self, noItems):
        if self.noItems == 0:   #if noItems = 0 it is empty.
            return True
        else:
            return False

    def isFull(self, noItems, maxSize):
        if self.noItems == self.maxSize:  #if noItems = maxSize it is full.
            return True
        else:
            return False

    def push(self, stack, item, maxSize, noItems, top):
        if s.isFull(noItems, maxSize):
            for i in range(0, self.top):
                stack[i] = stack[i+1]   #if is full move top and below down by one and make top = new item.
            stack[self.top] = item
        else:
            moves = (self.noItems-(self.top+1))   #judges the amount of moves that are required by working out how many items are between
                                                  #the number of items before and including top, and the total number of items.
            position = self.noItems-1   #index of final item in queue.
            for i in range(0, moves):  #moves the ones above the top up by one
                stack[position+1]=stack[position]
                position = position-1
            self.noItems = self.noItems + 1   #increments the variables as required.
            self.top = self.top + 1
            stack[(self.top)] = item
            return self.stack, self.noItems, self.top   #return new values to main program so can be manipulated there.

    def pop(self, stack, noItems, top):
        if s.isEmpty(self.noItems):
            return("Stack Empty, cannot perform operation.")   #if empty does not run.
        else:
            self.item = stack[self.noItems]     #top item is selected.
            stack[self.noItems] = ' '    #index is reset to nothing.
            self.noItems = self.noItems -1      #values incremented.
            self.top = self.top -1
            return self.item, self.noItems, self.top    #return new values so can be manipulated in main program.

    def peek(self, stack, top):
        self.item = stack[self.top]    #returns item at top.
        return self.item

    def back(self, stack, top):
        self.top = self.top - 1
        s.peek(stack, top)    #returns item at current top-1
        return self.item

    def forward(self, stack, top, noItems):
        self.top = self.top + 1
        s.peek(stack, top)    #returns item at current top+1
        return self.item
           


#hashTable works the exact same way a normal hash table does.
class HashTable:
    def __init__(self, hashTable, tableSize, email, password, UserKeyID):
        self.hashTable = hashTable
        self.tableSize = tableSize
        self.email = email
        self.password = password
        self.UserKeyID = UserKeyID

    def hashItem(self):
        hashArray = []
        valueASCII = 0
        position = 0
        combined = self.email+self.password
        for letter in combined:
            hashArray.append(letter)   #user email and password now split up into characters in list.
        for letter in hashArray:
            valueASCII = valueASCII + (ord(letter)*(position+1))    #calculates a value based upon the ascii of that character
                                                                    #multiplied by the position in the list (to reduce collisions in table).
            position += 1
        address = valueASCII % self.tableSize   #mods by tablesize to get address location.
        return address

    def addItem(self):
        address = self.hashItem()    #creates address.
        if self.hashTable[address] == '-':    #if address has nothing in it, set it = to UserKeyID (so it is stored there).
            self.hashTable[address] = self.UserKeyID
            empty = True
        else:
            empty = False
            done = False
            counter = 0
            while done == False:     #searches sequentially in spaces after the original until empty is found or
                                     #the whole table has been checked, when it states there is no more room.
                address = address + 1
                counter = counter + 1
                if counter == self.tableSize:
                    done = True
                    print("Table Full. Delete a profile in order to create room.")
                if address > self.tableSize - 1:
                    address = 0
                if self.hashTable[address] == '-':
                    self.hashTable[address] = self.UserKeyID
                    empty = True
                    done = True
        return empty    #returns this to main program as if it is True the program can continue executing,
                        #else it is halted as no login has been achieved.
            

    def logInSearch(self):
        notFound = True
        originalAddress = self.hashItem()   #generates address where should be stored.
        address = originalAddress
        if self.hashTable[originalAddress] == '-':   #if this is empty it is not in table.
            print("Incorrect Credentials. Access Denied.")
        else:    #else searches every non-empty found after this (until empty is found),
                 #selecting the email and password associated with the userKeyID from db and comparing it with input email and pword.
                 #if they match, access is garnted, else the search continues until correct one is found, empty is found, or the entire table is searched.
            counter = 0
            while notFound == True and counter < self.tableSize:
                if self.hashTable[address] != '-':
                    tempUserKeyID = self.hashTable[address]
                    sql = "select UserEmail, UserPassword from UserAccountDetails where UserKeyID=?"
                    values = (tempUserKeyID)
                    returned = selectItem("User_Details.db", sql, values)
                    dbEmail = returned[0]
                    dbPword = returned[1]
                    if dbEmail == self.email and dbPword == self.password:
                        notFound = False
                        if 'USERKEYID' not in globals():
                            global USERKEYID
                        USERKEYID = tempUserKeyID
                        print("Access Granted.")
                    elif counter == self.tableSize-1:
                        print("Incorrect Credentials. Access Denied.")
                    else:
                        pass
                else:
                    counter = 99
                    print("Incorrect Credentials. Access Denied.")
                counter = counter + 1
                address = ((address+1)%self.tableSize)
        return notFound
                

    def updateFile(self):  #writes the hashtable into the file for reading next log-in/sign-up.
        hashTableFile = open("NEA_hash_file_test.txt", "w")
        for i in range(0, self.tableSize):
            hashTableFile.write('%s \n' % (str(self.hashTable[i])))
        hashTableFile.close()





class signUpPage:
    def __init__(self, master):
        self.enterLabelFrame = Frame(master)
        self.enterLabelFrame.pack(side = TOP)

        self.userLabelFrame = Frame(master)
        self.userLabelFrame.pack(side = TOP)

        self.userEntryFrame = Frame(master)
        self.userEntryFrame.pack(side = TOP)

        self.passwordLabelFrame = Frame(master)
        self.passwordLabelFrame.pack(side = TOP)

        self.passwordEntryFrame = Frame(master)
        self.passwordEntryFrame.pack(side = TOP)

        self.logInButtonFrame = Frame(master)
        self.logInButtonFrame.pack(side = TOP, padx = 200, pady = 40)

        self.enterLabel = Label(self.enterLabelFrame, text = "Please Enter Email and Password to Sign Up.", fg = 'sky blue', bg = 'azure', height = 2, width = 57)
        self.enterLabel.pack(side = TOP)
        self.enterLabel.config(font=("Calibri", 16))
        
        self.userLabel = Label(self.userLabelFrame, text = "Email: ", fg = 'sky blue', bg = 'azure', height = 3, width = 57)
        self.userLabel.pack(side = TOP)
        self.userLabel.config(font=("Calibri", 16))

        self.userEntry = Entry(self.userEntryFrame, bg = 'sky blue', width = 16)
        self.userEntry.pack(side = TOP)
        self.userEntry.configure(font=("Calibri", 12))

        self.passwordLabel = Label(self.passwordLabelFrame, text = "Password: ", fg = 'sky blue', bg = 'azure', height = 3, width = 57)
        self.passwordLabel.pack(side = TOP)
        self.passwordLabel.config(font=("Calibri", 16))

        self.passwordEntry = Entry(self.passwordEntryFrame, bg = 'sky blue', width = 16)
        self.passwordEntry.pack(side = TOP)
        self.passwordEntry.configure(font=("Calibri", 12))

        self.logInButton = Button(self.logInButtonFrame, text = "Continue", fg = 'black', bg = 'azure', height = 1, width = 57, command = self.signUp)
        self.logInButton.pack(side = TOP)
        self.logInButton.config(font=("Calibri", 12))

    def signUp(self):
        userEmail = self.userEntry.get()
        userPassword = self.passwordEntry.get()
        
        #error checking for empty input fields
        if userEmail == '' or userPassword == '':
            print("Invalid Entry.")
            self.enterLabelFrame.destroy()
            self.userLabelFrame.destroy()
            self.userEntryFrame.destroy()
            self.passwordLabelFrame.destroy()
            self.passwordEntryFrame.destroy()
            self.logInButtonFrame.destroy()
            x = signUpPage(root)

        else:
            #primary key ID getting and setting.
            userKeyIDFile = open("NEA_UserKeyID.txt", "r")
            userKeyID = userKeyIDFile.readline()
            x = int(userKeyID)
            nextUserKeyID = x+1
            userKeyIDFile.close()
            userKeyIDFile = open("NEA_UserKeyID.txt", "w")
            x = str(nextUserKeyID)
            userKeyIDFile.write(x)
            userKeyIDFile.close
            
            #inserts appropriate info to User Account Details database.
            sql = "insert into UserAccountDetails (UserKeyID, UserEmail, UserPassword) values (?, ?, ?)"
            db_name = "User_Details.db"
            values = (userKeyID, userEmail, userPassword)
            insertItem(db_name, sql, values)
            
            #reads data from hashTable file, and so sets up the hashTable as a list by appending the elements in the file.
            hashTableFile = open("NEA_hash_file_test.txt", "r")
            data = hashTableFile.readlines()
            hashTable = []
            #this was done as the formatting on the data returned was different based upon how many characters there were stored on each line and this solved the issue.
            for i in range(0, 13):
                if data[i][0] == '-':
                    hashTable.append(data[i][0])   #if first element is '-' append just that.
                elif data[i][1] == ' ':
                    hashTable.append(data[i][0])   #if first element is not '-' (i.e a UserKeyID) and second is space (meaning it is 1 digit userKeyID) just append first element.
                else:
                    hashTable.append(data[i][:2])  #else it is a 2 digit userKeyID, so append both.
            hashTableFile.close()  
        
            tableSize = 13   
        
            h = HashTable(hashTable, tableSize, userEmail, userPassword, userKeyID)   #instantiates hashTable as object h.
            returned = h.addItem()   #add item and return the values for 'empty' from the method.
            if returned == True:
                h.updateFile()   #if it was successfully added, update the file and run below. Else, program ends.
                
                self.enterLabelFrame.destroy()
                self.userLabelFrame.destroy()
                self.userEntryFrame.destroy()
                self.passwordLabelFrame.destroy()
                self.passwordEntryFrame.destroy()
                self.logInButtonFrame.destroy()
                if 'USERKEYID' not in globals():  #sets it global so can always be accessed.
                    global USERKEYID
                USERKEYID = userKeyID
                x = SignUpUPD(root, userKeyID)
            else:
                pass

        


class logInPage:
    def __init__(self, master):
        self.enterLabelFrame = Frame(master)
        self.enterLabelFrame.pack(side = TOP)

        self.userLabelFrame = Frame(master)
        self.userLabelFrame.pack(side = TOP)

        self.userEntryFrame = Frame(master)
        self.userEntryFrame.pack(side = TOP)

        self.passwordLabelFrame = Frame(master)
        self.passwordLabelFrame.pack(side = TOP)

        self.passwordEntryFrame = Frame(master)
        self.passwordEntryFrame.pack(side = TOP)

        self.logInButtonFrame = Frame(master)
        self.logInButtonFrame.pack(side = TOP, padx = 200, pady = 40)

        self.enterLabel = Label(self.enterLabelFrame, text = "Please Enter Username and Password to Continue.", fg = 'sky blue', bg = 'azure', height = 2, width = 57)
        self.enterLabel.pack(side = TOP)
        self.enterLabel.config(font=("Calibri", 16))
        
        self.userLabel = Label(self.userLabelFrame, text = "Username: ", fg = 'sky blue', bg = 'azure', height = 3, width = 57)
        self.userLabel.pack(side = TOP)
        self.userLabel.config(font=("Calibri", 16))

        self.userEntry = Entry(self.userEntryFrame, bg = 'sky blue', width = 16)
        self.userEntry.pack(side = TOP)
        self.userEntry.configure(font=("Calibri", 12))

        self.passwordLabel = Label(self.passwordLabelFrame, text = "Password: ", fg = 'sky blue', bg = 'azure', height = 3, width = 57)
        self.passwordLabel.pack(side = TOP)
        self.passwordLabel.config(font=("Calibri", 16))

        self.passwordEntry = Entry(self.passwordEntryFrame, bg = 'sky blue', width = 16)
        self.passwordEntry.pack(side = TOP)
        self.passwordEntry.configure(font=("Calibri", 12))

        self.logInButton = Button(self.logInButtonFrame, text = "Continue", fg = 'black', bg = 'azure', height = 1, width = 57, command = self.check)
        self.logInButton.pack(side = TOP)
        self.logInButton.config(font=("Calibri", 12))

    def check(self):
        userEmail = self.userEntry.get()
        userPassword = self.passwordEntry.get()

        userKeyID = 'LOLitDONTmatter'

        #same as above reasons and method for instantiating hashTable this way (see above class).
        hashTableFile = open("NEA_hash_file_test.txt", "r")
        data = hashTableFile.readlines()
        hashTable = []
        for i in range(0, 13):
            if data[i][0] == '-':
                hashTable.append(data[i][0])
            elif data[i][1] == ' ':
                hashTable.append(data[i][0])
            else:
                hashTable.append(data[i][:2])
        hashTableFile.close()  
    
        tableSize = 13

        h = HashTable(hashTable, tableSize, userEmail, userPassword, userKeyID)
        returned = h.logInSearch()   #run logInSearch
        if returned == False:  #if it was found run this.
            self.enterLabelFrame.destroy()
            self.userLabelFrame.destroy()
            self.userEntryFrame.destroy()
            self.passwordLabelFrame.destroy()
            self.passwordEntryFrame.destroy()
            self.logInButtonFrame.destroy()
            x = Starter(root)
            s.push(stack, Starter, maxSize, noItems, top)
        else:
            pass   #else don't.
            
        
            

        
class frontPage:
    def __init__(self, master):
        self.titleFrame = Frame(master)
        self.titleFrame.pack(side=TOP)

        self.infoFrame1 = Frame(master)
        self.infoFrame1.pack(side=TOP, pady = 20)

        self.infoFrame2 = Frame(master)
        self.infoFrame2.pack(side=TOP)

        self.logSignFrame = Frame(master)
        self.logSignFrame.pack(side = TOP, padx = 20, pady = 40)

        self.imageFrame = Frame(master)
        self.imageFrame.pack(side = BOTTOM)


        self.titleLabel = Label(self.titleFrame, text = "Nutrition Tracker", fg = "white", bg = "sky blue", width = 25, height = 2)
        self.titleLabel.pack(side=TOP) 
        self.titleLabel.config(font=("Calibri", 28))

        self.infoLabel1 = Label(self.infoFrame1, text = "Welcome to Nutrition Tracker!", fg = "sky blue", bg = "azure", width = 50, height = 2)
        self.infoLabel1.pack(side = TOP)
        self.infoLabel1.config(font=("Calibri", 16))
        
        self.infoLabel2 = Label(self.infoFrame2, text = "Please Log In or Sign Up to Continue!", fg = "sky blue", bg = "azure", width = 50, height = 1)
        self.infoLabel2.pack(side = TOP)
        self.infoLabel2.config(font=("Calibri", 16))

        self.reCreateButton = Button(self.logSignFrame, text = "Factory Reset", fg = 'black', bg = 'azure', height = 1, width = 21, command = self.reCreate)
        self.reCreateButton.pack(side = BOTTOM)
        self.reCreateButton.config(font=("Calibri", 12))

        self.logButton = Button(self.logSignFrame, text = "Log In", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.log_in)
        self.logButton.pack(side = LEFT)
        self.logButton.config(font=("Calibri", 12))

        self.signButton = Button(self.logSignFrame, text = "Sign Up", fg = 'black', bg = 'azure', height = 1, width = 10, command = self.sign_up)
        self.signButton.pack(side = LEFT)
        self.signButton.config(font=("Calibri", 12))

        self.photo = PhotoImage(file="Test Image.png")
        self.imageLabel1 = Label(self.imageFrame, image=self.photo, width = 480, height = 160)
        self.imageLabel1.pack()

    #allows the user to choose what they want to do next from a button press.
    def log_in(self):
        self.titleFrame.destroy()
        self.infoFrame1.destroy()
        self.infoFrame2.destroy()
        self.logSignFrame.destroy()
        self.imageFrame.destroy()
        log_InPage = logInPage(root)

    def sign_up(self):
        self.titleFrame.destroy()
        self.infoFrame1.destroy()
        self.infoFrame2.destroy()
        self.logSignFrame.destroy()
        self.imageFrame.destroy()
        sign_UpPage = signUpPage(root)

    def reCreate(self):
        # if they choose to, all databases are recreated using above defined functions so they are empty, and the hash table is put back into null format, with '-' in every position.
        #the root (GUI) is destroyed and execution stopped.
        response = input("Are you sure you want to factory reset? (Y/N) ")
        if response.upper() == 'Y':
            create_db_UserDetails()
            create_db_Food()
            create_db_Exercise()
            hashTableFile = open("NEA_hash_file_test.txt", "w")
            for i in range(0, 13):
                hashTableFile.write('- \n')
            hashTableFile.close()
            print("All User Accounts Have been Deleted")
            global root
            root.destroy()
            sys.exit()
        else:
            pass

instantiate_dailyLogs()

#instantiates the 'stack'.
stack = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
item = 'Arbitrary'
top = -1
maxSize = 20
noItems = 0
s = Stack(stack, top, maxSize, noItems)

print("Please make sure you have all the necessary text, database, and image files saved, and stored in the same folder as this one. Thank you.\n\n")

#calls the first page to be shown to user. mainloop keeps page always shown as opposed to disappearing.
frontPage = frontPage(root)
root.mainloop()

