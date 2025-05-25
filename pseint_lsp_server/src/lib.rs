use tower_lsp::jsonrpc::Result;
use tower_lsp::lsp_types::*;
use tower_lsp::{Client, LanguageServer, LspService, Server};

#[derive(Debug)]
struct Backend {
    client: Client,
}

#[tower_lsp::async_trait]
impl LanguageServer for Backend {
    async fn initialize(&self, _: InitializeParams) -> Result<InitializeResult> {
        self.client
            .log_message(MessageType::INFO, "PSeInt LSP server initializing...")
            .await;
        Ok(InitializeResult {
            server_info: Some(ServerInfo {
                name: "pseint-lsp-server".to_string(),
                version: Some("0.1.0".to_string()),
            }),
            capabilities: ServerCapabilities {
                text_document_sync: Some(TextDocumentSyncCapability::Kind(
                    TextDocumentSyncKind::FULL, // Or INCREMENTAL if we handle it later
                )),
                // Add formatting capability later in Step 5
                // document_formatting_provider: Some(OneOf::Left(true)),
                ..ServerCapabilities::default()
            },
        })
    }

    async fn initialized(&self, _: InitializedParams) {
        self.client
            .log_message(MessageType::INFO, "PSeInt LSP server initialized.")
            .await;
    }

    async fn shutdown(&self) -> Result<()> {
        self.client
            .log_message(MessageType::INFO, "PSeInt LSP server shutting down...")
            .await;
        Ok(())
    }

    // Basic text document synchronization handlers (will be expanded later)
    async fn did_open(&self, params: DidOpenTextDocumentParams) {
        self.client
            .log_message(MessageType::INFO, &format!("File opened: {}", params.text_document.uri))
            .await;
        // Here you would typically parse the document or store its content
    }

    async fn did_change(&self, params: DidChangeTextDocumentParams) {
        self.client
            .log_message(MessageType::INFO, &format!("File changed: {}", params.text_document.uri))
            .await;
        // Here you would typically re-parse the document or update its content
    }

    async fn did_save(&self, params: DidSaveTextDocumentParams) {
        self.client
            .log_message(MessageType::INFO, &format!("File saved: {}", params.text_document.uri))
            .await;
    }

    async fn did_close(&self, params: DidCloseTextDocumentParams) {
        self.client
            .log_message(MessageType::INFO, &format!("File closed: {}", params.text_document.uri))
            .await;
    }
}

pub async fn run_server() {
    let stdin = tokio::io::stdin();
    let stdout = tokio::io::stdout();

    let (service, socket) = LspService::build(|client| Backend { client })
        .finish();

    Server::new(stdin, stdout, socket).serve(service).await;
}
