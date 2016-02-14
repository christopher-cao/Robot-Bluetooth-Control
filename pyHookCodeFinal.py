import pyHook, serial, time, collections, csv, os

start_time = time.time()
bluetooth = serial.Serial("COM21", 9600)



def disconnect():
    print("Bluetooth disconnected")
    bluetooth.close()

def connect():
    print("Bluetooth connected")
    bluetooth.open()


key_record = []
time_record =[]
file_counter=0
recording = False


def OnKeyboardEvent(event):
    global recording, start_time, key_record, time_record, file_counter, commands, times, lineCounter, bluetooth
    elapsed_time = time.time() - start_time
    
    print(event.KeyID)
    if (event.KeyID == 13):
        #Changes the state of recording with every button press
        recording = not recording
        
        #Resets the start time if recording is true
        if (recording):
            start_time = time.time()
            print("Now recording to " + str(file_counter) + ".csv!")
            return False
        
        #Prints the lists and clears them when recording is turned off (by pressing enter) 
        else:
            print("Saving now (PRESS ENTER BEFORE RECORDING AGAIN!!!)")
            print("Keys pressed: " + str(key_record))
            print("Time record: " + str(time_record))
            #SAVE THE LISTS IN CSV FILE
            #First save the two lists as a list of lists for writing in the CSV file
            fileName = str(file_counter) + ".csv"
            #pathFile = open("path" +str(file_counter) + ".csv", "wt")
            pathFile = open(fileName, "wt")
            file_counter +=1
            if file_counter == 2:
                file_counter = 0
            writer = csv.writer(pathFile)
            for x in range(len(time_record)):
                key_record[x] = str(key_record[x])
                time_record[x] = str(time_record[x])
                #writer.writerow([str(key_record[x]), str(time_record[x])])
            writer.writerow(key_record)
            writer.writerow(time_record)
                
                #Need to reconvert this time record to a float
            # convert time record to float
            key_record.clear()
            time_record.clear()
            print("This file was saved as: " + fileName)
            return False

    #If the key pressed is not enter and the current mode is recording, 
    elif (chr(event.Ascii) != '\r' and event.KeyID != 221 and event.KeyID != 162 and recording):
        bluetooth.write(str(chr(event.Ascii)).encode())
        print("Key: " + chr(event.Ascii) + " Time: " + str(elapsed_time))
        key_record.append(chr(event.Ascii))
        time_record.append(elapsed_time)
    
    #Open serial port with = key
    #elif(event.KeyID == 187):
        #connect()
    #Close serial port with - key 
    #elif(event.KeyID == 189):
        #disconnect()
    else:
        bluetooth.write(str(chr(event.Ascii)).encode())
        pass
        
    #If 'Tab' is pressed...
    if(event.KeyID == 9 and not recording):
            #Load the array from the file (read)
            timer = time.time()
            eventIndex = 0
            commands = [] #Need to empty the commands and times everytime tab is pressed
            times = []

            #Parse the csv here
            #fileName = input("Which file would you like to open?") + ".csv"
            fin = open("0.csv", 'r')
            fileReader = csv.reader(fin)

            lineCounter = 0
            for line in fin:
                line = line.strip()
                if (lineCounter == 0):
                    print(line)
                    commands = line.split(",")
                elif(lineCounter == 2):
                    print(line)
                    times = line.split(",")
                    for i in range(len(times)):
                        times[i] = float(times[i])
                else:
                    pass
                #print(commandList)
                #print(lineCounter)
                lineCounter += 1
            print(commands)
            print(times)
            
            while(True):
                if(eventIndex < len(commands)-1):
                    if(times[eventIndex] < time.time() - timer):
                        print("Command: " +commands[eventIndex] + "    |||     Time: " + str(times[eventIndex])) #send event through bluetooth
                        #send event through bluetooth
                        #For some reason ignores the first two commands
                        bluetooth.write(str(commands[eventIndex]).encode())
                        eventIndex +=1
                else:
                    bluetooth.write("m".encode())
                    break

    #If ] is pressed 
    if(event.KeyID == 192 and not recording):
                #Load the array from the file (read)
                timer = time.time()
                eventIndex = 0
                commands = [] #Need to empty the commands and times everytime tab is pressed
                times = []

                #Parse the csv here
                fin = open("1.csv", 'r')
                fileReader = csv.reader(fin)

                lineCounter = 0
                for line in fin:
                    line = line.strip()
                    if (lineCounter == 0):
                        print(line)
                        commands = line.split(",")
                    elif(lineCounter == 2):
                        print(line)
                        times = line.split(",")
                        for i in range(len(times)):
                            times[i] = float(times[i])
                    else:
                        pass
    
                    lineCounter += 1
                print(commands)
                print(times)
                
                while(True):
                    if(eventIndex < len(commands) -1):
                        if(times[eventIndex] < time.time() - timer):
                            print("Command: " +commands[eventIndex] + "    |||     Time: " + str(times[eventIndex])) #send event through bluetooth
                        #send event through bluetooth
                        #For some reason ignores the first two commands
                            bluetooth.write(str(commands[eventIndex]).encode())
                            eventIndex +=1
                    else:
                        bluetooth.write("m".encode())
                        break
                                              
    return True


hooks_manager = pyHook.HookManager ( )
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard ( )


