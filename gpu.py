from kp import Manager, Tensor, Algorithm, OpBase, OpAlgoDispatch, OpTensorSyncLocal, OpTensorSyncDevice, OpTensorSyncLocal
from itertools import chain
import numpy as np




def chain_lists(*args):
    return list(chain.from_iterable(args))

def get_shader(name):
    with open("./{}.spv".format(name), "rb") as file:
        return file.read()

def get_alg(mgr, data, shader_name):
    return mgr.algorithm(tensors=data, spirv=get_shader(shader_name))

def arr(mgr, data, dtype):
    return mgr.tensor_t(np.array(data, dtype=dtype))

def run_algorithm(mgr, data, output_len, shader_name, dtype):
    # Sequence of operations. However, if wVulkanritten properly, this can be done in 1 operation
    sq = mgr.sequence()


    if dtype == "uint32":
        dtype = np.uint32
    elif dtype == "int32":
        dtype = np.int32
    else:
        print("Somethign is wrong with data type")
        quit()

    # Not the most efficient way to do it, but screewwwww it
    # This is just a draft
    output = arr(mgr, [0 for i in range(output_len)], dtype)
    # I want to make my life easier, so all the data goes in as a list of lists
    data = [arr(mgr, d, dtype) for d in data] # MAKE THIS WORK PROPERLY BY SETTING TYPE TO INT32
   
    mem = chain_lists(data, [output])
   
    # Sync data from RAM to device
    sq.eval(OpTensorSyncDevice(mem))
    
    # Setup alg
    alg = get_alg(mgr, mem, shader_name)
    
    # Send alg to device and run it
    sq.eval(OpAlgoDispatch(alg))

    # Sync data from device to RAM
    sq.eval(OpTensorSyncLocal([output]))

    return output

def make_manager():
    mgr = Manager()
    return mgr
