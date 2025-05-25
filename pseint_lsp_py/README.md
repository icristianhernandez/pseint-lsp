# PSeInt Language Server (Python)

A Language Server Protocol (LSP) server for the PSeInt programming language, implemented in Python, with an initial focus on providing code formatting capabilities.

## Features

* **Code Formatting**: Automatically formats PSeInt source code files (`.psc`) based on a defined set of rules for indentation, keyword casing, spacing, and blank lines.

## Installation

1. **Prerequisites**:
    * Python 3.7+
    * `pip` (Python package installer)

2. **Setup**:
    * Clone this repository (or ensure the `pseint_lsp_py` directory is available).
    * Navigate to the `pseint_lsp_py` directory:

        ```bash
        cd pseint_lsp_py
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
python server.py
```

Most LSP clients will manage the execution of the server based on the configuration.

## Neovim Integration

To integrate this LSP server with Neovim, you can use the built-in `vim.lsp.start()` API. This provides a direct way to configure the server.

```lua
-- Direct Neovim LSP setup
-- Place this in your Neovim Lua configuration (e.g., init.lua or a dedicated lsp.lua)

-- Define how to start the PSeInt LSP server
-- IMPORTANT: Update this path to the actual location of server.py in your system!
local pseint_lsp_cmd = {'python', '/path/to/your/project/pseint_lsp_py/server.py'} 

-- Function to be called when the LSP client attaches to a buffer
local on_attach_pseint = function(client, bufnr)
  vim.notify("PSeInt LSP Attached to buffer: " .. bufnr, vim.log.levels.INFO)
  -- Example: Enable formatting keymap
  local map_opts = { buffer = bufnr, desc = "Format PSeInt file" }
  vim.keymap.set('n', '<leader>lf', vim.lsp.buf.format, map_opts)

  -- You can add other buffer-local settings or keymaps here
  -- For example, if you want to set up formatting on save:
  -- if client.supports_method("textDocument/formatting") then
  --   vim.api.nvim_create_autocmd('BufWritePre', {
  --     group = vim.api.nvim_create_augroup('PSeIntLspFormatOnSave', { clear = true }),
  --     buffer = bufnr,
  --     callback = function() vim.lsp.buf.format({ bufnr = bufnr, timeout_ms = 500 }) end
  --   })
  -- end
end

-- Autocommand to start the LSP client for PSeInt files
vim.api.nvim_create_autocmd('FileType', {
  pattern = 'pseint', -- Assumes .psc files are mapped to 'pseint' filetype
  callback = function()
    vim.lsp.start({
      name = 'pseint-lsp-py-direct', -- Unique name for this client instance
      cmd = pseint_lsp_cmd,
      -- root_dir can be customized. This is a basic example.
      root_dir = vim.fs.root(0, {'.git'}) or vim.fn.expand('%:p:h'), 
      on_attach = on_attach_pseint,
      capabilities = vim.lsp.protocol.make_client_capabilities(), -- Use default client capabilities
      -- filetypes = {'pseint', 'psc'} -- Redundant if using FileType autocommand on 'pseint'
    })
  end
})

-- Ensure Neovim recognizes .psc files as 'pseint' filetype
-- (Add this if not already configured elsewhere in your Neovim setup)
-- vim.filetype.add({
--   extension = {
--     psc = 'pseint',
--   },
-- })

-- As an alternative to the FileType autocommand above, you can explicitly define the 'pseint' filetype
-- if it's not automatically detected or if you prefer a more direct mapping for .psc files:
-- vim.api.nvim_create_autocmd({"BufNewFile", "BufRead"}, {
--   pattern = "*.psc",
--   callback = function()
--     vim.bo.filetype = "pseint"
--     -- Now, the FileType autocommand for 'pseint' above will trigger.
--   end,
-- })
```

**Important Notes for Manual Setup:**

* **Path to `server.py`**: Ensure the `pseint_lsp_cmd` variable in the Lua code correctly points to the absolute path of the `server.py` script within your cloned `pseint_lsp_py` directory.
* **Filetype Detection**: For the `FileType` autocommand to work, Neovim must recognize `.psc` files as the `pseint` filetype. If this isn't happening automatically, uncomment and use the `vim.filetype.add` example or the `BufNewFile,BufRead` autocommand provided in the Lua snippet to set the filetype.

## Usage

Once installed and configured with your editor (e.g., Neovim), the formatting capability should be available.

* In Neovim, with the example setup above, you can format the current PSeInt file using the keymap `<leader>lf` (or by directly calling `vim.lsp.buf.format()`).
* The server will log its activity to `/tmp/pseint_lsp.log`.

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
