import ast
import json
import os
import sqlite3

appData = os.getenv('APPDATA') + '\\EditorMFM'
database = os.path.join(appData, 'config.db')


def create_db():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # ## CREATE ## #
    cursor.execute("""
            CREATE TABLE configs (
                app_h INTEGER NOT NULL,
                app_w INTEGER NOT NULL,
                colors_theme TEXT NOT NULL,
                cor_pref TEXT NOT NULL,
                max INTEGER NOT NULL,
                theme TEXT NOT NULL
            );
            """)
    print('Tabela criada com sucesso.')
    list_colors = [
        [
            "Azul",
            "#bbdefb",
            "#1565c0"
        ],
        [
            "Ambar",
            "#ffecB3",
            "#ff6f00"
        ],
        [
            "Verde",
            "#d5ecd6",
            "#00dd00"
        ],
        [
            "Pink",
            "#fce4ec",
            "#e53080"
        ]
    ]
    list_pref = [
        "Azul",
        "#bbdefb",
        "#1565c0"
    ]
    conn.execute("INSERT INTO configs (app_h, app_w, colors_theme, cor_pref, max, theme) VALUES (?, ?, ?, ?, ?, ?)",
                 (600, 800, str(list_colors), str(list_pref), 0, "light"))
    conn.commit()
    conn.close()


def converter(campo):
    return ast.literal_eval(campo)


def select_all():
    # def project_settings():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM configs;
    """)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    json_data = json.dumps(data)
    obj = json.loads(json_data)
    obj[0]['colors_theme'] = eval(obj[0]['colors_theme'])
    obj[0]['cor_pref'] = eval(obj[0]['cor_pref'])
    return obj[0]


def update_data(data):
    # ## UPDATE ## #
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE configs SET app_h = ?, app_w = ?, colors_theme = ?, cor_pref = ?, max = ?, theme = ?
    """, (data['app_h'], data['app_w'], str(data['colors_theme']), str(data['cor_pref']), data['max'], data['theme']))
    conn.commit()
    conn.close()
