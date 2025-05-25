# PSeInt Language Server (Python)

A Language Server Protocol (LSP) server for the PSeInt programming language, implemented in Python, with an initial focus on providing code formatting capabilities.

## Features

* **Code Formatting**: Automatically formats PSeInt source code files (`.psc`) based on a defined set of rules for indentation, keyword casing, spacing, and blank lines.

## Installation

1. **Prerequisites**:
    * Python 3.7+
    * `pip` (Python package installer)

2. **Setup**:
    * Clone this repository (or ensure the `pseint-lsp` directory is available).
    * Navigate to the `pseint-lsp` directory:

        ```bash
        cd pseint-lsp
        ```

    * Create a Python virtual environment (recommended):

        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate
        ```

    * Install the required dependencies:

        ```bash
        pip install -r requirements.txt
        ```

## LSP Server Execution

The server uses standard input/output to communicate with the LSP client. It can be run directly:

```bash
python launch.py
```

Most LSP clients will manage the execution of the server based on the configuration.

## Neovim Integration

To integrate this LSP server with Neovim, you can use the modern `vim.lsp.config()` and `vim.lsp.enable()` API. This provides a cleaner and more maintainable way to configure the server.

### Modern Configuration (Recommended)

You can configure the PSeInt LSP in two ways:

#### Option 1: In your main configuration (init.lua)

Place this in your Neovim Lua configuration (e.g., `init.lua` or a dedicated `lsp.lua`):

```lua
-- Configure PSeInt LSP client
-- IMPORTANT: Update the cmd path to the actual location of launch.py in your system!
-- Make sure to use the Python executable from the virtual environment where pygls is installed
vim.lsp.config('pseint-lsp', {
  cmd = { '/path/to/your/project/pseint-lsp/.venv/bin/python', '/path/to/your/project/pseint-lsp/launch.py' },
  filetypes = { 'pseint' },
  root_markers = { '.git', 'proyecto.psc' }, -- Look for git repos or main project files
  name = 'pseint-lsp',
})

-- Set up filetype detection for .psc files
vim.filetype.add({
  extension = {
    psc = 'pseint',
  },
})

-- Enable the LSP client
vim.lsp.enable('pseint-lsp')

-- Optional: Configure LSP behavior and keymaps on attach
vim.api.nvim_create_autocmd('LspAttach', {
  group = vim.api.nvim_create_augroup('pseint-lsp-attach', { clear = true }),
  callback = function(args)
    local client = vim.lsp.get_client_by_id(args.data.client_id)
    local bufnr = args.buf
    
    -- Only apply to PSeInt LSP
    if client and client.name == 'pseint-lsp' then
      vim.notify("PSeInt LSP attached to buffer " .. bufnr, vim.log.levels.INFO)
      
      -- Set up buffer-local keymaps for LSP functions
      local map = function(mode, lhs, rhs, desc)
        vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = 'LSP: ' .. desc })
      end
      
      -- Format keybinding (if the server supports formatting)
      if client:supports_method('textDocument/formatting') then
        map('n', '<leader>lf', vim.lsp.buf.format, 'Format document')
        
        -- Optional: Auto-format on save
        vim.api.nvim_create_autocmd('BufWritePre', {
          group = vim.api.nvim_create_augroup('pseint-lsp-format-on-save', { clear = false }),
          buffer = bufnr,
          callback = function()
            vim.lsp.buf.format({ bufnr = bufnr, timeout_ms = 1000 })
          end,
        })
      end
      
      -- Additional LSP keymaps using Neovim's default bindings
      -- These are already available by default but you can customize them:
      -- map('n', 'grn', vim.lsp.buf.rename, 'Rename symbol')
      -- map('n', 'gra', vim.lsp.buf.code_action, 'Code action')
      -- map('n', 'grr', vim.lsp.buf.references, 'Show references')
      -- map('n', 'gd', vim.lsp.buf.definition, 'Go to definition')
      -- map('n', 'K', vim.lsp.buf.hover, 'Hover documentation')
    end
  end,
})
```

#### Option 2: Using a dedicated LSP configuration file

Alternatively, you can create a file at `~/.config/nvim/lsp/pseint-lsp.lua` (matching the client name). This file will be automatically loaded by Neovim:

**File: `~/.config/nvim/lsp/pseint-lsp.lua`**

```lua
-- This file is automatically loaded by Neovim's LSP system
-- IMPORTANT: Update the cmd path to the actual location of launch.py in your system!
-- Make sure to use the Python executable from the virtual environment where pygls is installed
return {
  cmd = { '/path/to/your/project/pseint-lsp/.venv/bin/python', '/path/to/your/project/pseint-lsp/launch.py' },
  filetypes = { 'pseint' },
  root_markers = { '.git', 'proyecto.psc' },
  name = 'pseint-lsp',
}
```

**Then in your `init.lua`, you only need:**

```lua
-- Set up filetype detection
vim.filetype.add({
  extension = {
    psc = 'pseint',
  },
})

