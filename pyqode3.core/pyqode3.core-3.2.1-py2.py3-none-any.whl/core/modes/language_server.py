# coding=utf-8

import subprocess
import shlex
from pylspclient import JsonRpcEndpoint, LspEndpoint, LspClient, lsp_structs
from pylspclient.lsp_structs import (
    TextDocumentItem, Position, CompletionContext, CompletionTriggerKind
)
from pyqode.core.api.mode import Mode


CLIENT_CAPABILITIES = {
    'textDocument': {
        'completion': {
            'completionItem': {
                'commitCharactersSupport': True,
                'documentationFormat': ['markdown', 'plaintext'],
                'snippetSupport': True},
                'completionItemKind': {
                    'valueSet': []
                },
                'contextSupport': True,
        },
        'documentSymbol': {
            'symbolKind': {
                'valueSet': []
            }
        },
        'publishDiagnostics': {
            'relatedInformation': True
        }
    }
}

clients = {}


class LanguageServer(Mode):
    
    def __init__(self, cmd, lang_id):
        
        super().__init__()
        self._lang_id = lang_id
        if lang_id in clients:
            self._client = clients[lang_id]
            return
        self._start_client(cmd)
        
    def document_symbol(self):
        
        td = self._text_document()
        self._client.didOpen(td)
        return self._client.documentSymbol(td)
        
    def completion(self):
        
        td = self._text_document()
        self._client.didOpen(td)
        return self._client.completion(
            td,
            self._cursor_position(),
            CompletionContext(CompletionTriggerKind.Invoked)
        )
        
    
    def _cursor_position(self):
        
        tc = self.editor.textCursor()
        return Position(tc.blockNumber(), tc.positionInBlock())

    def _start_client(self, cmd):
        
        self._server_process = subprocess.Popen(
            shlex.split(cmd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self._json_rpc_endpoint = JsonRpcEndpoint(
            self._server_process.stdin,
            self._server_process.stdout
        )
        self._endpoint = LspEndpoint(
            self._json_rpc_endpoint,
            notify_callbacks = {
                'textDocument/publishDiagnostics': self._publish_diagnostics
            }
        )
        self._client = LspClient(self._endpoint)
        self._server_capabilities = self._client.initialize(
            self._server_process.pid,
            None,
            None,
            None,
            CLIENT_CAPABILITIES,
            'off',
            None
        )
        self._client.initialized()
        clients[self._lang_id] = self._client
        
    def _uri(self):

        if self.editor.file.path:
            return 'file://' + self.editor.file.path
        
    def _text(self):
        
        return self.editor.toPlainText().replace(u'\u2029', u'\n')
        
    def _text_document(self):
        
        return TextDocumentItem(self._uri(), self._lang_id, 1, self._text())
        
    def _publish_diagnostics(self, *args):
        
        print(args)
