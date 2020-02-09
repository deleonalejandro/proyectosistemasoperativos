#
#Misc. Libraries
import os
import re
import time
import math
import sys
import statistics
from decimal     import Decimal, ROUND_DOWN

def SwapIn(ProcessLocation, SwapMemory):
    #Write code
    Indexes = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
    return Indexes


def SwapOut(FreeSpace, ProgramSize, SwapMemory, MainMemory, vFIFO, vLRU, Method):
#Fifo Method 
    if Method == 1:
        IndexesFinalLRU = []
        IndexesFinal = []
        newSpace = 0
        FIFOIndex = 0
        while newSpace < ProgramSize:
            Indexes = [i for i, s in enumerate(MainMemory) if vFIFO[FIFOIndex] in s]
            IndexesFinal.extend(Indexes)
            newSpace = len(IndexesFinal) + len(FreeSpace)
            FIFOIndex += 1 
    else:
        IndexesFinalLRU = []
        newSpace = 0
        LRUindex = 0
        while newSpace < ProgramSize:
            Indexes = [i for i, s in enumerate(MainMemory) if min(vLRU)[0] in s]
            IndexesFinal.extend(Indexes)
            newSpace = len(IndexesFinal) + len(FreeSpace)

            #Removing least recently used, for the second least recently used. 
            IndexesLRURemove = [i for i, s in enumerate(vLRU) if min(vLRU)[0] in s]
            IndexesFinalLRU.extend(IndexesLRURemove)

            for i in range(len(IndexesLRURemove)):
                vLRU.pop([IndexesLRURemove[i]])
        FIFOIndex = 0

    return [FIFOIndex, IndexesFinal, IndexesFinalLRU]
    