-- Enable the LSP (the configuration will be loaded from lsp/pseint-lsp.lua)
vim.lsp.enable('pseint-lsp')

-- Optional: Configure LSP behavior and keymaps on attach
vim.api.nvim_create_autocmd('LspAttach', {
  group = vim.api.nvim_create_augroup('pseint-lsp-attach', { clear = true }),
  callback = function(args)
    local client = vim.lsp.get_client_by_id(args.data.client_id)
    local bufnr = args.buf
    
    -- Only apply to PSeInt LSP
    if client and client.name == 'pseint-lsp' then
      vim.notify("PSeInt LSP attached to buffer " .. bufnr, vim.log.levels.INFO)
      
      -- Set up buffer-local keymaps for LSP functions
      local map = function(mode, lhs, rhs, desc)
        vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = 'LSP: ' .. desc })
      end
      
      -- Format keybinding (if the server supports formatting)
      if client:supports_method('textDocument/formatting') then
        map('n', '<leader>lf', vim.lsp.buf.format, 'Format document')
        
        -- Optional: Auto-format on save
        vim.api.nvim_create_autocmd('BufWritePre', {
          group = vim.api.nvim_create_augroup('pseint-lsp-format-on-save', { clear = false }),
          buffer = bufnr,
          callback = function()
            vim.lsp.buf.format({ bufnr = bufnr, timeout_ms = 1000 })
          end,
        })
      end
    end
  end,
})
```

**Note:** When using this approach, the configuration in `lsp/pseint-lsp.lua` will be automatically merged with any global configuration defined with `vim.lsp.config('*', {...})`.

### Complete Working Example

For reference, here's a complete working configuration file that you can use as `~/.config/nvim/lsp/pseint-lsp.lua`:

```lua
-- Complete working configuration for PSeInt LSP
-- Based on nvim-config-example.lua from the project
return {
    cmd = { "/home/crisarch/pseint-lsp/.venv/bin/python", "/home/crisarch/pseint-lsp/launch.py" },
    filetypes = { "pseint" },
    root_markers = { ".git", "proyecto.psc" },
    name = "pseint-lsp",
}
```

**Important Notes:**

* Make sure to update the paths in the `cmd` field to match your actual installation directory
* The Python path should point to the virtual environment where `pygls` is installed (`.venv/bin/python`)
* The launch script path should point to `launch.py` in your project directory
* Ensure you've installed the dependencies with `pip install -r requirements.txt` in the virtual environment

**Note:** When using this approach, the configuration in `lsp/pseint-lsp.lua` will be automatically merged with any global configuration defined with `vim.lsp.config('*', {...})`.

### Legacy Configuration (Alternative)

If you prefer the older `vim.lsp.start()` approach or need more control:

```lua
-- Set up filetype detection first
vim.filetype.add({
  extension = {
    psc = 'pseint',
  },
})

