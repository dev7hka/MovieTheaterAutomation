import sys
import string
hallist,seatlist = [],[]
outfile = open("out.txt","w")
def Printer(x): # Print function in order to print both in console and to the output file
    print(x)
    outfile.write(x+"\n")
def Createhall(name,row,column):
    if name in hallist:
        Printer("Warning: Cannot create the hall for the second time. The cinema has already "+name)
    elif row > 26 :
        Printer("Maximum limit of row is 26 !!!")
    else:
        hallist.append(name)
        templist = []
        for i in string.ascii_uppercase:
            for j in range(column):
                if string.ascii_uppercase.index(i) > row:
                    break
                templist.append([i,j,"null"])
        seatlist.append(templist)
        Printer("The hall '{}' having {} seats has been created".format(name,row*column))
def Check1(name,row,column): # to check if the given row and column is suitable
    check2,check3 = False,False
    for i in seatlist[hallist.index(name)]:
        if i[0] == row:
            check2 = True
            break
    for j in seatlist[hallist.index(name)]:
        if j[1] == column:
            check3= True
            break
    return check2,check3
def Check2(name,row,column): # to check if the seat's situation if it is appropriate to sell
    for i in seatlist[hallist.index(name)]:
        if i[0] == row and i[1] == column:
            return i[2]
def Check3(name): # to check if the given hallname is exists in theater
    check = True if name in hallist else False
    if check == False:
        Printer("There is no hall called " + name)
        return True
def SellTicket(pername,fare,name,seat): # to sell single seats such as B7 or A12
    if Check3(name) != True:
        a,b = Check1(name,seat[0],int(seat[1:]))
        if a == False:
            Printer("Error: The hall '{}' has less row than the specified index {}!".format(name,seat))
        if b == False:
            Printer("Error: The hall '{}' has less column than the specified index {}!".format(name,seat))
        else:
            if Check2(name,seat[0],int(seat[1:])) == "null":
                index = seatlist[hallist.index(name)].index([seat[0],int(seat[1:]),"null"])
                seatlist[hallist.index(name)][index] = [seat[0],int(seat[1:]),fare]
                Printer("Success: {} has bought {} at {}".format(pername,seat,name))
            else:
                Printer("Error: The seat {} cannot be sold to {} since it was already sold!".format(seat,pername))

def SellTicket2(pername,fare,name,seat): #to seat multi-seats such as A12-15 or c3-7
    if Check3(name) != True:
        x = seat.split("-")
        result = "good"
        for i in range(int(x[0][1:]),int(x[1])):
            a,b = Check1(name,x[0][0],i)
            if a == False:
                Printer("Error: The hall '{}' has less row than the specified index {}!".format(name,seat))
                result = "bad"
                break
            if b == False:
                Printer("Error: The hall '{}' has less column than the specified index {}!".format(name, seat))
                result = "bad"
                break
            else:
                if Check2(name,x[0][0],i) != "null":
                    Printer("Warning: The seats {} cannot be sold to {} due some of them have already been sold!".format(seat,pername))
                    result = "bad"
                    break
        if result == "good":
            for i in range(int(x[0][1:]),int(x[1])):
                index = seatlist[hallist.index(name)].index([x[0][0],i,"null"])
                seatlist[hallist.index(name)][index] = [x[0][0],i,fare]
            Printer("Success: {} has bought {} at {}".format(pername,seat,name))
def CancelTicket(name,seat): # to cancel single seats such as B12 or D7
    if Check3(name) != True:
        a,b = Check1(name,seat[0],int(seat[1:]))
        if a == False:
            Printer("Error: The hall '{}' has less row than the specified index {}!".format(name,seat))
        if b == False:
            Printer("Error: The hall '{}' has less column than the specified index {}!".format(name,seat))
        else:
            rst = Check2(name,seat[0],int(seat[1:]))
            if rst != "null":
                index = seatlist[hallist.index(name)].index([seat[0],int(seat[1:]),rst])
                seatlist[hallist.index(name)][index] = [seat[0],int(seat[1:]),"null"]
                Printer("Success: The seat {} at {} has been canceled and now ready to be sold again".format(seat,name))
            else:
                Printer("Error: The seat {} at {} has already been free! Nothing to cancel".format(seat,name))
