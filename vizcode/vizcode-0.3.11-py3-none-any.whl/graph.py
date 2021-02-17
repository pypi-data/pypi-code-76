from collections import defaultdict
from vizcode.constants import *
from art import *
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json
import subprocess
import tokenize
import hashlib
import pathlib
import re
import time

CURRENT_DIR_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/"

# Represents a graph created from source code containing nodes and an adjacency list. 
class Graph:
    nodes = {}
    adjacency_list = defaultdict(list)
    external_dependency_counts = defaultdict(lambda: 0)
    
    def __init__(self, title):
        self.title = title

    # Populates the graph's nodes and adjacency list after parsing through source code in inputed files. 
    def populate_graph(self, parsed_files):

        for parsed_file in parsed_files:
            file_path = parsed_file.file_path
            client = parsed_file.client

            self.__update_nodes(file_path, client)
        
        # The adjacency list relies on the nodes already being defined. 
        for parsed_file in parsed_files:
            file_path = parsed_file.file_path
            client = parsed_file.client

            self.__update_adjacency_list(file_path, client)

        return

    # Hashes a given string. 
    def __hash_value(self, s):
        return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]

    # Returns the scope in a simple way to parse. 
    def __format_scope(self, scope):
        first = scope.split('|')[0]
        end = scope.split('|')[1]

        first_row, first_col = first.split(':')
        end_row, end_col = end.split(':')
        return [int(first_row), int(first_col), int(end_row), int(end_col)]

    # Returns true if a node is an external dependency / built-in. 
    # Nodes tagged in this way will be removed. False otherwise. 
    def _is_builtin(self, node):

        prefix = node.split(".")[0]

        builtins = set(['builtins', 'datetime', 'random', 'io', 'os'])

        if prefix in builtins:
            return True

        return False

    # Updates the node dictionary with new nodes 
    def __update_nodes(self, file_path, client):
    
        # Returns a formatted node. 
        def format_node():
            nonlocal symbol_type, file_path, scope, name
            comment = ""
            code_path = FILE_CODE_PATH + self.__hash_value(file_path) + ".txt"
            explicit = False
            
            # Node declared inside of the file. 
            if 'EXPLICIT FUNCTION' in symbol_type:
                comment = get_comment(file_path, scope)
                explicit = True

            with open(file_path, 'r') as f:
                code = f.read()

            if scope is not None:
                scoped_code = self.__get_scoped_code(scope, code)
                self.__save_node_code(scoped_code, node)

            return {
                    "name": name,
                    "type": symbol_type,
                    "code_path": code_path,
                    "scope": scope,
                    "original_file_path": file_path,
                    "comment": comment,
                    "explicit": explicit,
                }
        
        # Returns (if possible) the comments for the specific function
        def get_comment(file_path, scope):
            start_line = scope[0]
            full_comment = ""

            fileObj = open(file_path, 'r')
            for toktype, tok, start, end, line in tokenize.generate_tokens(fileObj.readline):
                if toktype == tokenize.COMMENT:
                    if abs(start_line - start[0]) <= 3 and len(tok.split("#")) >= 2:
                        full_comment += tok.split('#')[1]
                        full_comment += " "
                if len(tok) >= 3 and tok[:3] == '"""':
                    if abs(start_line - start[0]) <= 3 and len(tok.split('"""')) >= 2:
                        full_comment += tok.split('"""')[1]
                        full_comment += " "

            return re.sub('\s+',' ', full_comment).strip()

        for symbol in client.symbols:
            node = symbol.split(' ')[2]
            symbol_type = symbol.split(':')[0]
            name = None
            scope = None
            
            # Get scope from symbol.
            if '|' in symbol:
                scope = symbol.split('[')[-1][:-1]
                scope = self.__format_scope(scope)

            # Get function name from symbol. 
            if '.' in symbol and "FUNCTION" in symbol_type:
                name = symbol.split('.')[-1].split(' ')[0]

            # Group python builtins together
            if "NON-INDEXED FUNCTION" in symbol_type and self._is_builtin(node):
                name = 'builtins'
                node = 'builtins'

            formatted_node = format_node()
            if node not in self.nodes and formatted_node['explicit']:
                self.nodes[node] = formatted_node

        return

    # Saves the code belonging to the node in the frontend directory.
    def __save_node_code(self, code, node):

        hashed_name = self.__hash_value(node)

        with open(CURRENT_DIR_PATH + NODE_CODE_PATH + hashed_name + ".txt", 'w+') as output_file:
            output_file.write(code)


    # Updates the adjacency list with new edges.
    def __update_adjacency_list(self, file_path, client):

        # Iterate through the processed references and add edges to the map. 
        for ref in self.__process_references(file_path, client):
            node_from, node_to = ref
            key = node_to

            # node from must not be explicit - should not happen
            if node_from not in self.nodes:
                continue

            # If true, node_to cannot be an explicit function
            if node_to not in self.nodes:
                # Need to create a key for this node and store it in the hash map
                key = node_to + "&" + file_path
                self.nodes[key] = {
                    "name": node_to,
                    "type": "Function",
                    "code_path": FILE_CODE_PATH + self.__hash_value(file_path) + ".txt",
                    "scope": None,
                    "original_file_path": file_path,
                    "comment": "",
                    "explicit": False,
                }

            self.adjacency_list[node_from].append(key) 

        return

    # Converts the client references to edges. 
    def __process_references(self, file_path, client):
        edges = []
        for ref in client.references:
            ref_type = ref.split(':')[0]
            # Get calls from references.
            if ref_type == "CALL":
                ref_split = ref.split('->')
                node_from = ref_split[0].split(' ')[1]
                node_to = ref_split[1].split(' ')[1]

                # Ignore any builtin node. If we do not remove the node here, 
                # an exception will be raised when we try to format the node
                # since we never added builtin nodes in __update_nodes. 
                if self._is_builtin(node_to):
                    continue

                scope = ref.split('at')[-1][2:-1]
                scope = self.__format_scope(scope)
                with open(file_path, 'r') as f:
                    code = f.read()
                
                scoped_code = self.__get_scoped_code(scope, code)
                self.__save_edge_code(scoped_code, node_from, node_to)

                if (node_from, node_to) not in edges:
                    edge = (node_from, node_to)
                    edges.append(edge)

        return edges

    # Saves the code belonging to the edge in the frontend directory.
    def __save_edge_code(self, code, node_from, node_to):

        hashed_name = self.__hash_value(node_from + node_to)

        with open(CURRENT_DIR_PATH + EDGE_CODE_PATH + hashed_name + ".txt", 'w+') as output_file:
            output_file.write(code)

    # Gets edge code from file defined by scope. 
    def __get_scoped_code(self, scope, code):

        first_row, first_col, end_row, end_col = scope

        lines = [line for line in code.split('\n')]
        lines_filtered = lines[int(first_row)-1: int(end_row)]

        return ''.join(lines_filtered) 

    # Saves the graph to a json file in the frontend directory. 
    def save_graph(self):
        graph = self.__build_json()
        with open(CURRENT_DIR_PATH + GRAPH_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(graph, f, ensure_ascii=False, indent=4)

        return 

    # Creates the graph containing all functions and their references. 
    def __get_main_graph(self):

        # Returns a formatted node.
        def format_node(node):
            node_info = self.nodes[node]
            hashed_name = self.__hash_value(node)

            highlighted_code_path = ""
            if node_info['explicit']:
                highlighted_code_path = "code/python/main/node-code/" + hashed_name + ".txt"

            return {
                "name": node,
                "type": "Function",
                "filePath": node_info["code_path"],
                "comment": node_info['comment'],
                "originalFilePath": node_info["original_file_path"],
                "highlightedCodePath": highlighted_code_path,
            }

        main_graph = {}
        main_graph["language"] = "python"
        graph_nodes = {}
        graph_edges = []
        for node in self.adjacency_list.keys():
            graph_nodes[node] = format_node(node)

            for node_to in self.adjacency_list[node]:
                
                suffix = ""
                node_to_name = node_to
                if "&" in node_to:
                    node_to_name, _ = node_to.split('&')
                    self.external_dependency_counts[node_to_name] += 1
                    suffix = str(self.external_dependency_counts[node_to_name]) 

                hashed_name = self.__hash_value(node + node_to)
                graph_edge = {
                    "from": node,
                    "to": node_to_name + suffix,
                    "data": {"props": []},
                    "highlightedCodePath": "code/python/main/edge-code/" + hashed_name + ".txt"
                }

                graph_nodes[node_to_name + suffix] = format_node(node_to)
                graph_nodes[node_to_name + suffix]['name'] = node_to_name
                graph_edges.append(graph_edge)

        main_graph["nodes"] = graph_nodes
        main_graph["edges"] = graph_edges

        return main_graph

    # Creates the graph containing all files and their references. 
    def __get_files_graph(self):

        # Returns a formatted node.
        def format_node(node):
            node_info = self.nodes[node]
            file_path = node_info['original_file_path']
            return {
                "name": file_path,
                "type": "File",
                "filePath": node_info["code_path"],
                "originalFilePath": file_path,
            }

        files_graph = {}
        files_graph["language"] = "python"
        graph_nodes = {}
        graph_edges = []

        seen_edges = set()

        for node in self.adjacency_list.keys():
            file_path = self.nodes[node]['original_file_path']

            graph_nodes[file_path] = format_node(node)

            for node_to in self.adjacency_list[node]:
                other_file_path = self.nodes[node_to]['original_file_path']
                graph_nodes[other_file_path] = format_node(node_to)

                if file_path != other_file_path and (file_path, other_file_path) not in seen_edges:
                    seen_edges.add((file_path, other_file_path))
                    graph_edge = {
                        "from": file_path,
                        "to": other_file_path,
                        "data": {"props": []},
                    }
                    graph_edges.append(graph_edge)

        files_graph["nodes"] = graph_nodes
        files_graph["edges"] = graph_edges

        return files_graph


    # Returns a json representation of the graph. 
    def __build_json(self):

        data = {}
        data["title"] = self.title
        data["main"] = self.__get_main_graph()
        data["files"] = self.__get_files_graph()


        return data

    # Start frontend application that displays the graph on the browser.  
    def start_frontend(self):

        # Displays ASCII text of "VizCode"
        print(text2art("VizCode"))

        os.chdir(CURRENT_DIR_PATH + FRONT_END_PATH + 'build')
        PORT = 8000

        time.sleep(1)
        
        bash_command =  f"open http://localhost:{PORT}"
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        process.communicate()

        try:
            httpd = HTTPServer(('', PORT), SimpleHTTPRequestHandler)
            print(f"VizCode is ready at: http://127.0.0.1:{PORT}")
            httpd.serve_forever()

        except KeyboardInterrupt:
            httpd.shutdown()
            httpd.server_close()
            print("\nVizCode is powering down...")

        except: 
            print("Oops you already have VizCode open. Please close VizCode and try again.")
            print("VizCode is powering down...")
        
        return

