import json
import os
from pathlib import Path

from atual_path import local_path

base_path = Path(local_path(), './data')


def project_settings():
    set_json = os.path.normpath(os.path.join(base_path, 'set_project.json'))
    with open(set_json, 'r', encoding='utf8') as f:
        return json.load(f)


def save_new_conf(new_conf):
    json_path = os.path.normpath(os.path.join(base_path, 'set_project.json'))
    with open(json_path, 'w', encoding='utf8') as f:
        json.dump(new_conf, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
