from gpu import make_manager, run_algorithm

# Initialize Kompute Manager
mgr = make_manager()

a = [1, 2, 3]
b = [4, 5, 6]

res = run_algorithm(mgr, [a, b], "adding")

# Output the result
print("Result:", res.data())

# Clean up resources
mgr.destroy()
