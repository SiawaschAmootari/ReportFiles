import os, time
import TestGui
def main():
    print("in Watchdog")
    path_to_watch = "C:\\Users\\samootari\\OneDrive\\Desktop\\Python"
        
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    done = True
    while done:
        time.sleep (10)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added: print ("Added: ", ", ".join (added)) 
        if removed: print ("Removed: ", ", ".join (removed))
    

        print(type(added))
    
        if len(added)>0:
            if ".xml" in added[-1]:
                print("i´m in")
                TestGui.start_app(added)  
                 
                   # before = dict ([(f, None) for f in os.listdir (path_to_watch)])
                   # done = False
                   # exit()
if __name__ == "__main__":
    main() 