-- Autocommand to start the LSP client for PSeInt files
vim.api.nvim_create_autocmd('FileType', {
  pattern = 'pseint',
  callback = function()
    vim.lsp.start({
      name = 'pseint-lsp',
      cmd = { 'python', '/path/to/your/project/pseint_lsp_py/server.py' },
      root_dir = vim.fs.root(0, { '.git', 'proyecto.psc' }) or vim.fn.expand('%:p:h'),
    })
  end,
})
```

### Installation Notes

* **Server Path**: Update the `cmd` field to point to the absolute path of the `server.py` script in your cloned directory.
* **Configuration Location**: You can place the configuration either:
  * Directly in your `init.lua` (Option 1)
  * In a dedicated file `~/.config/nvim/lsp/pseint-lsp.lua` (Option 2) - this file will be automatically loaded by Neovim
* **Dependencies**: Ensure Python and the required packages (from `requirements.txt`) are installed and accessible.
* **Root Directory**: The LSP server will use the directory containing `.git` or `proyecto.psc` files as the project root. Adjust `root_markers` as needed.
* **Default Keymaps**: Neovim provides default LSP keymaps:
  * `grn` - Rename symbol
  * `gra` - Code action  
  * `grr` - Show references
  * `gri` - Go to implementation
  * `gd` - Go to definition (via `tagfunc`)
  * `K` - Hover documentation
  * `gO` - Document symbols
  * `CTRL-S` (insert mode) - Signature help

## Usage

Once installed and configured with your editor (e.g., Neovim), the formatting capability should be available.

### In Neovim

With the modern configuration setup above:

* **Format document**: Use `<leader>lf` (if configured) or the default `gq` command
* **Auto-format on save**: Automatically formats the file when saving (if enabled in config)
* **Default LSP keymaps** (available automatically):
  * `grn` - Rename symbol under cursor
  * `gra` - Show available code actions
  * `grr` - Show all references to symbol
  * `gri` - Go to implementation
  * `gd` - Go to definition
  * `K` - Show hover documentation
  * `gO` - Show document symbols
  * `CTRL-S` (insert mode) - Show signature help

You can also call LSP functions directly:

* `:lua vim.lsp.buf.format()` - Format current buffer
* `:LspInfo` - Show LSP client status
* `:checkhealth vim.lsp` - Check LSP health

### Server Logs

The server logs its activity to `/tmp/pseint_lsp.log` for debugging purposes.

## Developer Information

### Project Structure

* `pseint_lsp_py/`: Main directory for the Python LSP server.
  * `server.py`: The LSP server implementation using `pygls`.
  * `formatter.py`: Contains the PSeInt code formatting logic, adapted from the original `pseint-formatter.py`.
  * `requirements.txt`: Python dependencies.
  * `tests/`: Unit tests.
    * `test_formatter.py`: Unit tests for `formatter.py`.
* `pseint-formatter.py`: Original standalone formatter script (in repository root).
* `reference_code*.psc`: PSeInt example files (in repository root).

### Formatting Logic (`formatter.py`)

The `formatter.py` script implements PSeInt formatting rules, including:

* **Keyword Casing**: Converts keywords (e.g., `proceso`, `leer`, `FinSi`) to their proper case (e.g., `Proceso`, `Leer`, `FinSi`). A comprehensive list of keywords is maintained.
* **Indentation**: Applies 4-space indentation for blocks like `Proceso`, `Si-Entonces-Sino`, `Mientras`, `Para`, `Segun`, `Repetir`, `SubProceso`, `Funcion`.
* **Spacing**:
  * Adds spaces around operators (`<-`, `+`, `=`, `>`, etc.).
  * Ensures a space after commas.
  * Normalizes spacing around parentheses.
  * Manages spacing after keywords.
* **Blank Lines**:
  * Collapses multiple consecutive blank lines into a single blank line.
  * Removes blank lines at the very beginning and end of the file.
  * Removes blank lines found immediately before block-ending keywords (e.g., `FinProceso`).
* **Comments**: Preserves comments and ensures a space after `//`.
* **Semicolons/Colons**: Removes leading spaces before trailing semicolons or colons on a line.
* **Line Endings**: Removes trailing whitespace from all lines.

