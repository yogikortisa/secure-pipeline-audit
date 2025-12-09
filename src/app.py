#!/usr/bin/env python3
"""
SECURE Application - DevSecOps Best Practices

This script demonstrates secure coding practices to mitigate
Software and Data Integrity Failures (OWASP A08:2021)

SECURITY CONTROLS IMPLEMENTED:
1. No hardcoded credentials - uses environment variables
2. Safe expression evaluation - no eval() or exec()
3. Input validation and sanitization
4. No insecure deserialization
5. No remote code execution
"""

import os
import json
import ast
import operator
from typing import Any, Dict, Optional


def get_config_from_env() -> Dict[str, Any]:
    """
    SECURE: Load configuration from environment variables only
    No hardcoded secrets, no fallback to insecure defaults
    """
    config = {
        "api_key": os.getenv("API_KEY"),
        "database_url": os.getenv("DATABASE_URL"),
        "debug": os.getenv("DEBUG", "false").lower() == "true"
    }
    
    # SECURE: Never print sensitive values, even in debug mode
    if config["debug"]:
        print("Debug mode enabled")
        print(f"API Key configured: {'Yes' if config['api_key'] else 'No'}")
        print(f"Database configured: {'Yes' if config['database_url'] else 'No'}")
    
    return config


class SafeCalculator:
    """
    SECURE: Safe mathematical expression evaluator
    Uses AST parsing instead of eval() to prevent code injection
    """
    
    # Allowed operators for safe evaluation
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    @classmethod
    def evaluate(cls, expression: str) -> float:
        """
        Safely evaluate a mathematical expression
        Only allows basic arithmetic operations
        """
        # SECURE: Validate input
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string")
        
        # SECURE: Limit expression length to prevent DoS
        if len(expression) > 100:
            raise ValueError("Expression too long (max 100 characters)")
        
        try:
            tree = ast.parse(expression, mode='eval')
            return cls._eval_node(tree.body)
        except (SyntaxError, TypeError, KeyError) as e:
            raise ValueError(f"Invalid expression: {e}")
    
    @classmethod
    def _eval_node(cls, node: ast.AST) -> float:
        """Recursively evaluate AST nodes"""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants allowed")
        
        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op = cls.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(left, right)
        
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op = cls.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(operand)
        
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")


def validate_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    SECURE: Validate and sanitize user input
    """
    validated = {}
    
    # Validate user_id - must be alphanumeric
    user_id = data.get("user_id", "")
    if user_id and isinstance(user_id, str) and user_id.isalnum():
        validated["user_id"] = user_id[:50]  # Limit length
    else:
        validated["user_id"] = None
    
    # Validate action - must be from allowed list
    action = data.get("action", "")
    allowed_actions = ["calculate", "info", "status"]
    if action in allowed_actions:
        validated["action"] = action
    else:
        validated["action"] = None
    
    # Validate payload based on action
    payload = data.get("payload", "")
    if validated["action"] == "calculate" and isinstance(payload, str):
        # Only allow safe characters for math expressions
        safe_chars = set("0123456789+-*/() .")
        if all(c in safe_chars for c in payload):
            validated["payload"] = payload[:100]
        else:
            validated["payload"] = None
    else:
        validated["payload"] = str(payload)[:200] if payload else None
    
    return validated


def process_request(data: Dict[str, Any]) -> str:
    """
    SECURE: Process validated user requests
    No eval(), no exec(), no dynamic code execution
    """
    validated = validate_input(data)
    
    if validated["action"] is None:
        return "Error: Invalid or unsupported action"
    
    if validated["action"] == "calculate":
        if validated["payload"]:
            try:
                result = SafeCalculator.evaluate(validated["payload"])
                return f"Result: {result}"
            except ValueError as e:
                return f"Calculation error: {e}"
        return "Error: No expression provided"
    
    elif validated["action"] == "info":
        return "Secure Pipeline Demo Application v1.0"
    
    elif validated["action"] == "status":
        return "Status: Running (secure mode)"
    
    return "Error: Unknown action"


def load_data_safely(json_string: str) -> Optional[Dict]:
    """
    SECURE: Parse JSON safely instead of using pickle
    JSON is a safe data format that cannot execute code
    """
    try:
        # SECURE: Use JSON instead of pickle for data serialization
        data = json.loads(json_string)
        
        # SECURE: Validate data structure
        if not isinstance(data, dict):
            raise ValueError("Data must be a JSON object")
        
        return data
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except ValueError as e:
        print(f"Validation error: {e}")
        return None


def main():
    print("=" * 60)
    print("SECURE APPLICATION - DevSecOps Best Practices")
    print("This application demonstrates secure coding patterns")
    print("=" * 60)
    print()
    
    # Load configuration securely
    config = get_config_from_env()
    
    print("--- Security Controls Demonstrated ---\n")
    
    # Demo 1: Safe calculator (no eval)
    print("[1] Safe Calculator Demo:")
    print("    Using AST-based evaluation instead of eval()")
    try:
        result = SafeCalculator.evaluate("2 + 2 * 3")
        print(f"    Expression: 2 + 2 * 3 = {result}")
    except ValueError as e:
        print(f"    Error: {e}")
    print()
    
    # Demo 2: Safe calculator rejects malicious input
    print("[2] Malicious Input Rejection Demo:")
    malicious_inputs = [
        "__import__('os').system('whoami')",
        "open('/etc/passwd').read()",
        "exec('print(1)')"
    ]
    for malicious in malicious_inputs:
        try:
            SafeCalculator.evaluate(malicious)
            print(f"    UNEXPECTED: '{malicious[:30]}...' was accepted")
        except ValueError:
            print(f"    BLOCKED: '{malicious[:30]}...'")
    print()
    
    # Demo 3: Input validation
    print("[3] Input Validation Demo:")
    test_data = {"user_id": "user123", "action": "calculate", "payload": "10 * 5"}
    validated = validate_input(test_data)
    print(f"    Input: {test_data}")
    print(f"    Validated: {validated}")
    print()
    
    # Demo 4: Safe JSON parsing (instead of pickle)
    print("[4] Safe Data Parsing Demo:")
    print("    Using JSON instead of pickle for data serialization")
    json_data = '{"name": "test", "value": 42}'
    parsed = load_data_safely(json_data)
    print(f"    Parsed data: {parsed}")
    print()
    
    # Demo 5: No hardcoded secrets
    print("[5] Secrets Management Demo:")
    print("    API Key: [loaded from environment variable]")
    print("    Database: [loaded from environment variable]")
    print("    No hardcoded credentials in source code!")
    print()
    
    print("=" * 60)
    print("Pipeline execution completed (secure version)")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

