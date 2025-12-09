#!/usr/bin/env python3
"""
INSECURE Application - FOR EDUCATIONAL PURPOSES ONLY

This script contains intentional security vulnerabilities to demonstrate
Software and Data Integrity Failures (OWASP A08:2021)

VULNERABILITIES IN THIS CODE:
1. Hardcoded credentials/API keys
2. Uses eval() on user input - Code injection
3. No input validation
4. Insecure deserialization with pickle
5. Downloads and executes code from untrusted source
"""

import os
import pickle
import base64
import urllib.request

# VULNERABLE: Hardcoded credentials
API_KEY = "sk-production-key-super-secret-12345"
DATABASE_PASSWORD = "admin123"
SECRET_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.secret"

# VULNERABLE: Hardcoded database connection string with credentials
DB_CONNECTION = "postgresql://root:password123@prod-db.example.com:5432/production"


def insecure_eval_calculator(expression):
    """
    VULNERABLE: Uses eval() to process user input
    An attacker could execute arbitrary code by passing malicious expressions
    Example attack: __import__('os').system('rm -rf /')
    """
    print(f"Calculating: {expression}")
    # VULNERABLE: Direct eval of user input
    result = eval(expression)
    return result


def insecure_deserialize(data):
    """
    VULNERABLE: Uses pickle to deserialize untrusted data
    Pickle can execute arbitrary code during deserialization
    """
    print("Deserializing data...")
    # VULNERABLE: Deserializing untrusted data
    decoded = base64.b64decode(data)
    obj = pickle.loads(decoded)
    return obj


def download_and_execute(url):
    """
    VULNERABLE: Downloads code from URL and executes it
    This is a supply chain attack vector - no integrity verification
    """
    print(f"Downloading code from: {url}")
    try:
        # VULNERABLE: No SSL verification, no integrity check
        response = urllib.request.urlopen(url, timeout=10)
        code = response.read().decode('utf-8')
        print("Executing downloaded code...")
        # VULNERABLE: Executing untrusted remote code
        exec(code)
    except Exception as e:
        print(f"Download failed (expected in demo): {e}")


def load_config_from_env():
    """
    Loads configuration from environment variables
    Note: Even this 'safer' approach has issues in this codebase
    """
    config = {
        "api_key": os.getenv("API_KEY", API_KEY),  # Falls back to hardcoded key
        "db_password": os.getenv("DB_PASSWORD", DATABASE_PASSWORD),
        "debug": os.getenv("DEBUG", "true").lower() == "true"
    }
    
    # VULNERABLE: Printing sensitive configuration
    if config["debug"]:
        print("=== DEBUG MODE: Configuration ===")
        print(f"API Key: {config['api_key']}")
        print(f"DB Password: {config['db_password']}")
        print(f"DB Connection: {DB_CONNECTION}")
    
    return config


def process_user_data(data):
    """
    VULNERABLE: No input validation or sanitization
    """
    # VULNERABLE: Directly using user input without validation
    user_id = data.get("user_id")
    action = data.get("action")
    payload = data.get("payload")
    
    print(f"Processing request for user {user_id}")
    
    # VULNERABLE: Using eval on user-provided action
    if action == "calculate":
        return insecure_eval_calculator(payload)
    elif action == "deserialize":
        return insecure_deserialize(payload)
    elif action == "execute_remote":
        return download_and_execute(payload)
    else:
        return f"Unknown action: {action}"


def main():
    print("=" * 60)
    print("INSECURE APPLICATION - FOR EDUCATIONAL PURPOSES ONLY")
    print("This application contains intentional security vulnerabilities")
    print("=" * 60)
    print()
    
    # Load configuration (exposes secrets in debug mode)
    config = load_config_from_env()
    
    print("\n--- Demonstrating Vulnerabilities ---\n")
    
    # Demo 1: Unsafe eval (would be dangerous with real user input)
    print("[1] Eval Calculator Demo:")
    try:
        result = insecure_eval_calculator("2 + 2 * 3")
        print(f"    Result: {result}\n")
    except Exception as e:
        print(f"    Error: {e}\n")
    
    # Demo 2: Show that remote code execution is attempted
    print("[2] Remote Code Download Demo:")
    print("    Attempting to download from untrusted source...")
    download_and_execute("https://example.com/malicious.py")
    print()
    
    # Demo 3: Show hardcoded secrets
    print("[3] Hardcoded Secrets Demo:")
    print(f"    API_KEY: {API_KEY[:20]}...")
    print(f"    SECRET_TOKEN: {SECRET_TOKEN[:30]}...")
    print()
    
    print("=" * 60)
    print("Pipeline execution completed (insecure version)")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

