import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import datetime

def getHoursFromData(data):
    """
    Data is the dictionaty with all the data and calculates the acumulative
    hours for each category.
    """
    hoursDicc = {}
    total = 0
    for k, v in data.items():
        if k != "Entry":
            hoursDicc[k] = sum(v)

        if k in ["Programming", "Reading", "Music", "Gaming", "Others", "Watched"]:
            total += sum(v)

    hoursDicc["Total"] = total

    return hoursDicc

def lowerUpperBandForLevel(lvl):
    """
    Input is the level and returns a list with the lower and upped band
    for the current level
    """
    if lvl == 1: 
        return [0, 10]
    if lvl == 2: 
        return [10, 50]
    if lvl == 3: 
        return [50, 100]
    if lvl == 4: 
        return [100, 250]
    if lvl == 5: 
        return [250, 500]
    if lvl == 6: 
        return [500, 1000]
    
def levelStatus(hs):
    """
    Convertion from hours to level
    """
    if hs >= 0 and hs < 10:
        return 1
    if hs >= 10 and hs < 50:
        return 2
    if hs >= 50 and hs < 100:
        return 3
    if hs >= 100 and hs < 250:
        return 4
    if hs >= 250 and hs < 500:
        return 5

def getLevelFromData(dataHours):
    """
    Gets the level for each category base on the acumulative hours calculate
    from all the data 
    """
    levelDicc = {}
    for k, v in dataHours.items():
        levelDicc[k] = levelStatus(v)
 
    return levelDicc

def updateDatabase(allData, newEntry):
    for k, v in allData.items():
        v.append(newEntry[k]) 
    return allData

def calculateChanges(stateChanges, initalState):
    """
    Calculate the changes make comparing the original state and
    the changes made by the user.
    """
    onlyChanges = {}
    for k, v in stateChanges.items():
        onlyChanges[k] = stateChanges[k] - initalState[k]
    
    onlyChanges["Entry"] = date.today()
    return onlyChanges

def catToActivity(category):
    """
    Return the specific subcateogries from the given category
    """
    if category == "Programming":
        activiy_names = ["Code", "IA", "Papers"]
    if category == "Reading":
        activiy_names = ["Fiction", "Technical", ""]
    if category == "Music":
        activiy_names = ["Classical", "Improv", ""]
    if category == "Gaming":
        activiy_names = ["Single Play", "Bros", ""]
    if category == "Others":
        activiy_names = ["Language", "Sport", "Outside"]
    if category == "Watched":
        activiy_names = ["Movie", "Anime", "Series"]
    
    return activiy_names

def resetGlobalValue(state):
    category =  ["Programming", "Reading", "Music", "Gaming", "Others", "Watched"]
    totalHours = 0
    for cat in category:
        activity_names = catToActivity(cat)
        newHoursAdded = 0

        for act in activity_names:
            if act != "":
                newHoursAdded += state[act]
    
        state[cat] = newHoursAdded
        totalHours += newHoursAdded

    state["Total"] = totalHours

    return state

def addHours(category, state, activity, add):
    activiy_names = catToActivity(category) 
    
    if add:
        state[activiy_names[activity]] += 1
        state = resetGlobalValue(state)
        return state
    else:
        state[activiy_names[activity]] -= 1
        state = resetGlobalValue(state)
        return state

def barUpdate(barObject, mid, bound):
    barObject.setFormat("")
    div = bound[1] - bound[0]
    porcentaje = int(((mid - bound[0]) /div) * 100)
    barObject.setValue(porcentaje)

    return porcentaje

def dateEntrySegmentation(dayDelay, data):
    daysEntries = list(data["Entry"])  #List with all the entry dates
    limitDay = date.today() - datetime.timedelta(dayDelay)

    for i in range(len(daysEntries)):
        if daysEntries[i] > limitDay:  
            return i 

def midLabelSetup(label, midVal, porcentaje, offset, side):
    if side:
        shift = 35
    else:
        shift = 425

    if porcentaje > 5 and porcentaje < 95:
        label.setText(str(midVal))
        deltax = int(3.05 * porcentaje + shift)
        label.move(deltax, offset)
    else:
        label.setText("")