### Running Tests

The project includes comprehensive tests written using Python's `unittest` framework and `pytest`. Tests are located in the `tests/` directory and cover:

* **`test_formatter.py`**: Core formatting functionality tests
* **`test_edge_cases.py`**: Edge cases and error handling tests  
* **`test_integration.py`**: Integration tests using real PSeInt code examples
* **`test_server.py`**: LSP server functionality tests

#### Prerequisites

Make sure you have the test dependencies installed:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes all necessary testing dependencies:

* **Core dependencies**: `pygls`, `lsprotocol`, `pytest`, `pytest-asyncio`
* **Optional testing features**: `pytest-cov` (coverage), `pytest-xdist` (parallel execution)

**For Fish shell users:** The installation command works the same way.

#### Running All Tests

1. **Using pytest (recommended)**:

   From the `pseint_lsp_py` directory:

   ```bash
   python -m pytest tests/ -v
   ```

   From the repository root:

   ```bash
   python -m pytest pseint_lsp_py/tests/ -v
   ```

   **For Fish shell users:**

   ```fish
   python -m pytest tests/ -v
   # or from repository root:
   python -m pytest pseint_lsp_py/tests/ -v
   ```

2. **Using unittest**:

   From the `pseint_lsp_py` directory:

   ```bash
   python -m unittest discover tests -v
   ```

   From the repository root:

   ```bash
   python -m unittest discover pseint_lsp_py.tests -v
   ```

   **For Fish shell users:**

   ```fish
   python -m unittest discover tests -v
   # or from repository root:
   python -m unittest discover pseint_lsp_py.tests -v
   ```

#### Running Specific Test Files

* **Formatter tests only**:

  ```bash
  python -m pytest tests/test_formatter.py -v
  ```

* **Edge cases tests only**:

  ```bash
  python -m pytest tests/test_edge_cases.py -v
  ```

* **Integration tests only**:

  ```bash
  python -m pytest tests/test_integration.py -v
  ```

* **Server tests only**:

  ```bash
  python -m pytest tests/test_server.py -v
  ```

**Note:** All the above commands work the same way in Fish shell.

#### Running with Coverage

To check test coverage, first install the coverage dependency (if not already installed):

```bash
pip install pytest-cov
```

Then run tests with coverage:

```bash
python -m pytest tests/ --cov=pseint_lsp_py --cov-report=html
```

This will generate an HTML coverage report in `htmlcov/index.html`.

**For Fish shell users:** The commands work exactly the same way.

#### Advanced Test Options

* **Run tests in parallel** (faster execution):

  ```bash
  pip install pytest-xdist
  python -m pytest tests/ -n auto -v
  ```

* **Run tests with extra verbose output**:

  ```bash
  python -m pytest tests/ -vv
  ```

* **Run tests and stop on first failure**:

  ```bash
  python -m pytest tests/ -x -v
  ```

* **Run only failed tests from last run**:

  ```bash
  python -m pytest tests/ --lf -v
  ```

#### Test Configuration

The tests use `pytest-asyncio` for async test support. The configuration can be adjusted by creating a `pytest.ini` file if needed.

**Note:** All pytest commands work the same way in Fish shell, Bash, or other shells.

### Contribution

Contributions are welcome! If you find issues or want to add features (like diagnostics, auto-completion, etc.):

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes, including adding relevant tests. Ensure all tests pass.
4. Add type hints and docstrings to new or modified Python code.
5. Update documentation if necessary.
6. Submit a pull request.
