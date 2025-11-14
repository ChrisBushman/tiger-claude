#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Claude API client for OS X Tiger / Python 3.10+
Requires modern OpenSSL (3.x) to be built and linked
"""

import urllib.request
import urllib.error
import json
import sys
import os
import ssl

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
API_URL = 'https://api.anthropic.com/v1/messages'
API_VERSION = '2023-06-01'
MODEL = 'claude-sonnet-4-20250514'
MAX_TOKENS = 4000

def check_ssl():
    """Check if we have modern SSL support"""
    try:
        ssl_version = ssl.OPENSSL_VERSION
        print(f"Using: {ssl_version}")
        # Check for TLS 1.2 support
        if not hasattr(ssl, 'PROTOCOL_TLSv1_2'):
            print("WARNING: TLS 1.2 support may not be available")
            print("You may need to rebuild Python's ssl module against OpenSSL 3.x")
            return False
        return True
    except AttributeError:
        print("ERROR: SSL module not available or too old")
        return False

def read_file(filepath):
    """Read a file and return its contents"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def call_claude_api(prompt):
    """
    Make a direct API call to Claude
    
    Args:
        prompt: The prompt to send to Claude
    
    Returns:
        Claude's response text, or error message
    """
    if not ANTHROPIC_API_KEY:
        return "ERROR: ANTHROPIC_API_KEY environment variable not set"
    
    # Build the request payload
    payload = {
        'model': MODEL,
        'max_tokens': MAX_TOKENS,
        'messages': [
            {'role': 'user', 'content': prompt}
        ]
    }
    
    try:
        # Create the request
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'x-api-key': ANTHROPIC_API_KEY,
                'anthropic-version': API_VERSION
            }
        )

        # Make the API call
        # Note: This requires modern OpenSSL with TLS 1.2+ support
        response = urllib.request.urlopen(req, timeout=60)
        result = json.loads(response.read().decode('utf-8'))

        # Extract the response text
        if 'content' in result and len(result['content']) > 0:
            return result['content'][0]['text']
        else:
            return "ERROR: Unexpected response format"

    except urllib.error.HTTPError as e:
        error_body = e.read()
        try:
            error_json = json.loads(error_body)
            return f"API Error ({e.code}): {error_json.get('error', {}).get('message', 'Unknown error')}"
        except:
            return f"HTTP Error {e.code}: {error_body}"
    except urllib.error.URLError as e:
        return f"Connection Error: {e.reason}"
    except Exception as e:
        return f"Error: {e}"

def send_to_claude(prompt, context_files=None):
    """
    Send a prompt to Claude with optional file context
    
    Args:
        prompt: The question/request
        context_files: List of file paths to include as context
    """
    full_prompt = prompt
    
    if context_files:
        full_prompt += "\n\nContext files:\n"
        for filepath in context_files:
            content = read_file(filepath)
            if content:
                full_prompt += f"\n--- {filepath} ---\n{content}\n"
            else:
                full_prompt += f"\n--- {filepath} ---\n[Could not read file]\n"
    
    return call_claude_api(full_prompt)

def interactive_mode():
    """Run in interactive mode"""
    print("Claude Client for PowerBook G4 (Direct API)")
    print("")

    # Check SSL capabilities
    if not check_ssl():
        print("\nWARNING: SSL issues detected. API calls may fail.")
        print("Make sure Python is linked against OpenSSL 3.x\n")

    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("Set it with: export ANTHROPIC_API_KEY=sk-ant-...")
        return

    print("\nCommands:")
    print("  ask <question> - Ask Claude a question")
    print("  file <path> <question> - Ask about a specific file")
    print("  explain <path> - Ask Claude to explain a file")
    print("  fix <path> - Ask Claude to suggest fixes for a file")
    print("  review <path> - Get a code review")
    print("  test <path> - Generate tests for code")
    print("  quit - Exit")
    print("")
    
    while True:
        try:
            line = input("claude> ")
            line = line.strip()

            if not line:
                continue

            if line == "quit":
                break

            parts = line.split(None, 2)
            command = parts[0] if parts else ""

            if command == "ask":
                if len(parts) < 2:
                    print("Usage: ask <question>")
                    continue
                question = " ".join(parts[1:])
                print("\nThinking...")
                response = send_to_claude(question)
                print(f"\n{response}\n")

            elif command == "file":
                if len(parts) < 3:
                    print("Usage: file <path> <question>")
                    continue
                filepath = parts[1]
                question = parts[2]
                print("\nAnalyzing...")
                response = send_to_claude(question, [filepath])
                print(f"\n{response}\n")

            elif command == "explain":
                if len(parts) < 2:
                    print("Usage: explain <path>")
                    continue
                filepath = parts[1]
                print("\nAnalyzing...")
                response = send_to_claude(
                    "Please explain what this code does, how it works, and any important details:",
                    [filepath]
                )
                print(f"\n{response}\n")

            elif command == "fix":
                if len(parts) < 2:
                    print("Usage: fix <path>")
                    continue
                filepath = parts[1]
                print("\nAnalyzing...")
                response = send_to_claude(
                    "Please review this code and suggest improvements, bug fixes, or optimizations:",
                    [filepath]
                )
                print(f"\n{response}\n")

            elif command == "review":
                if len(parts) < 2:
                    print("Usage: review <path>")
                    continue
                filepath = parts[1]
                print("\nReviewing...")
                response = send_to_claude(
                    "Please perform a thorough code review, checking for bugs, security issues, style problems, and suggesting improvements:",
                    [filepath]
                )
                print(f"\n{response}\n")

            elif command == "test":
                if len(parts) < 2:
                    print("Usage: test <path>")
                    continue
                filepath = parts[1]
                print("\nGenerating tests...")
                response = send_to_claude(
                    "Please generate unit tests for this code. Include edge cases and error conditions:",
                    [filepath]
                )
                print(f"\n{response}\n")

            else:
                print(f"Unknown command: {command}")

        except KeyboardInterrupt:
            print("\nUse 'quit' to exit")
        except EOFError:
            break

    print("Goodbye!")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments, run interactive mode
        interactive_mode()
    elif sys.argv[1] == "--check-ssl":
        # Check SSL configuration
        print("Checking SSL configuration...\n")
        check_ssl()
    elif len(sys.argv) == 2:
        # Single argument, treat as a question
        if not ANTHROPIC_API_KEY:
            print("ERROR: ANTHROPIC_API_KEY not set")
            sys.exit(1)
        response = send_to_claude(sys.argv[1])
        print(response)
    else:
        # Multiple arguments, first is question, rest are files
        if not ANTHROPIC_API_KEY:
            print("ERROR: ANTHROPIC_API_KEY not set")
            sys.exit(1)
        question = sys.argv[1]
        files = sys.argv[2:]
        response = send_to_claude(question, files)
        print(response)

if __name__ == '__main__':
    main()