def index_month_division(day, list_of_days):
    for i in range(len(list_of_days)):
        if list_of_days[i] <= day:
            return i
    return 0

def createPlot(typePlot, categoryPlot, timePlot, data, fig):
    if categoryPlot == "Main":
        categories =  ["Programming", "Reading", "Music", "Gaming", "Others", "Watched"]
    elif categoryPlot == "All":
        categories = ["Code", "IA", "Papers", "Fiction", "Technical", "Classical", "Improv", "Single Play", "Bros", 
                      "Language", "Sport", "Outside", "Movie", "Anime", "Series"]
    else:
        categories = catToActivity(categoryPlot)
        if categories[-1] == "":
            categories.pop()
    
    if timePlot == "Week":
        delayDays = 7
        idxTime = dateEntrySegmentation(delayDays, data) 
        dataPlot = {}
        for cat in categories:
            dataPlot[cat] = sum(data[cat][idxTime:])

    if timePlot == "Month":
        #Untested
        delayDays = 30
        idxTime = dateEntrySegmentation(delayDays, data) 
        dataPlot = {}
        for cat in categories:
            dataPlot[cat] = sum(data[cat][idxTime:])

    if timePlot == "6Months":
        #Untested
        delayDays = 180
        idxTime = dateEntrySegmentation(delayDays, data) 
        dataPlot = {}
        for cat in categories:
            dataPlot[cat] = sum(data[cat][idxTime:])

    if timePlot == "Year":
        #Untested
        delayDays = 365
        idxTime = dateEntrySegmentation(delayDays, data) 
        dataPlot = {}
        for cat in categories:
            dataPlot[cat] = sum(data[cat][idxTime:])

    if timePlot == "All":
        dataPlot = {}
        for cat in categories:
            dataPlot[cat] = sum(data[cat])

    ax1 = fig.add_axes([0.12,0.15,0.8,0.8])
    if typePlot == "Pie":
        size = list(dataPlot.values())
        labels = list(dataPlot.keys())
        ax1.pie(size, labels=labels, autopct='%1.1f%%')

    if typePlot == "Barras":
        size = list(dataPlot.values())
        labels = list(dataPlot.keys())
        ax1.bar(labels, size, width=0.4)
        ax1.set_ylabel("Hours")
        plt.xticks(fontsize=8,rotation=30)
    
    if typePlot == "Graph":
        type_lines = {"Programming" : "-", "Reading" : "--", "Music": "v",
                      "Watched": ":", "Others" : "s", "Gaming" : "-.",
                      "Code" : "--", "IA" : ":", "Papers" : "-.", 
                      "Fiction" : "--", "Technical" : ":",
                      "Classical" : "--", "Improv" : ":",
                      "Single Play" : "--", "Bros" : ":",
                      "Language" : "--", "Sports" : ":", "Outside" : "-.", 
                      "Movie" : "--", "Anime" : ":", "Series" : "-.", 
                      }

        if timePlot == "Week":
            days = 7
            base = date.today()
            all_days_week = [base - datetime.timedelta(days=x) for x in range(days)]
            days_used = data["Entry"][idxTime:]
            for cat in categories:
                data_per_cat = data[cat][idxTime:]
                data_ordered = np.zeros(days)
                for i in range(len(days_used)):
                    idx_day = all_days_week.index(days_used[i])
                    data_ordered[idx_day] = data_per_cat[i]

                ax1.plot(list(range(days)), data_ordered[::-1], type_lines[cat], label=cat, alpha=0.8)

            ax1.legend()
            ax1.grid()
            ax1.set_xticks(list(range(days)), all_days_week[::-1])
            plt.xticks(fontsize=8, rotation=30)

        if timePlot == "Month":
            days = 7
            base = date.today()
            relevant_days = [base - datetime.timedelta(days=x) for x in range(0,31,5)]  #Count only 6 days of the month
            days_used = data["Entry"][idxTime:]
            for cat in categories:
                data_per_cat = data[cat][idxTime:]
                data_ordered = np.zeros(days)
                for i in range(len(days_used)):
                    idx_day = index_month_division(days_used[i], relevant_days)
                    data_ordered[idx_day] += data_per_cat[i]

                ax1.plot(list(range(days)), data_ordered[::-1], type_lines[cat], label=cat, alpha=0.8)

            ax1.legend()
            ax1.grid()
            ax1.set_xticks(list(range(days)),relevant_days[::-1])
            plt.xticks(fontsize=8, rotation=30)

        if timePlot == "6Month":
            days = 7
            base = date.today()
            relevant_days = [base - datetime.timedelta(days=x) for x in range(0,181,30)]  #Count each month
            days_used = data["Entry"][idxTime:]
            for cat in categories:
                data_per_cat = data[cat][idxTime:]
                data_ordered = np.zeros(days)
                for i in range(len(days_used)):
                    idx_day = index_month_division(days_used[i], relevant_days)
                    data_ordered[idx_day] += data_per_cat[i]

                ax1.plot(list(range(days)), data_ordered[::-1], type_lines[cat], label=cat, alpha=0.8)

            ax1.legend()
            ax1.grid()
            ax1.set_xticks(list(range(days)),relevant_days[::-1])
            plt.xticks(fontsize=8, rotation=30)

