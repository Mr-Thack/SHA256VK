from gpu import make_manager, run_algorithm
import hashlib

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

# Initialize Kompute Manager
mgr = make_manager()

a = [ 1, 2, 3 ]
b = [ 4, 5, 6 ]

res = run_algorithm(mgr, [a, b], 3, "adding", "uint32")

# Output the result
print("Result:", res.data())

# Clean up resources
mgr.destroy()
