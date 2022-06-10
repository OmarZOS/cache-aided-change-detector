# The perfect dataset for this context is supposed to take users 
# publications into different timestamps timestamps

from count_test import run_test
from memory_test import run_memory_test
from size_test import run_trace_test
from time_test import run_time_test


dates = {}

# def FunctionName(args):
    
def master():
    
    # run_test()
    
    # # #what a uselessness..
    #run_memory_test()
    run_time_test()
    #run_trace_test()


    



if __name__=="__main__":
    master()