def setMainWin(mainGui, state, levels):
    #Level control
    mainGui.labelNivelGeneral.setText(str(levels["Total"]))
    mainGui.labelNivelProgramming.setText(str(levels["Programming"]))
    mainGui.labelNivelReading.setText(str(levels["Reading"]))
    mainGui.labelNivelMusic.setText(str(levels["Music"]))
    mainGui.labelNivelGaming.setText(str(levels["Gaming"]))
    mainGui.labelNivelWatched.setText(str(levels["Watched"]))
    mainGui.labelNivelLenguage.setText(str(levels["Others"]))

    #Bounds control
    bProg = lowerUpperBandForLevel(levels["Programming"])
    bRead = lowerUpperBandForLevel(levels["Reading"])
    bMusic = lowerUpperBandForLevel(levels["Music"])
    bGam = lowerUpperBandForLevel(levels["Gaming"])
    bWat = lowerUpperBandForLevel(levels["Watched"])
    bLan = lowerUpperBandForLevel(levels["Others"])

    mainGui.labelBarInfProgramming.setText(str(bProg[0]))
    mainGui.labelBarSupProgramming.setText(str(bProg[1]))
    mainGui.labelBarInfReading.setText(str(bRead[0]))
    mainGui.labelBarSupReading.setText(str(bRead[1]))
    mainGui.labelBarInfMusic.setText(str(bMusic[0]))
    mainGui.labelBarSupMusic.setText(str(bMusic[1]))
    mainGui.labelBarInfGaming.setText(str(bGam[0]))
    mainGui.labelBarSupGaming.setText(str(bGam[1]))
    mainGui.labelBarInfWatched.setText(str(bWat[0]))
    mainGui.labelBarSupWatched.setText(str(bWat[1]))
    mainGui.labelBarInfLenguage.setText(str(bLan[0]))
    mainGui.labelBarSupLenguage.setText(str(bLan[1]))

    #Bar status
    midP = state["Programming"]
    midR = state["Reading"]
    midM = state["Music"]
    midG = state["Gaming"]
    midW = state["Watched"]
    midL = state["Others"]

    porP = barUpdate(mainGui.barProgramming, midP, bProg)
    porR = barUpdate(mainGui.barReading, midR, bRead)
    porM = barUpdate(mainGui.barMusic, midM, bMusic)
    porG = barUpdate(mainGui.barGaming, midG, bGam)
    porW = barUpdate(mainGui.barWatched, midW, bWat)
    porL = barUpdate(mainGui.barLenguage, midL, bLan)
    
    #Mid label
    midLabelSetup(mainGui.labelBarMidPrograming, midP, porP, 321, True)
    midLabelSetup(mainGui.labelBarMidReading, midR, porR, 471, True)
    midLabelSetup(mainGui.labelBarMidMusic, midM, porM, 631, True)
    midLabelSetup(mainGui.labelBarMidGaming, midG, porG, 321, False)
    midLabelSetup(mainGui.labelBarMidWatched, midW, porW, 471, False)
    midLabelSetup(mainGui.labelBarMidLenguage, midL, porL, 631, False)