#Main paging definition, this section covers the FIFO paging system but still missing LIFO
def CheckMemory(MainMemory, SwapMemory, PageFrameSize, Method):
    #Lista F 
    ToPrintF = []
    #Index to iterate through the whole instruction list
    #Printout variable to inspect the output
    ToPrintOut = []
    #Page number initializer
    PageNum = 0
    #Number of page, recovered from instruction set
    num = 0
    #Initializer for the index that'll be used up next
    Index = 0
    #Boolean variable that will test the list and notify of any jumps in the memory
    Jumped = False
    #Iterator to go through the list
    IteratorForMainMemory = 0
    #List of processes currently in the memory
    ListofProcessesAdded = []
    #Iterator for memory, this will move through the memory range
    IteratorForSwapMemory = 0
    #Variable to hold the program size in itself, it will be modified later
    InitialProgramSize = 0
    #Variable that will hold the process ID from the client
    ProcessID = 0
    #I will explain this variable later on...
    RemainingMemoryToAddress = 0
    #Total execution time
    Turnaround = 0.00000000000
    #NOT USED, pending implementation
    Freememory = []
    #Boolean variable to test if process is in main memory
    IsInMainMemory = False
    #Boolean variable to test if process is in swap memory
    IsInSwapMemory = False
    #Method FIFO = 1 and LRU = 0
    SelectedMethod = int(Method) 
    #Creating lists
    FIFO = []
    LRU = []



    #Begin by trying to iterate through the list, this is to check if the list is valid
    start_time = time.time()

    while Index < len(InstructionsToRun):
        #If the list wasn't empty then we can begin processing the data, we know that the client is sending a tuple and a quadruple
        print("\nInstruction to run")
        ToPrintOut.append(["Instruction: " + InstructionsToRun[Index]])
        print(InstructionsToRun[Index])

        #If we find a designator P then it indicates that we must load the program
        if 'P' in InstructionsToRun[Index]:
            #We split the data to make it easier to iterate through the tuple or quadruple
            SplittedData = InstructionsToRun[Index].split(' ')
            #This will check if the string of instructions came up fine, again
            try:
                print("Program size: "+ SplittedData[1]+ " bytes")
                #We obtain the Initial Program Size from the client
                InitialProgramSize = SplittedData[1]
                #We obtain the Process ID
                ProcessID = SplittedData[2][0:-1]
                #ProcessID = ''.join(SplittedData[2].splitlines())
                #We need the program size to see how much memory it will use
                ProgramSize = math.ceil(int(InitialProgramSize)/PageFrameSize)
                #We proceed to try loading up the memory, specially important to switch memories
                try:
                    ProcessLocation = ("Process ID" + " " + str(ProcessID))
                    ListofProcessesAdded.append(str(ProcessLocation))

                    #Loop to cycle through the main memory list and fill it up with the program
                    #Check if process ID is in the memory
                    #Check if Process is already in the system

                    IsInMainMemory = any(ProcessLocation in sl for sl in MainMemory)
                    IsInSwapMemory = any(ProcessLocation in sl for sl in SwapMemory)

                    if IsInMainMemory == True:
                        print("Program is loaded in main memory")
                        LRU.append([ProcessLocation,time.time()])

                    
                    if IsInMainMemory == False:
                        print("Program is not loaded in main memory")
                        #Looks for free pages in main memory
                        FreeSpace = [x for x, s in enumerate(MainMemory) if "Page #" in s]

                        if ProgramSize <= len(FreeSpace):
                            Capacity = True

                            if IsInSwapMemory == False:

                                ToPrintOut.append(["-------Process loaded------\n"])
                                for i in range(0, ProgramSize):
                                    MainMemory[FreeSpace[i]][2] = "Page "+str(i)
                                    MainMemory[FreeSpace[i]][3] = ProcessLocation
                                    
                                    #Printing physical address
                                    print("Page {0} in Physical Address: {1}".format(i, str(MainMemory[FreeSpace[i]][1])))
                                    ToPrintOut.append("Page "+str(i)+ " in Physical Address: "+ str(MainMemory[FreeSpace[i]][1]))
                                
                                FIFO.append(ProcessLocation)
                                LRU.append([ProcessLocation,time.time()])
                            else:
                                IndexToSwapIn = SwapIn(ProcessLocation, SwapMemory)
                                for i in range(0, len(IndexToSwapIn[1])):
                                    MainMemory[FreeSpace[i]][2] = SwapMemory[IndexToSwapIn[i]][2]
                                    MainMemory[FreeSpace[i]][3] = SwapMemory[IndexToSwapIn[i]][3]
                                    
                                    #Printing physical address
                                    print("Page {0} in Physical Address: {1}".format(i,str(MainMemory[FreeSpace[i]][1])))
                                    ToPrintOut.append("Page "+str(i)+ " in Physical Address: "+ str(MainMemory[FreeSpace[i]][1]))
                                
                                FIFO.append(ProcessLocation)
                                LRU.append([ProcessLocation,time.time()])

                        elif ProgramSize > len(MainMemory):
                            print("Error: Program does not fit into memory")
                            pass
                        
                        else:
                            print("Warning: Page Fault")
                            #Saving page fault
                            ToPrintF.append([ProcessLocation, 0, 1])
                            print("-----Switching to SwapMemory-------")
                            IndexToSwapOut = SwapOut(FreeSpace, ProgramSize, SwapMemory, MainMemory, FIFO, LRU, SelectedMethod)
                            
                            #Deleting FIFO Array and LRU Array indexes
                            for j in range(len(IndexToSwapOut[2])):
                                LRU.pop(IndexToSwapOut[2][j])

                            FIFO[0:IndexToSwapOut[0]] = []


                            #Check if swap memory has space
                            FreeSpaceSwap = [x for x, s in enumerate(SwapMemory) if "Page #" in s]
                            print("Loading SwapMemory")
                            for i in range(0, len(IndexToSwapOut[1])):
                                SwapMemory[FreeSpaceSwap[i]][2] = MainMemory[IndexToSwapOut[1][i]][2]
                                SwapMemory[FreeSpaceSwap[i]][3] = MainMemory[IndexToSwapOut[1][i]][3]
                                print("{0} from {1} into  SwapAddress: {2}".format(MainMemory[IndexToSwapOut[1][i]][2], MainMemory[IndexToSwapOut[1][i]][3], str(SwapMemory[FreeSpaceSwap[i]][1])))
                               

                            #Deleting main memory 
                            for i in range(len(IndexToSwapOut[1])):
                                MainMemory[IndexToSwapOut[1][i]][2] = "Page #"
                                MainMemory[IndexToSwapOut[1][i]][3] = "Process ID #"

                            #Calculating new space
                            FreeSpace = [x for x, s in enumerate(MainMemory) if "Page #" in s]

                            ToPrintOut.append(["-------Process loaded------\n"])
                            print("Loading from SwapMemory to MainMemory")
                            for i in range(0, ProgramSize):
                                MainMemory[FreeSpace[i]][2] = "Page "+str(i)
                                MainMemory[FreeSpace[i]][3] = ProcessLocation
                                #Printing physical address
                                print("Page {0} in Physical Address: {1}".format(i,str(MainMemory[FreeSpace[i]][1])))
                                ToPrintOut.append("Page "+str(i)+ " in Physical Address: "+ str(MainMemory[FreeSpace[i]][1]))
                            
                            FIFO.append(ProcessLocation)
                            LRU.append([ProcessLocation,time.time()])

                except:
                    print("Trouble!!!!!!!!!!!!!")
            except:
                print("Trouble^2")

                        

        elif 'A' in InstructionsToRun[Index]:

            SplittedData = InstructionsToRun[Index].split(' ')

            #Check if we received all data and its validity
            try:
                AccessVirtualMem = SplittedData[1]
                AccessVirtualMem = int(AccessVirtualMem)
                AccessProcessID = SplittedData[2]
                AccessProcessID = int(AccessProcessID)
                AccessModifierBit = SplittedData[3]
                AccessModifierBit = int(AccessModifierBit)
                #Manual check
                #Calculate the real address and the page frame.
                LogicPageAddress = math.floor(AccessVirtualMem/PageFrameSize)
                #Append a string with the desired page number to find real address
                PageNumLoc = ("Page" + " " + str(LogicPageAddress))
                #Append a string with the desired process ID to find the memory location
                ProcessLocation = ("Process ID" + " " + str(AccessProcessID))
                RealAdIndex = [i for i, s in enumerate(MainMemory) if PageNumLoc in s and ProcessLocation in s]

            except:
                pass

            if len(RealAdIndex) == 1:
                RealAddress = MainMemory[RealAdIndex[0]][1]
                MainMemory[RealAdIndex[0]][0] = AccessModifierBit
                print("Real Address " + str(RealAddress))
                print("Read")

                if AccessModifierBit == 1:
                        print("Modified")

                ToPrintOut.append("Real Address " + str(RealAddress))
                LRU.append([ProcessLocation,time.time()])

            else:
                print("Warning: Page Fault \n")
                #Saving page fault
                ToPrintF.append([ProcessLocation, 0, 1])
                if any(ProcessLocation in sl for sl in SwapMemory):
                    IndexToSwapIn = SwapIn(ProcessLocation, SwapMemory)
                    ProgramSize = len(IndexToSwapIn)

                    FreeSpace = [x for x, s in enumerate(MainMemory) if "Page #" in s]
                    
                    if ProgramSize <= len(FreeSpace):
                        Capacity = True
                        ToPrintOut.append(["-------Process loaded------\n"])

                        for i in range(0, ProgramSize):
                            MainMemory[FreeSpace[i]][0] = SwapMemory[IndexToSwapIn[i]][0]
                            MainMemory[FreeSpace[i]][2] = SwapMemory[IndexToSwapIn[i]][2]
                            MainMemory[FreeSpace[i]][3] = SwapMemory[IndexToSwapIn[i]][3]
                            #Printing physical address
                            print("Page {0} in Physical Address: {1} from Swap Memory Adress: {2}".format(i,str(MainMemory[FreeSpace[i]][1]),SwapMemory[IndexToSwapIn[i]][1]))
                            ToPrintOut.append("Page "+str(i)+ " in Physical Address: "+ str(MainMemory[FreeSpace[i]][1])+" from Swap Memory Adress" + str(SwapMemory[IndexToSwapIn[i]][1]))
                            SwapMemory[IndexToSwapIn[i]][3] = "Process ID #"
                            SwapMemory[IndexToSwapIn[i]][2] = "Page #"
                            SwapMemory[IndexToSwapIn[i]][0] = 0
                                
                        FIFO.append(ProcessLocation)
                        LRU.append([ProcessLocation,time.time()])
                    else:
                        print("-----Switching to SwapMemory-------")
                        IndexToSwapOut = SwapOut(FreeSpace, ProgramSize, SwapMemory, MainMemory, FIFO, LRU, SelectedMethod)
                        
                        #Deleting FIFO Array and LRU Array indexes
                        for j in range(len(IndexToSwapOut[2])):
                            LRU.pop(IndexToSwapOut[2][j])

                        FIFO[0:IndexToSwapOut[0]] = []


                        #Check if swap memory has space
                        FreeSpaceSwap = [x for x, s in enumerate(SwapMemory) if "Page #" in s]
                        for i in range(0, len(IndexToSwapOut[1])):
                            SwapMemory[FreeSpaceSwap[i]][0] = MainMemory[IndexToSwapOut[1][i]][0]
                            SwapMemory[FreeSpaceSwap[i]][2] = MainMemory[IndexToSwapOut[1][i]][2]
                            SwapMemory[FreeSpaceSwap[i]][3] = MainMemory[IndexToSwapOut[1][i]][3]
                            

                        #Deleting main memory and swapmemory
                        for i in range(len(IndexToSwapOut[1])):
                            MainMemory[IndexToSwapOut[1][i]][0] = 0
                            MainMemory[IndexToSwapOut[1][i]][2] = "Page #"
                            MainMemory[IndexToSwapOut[1][i]][3] = "Process ID #"

                        IndexToRemove = [idx for idx, val in enumerate(SwapMemory) if ProcessLocation in val]
                           
                        for y in range(len(IndexToRemove)):
                            print("Page {0} deleted from SwapAddress: {1}".format(y, str(SwapMemory[IndexToRemove[y]][1])))
                            ToPrintOut.append("Page "+str(y)+ " deleted from Swap Address: "+ str(SwapMemory[IndexToRemove[y]][1]))
                            SwapMemory[IndexToRemove[y]][0] = 0
                            SwapMemory[IndexToRemove[y]][2] = "Page #"
                            SwapMemory[IndexToRemove[y]][3] = "Process ID #"
                        print(ProcessLocation + " successfully deleted from Swap Memory.")                        

                        #Calculating new space
                        FreeSpace = [x for x, s in enumerate(MainMemory) if "Page #" in s]

                        ToPrintOut.append(["-------Process loaded------\n"])
                        print("Loading from SwapMemory to MainMemory")
                        for i in range(0, ProgramSize):
                            MainMemory[FreeSpace[i]][0] = AccessModifierBit
                            MainMemory[FreeSpace[i]][2] = "Page "+str(i)
                            MainMemory[FreeSpace[i]][3] = ProcessLocation
                            #Printing physical address
                            print("Page {0} in Physical Address: {1}".format(i,str(MainMemory[FreeSpace[i]][1])))
                            ToPrintOut.append("Page "+str(i)+ " in Physical Address: "+ str(MainMemory[FreeSpace[i]][1]))
                        
                        FIFO.append(ProcessLocation)
                        LRU.append([ProcessLocation,time.time()])

                    RealAdIndex = [i for i, s in enumerate(MainMemory) if PageNumLoc in s and ProcessLocation in s]
                    RealAddress = MainMemory[RealAdIndex[0]][1]
                    MainMemory[RealAdIndex[0]][0] = AccessModifierBit
                    print("Real Address " + str(RealAddress))
                    print("Read")

                    if AccessModifierBit == 1:
                        print("Modified")

                    ToPrintOut.append("Real Address " + str(RealAddress))
                    LRU.append([ProcessLocation,time.time()])

                else:
                    print("Process not in main or swap memory")
                    ToPrintOut.append("Process not in main or swap memory")
                
                

        elif 'L' in InstructionsToRun[Index]:
            SplittedDataL = InstructionsToRun[Index].split(' ')
            ProcessIDL = ''.join(SplittedDataL[1].splitlines())
            ProcessLocationL = ("Process ID" + " " + str(ProcessIDL))
            ToPrintOut.append("Deleted " + str(ProcessLocationL))
            try:
                ListofProcessesAdded.remove(str(ProcessLocationL))
                FIFO.remove(str(ProcessLocationL))
                
                

                #Delete from Main Memory

                IndexToRemove = [idx for idx, val in enumerate(MainMemory) if ProcessLocationL in val]

                for y in range(len(IndexToRemove)):
                    print("Page {0} deleted from Physical Address: {1}".format(y, str(MainMemory[IndexToRemove[y]][1])))
                    ToPrintOut.append("Page "+str(y)+ " deleted from Physical Address: "+ str(MainMemory[IndexToRemove[y]][1]))
                    MainMemory[IndexToRemove[y]][2] = "Page #"
                    MainMemory[IndexToRemove[y]][3] = "Process ID #"
                
                ListMinLRU = [LRU[i] for i, s in enumerate(LRU) if ProcessLocationL in s]
                minLRU = min(ListMinLRU)
                TurnATime = time.time() - minLRU[1]
                ToPrintF.append([ProcessLocationL, TurnATime, 0])

                #Deleting process from LRU
                LRUindex = [idx for idx, val in enumerate(LRU) if ProcessLocationL in val]
                for i in range(len(LRUindex)):
                    LRU.pop(LRUindex[i])
                

            except:
                print("Process is not in main memory, unable to comply with command")

            #Try to remove the process from the stack, if there's a process in the memory it will remove it
            #and it will check the swap memory to load it again
            if any(ProcessLocationL in sl for sl in SwapMemory):

                #Delete from Swap Memory

                IndexToRemove = [idx for idx, val in enumerate(SwapMemory) if ProcessLocationL in val]
                           
                for y in range(len(IndexToRemove)):
                    print("Page {0} deleted from SwapAddress: {1}".format(y, str(SwapMemory[IndexToRemove[y]][1])))
                    ToPrintOut.append("Page "+str(y)+ " deleted from Swap Address: "+ str(SwapMemory[IndexToRemove[y]][1]))
                    SwapMemory[IndexToRemove[y]][2] = "Page #"
                    SwapMemory[IndexToRemove[y]][3] = "Process ID #"
                print("Process successfully deleted from Swap Memory.")
                #Saving turnaround time
                ListMinLRU = [LRU[i] for i, s in enumerate(LRU) if ProcessLocationL in s]
                minLRU = min(ListMinLRU)
                TurnATime = time.time() - minLRU[1]
                ToPrintF.append([ProcessLocationL, TurnATime, 0])
            
            else:
                print("Process not in swap memory")                   

        elif 'E' in InstructionsToRun[Index]:
            print("Exiting...")
            with open('Result.txt', 'w') as f:
                for item in ToPrintOut:
                    f.write("%s\n" % item)
                f.close()
            break

        elif 'F' in InstructionsToRun[Index]:
            TotalSwaps = 0
            TotalTime = 0
            counter = 0
            print("Warning: When a page fault occurs, turnaround is 0.\n ")
            print("Process\t\t Turnaround[s]\t Page Fault \n----------------------------------------------")
            for i in range(len(ToPrintF)):
                print("{0}\t {1:2.4f}\t\t {2}".format(ToPrintF[i][0],ToPrintF[i][1],ToPrintF[i][2]))
                if ToPrintF[i][1] > 0:
                    counter += 1
                if ToPrintF[i][2] == 1:
                    TotalSwaps += 1  
                TotalTime += ToPrintF[i][1]
            print("Total swap-in and swap-out----> "+ str(TotalSwaps))
            #Creating average
            TurnAmean = TotalTime/counter
            print("Turnaround Average-----> "+ str(TurnAmean))

            
            


        end_time = time.time()
        Turnaround_P = end_time - start_time
        ToPrintOut.append(["Turnaround: " + str(Turnaround_P)])                        
        Index += 1

