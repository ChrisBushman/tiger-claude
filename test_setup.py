#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic script for Claude PowerBook client
Tests SSL, Python, and API connectivity
"""

import sys
import os

def print_header(text):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def check_python():
    """Check Python version"""
    print_header("Python Version")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")

    if sys.version_info < (3, 10):
        print(f"WARNING: Python 3.10+ recommended, you have {sys.version}")
        return False
    else:
        print("OK: Python version is compatible")
        return True

def check_ssl():
    """Check SSL module and OpenSSL version"""
    print_header("SSL/TLS Support")

    try:
        import ssl
        print("SSL module: Available")
        print(f"OpenSSL version: {ssl.OPENSSL_VERSION}")

        # Check for TLS 1.2
        if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
            print("TLS 1.2: Supported")
        else:
            print("TLS 1.2: NOT SUPPORTED (required for Claude API)")
            print("You need to rebuild Python against OpenSSL 3.x")
            return False

        # Check for TLS 1.3
        if hasattr(ssl, 'PROTOCOL_TLS'):
            print("TLS 1.3: Supported")
        else:
            print("TLS 1.3: Not available (not critical)")

        print("OK: SSL support looks good")
        return True

    except ImportError:
        print("ERROR: SSL module not available!")
        print("Python was not compiled with SSL support")
        return False

def check_json():
    """Check JSON module"""
    print_header("JSON Support")

    try:
        import json
        print("JSON module: Available")

        # Test encoding/decoding
        test_obj = {'test': 'value', 'number': 42}
        encoded = json.dumps(test_obj)
        decoded = json.loads(encoded)

        if decoded == test_obj:
            print("JSON encoding/decoding: Working")
            print("OK: JSON support is good")
            return True
        else:
            print("ERROR: JSON encoding/decoding failed")
            return False

    except ImportError:
        print("ERROR: JSON module not available")
        print("This should be included in Python 3.10+")
        return False

def check_urllib():
    """Check urllib for HTTP support"""
    print_header("HTTP/HTTPS Support")

    try:
        import urllib.request
        print("urllib.request module: Available")

        # Check for HTTPS handler
        https_handler = urllib.request.HTTPSHandler()
        print("HTTPS handler: Available")
        print("OK: HTTP/HTTPS support is good")
        return True

    except ImportError:
        print("ERROR: urllib.request not available")
        return False

def check_api_key():
    """Check if API key is set"""
    print_header("API Configuration")

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')

    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY=sk-ant-...")
        print("Or add to ~/.bash_profile for permanent setup")
        return False

    # Don't print the full key for security
    if api_key.startswith('sk-ant-'):
        print("API key: Set (starts with sk-ant-)")
        print(f"API key length: {len(api_key)} characters")
        print("OK: API key is configured")
        return True
    else:
        print("WARNING: API key doesn't start with 'sk-ant-'")
        print("Make sure you're using a valid Anthropic API key")
        return False

def check_certificates():
    """Check SSL certificate configuration"""
    print_header("SSL Certificates")

    cert_file = os.environ.get('SSL_CERT_FILE', '')

    if cert_file:
        print(f"SSL_CERT_FILE: {cert_file}")
        if os.path.exists(cert_file):
            print("Certificate file: Exists")
        else:
            print("WARNING: Certificate file not found")
    else:
        print("SSL_CERT_FILE: Not set (using system default)")

    # Check common certificate locations
    cert_locations = [
        '/usr/local/ssl/cert.pem',
        '/usr/local/ssl/certs/ca-bundle.crt',
        '/etc/ssl/cert.pem',
        '/System/Library/OpenSSL/certs',
    ]

    print("\nChecking common certificate locations:")
    found = False
    for loc in cert_locations:
        if os.path.exists(loc):
            print(f"  {loc} - Found")
            found = True
        else:
            print(f"  {loc} - Not found")

    if not found and not cert_file:
        print("\nWARNING: No certificate bundle found")
        print("SSL verification may fail")
        print("Download certificates from: https://curl.se/ca/cacert.pem")
        return False

    print("OK: Certificate configuration looks reasonable")
    return True

def test_https_connection():
    """Test a simple HTTPS connection"""
    print_header("HTTPS Connection Test")

    try:
        import urllib.request
        import urllib.error
        print("Testing HTTPS connection to api.anthropic.com...")

        req = urllib.request.Request('https://api.anthropic.com')
        response = urllib.request.urlopen(req, timeout=10)
        print("Connection: SUCCESS")
        print(f"Response code: {response.code}")
        print("OK: Can connect to Anthropic API")
        return True

    except urllib.error.HTTPError as e:
        # HTTPError means we successfully connected via HTTPS!
        # The server just returned an HTTP error code (like 404)
        print("Connection: SUCCESS")
        print(f"Response code: {e.code}")
        print("OK: HTTPS connection established (HTTP error is expected)")
        return True

    except urllib.error.URLError as e:
        print("Connection: FAILED")
        print(f"Error: {e.reason}")

        if 'CERTIFICATE' in str(e.reason).upper():
            print("\nThis is a certificate validation error.")
            print("Try: export SSL_CERT_FILE=/path/to/cacert.pem")
        elif 'SSL' in str(e.reason).upper():
            print("\nThis is an SSL/TLS error.")
            print("Make sure OpenSSL 3.x is installed and Python is linked to it")

        return False
    except Exception as e:
        print("Connection: FAILED")
        print(f"Error: {e}")
        return False

def test_api_call():
    """Test an actual API call to Claude"""
    print_header("Claude API Test")

    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        print("Skipping: API key not set")
        return False

    try:
        import urllib.request
        import urllib.error
        import json

        print("Making test API call...")
        print("(This will use a small amount of your API credits)")

        payload = {
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 50,
            'messages': [
                {'role': 'user', 'content': 'Say "Hello from PowerBook G4!" and nothing else.'}
            ]
        }

        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01'
            }
        )

        response = urllib.request.urlopen(req, timeout=30)
        result = json.loads(response.read().decode('utf-8'))

        if 'content' in result and len(result['content']) > 0:
            claude_response = result['content'][0]['text']
            print("\nClaude's response:")
            print(f'  "{claude_response}"')
            print("\nSUCCESS: Everything is working!")
            return True
        else:
            print("ERROR: Unexpected response format")
            return False

    except urllib.error.HTTPError as e:
        print(f"API call failed with HTTP error {e.code}")
        try:
            error_body = json.loads(e.read())
            print(f"Error message: {error_body.get('error', {}).get('message', 'Unknown')}")
        except:
            print("Could not parse error response")
        return False
    except Exception as e:
        print(f"API call failed: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("=" * 60)
    print("Claude PowerBook Client - Diagnostic Test")
    print("=" * 60)

    results = []

    results.append(('Python', check_python()))
    results.append(('SSL/TLS', check_ssl()))
    results.append(('JSON', check_json()))
    results.append(('HTTP/HTTPS', check_urllib()))
    results.append(('API Key', check_api_key()))
    results.append(('Certificates', check_certificates()))
    results.append(('HTTPS Connection', test_https_connection()))
    results.append(('API Call', test_api_call()))

    # Summary
    print_header("Summary")

    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {name}: {status}")
        if not passed:
            all_passed = False

    print("")
    if all_passed:
        print("SUCCESS! Everything is working correctly.")
        print("You can now use the Claude client: ./tiger-claude.py")
    else:
        print("PROBLEMS DETECTED. Please fix the issues above.")
        print("Refer to BUILDING.md for detailed instructions.")

    print("")

if __name__ == '__main__':
    main()
