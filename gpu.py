from kp import Manager, Tensor, Algorithm, OpBase, OpAlgoDispatch, OpTensorSyncLocal, OpTensorSyncDevice, OpTensorSyncLocal
from itertools import chain


def chain_lists(*args):
    return list(chain.from_iterable(args))

def get_shader(name):
    with open("./shaders/{}.spv".format(name), "rb") as file:
        return file.read()

def get_alg(mgr, data, shader_name):
    return mgr.algorithm(tensors=data, spirv=get_shader(shader_name))

def run_algorithm(mgr, data, shader_name):
    # Sequence of operations. However, if written properly, this can be done in 1 operation
    sq = mgr.sequence()
   
    output = mgr.tensor([0 for i in range(len(data[0]))])
    # I want to make my life easier, so all the data goes in as a list of lists
    data = [mgr.tensor(d) for d in data] # MAKE THIS WORK PROPERLY BY SETTING TYPE TO INT32
   
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
