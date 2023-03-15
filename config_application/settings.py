import json
import os


def project_settings():
    app_path = os.path.abspath(os.getcwd())
    folder = "config_application"
    path = os.path.join(app_path, folder)
    set_json = os.path.normpath(os.path.join(path, 'set_project.json'))
    with open(set_json, 'r', encoding='utf8') as f:
        return json.load(f)


def save_new_conf(new_conf):
    app_path = os.path.abspath(os.getcwd())
    folder = "config_application"
    path = os.path.join(app_path, folder)
    json_path = os.path.normpath(os.path.join(path, 'set_project.json'))
    with open(json_path, 'w', encoding='utf8') as f:
        json.dump(new_conf, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
