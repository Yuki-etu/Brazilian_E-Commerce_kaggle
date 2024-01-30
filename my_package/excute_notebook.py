"""
別のnotebookファイルを実行するための関数です。

---parameter---
notebook_path : 実行するnotebookファイルのパス

"""

import nbformat
import os
import subprocess
from nbconvert import PythonExporter

def execute_notebook(notebook_path):
    
    # カレントディレクトリを現在のディレクトリに変更
    this_script_path = "./make_data.ipynb"
    this_script_dir = os.path.dirname(os.path.abspath(this_script_path))
    os.chdir(this_script_dir)

    # 実行するnotebookファイルのディレクトリを取得
    notebook_dir = os.path.dirname(os.path.abspath(notebook_path))

    # notebookのファイル名を取得
    notebook_file = os.path.basename(notebook_path)

    # カレントディレクトリをノートブックのディレクトリに変更    <- 実行するnotebookファイル内の相対パスを正常に実行するため。
    os.chdir(notebook_dir)

    with open(os.path.join(notebook_dir, notebook_file), 'r', encoding='utf-8') as f:
        nb_content = nbformat.read(f, as_version=4)

    exporter = PythonExporter()
    (python_code, resources) = exporter.from_notebook_node(nb_content)

    # ノートブックを実行し、標準出力を捕捉する
    process = subprocess.Popen(['python', '-c', python_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    # カレントディレクトリを現在のディレクトリに変更   <- 変更したカレントディレクトリを元に戻すため。
    os.chdir(this_script_dir)

    # エラーがあれば表示
    if stderr:
        print("Error during notebook execution:")
        print(stderr)