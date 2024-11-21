#!/usr/bin/python
import hashlib
import numpy as np 
from kp import Manager, Tensor, Buffer, Algorithm, OpBase, OpAlgoDispatch, OpTensorSyncLocal, OpTensorSyncDevice, OpTensorSyncLocal



def compare_sha256 ( res : bytes, data : bytes ) -> bool:
    """
    Compares a given SHA - 256 hash(res)with the hash computed using hashlib for the same data .

    Parameters :
    res(bytes): The SHA - 256 hash result to be compared .
    data(bytes): The original data to hash for comparison .

    Returns :
    bool : True if the hashes match, False otherwise .
    """
    # Compute the SHA-256 hash using hashlib
    expected_hash = hashlib . sha256(data). digest()
    # Compare and return the result
    return res == expected_hash


def numpy_uint32_to_hex(numpy_array):
    # Check if the array is of type uint32
    if numpy_array.dtype != np.uint32:
        return "The numpy array should have dtype=np.uint32 for this conversion."
    
    # Cast the numpy array to uint8 and convert to bytes
    byte_array = numpy_array.view(np.uint8).tobytes()

    # Convert the byte array to a hex string
    hex_string = byte_array.hex()
    return hex_string


dtype = np.uint32
buftype = Buffer.DeviceType.SHARED

input_string = "hello world"

# Initialize Kompute Manager
mgr = Manager()

# Initial data 
input_data = np.array(input_string.decode('utf-8'), dtype=dtype)

# This is the hash state, and will be used to store the ouput 
chain = np.zeros(8, dtype=dtype)

chain_buffer = Buffer(manager, chain, buftype)
block_buffer = Buffer(manager, np.zeros(16, dtype=dtype), buftype) 
offset_buffer = Buffer(manager, np.array([0], dtype=dtype), buftype) 
length_buffer = Buffer(manager, np.array([len(input_data) * 4], dtype=dtype), buftype) 
data_buffer = Buffer(manager, input_data, buftype) 


sq = mgr.sequence()




# res = run_algorithm(mgr, [padded_tensor], 8, "alg", "uint32")

# Output the result
# print("Result:", numpy_uint32_to_hex(res.data()))

# Clean up resources
mgr.destroy()
