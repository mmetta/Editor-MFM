from sqlite_data import select_all

config = select_all()


def style_qmenu_bar():
    smb = f"""
                QMenuBar::item:selected {{
                    background-color: {config['cor_pref'][2]};
                    color: #ffffff;
                }}
            """
    return smb


def style_tool_bar():
    stb = f"""
                QToolBar {{border: 1px solid {config['cor_pref'][2]};}}
                QToolTip {{ color: {config['cor_pref'][2]}; background-color: #ffffff; border: none; }}
            """
    return stb


def style_font_color(color):
    bgc = f"""
                QPushButton {{border: 1px solid {config['cor_pref'][2]}; background-color: {color};}}
                QPushButton Cores {{color: {config['cor_pref'][2]}; background-color: #ffffff; border: none;}}
            """
    return bgc


def style_font_family():
    ffm = f"""
                QComboBox {{border: 1px solid {config['cor_pref'][2]};}}
                QComboBox Fonte {{color: {config['cor_pref'][2]}; background-color: #ffffff; border: none;}}
            """
    return ffm


def style_font_size():
    sfs = f"""
                QSpinBox {{border: 1px solid {config['cor_pref'][2]};}}
                QSpinBox Tamanho {{color: {config['cor_pref'][2]}; background-color: #ffffff; border: none;}}
            """
    return sfs


def style_qmenu():
    i = 3 if config['theme'] == 'dark' else 1
    sm = f"""
            QMenu::item:selected {{
                background-color: {config['cor_pref'][i]};
            }}
            QMenu::item:pressed {{
                background-color: {config['cor_pref'][2]};
            }}
        """
    return sm