def customLayout(gui, category, level, hours):
    """
    gui: Object with the window with the components.
    Category: String with the name of the category.
    Levels: Dicc with the info of the levels.
    Hours: Dicc with the info of the accumulated hours.
    Creates the pop up window with the appropiate template for
    each category.

    """
    gui.generalName.setText(category)
    activiy_names = catToActivity(category) 
    
    bounds1 = lowerUpperBandForLevel(level[activiy_names[0]]) 
    bounds2 = lowerUpperBandForLevel(level[activiy_names[1]]) 

    middle1 = hours[activiy_names[0]]
    middle2 = hours[activiy_names[1]]
    if activiy_names[2] != "":
        bounds3 = lowerUpperBandForLevel(level[activiy_names[2]]) 
        middle3 = hours[activiy_names[2]]

    #Name of the activities
    gui.activity1.setText(activiy_names[0])
    gui.labelNivelAct1.setText(str(level[activiy_names[0]]))
    gui.activity2.setText(activiy_names[1])
    gui.labelNivelAct2.setText(str(level[activiy_names[1]]))
    gui.activity2.setText(activiy_names[1])
    gui.activity3.setText(activiy_names[2])

    #Name of the upped and lower bounds
    gui.labelBarInfAct1.setText(str(bounds1[0]))
    gui.labelBarSupAct1.setText(str(bounds1[1]))
    gui.labelBarInfAct2.setText(str(bounds2[0]))
    gui.labelBarSupAct2.setText(str(bounds2[1]))
    if activiy_names[2] != "":
        gui.labelBarInfAct3.setText(str(bounds3[0]))
        gui.labelBarSupAct3.setText(str(bounds3[1]))
        gui.labelNivelAct3.setText(str(level[activiy_names[2]]))
    else:
        gui.addButtonAct3.hide()
        gui.minusButtonAct3.hide()
        gui.labelBarInfAct3.setText("")
        gui.labelBarSupAct3.setText("")
        gui.labelNivelAct3.setText("")

    #Bar position
    gui.barActivity1.setFormat("")
    porcentajeValue1 = int(((middle1 - bounds1[0]) / (bounds1[1] - bounds1[0])) * 100)
    gui.barActivity1.setValue(porcentajeValue1)

    gui.barActivity2.setFormat("")
    porcentajeValue2 = int(((middle2 - bounds2[0]) / (bounds2[1] - bounds2[0])) * 100)

    gui.barActivity2.setValue(porcentajeValue2)

    if activiy_names[2] != "":
        gui.barActivity3.setFormat("")
        porcentajeValue3 = int(((middle3 - bounds3[0]) / (bounds3[1] - bounds3[0])) * 100)
        gui.barActivity3.setValue(porcentajeValue3)
    else:
        gui.barActivity3.hide()
    
    #Middle hours mark
    if porcentajeValue1 > 5 and porcentajeValue1 < 95:
        gui.labelBarMidAct1.setText(str(middle1))
        deltax = int(3.05 * porcentajeValue1 + 27)
        gui.labelBarMidAct1.move(deltax, 178)
    else:
        gui.labelBarMidAct1.setText("")

    if porcentajeValue2 > 5 and porcentajeValue2 < 95:
        gui.labelBarMidAct2.setText(str(middle2))
        deltaX = int(3.05 * porcentajeValue2 + 27)
        gui.labelBarMidAct2.move(deltaX, 328)
    else:
        gui.labelBarMidAct2.setText("")

    if activiy_names[2] != "":
        if porcentajeValue3 > 5 and porcentajeValue3 < 95:
            gui.labelBarMidAct3.setText(str(middle3))
            deltaX = int(3.05 * porcentajeValue3 + 27)
            gui.labelBarMidAct3.move(deltaX, 474)
        else:
            gui.labelBarMidAct3.setText("")
    else:
        gui.labelBarMidAct3.setText("")

