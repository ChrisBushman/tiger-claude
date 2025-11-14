# tiger-claude Client - Quick Start

## What This Is

A standalone Claude AI assistant that runs directly on your vintage Macintosh (like a PowerBook G4!) running OS X Tiger, making API calls without requiring a proxy server. Perfect for bringing modern AI assistance to vintage hardware!

## Prerequisites

✓ Vintage Mac (like a PowerBook G4) running OS X Tiger (10.4.x)
✓ Python 3.10+ built and installed (see BUILDING.md)
✓ OpenSSL 3.2.x built and installed (see BUILDING.md)
✓ Network connection
✓ Anthropic API key

## Installation

### 1. Get Your API Key

Visit https://console.anthropic.com on a modern device:
- Sign up or log in
- Go to API Keys section
- Create a new key (starts with `sk-ant-`)
- Save it securely!

### 2. Transfer Files to Mac

Copy these files to your vintage Mac:
- `tiger-claude.py` - The main client
- `BUILDING.md` - OpenSSL build guide (if not done yet)

### 3. Set Up API Key

```bash
# Add to ~/.bash_profile
echo 'export ANTHROPIC_API_KEY=sk-ant-your-actual-key-here' >> ~/.bash_profile
source ~/.bash_profile
```

### 4. Make Executable

```bash
chmod +x tiger-claude.py
```

### 5. Test It!

```bash
# Run full diagnostic test
python3 test_setup.py

# Check SSL configuration
python3 tiger-claude.py --check-ssl

# Try a simple question
python3 tiger-claude.py "Hello, Claude!"
```

## Usage

### Interactive Mode (Recommended)

```bash
python3 tiger-claude.py
```

Then use commands:
```
claude> ask What is a Python decorator?
claude> explain mycode.py
claude> fix buggy_script.c
claude> review main.js
claude> test calculator.py
```

### Command Line Mode

```bash
# Quick questions
python3 tiger-claude.py "Explain quicksort algorithm"

# Ask about a file
python3 tiger-claude.py "What does this code do?" script.py

# Multiple files for context
python3 tiger-claude.py "How do these work together?" main.c utils.c header.h
```

## Available Commands (Interactive Mode)

| Command | Usage | Description |
|---------|-------|-------------|
| `ask` | `ask <question>` | Ask Claude anything |
| `file` | `file <path> <question>` | Ask about a specific file |
| `explain` | `explain <path>` | Get detailed code explanation |
| `fix` | `fix <path>` | Get improvement suggestions |
| `review` | `review <path>` | Get thorough code review |
| `test` | `test <path>` | Generate unit tests |
| `quit` | `quit` | Exit the program |

## Examples

### Learning a New Language

```bash
claude> ask Teach me the basics of Ruby
claude> ask Show me Ruby array methods with examples
```

### Code Explanation

```bash
claude> explain recursive_function.py
# Claude explains the recursion, base cases, and how it works
```

### Getting Help with Bugs

```bash
claude> fix segfaulting_program.c
# Claude identifies potential segfault causes and suggests fixes
```

### Code Review

```bash
claude> review my_web_app.js
# Claude reviews for bugs, security issues, style, performance
```

### Generating Tests

```bash
claude> test math_functions.py
# Claude generates comprehensive unit tests
```

## Tips for Best Results

1. **Be specific**: "Explain the quicksort algorithm" vs "Explain sorting"
2. **Provide context**: Use `file` command to include relevant code
3. **Ask follow-ups**: Claude remembers context within a session
4. **Break down problems**: Ask about components separately if needed

## Editor Integration

### Vim

Add to `~/.vimrc`:
```vim
" Explain visual selection
vnoremap <leader>ce :w !python3 ~/tiger-claude.py "Explain this code:"<CR>

" Review current file
nnoremap <leader>cr :!python3 ~/tiger-claude.py review %<CR>

" Fix current file
nnoremap <leader>cf :!python3 ~/tiger-claude.py fix %<CR>

" Ask about function under cursor
nnoremap <leader>ca :!python3 ~/tiger-claude.py "What does this function do?" %<CR>
```

### Emacs

Add to `~/.emacs`:
```elisp
;; Send region to Claude
(defun claude-explain-region (start end)
  (interactive "r")
  (shell-command-on-region start end "python3 ~/tiger-claude.py 'Explain this code:'"))

(global-set-key (kbd "C-c c e") 'claude-explain-region)
```

### BBEdit

Create a script in `~/Library/Application Support/BBEdit/Scripts/`:
```bash
#!/bin/bash
# Ask Claude about current file
python3 ~/tiger-claude.py "Explain this code:" "$BB_DOC_PATH"
```

## Performance

Typical response times on PowerBook G4:
- Simple questions: 2-5 seconds
- Code explanations: 3-8 seconds  
- Complex reviews: 5-15 seconds

Most time is network latency, not your PowerBook!

## Costs

Claude API pricing (approximate):
- $3 per million input tokens (roughly $3 per 750,000 words)
- Typical question: $0.01 - $0.05
- Very affordable for personal use!

You can monitor usage at https://console.anthropic.com

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY=your-key-here
# Or add to ~/.bash_profile permanently
```

### "SSL certificate verification failed"
```bash
# Install CA certificates
export SSL_CERT_FILE=/usr/local/ssl/cert.pem
```

### "Connection timed out"
- Check network connection
- Firewall might be blocking HTTPS
- Try from different network

### Python can't find ssl module
- Rebuild Python against new OpenSSL (see BUILDING.md)
- Check: `python3 -c "import ssl"`

### Slow responses
- Normal on older hardware
- Network latency is main factor
- Claude's API is fast, your connection might be slow

## Advanced Usage

### Save Responses to File

```bash
python3 tiger-claude.py "Explain Python generators" > explanation.txt
```

### Pipe Code to Claude

```bash
cat mycode.py | python3 tiger-claude.py "Review this:"
```

### Batch Processing

```bash
for file in *.c; do
    echo "Reviewing $file..."
    python3 tiger-claude.py "Quick code review:" "$file" >> review_results.txt
done
```

## What You Can Do

✓ Learn programming concepts
✓ Debug code
✓ Get explanations of complex code
✓ Generate tests
✓ Code reviews
✓ Refactoring suggestions
✓ Algorithm explanations
✓ Best practices advice
✓ General programming questions
✓ Documentation help

## What Claude Can't Do

✗ Execute code on your machine
✗ Modify files directly (you do that)
✗ Access your files without you providing them
✗ Remember between different sessions
✗ Browse the web or access external resources

## Support

- Anthropic API docs: https://docs.anthropic.com
- API status: https://status.anthropic.com
- Support: https://support.anthropic.com

## Have Fun!

You now have a modern AI assistant running on vintage hardware. That's pretty cool! 🎉

Use it to learn, debug, and make your PowerBook G4 a surprisingly capable development machine.

Happy coding!
