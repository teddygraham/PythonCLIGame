#!/usr/bin/env python3
"""
Challenge validation module for PyAdventure
Handles code execution, validation, and feedback for Python challenges
"""

import sys
import io
import contextlib
from typing import Dict, Any, List


class ChallengeValidator:
    """Validates Python code challenges"""
    
    def __init__(self):
        self.safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sorted': sorted,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round,
                'type': type,
                'isinstance': isinstance,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'dir': dir,
                'help': help,
            }
        }
    
    def validate_code(self, user_code: str, expected_output: str = None, test_cases: List[Dict] = None) -> Dict[str, Any]:
        """
        Validate user-submitted Python code
        
        Args:
            user_code: The code submitted by the user
            expected_output: Expected output when code is run
            test_cases: List of test cases with inputs and expected outputs
            
        Returns:
            Dict with success status, message, and output
        """
        if not user_code.strip():
            return {
                "success": False,
                "message": "Please enter some code!",
                "output": None
            }
        
        # Capture stdout
        output_buffer = io.StringIO()
        
        try:
            # Execute code in safe environment
            with contextlib.redirect_stdout(output_buffer):
                exec(user_code, self.safe_globals.copy())
            
            actual_output = output_buffer.getvalue().strip()
            
            # If we have expected output, check it
            if expected_output is not None:
                if actual_output == expected_output:
                    return {
                        "success": True,
                        "message": "Great job! Your code produces the correct output.",
                        "output": actual_output
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Output doesn't match. Expected: '{expected_output}', Got: '{actual_output}'",
                        "output": actual_output
                    }
            
            # If we have test cases, run them
            if test_cases:
                return self._run_test_cases(user_code, test_cases)
            
            # If no specific validation, just check that code runs
            return {
                "success": True,
                "message": "Code executed successfully!",
                "output": actual_output
            }
            
        except SyntaxError as e:
            return {
                "success": False,
                "message": f"Syntax error: {e}",
                "output": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Runtime error: {e}",
                "output": None
            }
    
    def _run_test_cases(self, user_code: str, test_cases: List[Dict]) -> Dict[str, Any]:
        """Run a series of test cases against the user's code"""
        passed = 0
        total = len(test_cases)
        
        for i, test_case in enumerate(test_cases):
            # Prepare test environment
            test_globals = self.safe_globals.copy()
            
            # Set up inputs if provided
            if "inputs" in test_case:
                for var_name, value in test_case["inputs"].items():
                    test_globals[var_name] = value
            
            # Capture output
            output_buffer = io.StringIO()
            
            try:
                with contextlib.redirect_stdout(output_buffer):
                    exec(user_code, test_globals)
                
                actual_output = output_buffer.getvalue().strip()
                expected_output = test_case.get("expected_output", "")
                
                if actual_output == expected_output:
                    passed += 1
                else:
                    return {
                        "success": False,
                        "message": f"Test case {i+1} failed. Expected: '{expected_output}', Got: '{actual_output}'",
                        "output": actual_output
                    }
                    
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Test case {i+1} failed with error: {e}",
                    "output": None
                }
        
        return {
            "success": True,
            "message": f"All {total} test cases passed!",
            "output": f"{passed}/{total} tests passed"
        }
    
    def get_hint(self, challenge_type: str) -> str:
        """Get a hint for a specific type of challenge"""
        hints = {
            "variable": "Remember to use the assignment operator (=) to create a variable",
            "print": "Use the print() function to display output",
            "string": "Strings are created with quotes, like 'Hello' or \"Hello\"",
            "number": "Numbers don't need quotes. Use int() for integers, float() for decimals",
            "list": "Lists are created with square brackets: [1, 2, 3]",
            "function": "Functions are defined with 'def function_name():' followed by indented code",
            "loop": "Use 'for' loops to repeat code: 'for i in range(5):'",
            "conditional": "Use 'if' statements to make decisions: 'if condition:'"
        }
        
        return hints.get(challenge_type, "Think about what the code is trying to accomplish")
    
    def create_challenge(self, challenge_type: str, difficulty: str = "beginner") -> Dict[str, Any]:
        """Create a new challenge of a specific type"""
        challenges = {
            "variable": {
                "prompt": "Create a variable called 'name' and set it to your name",
                "expected_output": None,
                "hint": "Use the assignment operator (=) to create a variable"
            },
            "print": {
                "prompt": "Print the message 'Hello, World!'",
                "expected_output": "Hello, World!",
                "hint": "Use the print() function"
            },
            "math": {
                "prompt": "Calculate 15 + 27 and print the result",
                "expected_output": "42",
                "hint": "Use the + operator for addition"
            }
        }
        
        return challenges.get(challenge_type, challenges["print"])