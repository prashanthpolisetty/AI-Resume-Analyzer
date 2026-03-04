def run_chain_with_logging(chain_func, *args, chain_name="Unnamed Chain"):
    
    print(f"▶ Running {chain_name}...")

    try:
        result = chain_func(*args)
        print(f"{chain_name} completed successfully.\n")
        return result
    except Exception as e:
        print(f"{chain_name} failed: {str(e)}\n")
        return f"[ERROR] {chain_name} failed: {str(e)}"
