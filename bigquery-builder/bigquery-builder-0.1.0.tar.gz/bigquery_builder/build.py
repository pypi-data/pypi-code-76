import os
import json
import hashlib
from collections import deque
from urllib.parse import quote_plus
import google.auth
from google.cloud import bigquery

class Builder():
    SQL_TOP_KEYWORDS = ["SELECT", "FROM", "WHERE", "GROUP", "ORDER", "HAVING"]
    project_id = google.auth.default()[1]
    client = bigquery.Client()
    model_path = os.path.join(".", "models")

    def create_view(self, dataset: str, view_name: str, node_name: str = "Semantics"):
        with open(os.path.join(self.model_path, "views", view_name + ".sql")) as fp:
            query = fp.read()

        if node_name == "Semantics":
            view_id = ".".join([self.project_id, dataset, view_name])
        else:
            view_id = ".".join([self.project_id, "debug", hashlib.md5(view_name.encode()).hexdigest()])
            node_name = node_name.replace(";", "")
            query = query.replace("SELECT * FROM Semantics", "SELECT * FROM " + node_name)

        self.client.delete_table(view_id, not_found_ok=True)
        view = bigquery.Table(view_id)
        view.view_query = query
        view = self.client.create_table(view)
        print(str(view.reference))

    def create_table(self, dataset: str, table_name: str):
        table_id = ".".join([self.project_id, dataset, table_name])
        with open(os.path.join(self.model_path, "tables", table_name + ".json")) as fp:
            table_conf = json.load(fp)
        source = table_conf.pop("source")
        create_query = "SELECT * FROM `{}`".format(source.replace(";", ""))

        if "time_partitioning" in table_conf:
            table_conf["time_partitioning"] = bigquery.table.TimePartitioning(**table_conf["time_partitioning"])
        job_config = bigquery.QueryJobConfig(
            destination=table_id,
            **table_conf
        )
        create_job = self.client.query(create_query, job_config=job_config)
        create_job.result()
        print(table_id)

    def get_dependencies(self, type: str, name: str):
        with open(os.path.join(self.model_path, type, name, "config.json")) as fp:
            conf = json.load(fp)
        dependencies = conf.pop("dependencies")
        view_dep = [{"type": "view", "name": i.split(".")[-1]} for i in dependencies.get("views", [])]
        table_dep = [{"type": "table", "name": i.split(".")[-1]} for i in dependencies.get("tables", [])]
        return view_dep + table_dep

    def get_preview_url(self, dataset: str, name: str, node_name: str = "Semantics"):
        if node_name == "Semantics":
            preview_config = json.dumps({"projectId": self.project_id,
                                         "datasetId": dataset,
                                         "tableId": name,
                                         "billingProjectId": self.project_id,
                                         "connectorType": "BIG_QUERY",
                                         "sqlType": "STANDARD_SQL"}, ensure_ascii=False)
        else:
            self.create_view(dataset, name, node_name)
            preview_config = json.dumps({"projectId": self.project_id,
                                         "datasetId": "debug",
                                         "tableId": hashlib.md5(name.encode()).hexdigest(),
                                         "billingProjectId": self.project_id,
                                         "connectorType": "BIG_QUERY",
                                         "sqlType": "STANDARD_SQL"}, ensure_ascii=False)
        return "https://datastudio.google.com/u/0/explorer?config=" + quote_plus(preview_config)

    def get_first_sql_comments(self, part: list):
        text_mode = "\n".join(part)
        comments = text_mode.split("/*")[1].split("*/", 1)[0] if "/*" in text_mode else ""
        return comments.split("\n")

    def view_parser(self, view_name: str):
        with open(os.path.join(self.model_path, "views", view_name, "main.sql")) as fp:
            view_query = deque([line.rstrip() for line in fp])
        parsed_data = {"nodes": []}
        begin, body, end = [], [], []
        node = []
        while True:
            begin.append(view_query.popleft())
            if begin[-1].strip().lower() == "with" or not view_query:
                parsed_data["comment"] = self.get_first_sql_comments(begin)
                break
        while True:
            end.append(view_query.pop())
            if end[-1].strip().lower() == "select * from semantics" or not view_query:
                break
        view_query = list(view_query)
        for last, current in zip(view_query[:-1], view_query[1:]):
            node.append(last)
            if last.strip().lower() == '),' and current.strip().lower().endswith('as ('):
                body.append(node.copy())
                node = []
        body.append(node)

        for node in body:
            node_dict, current_keyword = {"void": []}, "void"
            node_dict["comments"] = self.get_first_sql_comments(node)
            for line in node:
                if "name" not in node_dict:
                    node_dict["name"] = line.strip().split(" ")[0]
                    continue
                if line.strip().split(" ")[0].upper() in self.SQL_TOP_KEYWORDS:
                    current_keyword = line.strip().split(" ")[0].lower()
                    node_dict[current_keyword] = []
                node_dict[current_keyword].append(line)
            if "from" in node_dict:
                from_clause = " ".join([frag.strip() for frag in node_dict["from"]]).split(" ")[1:]
                node_dict["dependencies"] = []
                for piece in from_clause:
                    if piece.upper() in ["USING", "ON"]:
                        break
                    if piece.upper() in ["JOIN", "INNER", "LEFT", "RIGHT", "OUTER", "CROSS", "FULL", "),"]:
                        continue
                    node_dict["dependencies"].append(piece)
            parsed_data["nodes"].append(node_dict)
        return parsed_data

