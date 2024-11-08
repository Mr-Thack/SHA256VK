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

def sha256_padding(input_string):
    # Step 1: Convert the input string to bytes
    message_bytes = input_string.encode('utf-8')
    message_length = len(message_bytes)
    
    # Step 2: Calculate total length for padding (512 bits per block, minus 64 bits for length field)
    padding_length = (56 - (message_length + 1) % 64) % 64
    total_length = message_length + 1 + padding_length + 8  # Includes 8 bytes for the length

    # Step 3: Create padded byte array
    padded_message = bytearray(message_bytes)
    padded_message.append(0x80)  # Append the '1' bit as 0x80
    
    # Step 4: Add `0x00` bytes until reaching the last 64 bits of the block
    padded_message.extend([0] * padding_length)
    
    # Step 5: Append the length of the original message in bits (big-endian)
    padded_message.extend((message_length * 8).to_bytes(8, byteorder='big'))
    
    # Convert to a numpy array for tensor compatibility, using 32-bit unsigned integers
    padded_array = np.frombuffer(padded_message, dtype=np.uint32)

    return padded_array

# Example usage
input_string = "hello world"
padded_tensor = sha256_padding(input_string)
print("Padded Tensor:\n", padded_tensor)


# Initialize Kompute Manager
mgr = make_manager()

res = run_algorithm(mgr, [a, b], 8, "adding", "uint32")

# Output the result
print("Result:", res.data())

# Clean up resources
mgr.destroy()
