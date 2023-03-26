from config_app.settings import project_settings

config = project_settings()


def style_qmenu():
    sml = ""
    if config['theme'] == 'light':
        sml = """
                QMenu::item {
                        background-color: #fff;
                    }
            """
    sm = f"""
            QMenu::item:selected {{
                background-color: {config['cor_pref'][1]};
                color: default;
            }}
            QMenu::item:pressed {{
                background-color: {config['cor_pref'][2]};
            }}
        """
    return sml + sm


def style_qmenu_bar():
    smb = f"""
                QMenuBar::item:selected {{
                    background-color: {config['cor_pref'][1]};
                    color: default;
                }}
            """
    return smb


def style_qtool_bar():
    if config['theme'] == 'dark':
        stb = f"""
                    QToolBar {{
                        background-color: #000;
                        border: 1px solid {config['cor_pref'][2]};
                    }}
                    QToolBar QToolButton {{
                        background-color: #000;
                    }}
                    QToolBar QToolButton:hover {{
                        background-color: {config['cor_pref'][1]};
                        color: default;
                    }}
                """
    else:
        stb = f"""
                    QToolBar {{
                        background-color: #fff;
                        border: 1px solid {config['cor_pref'][2]};
                    }}
                    QToolBar QToolButton {{
                        background-color: #fff;
                    }}
                    QToolBar QToolButton:hover {{
                        background-color: {config['cor_pref'][1]};
                        color: default;
                    }}
                """
    return stb


def style_qtext_edit():
    if config['theme'] == 'dark':
        ste = "border: 1px solid #333;"
    else:
        ste = "border: 1px solid #ddd;"
    return ste


def style_qcombo_box():
    scb = f"""
                QComboBox:!editable {{
                    border: 1px solid {config['cor_pref'][2]};
                }}
                QComboBox:!editable:on {{
                    background: {config['cor_pref'][1]};
                    color: default;
                }}
                QComboBox QAbstractItemView {{
                    border: 1px solid {config['cor_pref'][2]};
                    selection-background-color: {config['cor_pref'][1]};
                    selection-color: default;
                }}
                QComboBox QAbstractItemView::itemView {{
                    min-height: 30px;
                }}
            """
    return scb


def style_qline_edit():
    let = f"""
                QLineEdit:read-only{{
                    border: 0;
                    background: {config['cor_pref'][1]};
                    color: #ddd
                }}
                QLineEdit {{
                    border: 1px solid #ddd;
                }}
                QLineEdit:focus {{
                    border: 1px solid {config['cor_pref'][2]};
                    selection-background-color: {config['cor_pref'][1]};
                    selection-color: default;
                }}
            """
    return let


def style_qspin_box():
    ssb = f"""
            QSpinBox {{
                border: 1px solid {config['cor_pref'][2]};
                selection-
                selection-color: default;
            }}
    """
    return ssb


def style_qpush_button():
    spb = f"""
        QPushButton {{
            background-color: {config['cor_pref'][1]};
            border: 1px solid {config['cor_pref'][2]};
            color: {config['cor_pref'][2]};
            border-radius: 0;
            padding-top: 4px;
            padding-bottom: 4px;
        }}
        QPushButton:hover {{
            background-color: {config['cor_pref'][2]};
            border: 1px solid {config['cor_pref'][1]};
            color: {config['cor_pref'][1]};
        }}
    """
    return spb
