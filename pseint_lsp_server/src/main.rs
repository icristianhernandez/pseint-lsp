use pseint_lsp_server::run_server;

#[tokio::main]
async fn main() {
    // Setup logging later if needed (e.g., to a file or stderr)
    // For now, LSP client logging is used in lib.rs

    eprintln!("PSeInt LSP Server starting via stderr..."); // For initial confirmation
    run_server().await;
    eprintln!("PSeInt LSP Server stopped via stderr."); // For shutdown confirmation
}