def CancelTicket2(name,seat): # to cancel multi-seats such as E15-21 or G3-5
    if Check3(name) != True:
        x = seat.split("-")
        result = "good"
        for i in range(int(x[0][1:]), int(x[1])):
            a, b = Check1(name, x[0][0], i)
            if a == False:
                Printer("Error: The hall '{}' has less row than the specified index {}!".format(name, seat))
                result = "bad"
                break
            if b == False:
                Printer("Error: The hall '{}' has less column than the specified index {}!".format(name, seat))
                result = "bad"
                break
            else:
                if Check2(name, x[0][0], i) == "null":
                    Printer("Error: The seats {} at ’{}’ has already been free! Nothing to cancel".format(seat,name))
                    result = "bad"
                    break
        if result == "good":
            for i in range(int(x[0][1:]), int(x[1])):
                index = seatlist[hallist.index(name)].index([x[0][0], i,Check2(name,x[0][0],i)])
                seatlist[hallist.index(name)][index] = [x[0][0], i,"null"]
            Printer("Success: The seats {} at ’{}’ have been canceled and now ready to be sold again".format(seat, name))
        if result == "bad":
            x = seat.split("-")
            for i in range(int(x[0][1:]),int(x[1])):
                CancelTicket(name,x[0][0]+str(i))
def Balance(name): # shows the revenue of the given hall
    if Check3(name) != True:
        sumst,sumfl = 0,0
        for i in seatlist[hallist.index(name)]:
            if i[2] == "student":
                sumst += 5
            elif i[2] == "full":
                sumfl += 10
        Printer("Hall report of '{}'".format(name))
        Printer((len("Hall report of '{}'".format(name))*"-"))
        Printer("Sum of students = {}, Sum of full fares = {}, Overall = {}".format(sumst,sumfl,sumst+sumfl))
def ShowHall(name): # to visualize the theater seats
    if Check3(name) != True:
        showlist = []
        a,b = "A",0
        for i in seatlist[hallist.index(name)]:
            if i[0] == a:
                b=i[1]
            else:
                break
        line = "  "
        for i in range(b+1):
            if i < 9:
                line+=str(i) +"  "
            elif i < 100:
                line+=str(i) +" "
            else:
                line+=str(i) +""
        showlist.append(line)
        line = "A "
        b = "A"
        for i in seatlist[hallist.index(name)]:
            if i[0] == b:
                if i[2] == "full":
                    line+="F  "
                elif i[2] == "student":
                    line+="S  "
                else:
                    line+="X  "
            else:
                showlist.append(line.rstrip())
                b= i[0]
                line = i[0] + " "
                if i[2] == "null":
                    line+="X  "
                elif i[2] == "student":
                    line+="S  "
                else:
                    line+="F  "
        Printer("Printing hall layout of " + name)
        for i in showlist[::-1]:
            Printer(i)
inputfile = open(sys.argv[1],"r")
commands = []
for line in inputfile:
    line = line.rstrip(" ")
    line = line.replace("\n","")
    x = line.split(" ",)
    commands.append(x)
inputfile.close()
for line in commands:
    if line[0] == "CREATEHALL":
        x = line[2].split("x")
        if len(line) < 3:
            Printer("Error: Not enough parameters for creating a hall!")
        elif len(line) > 3:
            Printer("Error: Too much parameters for creating a hall")
        elif len(x) != 2:
            Printer("Given seat numbers is not suitable to create hall! ")
        else:
            Createhall(line[1],int(x[0]),int(x[1]))
    elif line[0] == "SELLTICKET":
        if len(line) == 5 :
            if "-" in line[4]:
                SellTicket2(line[1],line[2],line[3],line[4])
            else:
                SellTicket(line[1],line[2],line[3],line[4])
        else:
            seats = line[4:]
            for seat in seats:
                if "-" in seat:
                    SellTicket2(line[1],line[2],line[3],seat)
                else:
                    SellTicket(line[1],line[2],line[3],seat)
    elif line[0] == "CANCELTICKET":
        if len(line) == 3:
            if "-" in line[2]:
                CancelTicket2(line[1],line[2])
            else:
                CancelTicket(line[1],line[2])
        else:
            seats = line[2:]
            for i in seats:
                if "-" in i:
                    CancelTicket2(line[1],i)
                else:
                    CancelTicket(line[1],i)
    elif line[0] == "BALANCE":
        if len(line) == 2 :
            Balance(line[1])
        else:
            for i in line[1:]:
                Balance(i)
    elif line[0] == "SHOWHALL":
        if len(line) == 2:
            ShowHall(line[1])
        else:
            for i in line[1:]:
                ShowHall(i)
outfile.close()