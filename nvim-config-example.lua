-- Fixed configuration for nvim/lsp/pseint-lsp.lua
return {
    cmd = { "/home/crisarch/pseint-lsp/.venv/bin/python", "/home/crisarch/pseint-lsp/launch.py" },
    filetypes = { "pseint" },
    root_markers = { ".git", "proyecto.psc" },
    name = "pseint-lsp",
}
