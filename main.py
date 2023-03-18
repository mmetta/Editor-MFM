import base64
import os
import sys
import webbrowser

from PySide6.QtPrintSupport import *

from Dialog_link import DialogLink
from pyCore import *

import qdarkstyle
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from Dialog_about import DialogAbout
from Dialog_config import DialogConfig
from config_application.estilos_config import style_qmenu, style_qmenu_bar, style_qtool_bar, style_qtext_edit, \
    style_qcombo_box, style_qspin_box, style_qpush_button
from config_application.settings import project_settings
from config_application.icon_coloring import cor_icon

config = project_settings()

if config['theme'] == 'dark':
    tema = DarkPalette
else:
    tema = LightPalette


class MainApp(QMainWindow):
    """ the main class of our app """

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)

        # window title
        self.title = "MFM Editor 0.0.1"
        self.setWindowTitle(self.title)
        self.setMinimumSize(config['app_w'], config['app_h'])
        if config['max']:
            self.showMaximized()
        self.closeEvent = self.fechar
        self.th_cores = []

        # editor section
        self.editor = QTextEdit(self)
        self.editor.setAcceptDrops(True)
        self.editor.setMinimumWidth(794)
        self.editor.setMaximumWidth(794)
        self.editor.setStyleSheet('border: 0;')
        self.editor.viewport().setStyleSheet(style_qtext_edit())
        self.editor.setViewportMargins(80, 80, 80, 0)
        self.editor.setLocale(QLocale('pt_BR'))
        self.setCentralWidget(self.editor)

        # create menubar and toolbar first
        self.create_menu_bar()
        self.create_toolbar()

        # after craeting toolabr we can call and select font size
        font = QFont('Arial', 12, 400)
        self.editor.setFont(font)
        self.editor.setFontPointSize(12)

        self.editor.selectionChanged.connect(self.status_editor)
        self.editor.textChanged.connect(self.editor_changed)

        # stores path
        self.path = ''

        self.alterado = ''
        self.n_chr = ''

    def fechar(self, event):
        if self.alterado == '*' and self.editor.toPlainText() != '':
            self.dialog_save(event)
        else:
            self.new_file()

    # ###############################
    # ####  Drag and Drop  ####
    # ###############################

    def dragEnterEvent(self, event):
        print(event)
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, source):
        print(source)
        cursor = self.editor.textCursor()
        document = self.editor.document()
        print(source)
        if source.hasUrls():
            for u in source.urls():
                # file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile():
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())
                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break
            else:
                # If all were valid images, finish here.
                return
        elif source.hasImage():
            image = source.imageData()
            print(image)
            # uuid = hexuuid()
            # document.addResource(QTextDocument.ImageResource, uuid, image)
            # cursor.insertImage(uuid)
            return

    # ###############################
    # ####  DIALOG confirm save  ####
    # ###############################

    def dialog_save(self, ev):
        if not ev:
            ev = 'fechar'
        self.evento = ev
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle('Salvar')
        self.dlg.setWindowIcon(cor_icon(f"icons/light/save.svg"))
        self.dlg.setMinimumSize(320, 90)
        lay_v = QVBoxLayout(self.dlg)
        nome = self.path
        if nome == '':
            nome = 'Documento sem nome'
        lbl1 = QLabel(nome)
        btn_yes = QPushButton('Salvar')
        btn_yes.setStyleSheet(style_qpush_button())
        btn_yes.clicked.connect(self.yes_save)
        btn_no = QPushButton('Não salvar')
        btn_no.setStyleSheet(style_qpush_button())
        btn_no.clicked.connect(self.no_save)
        btn_cancel = QPushButton('Cancelar')
        btn_cancel.setStyleSheet(style_qpush_button())
        btn_cancel.clicked.connect(self.cancel_save)
        lay_h = QHBoxLayout()
        lay_h.addWidget(btn_cancel)
        lay_h.addWidget(btn_no)
        lay_h.addWidget(btn_yes)
        lay_v.addWidget(lbl1)
        lay_v.addLayout(lay_h)
        self.dlg.exec()

    def cancel_save(self):
        if self.evento != 'fechar':
            self.evento.ignore()
        self.dlg.close()

    def no_save(self):
        if self.evento == 'fechar':
            self.new_file()
        self.dlg.close()

    def yes_save(self):
        self.file_save()
        self.alterado = ''
        self.update_title()
        if self.evento == 'fechar':
            self.new_file()
        self.dlg.close()

    def editor_changed(self):
        if self.editor.toPlainText() == '':
            self.alterado = ''
            self.path = ''
            self.update_title()
        if self.n_chr != 'open' and self.editor.toPlainText() != '':
            self.alterado = '*'
            self.update_title()
        if self.n_chr == 'open':
            self.n_chr = ''

    # ###############################
    # ####    CREATE MENU BAR    ####
    # ###############################

    def create_menu_bar(self):
        menuBar = QMenuBar(self)

        menuBar.setStyleSheet(style_qmenu_bar())

        """ add elements to the menubar """
        # App icon will go here
        # app_icon = menuBar.addMenu(QIcon("doc_icon.png"), "icon")

        # file menu **
        file_menu = QMenu("Arquivo", self)
        menuBar.addMenu(file_menu)

        new_action = QAction('Novo', self)
        new_action.triggered.connect(self.fechar)
        file_menu.addAction(new_action)

        open_action = QAction('Abrir', self)
        open_action.triggered.connect(self.file_open)
        file_menu.addAction(open_action)

        save_action = QAction('Salvar', self)
        save_action.triggered.connect(self.file_save)
        file_menu.addAction(save_action)

        rename_action = QAction('Salvar como', self)
        rename_action.triggered.connect(self.file_saveas)
        file_menu.addAction(rename_action)

        file_menu.addSeparator()

        pdf_action = QAction("Salvar em PDF", self)
        pdf_action.triggered.connect(self.save_pdf)
        file_menu.addAction(pdf_action)
        file_menu.setStyleSheet(style_qmenu())

        printer_action = QAction("Imprimir", self)
        printer_action.triggered.connect(self.print_page)
        file_menu.addAction(printer_action)
        file_menu.setStyleSheet(style_qmenu())

        preview_action = QAction("Visualizar impressão", self)
        preview_action.triggered.connect(self.handlePreview)
        file_menu.addAction(preview_action)
        file_menu.setStyleSheet(style_qmenu())
        
        file_menu.addSeparator()

        fechar_action = QAction('Fechar', self)
        fechar_action.triggered.connect(self.fechar)
        file_menu.addAction(fechar_action)

        # edit menu **
        edit_menu = QMenu("Editar", self)
        menuBar.addMenu(edit_menu)

        # copy
        copy_action = QAction('Copiar', self)
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)

        # paste
        paste_action = QAction('Colar', self)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)

        # clear
        clear_action = QAction('Apagar tudo', self)
        clear_action.triggered.connect(self.editor.clear)
        edit_menu.addAction(clear_action)

        # select all
        select_action = QAction('Selecionar tudo', self)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)
        edit_menu.setStyleSheet(style_qmenu())

        # view menu **
        view_menu = QMenu("Janela", self)
        menuBar.addMenu(view_menu)

        # minimize
        minscr_action = QAction('Minimizar', self)
        minscr_action.triggered.connect(lambda: self.showMinimized())
        view_menu.addAction(minscr_action)

        # maxmize
        maxscr_action = QAction('Maximizar', self)
        maxscr_action.triggered.connect(lambda: self.showMaximized())
        view_menu.addAction(maxscr_action)

        # fullscreen
        fullscr_action = QAction('Tela cheia', self)
        fullscr_action.triggered.connect(lambda: self.showFullScreen())
        view_menu.addAction(fullscr_action)

        # normal screen
        normscr_action = QAction('Tela normal', self)
        normscr_action.triggered.connect(lambda: self.showNormal())
        view_menu.addAction(normscr_action)
        view_menu.setStyleSheet(style_qmenu())

        # About menu **
        about_menu = QMenu("Sobre", self)
        menuBar.addMenu(about_menu)

        # Help
        help_action = QAction('Ajuda', self)
        help_action.triggered.connect(self.abrir_help)
        about_menu.addAction(help_action)

        # App Settings
        config_action = QAction('Configurações', self)
        config_action.triggered.connect(DialogConfig)
        about_menu.addAction(config_action)

        # About
        about_action = QAction('Sobre...', self)
        about_action.triggered.connect(DialogAbout)
        about_menu.addAction(about_action)
        about_menu.setStyleSheet(style_qmenu())

        self.setMenuBar(menuBar)

        self.colors = ['ffffff', 'cccccc', '808080', '000000', 'ffff00', 'ff0000', '0000ff', '00ff00']

    # #################################
    # ####  STATUS EDITOR MONITOR  ####
    # #################################

    def status_editor(self):
        self.font_size.setValue(int(self.editor.fontPointSize()))
        self.font_combo.setCurrentText(self.editor.fontFamily())
        for i, cor in enumerate(self.colors):
            if self.editor.textColor().name() == f'#{cor}':
                self.font_color.setCurrentIndex(i)

    # ###############################
    # ####    CREATE TOOL BAR    ####
    # ###############################

    def create_toolbar(self):
        # Using a title
        ToolBar = QToolBar("Tools", self)
        ToolBar.setContentsMargins(0, 0, 0, 0)

        self.th_cor = config['cor_pref'][2]

        ToolBar.setStyleSheet(style_qtool_bar())

            # undo
        undo_action = QAction(cor_icon(f"icons/light/undo.svg"), 'Desfazer', self)
        undo_action.triggered.connect(self.editor.undo)
        ToolBar.addAction(undo_action)

        # redo
        redo_action = QAction(cor_icon(f"icons/light/redo.svg"), 'Refazer', self)
        redo_action.triggered.connect(self.editor.redo)
        ToolBar.addAction(redo_action)

        # adding separator
        ToolBar.addSeparator()

        # cut
        cut_action = QAction(cor_icon(f"icons/light/cut.svg"), 'Cortar', self)
        cut_action.triggered.connect(self.editor.cut)
        ToolBar.addAction(cut_action)

        # copy
        copy_action = QAction(cor_icon(f"icons/light/copy.svg"), 'Copiar', self)
        copy_action.triggered.connect(self.editor.copy)
        ToolBar.addAction(copy_action)

        # paste
        paste_action = QAction(cor_icon(f"icons/light/paste.svg"), 'Colar', self)
        paste_action.triggered.connect(self.editor.paste)
        ToolBar.addAction(paste_action)

        # adding separator
        ToolBar.addSeparator()

        # fonts
        font_family = ['Arial', 'Arial Black', 'Calibri', 'Comic Sans MS', 'Corbel',
            'Courrier New', 'Elephant', 'Georgia', 'Segoe Script', 'Tahoma',
            'Times New Roman', 'Verdana']
        self.font_combo = QComboBox(self)
        self.font_combo.addItems(font_family)
        self.font_combo.activated.connect(self.set_font)  # connect with function
        self.font_combo.setStyleSheet(style_qcombo_box())
        self.font_combo.setMaxVisibleItems(len(font_family))
        self.font_combo.setFont(QFont('Arial', 9))
        ToolBar.addWidget(self.font_combo)

        # font size
        self.font_size = QSpinBox(self)
        self.font_size.setValue(12)
        self.font_size.valueChanged.connect(self.set_font_size)
        self.font_size.setFont(QFont('Arial', 9))
        self.font_size.setStyleSheet(style_qspin_box())
        ToolBar.addWidget(self.font_size)

        # color
        self.font_color = QComboBox(self)
        self.model = self.font_color.model()
        for cor in self.colors:
            path_icon = f'icons/{cor}.png'
            cor_item = f'#{cor}'
            item = QStandardItem()
            item.setText(str(cor_item))
            item.setTextAlignment(Qt.AlignCenter)
            item.setIcon(QIcon(path_icon))
            self.model.appendRow(item)
        self.font_color.activated.connect(self.set_color)
        self.font_color.setStyleSheet(style_qcombo_box())
        ToolBar.addWidget(self.font_color)

        # separator
        ToolBar.addSeparator()

        # bold
        bold_action = QAction(cor_icon(f"icons/light/bold.svg"), 'Bold', self)
        bold_action.triggered.connect(self.bold_text)
        ToolBar.addAction(bold_action)

        # underline
        underline_action = QAction(cor_icon(f"icons/light/underline.svg"), 'Underline', self)
        underline_action.triggered.connect(self.underline_text)
        ToolBar.addAction(underline_action)

        # italic
        italic_action = QAction(cor_icon(f"icons/light/italic.svg"), 'Italic', self)
        italic_action.triggered.connect(self.italic_text)
        ToolBar.addAction(italic_action)

        # separator
        ToolBar.addSeparator()

        # text alignment
        left_alignment_action = QAction(cor_icon(f"icons/light/left-align.svg"), 'Esquerda', self)
        left_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        ToolBar.addAction(left_alignment_action)

        center_action = QAction(cor_icon(f"icons/light/center-align.svg"), 'Centralizar', self)
        center_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        ToolBar.addAction(center_action)

        justification_action = QAction(cor_icon(f"icons/light/justify-align.svg"), 'Justificado', self)
        justification_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        ToolBar.addAction(justification_action)

        right_alignment_action = QAction(cor_icon(f"icons/light/right-align.svg"), 'Direita', self)
        right_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        ToolBar.addAction(right_alignment_action)

        # separator
        ToolBar.addSeparator()

        image_action = QAction(cor_icon(f"icons/light/picture.svg"), 'Imagem', self)
        image_action.triggered.connect(self.insert_image)
        ToolBar.addAction(image_action)

        link_action = QAction(cor_icon(f"icons/light/link-plus.svg"), 'Link', self)
        link_action.triggered.connect(self.insert_link)
        ToolBar.addAction(link_action)

        self.addToolBar(ToolBar)

        ToolBar.setIconSize(QSize(18, 18))
        ToolBar.setFixedHeight(36)

    # ###################################
    # ####   INSERT LINK FUNCTION   ####
    # ###################################

    def insert_link(self):
        if self.editor.textCursor().selectedText():
            nome = self.editor.textCursor().selectedText()
        else:
            nome = ''
        dg = DialogLink(nome)
        str_link = f'<a href="{dg.link_url}">{dg.link_nome}</a>'
        document = self.editor.document()
        cursor = QTextCursor(document)
        if nome == '':
            pos = self.editor.textCursor().position()
            cursor.setPosition(pos)
            cursor.insertHtml(str_link)
        else:
            self.editor.textCursor().removeSelectedText()
            pos = self.editor.textCursor().position()
            cursor.setPosition(pos)
            cursor.insertHtml(str_link)

    # ###################################
    # ####   INSERT IMAGE FUNCTION   ####
    # ###################################

    def insert_image(self):
        try:
            img, _ = QFileDialog.getOpenFileName(self, "Escolha uma imagem", "", "Image Files(*.png *.gif *.jpg *jpeg *.svg)")
        except Exception as e:
            print(e)
        else:
            document = self.editor.document()
            cursor = QTextCursor(document)
            pos = self.editor.textCursor().position()
            cursor.setPosition(pos)
            image = QPixmap(img)
            ba = QByteArray()
            buffer = QBuffer(ba)
            image.save(buffer, 'PNG', quality=95)
            binary = base64.b64encode(ba.data())
            HTMLBin = "<img src= \"data:image/*;base64,{}\" max-width=50% max-height=50%></img>".format(
                str(binary, 'utf-8'))
            cursor.insertHtml(HTMLBin)

    # ###################################
    # #### MENU e TOOL BAR FUNCTIONS ####
    # ###################################

    def italic_text(self):
        # if already italic, change into normal, else italic
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not (state))

    def underline_text(self):
        # if already underlined, change into normal, else underlined
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not (state))

    def bold_text(self):
        # if already bold, make normal, else make bold
        if self.editor.fontWeight() != QFont.Bold:
            self.editor.setFontWeight(QFont.Bold)
            return
        self.editor.setFontWeight(QFont.Normal)

    def set_color(self):
        sel_color = self.font_color.currentText()
        self.editor.setTextColor(QColor(sel_color))

    def set_font(self):
        font_family = self.font_combo.currentText()
        value = self.font_size.value()
        font = QFont(font_family, value)
        # font.setFamily(font_family)
        self.editor.setCurrentFont(font)

    def set_font_size(self):
        value = self.font_size.value()
        self.editor.setFontPointSize(value)

    def new_file(self):
        self.editor.setHtml('')
        self.path = ''
        self.alterado = ''
        self.update_title()

    def abrir_help(self):
        app_path = os.path.abspath(os.getcwd())
        folder = "about"
        path = os.path.join(app_path, folder)
        path_help = os.path.normpath(os.path.join(path, 'mfm_editor_help.html'))
        webbrowser.open(path_help)

    # #################################
    # ####  OPEN e SAVE FUNCTIONS  ####
    # #################################

    def file_open(self):
        self.path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Mario F Metta Docs(*.mfm)")
        try:
            with open(self.path, 'r') as f:
               text = f.read()
        except Exception as e:
            print(e)
        else:
            self.n_chr = 'open'
            self.editor.setHtml(text)
            self.update_title()

    def file_save(self):
        if self.path == '':
            # If we do not have a path, we need to use Save As.
            self.file_saveas()

        text = self.editor.toHtml()

        try:
            with open(self.path, 'w') as f:
                f.write(text)
                self.update_title()
        except Exception as e:
            print(e)

    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Mario F Metta Docs(*.mfm)")

        if self.path == '':
            return  # If dialog is cancelled, will return ''

        text = self.editor.toHtml()

        try:
            if self.path[-4:] != '.mfm':
                self.path = self.path + '.mfm'
            with open(self.path, 'w') as f:
                f.write(text)
                self.alterado = ''
                self.update_title()
        except Exception as e:
            print(e)

    def update_title(self):
        if self.path != '':
            part = self.path.split('/')
            n = len(part)
            self.setWindowTitle(self.title + ' - ' + part[n - 1] + self.alterado)
        else:
            self.setWindowTitle(self.title + ' ' + self.alterado)

    def printPreview(self, printer):
        printer.setResolution(96)
        printer.setPageSize(QPageSize.PageSizeId.A4)
        text = self.editor.document()
        printer.setPageMargins(QMargins(0, 0, 0, 0), QPageLayout.Unit.Millimeter)
        text.print_(printer)

    def handlePreview(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.printPreview)
        dialog.exec()

    def print_page(self):
        printer = QPrinter()
        printer.setResolution(96)
        printer.setPageSize(QPageSize.PageSizeId.A4)
        document = self.editor.document()
        dlg = QPrintDialog(printer)
        if dlg.exec():
            print(printer.outputFormat())
            document.print_(printer)

    def save_pdf(self):
        if self.editor.toPlainText() != '':  # if name not empty
            printer = QPrinter()
            printer.setResolution(96)
            printer.setPageSize(QPageSize.PageSizeId.A4)
            printer.setOutputFormat(QPrinter.PdfFormat)
            f_name, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF files (*.pdf)")
            if f_name[-4:] != '.pdf':
                f_name = f_name + '.pdf'
            printer.setOutputFileName(f_name)
            text = self.editor.document()
            printer.setPageMargins(QMargins(0, 0, 0, 0), QPageLayout.Unit.Millimeter)
            text.print_(printer)


app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icons/favicon.ico"))
app.setStyleSheet(qdarkstyle.load_stylesheet(tema))
window = MainApp()
window.show()
sys.exit(app.exec())
