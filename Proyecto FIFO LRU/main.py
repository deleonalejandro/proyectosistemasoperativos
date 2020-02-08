#Misc. Libraries
import os
import re
import time
import math
import sys
from decimal     import Decimal, ROUND_DOWN

def SwapIn(SwappingPages, Method):
    try:
        #Avoiding errors
        if Method != 1 and Method != 0:
            print("Incorrectly defined method, will assume FIFO")
            Method = 1

        if Method == 1:
            #Here write FIFO code
        elif Method == 0:
            #Here write LRU code
    except:
        print("Error")
    


#Main paging definition, this section covers the FIFO paging system but still missing LIFO
def CheckMemory(MainMemory, SwapMemory, PageFrameSize):
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
    #Create lists FIFO and LRU for swapping. 
    FIFO = []
    LRU = []



    #Begin by trying to iterate through the list, this is to check if the list is valid
    start_time = time.time()

    while Index < len(InstructionsToRun):
        #If the list wasn't empty then we can begin processing the data, we know that the client is sending a tuple and a quadruple
        print("Instruction to run")
        ToPrintOut.append(["Instruction: " + InstructionsToRun[Index]])
        print(InstructionsToRun[Index])

        #If we find a designator P then it indicates that we must load the program
        if 'P' in InstructionsToRun[Index]:
            #We split the data to make it easier to iterate through the tuple or quadruple
            SplittedData = InstructionsToRun[Index].split(' ')
            #This will check if the string of instructions came up fine, again
            try:
                print(SplittedData[1])
                #We obtain the Initial Program Size from the client
                InitialProgramSize = SplittedData[1]
                #We obtain the Process ID
                #ProcessID = SplittedData[2]
                ProcessID = ''.join(SplittedData[2].splitlines())
                #We need the program size to see how much memory it will use
                ProgramSize = math.ceil(int(InitialProgramSize)/PageFrameSize)
                #We proceed to try loading up the memory, specially important to switch memories
                try:
                    ProcessLocation = ("Process ID" + " " + str(ProcessID))
                    ListofProcessesAdded.append(str(ProcessLocation))

                    #Loop to cycle through the main memory list and fill it up with the program
                    #Check if process ID is in the memory
                    #Check if Process is already in the system

                    if IsInMainMemory == True:
                        print("Program is loaded in main memory")
                    
                    if IsInMainMemory == False:
                        print("Program is not loaded in main memory")

                        #If it's not in the main memory, check if it's in the swap memory
                        IsInSwapMemory = any(ProcessLocation in sl for sl in SwapMemory)
                        
                        if IsInSwapMemory == True:
                            print("Take it out")
                        else:
                            print("Load it up")
                            num = 0

                            if Jumped == False:

                                for x in range(PageNum, ProgramSize):
                                    MainMemory[IteratorForMainMemory].remove("Process ID #")
                                    MainMemory[IteratorForMainMemory].insert(3, str("Process ID" + " " + ProcessID))
                                    MainMemory[IteratorForMainMemory].remove("Page #")
                                    MainMemory[IteratorForMainMemory].insert(2, "Page " + str(num))
                                    num += 1
                                    IteratorForMainMemory += 1

                            #Start from the bottom position of a previously defined process! Index - 1 to get the last used one before the last last one added
                            elif Jumped == True:
                                #Fill the memory according to open spaces!
                                print()
                                print()
                                #Max of process 2
                                try:
                                    try:
                                        IndexesOfProcesses = len(ListofProcessesAdded)
                                        LastPreviousProcessUsed = (IndexesOfProcesses - 3)
                                        LastPreviousPreviousProcessUsed = (IndexesOfProcesses - 2)
                                        print(ListofProcessesAdded[LastPreviousProcessUsed])
                                        print(ListofProcessesAdded[LastPreviousPreviousProcessUsed])
                                    except:
                                        pass

                                    SegmentedMemory1 = max(idx for idx, val in enumerate(MainMemory) if ListofProcessesAdded[LastPreviousProcessUsed] in val)
                                    SegmentedMemory1 += 1
                                    print(SegmentedMemory1)
                                    SegmentedMemory2 = max(idx for idx, val in enumerate(MainMemory) if ListofProcessesAdded[LastPreviousPreviousProcessUsed] in val)
                                    SegmentedMemory2 += 1
                                    print("Seg")
                                    print(SegmentedMemory2)

                                    for y in range(PageNum, ProgramSize):
                                        MainMemory[SegmentedMemory1].remove("Process ID #")
                                        MainMemory[SegmentedMemory1].insert(3, str("Process ID" + " " + ProcessID))
                                        MainMemory[SegmentedMemory1].remove("Page #")
                                        MainMemory[SegmentedMemory1].insert(2, "Page " + str(num))
                                        num += 1
                                        SegmentedMemory1 += 1

                                except:
                                    for x in range(y, ProgramSize):
                                        MainMemory[SegmentedMemory2].remove("Process ID #")
                                        MainMemory[SegmentedMemory2].insert(3, str("Process ID" + " " + ProcessID))
                                        MainMemory[SegmentedMemory2].remove("Page #")
                                        MainMemory[SegmentedMemory2].insert(2, "Page " + str(num))
                                        num += 1
                                        SegmentedMemory2 += 1                                                
                                    print("Switching sides")
                                #Max of process 3

                    RemainingMemoryToAddress = ProgramSize - x 
                    #If all is fine proceed to load it...

                except:
                    print("Main memory full, switching to swap")
                    RemainingMemoryToAddress = ProgramSize - x 
                    for y in range(PageNum, RemainingMemoryToAddress):
                        SwapMemory[IteratorForSwapMemory].remove("Page #")
                        SwapMemory[IteratorForSwapMemory].insert(3, "Page " + str(num))
                        SwapMemory[IteratorForSwapMemory].remove("Process ID #")
                        SwapMemory[IteratorForSwapMemory].insert(2, str("Process ID" + " " + ProcessID))

                        num += 1
                        IteratorForSwapMemory += 1                                            
                    num += 0


                    MemoryIndexesSwap = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
                    CheckSize = len(MemoryIndexesSwap)
                    if CheckSize <= 0:
                        print("==")                               

                    else:
                        try:
                            MemoryIndexesSwap = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
                            IndexRangeMemorySwap = len(MemoryIndexesSwap)
                            MemoryRangesSwap = []
                            for k in range(0, IndexRangeMemorySwap):
                                print(SwapMemory[0][1])
                                print(SwapMemory[0][0])
                                print(SwapMemory[1][0])

                                MemoryRangesSwap.append(SwapMemory[MemoryIndexesSwap[k]][0])
                            print(MemoryRangesSwap[0])

                            #Print the physical address in which the process is located
                            Bottom = len(SwapMemory)
                            for m in range(0, IndexRangeMemorySwap):
                                ToPrintOut.append("S[" + str(MemoryRangesSwap[m]) + ":" + str(Bottom) + "]")
                            #The real address in this case is the position where the first page of the program is loaded
                            #We obtain this by getting the first position of the list where the program is at
                        except:
                            print("==")


                try:
                    #Append a string with the desired process ID to find the memory location
                    ProcessLocation = ("Process ID" + " " + str(ProcessID))
                    #Iterate through the entire memory to find the last instance of the process that got loaded

                    BottomMainMemStack = max(idx for idx, val in enumerate(MainMemory) if ProcessLocation in val) 
                    TopMainMemStack = min(idx for idx, val in enumerate(MainMemory) if ProcessLocation in val) 
                    print()

                    MemoryIndexes = [i for i, s in enumerate(MainMemory) if ProcessLocation in s]
                    IndexRangeMemory = len(MemoryIndexes)
                    MemoryRanges = []
                    for x in range(0, IndexRangeMemory):
                        MemoryRanges.append(MainMemory[MemoryIndexes[x]][1])
                    
                    #Print the physical address in which the process is located
                    for y in range(0, IndexRangeMemory):
                        print("M[" + MemoryRanges[y] + "]")
                        ToPrintOut.append("M[" + MemoryRanges[y] + "]")


                    Bottom = len(SwapMemory)
                    MemoryIndexesSwap = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
                    CheckSize = len(MemoryIndexesSwap)
                    if CheckSize <= 0:
                        ToPrintOut.append("S[" + "1" + "-" + str(Bottom) + "]")
                        print("==")                               

                    else:
                        try:
                            MemoryIndexesSwap = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
                            IndexRangeMemorySwap = len(MemoryIndexesSwap)
                            MemoryRangesSwap = []
                            for k in range(0, IndexRangeMemorySwap):
                                MemoryRangesSwap.append(SwapMemory[MemoryIndexesSwap[k]][0])
                                

                            #Print the physical address in which the process is located
                            #The real address in this case is the position where the first page of the program is loaded
                            #We obtain this by getting the first position of the list where the program is at
                        except:
                            print("==")
                except:
                    pass
                                                    

            #Throw an error code if the programand quit immediately
            except:
                print("Trouble!")

        elif 'A' in InstructionsToRun[Index]:

            TopMainMemStack = 0
            BottomMainMemStack = 0
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
                RealAddress = MainMemory[RealAdIndex][1]

                #Proceed to try to read the physical address of the program
                try:
                    
                    #Print the physical address in which the process is located
                    for y in range(0, IndexRangeMemory):
                        print("M[" + MemoryRanges[y] + "]")
                        ToPrintOut.append("M[" + MemoryRanges[y] + "]")


                    MemoryIndexesSwap = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
                    CheckSize = len(MemoryIndexesSwap)
                    if CheckSize <= 0:
                        print("==")                               

                    else:
                        try:
                            MemoryIndexesSwap = [i for i, s in enumerate(SwapMemory) if ProcessLocation in s]
                            IndexRangeMemorySwap = len(MemoryIndexesSwap)
                            MemoryRangesSwap = []
                            for k in range(0, IndexRangeMemorySwap):
                                print()
                                print(SwapMemory[0][0])
                                print(MemoryIndexesSwap[0])
                                print(MemoryIndexesSwap[1])
                                
                                MemoryRangesSwap.append(SwapMemory[MemoryIndexesSwap[k][0]])

                            #Print the physical address in which the process is located
                            for m in range(0, IndexRangeMemorySwap):
                                print("S[" + str(MemoryRangesSwap[m]) + "]") 
                                ToPrintOut.append("S[" + str(MemoryRangesSwap[m]) + "]")
                            #The real address in this case is the position where the first page of the program is loaded
                            #We obtain this by getting the first position of the list where the program is at
                        except:
                            print("==")

                    print("Real Address " + str(RealAddress))
                    print("Read")
                    if AccessModifierBit == 1:
                        
                        print("Read and Modified")

                    ToPrintOut.append("Real Address " + str(RealAddress))

                except:
                    print("Unable to iterate this memory or no process was found")
                


        elif 'L' in InstructionsToRun[Index]:
            SplittedDataL = InstructionsToRun[Index].split(' ')
            ProcessIDL = ''.join(SplittedDataL[1].splitlines())
            ProcessLocationL = ("Process ID" + " " + str(ProcessIDL))
            ToPrintOut.append("Deleted " + str(ProcessLocationL))
            try:
                ListofProcessesAdded.remove(str(ProcessLocationL))
            except:
                print("Process is not in memory, unable to comply with command")
            #Try to remove the process from the stack, if there's a process in the memory it will remove it
            #and it will check the swap memory to load it again
            try:
                BottomMainMemStack = min(idx for idx, val in enumerate(MainMemory) if ProcessLocationL in val)
                TopMainMemStack = max(idx for idx, val in enumerate(MainMemory) if ProcessLocationL in val)
                TopMainMemStack += 1
                #try:

                    #print("Freeing memory locations " + MainMemory[BottomMainMemStack][1] + " " + MainMemory[TopMainMemStack - 1][1])
                    #print(ProcessLocation + " " + "Has been removed from memory")
                    #print(MainMemory[BottomMainMemStack])
                    #print(MainMemory[TopMainMemStack])
                #except:
                    #print("Process in swap memory")
                    
                PageNumToRemove = 0
                
                for y in range(BottomMainMemStack, TopMainMemStack):
                    MainMemory[y].remove("Page " + str(PageNumToRemove))
                    MainMemory[y].insert(2, "Page #")
                    MainMemory[y].remove(ProcessLocationL)
                    MainMemory[y].insert(3, str("Process ID #"))
                    PageNumToRemove += 1
                    PageRecorder = PageNumToRemove
                Jumped = True
                PositionMemory = BottomMainMemStack

                #Check if the process is in the swap memory
                try:
                    BottomSwapMemStack = min(idx for idx, val in enumerate(SwapMemory) if ProcessLocationL in val)
                    TopSwapMemStack = max(idx for idx, val in enumerate(SwapMemory) if ProcessLocationL in val)
                    TopSwapMemStack += 1
                    PageNumToRemove = 0
                
                    for y in range(BottomSwapMemStack, TopSwapMemStack):
                        SwapMemory[y].remove("Page " + str(PageRecorder))
                        SwapMemory[y].insert(2, "Page #")
                        SwapMemory[y].remove(ProcessLocationL)
                        SwapMemory[y].insert(3, str("Process ID #"))
                        PageRecorder += 1
                except:
                    print("Swap memory free of process")

            except:
                try:
                    BottomSwapMemStack = min(idx for idx, val in enumerate(SwapMemory) if ProcessLocationL in val)
                    TopSwapMemStack = max(idx for idx, val in enumerate(SwapMemory) if ProcessLocationL in val)
                    TopSwapMemStack += 1
                    print("Freeing memory locations " + SwapMemory[BottomSwapMemStack][1] + " " + SwapMemory[TopSwapMemStack][1])
                    print(ProcessLocation + " " + "Has been removed from memory")
                    print(SwapMemory[BottomSwapMemStack])
                    print(MainMemory[TopSwapMemStack])
                    PageNumToRemove = 0
                
                    for y in range(BottomSwapMemStack, TopSwapMemStack):
                        SwapMemory[y].remove("Page " + str(PageNumToRemove))
                        SwapMemory[y].insert(2, "Page #")
                        SwapMemory[y].remove(ProcessLocationL)
                        SwapMemory[y].insert(3, str("Process ID #"))
                        PageNumToRemove += 1
                except:
                    pass                      

        elif 'E' in InstructionsToRun[Index]:
            print("Exiting...")
            with open('Result.txt', 'w') as f:
                for item in ToPrintOut:
                    f.write("%s\n" % item)
                f.close()
            break

        elif 'F' in InstructionsToRun[Index]:
            pass

        end_time = time.time()
        Turnaround_P = end_time - start_time
        ToPrintOut.append(["Turnaround: " + str(Turnaround_P)])                        
        Index += 1

def MemoryGenerator(RealMemorySize, SwapMemorySize, PageSize):
    PageFrames = 0
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
            SwapMemory.append([swapMemList[Tracker], "Page #", "Process ID #"])
            Tracker += 1
            PageFrameTracker +=1
        #Auxiliary address memory creation, Swap memory
        CheckMemory(PhysicalAddress, SwapMemory, PageSize)
        

#Begin here
DatosEjecucion = open('ArchivoTrabajo.txt', 'r')
InstructionsToRun = DatosEjecucion.readlines()
print("Datos recibidos")
#Input Data for the Memory sizes -> Like This MemoryGenerator(Main Memory Size, Swap Memory Size, Page Size, Instructions (Already Added into File))
#In this project use the following:
MemoryGenerator(2048, 4096, 16)

#Ignore error, we are only trying to summon the function
