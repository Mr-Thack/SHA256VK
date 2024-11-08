#!/usr/bin/python
from gpu import make_manager, run_algorithm
import hashlib
import numpy as np 

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



input_string = "hello world"

# Initialize Kompute Manager
mgr = make_manager()

res = run_algorithm(mgr, [padded_tensor], 8, "alg", "uint32")

# Output the result
print("Result:", numpy_uint32_to_hex(res.data()))

# Clean up resources
mgr.destroy()
