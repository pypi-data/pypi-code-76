import pathlib

CURRENT_DIR_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/"
FRONT_END_PATH = "frontend/"
PUBLIC_PATH = FRONT_END_PATH + "build/"
FILE_CODE_PATH = "code/python/main/"
NODE_CODE_PATH = PUBLIC_PATH + FILE_CODE_PATH + "node-code/"
EDGE_CODE_PATH = PUBLIC_PATH + FILE_CODE_PATH + "edge-code/"
GRAPH_FILE_PATH = PUBLIC_PATH + "python_graph.json"
VIZCODE_PATH = "vizcode/"
CREDENTIALS_PATH = PUBLIC_PATH + "credentials.json"