def MemoryGenerator(RealMemorySize, SwapMemorySize, PageSize, Method):
    PageFrames = 0
    SelectedMethod = Method
    AuxiliaryPageFrames = 0
    RunCheck = []
    #Generate the physical address list!
    if RealMemorySize != 0 and PageSize != 0:
        Tracker = 0
        PageFrameTracker = 0
        ModifierBit = 0
        PageFrames = RealMemorySize / PageSize
        AuxiliaryPageFrames = SwapMemorySize / PageSize
        mainMemList = [hex(x) for x in range(int(PageFrames))]
        swapMemList = [x for x in range(int(AuxiliaryPageFrames))]
        PhysicalAddress = []
        SwapMemory = []
        #Physical address memory creation, Main memory
        while Tracker < int(PageFrames):
            PhysicalAddress.append([ModifierBit, mainMemList[Tracker], "Page #", "Process ID #"])
            Tracker += 1
            PageFrameTracker +=1

        #Generate only if we exceed main memory range
        Tracker = 0
        while Tracker < int(AuxiliaryPageFrames):
            SwapMemory.append([ModifierBit, swapMemList[Tracker], "Page #", "Process ID #"])
            Tracker += 1
            PageFrameTracker +=1
        #Auxiliary address memory creation, Swap memory
        CheckMemory(PhysicalAddress, SwapMemory, PageSize, SelectedMethod)
        

#Begin here´
print("Usage: Open your file and select method ")
DatosEjecucion = open('.\Proyecto FIFO LRU\ArchivoTrabajo.txt', 'r')
InstructionsToRun = DatosEjecucion.readlines()
print("Datos recibidos")
#Input Data for the Memory sizes -> Like This MemoryGenerator(Main Memory Size, Swap Memory Size, Page Size, Instructions (Already Added into File))
#In this project use the following:
smethod = input("FIFO press 1 \n LRU press 2 \n")

MemoryGenerator(2048, 4096, 16, smethod)

#Ignore error, we are only trying to summon the function
