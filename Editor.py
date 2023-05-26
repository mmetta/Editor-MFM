import base64
import os
import sys
import webbrowser
from pathlib import Path

from PySide6.QtCore import QSize, Signal, QByteArray, QBuffer, QMargins, QFile, QIODevice, Qt, QLocale
from PySide6.QtGui import QAction, QColor, QTextCursor, QPixmap, QPageSize, QPageLayout, QFontDatabase, QFont, \
    QTextListFormat, QTextFrameFormat
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtWidgets import QWidget, QTextEdit, QColorDialog, QMenuBar, QMenu, QVBoxLayout, QToolBar, QPushButton, \
    QFileDialog, QDialog, QLabel, QHBoxLayout, QComboBox, QSpinBox, QFontDialog

from Custom_table_format import CustomTableFormat
from Dialog_about import DialogAbout
from Dialog_Confirm import CustomDialog
from Dialog_link import DialogLink
from Dialog_resize_img import ResizeDialog
from Dialog_table_config import DialogTableConfig
from atual_path import local_path
from estilos import style_qmenu_bar, style_font_color, style_font_family, style_font_size, style_qmenu, style_tool_bar
from icon_coloring import cor_icon

base_path = Path(local_path(), './')


class MyEditor(QTextEdit):
    imageInserted = Signal(str)

    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        # if source.hasImage():
        if source.hasUrls():
            url = source.urls()
            path = str(url[0].toLocalFile())
            self.imageInserted.emit(path)
        else:
            super().insertFromMimeData(source)


class Editor(QWidget):
    edit_title = Signal(str)
    get_config = Signal(str)
    show_minimized = Signal()
    show_maximized = Signal()
    show_full_screen = Signal()
    show_normal = Signal()

    def __init__(self):
        super().__init__()

        self.font_color = QPushButton()
        self.font_combo = QComboBox(self)
        self.font_size = QSpinBox(self)
        self.font_size.setValue(12)

        self.editor = MyEditor(self)
        locale = QLocale('pt-BR')
        self.editor.setLocale(locale)

        lay_footer = QHBoxLayout()
        self.lbl_footer = QLabel()
        lay_footer.setContentsMargins(20, 2, 2, 20)
        lay_footer.addWidget(self.lbl_footer)

        # add 16px to compensate for the scrollbar that will always be visible
        width = self.mm_to_pixel(210) + 16
        self.editor.setFixedWidth(width)
        page = QPageSize(QPageSize.A4)
        page_size = page.sizePixels(QPageSize.A4, 96)
        self.editor.document().setPageSize(page_size)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.editor.document().setDefaultFont(QFont('Arial', 12, 400))
        self.editor.document().setDocumentMargin(float(self.mm_to_pixel(22)))

        font = QFont()
        font.setPointSize(12)
        self.editor.setFont(font)

        self.lay_v = QVBoxLayout(self)
        self.menuBar = QMenuBar(self)
        self.menuBar.setStyleSheet(style_qmenu_bar())
        self.create_menu_bar()
        self.create_toolbar()
        lay_h = QHBoxLayout()
        lay_h.setContentsMargins(0, 10, 0, 0)
        lay_h.addWidget(self.editor)

        self.lay_v.addLayout(lay_h)
        self.lay_v.addLayout(lay_footer)

        self.title = 'Editor 0.0.3'
        self.dialog_save = QDialog()
        self.dialog_preview = QDialog()
        self.path = ''
        self.alter = ''
        self.n_chr = ''
        self.evento = ''
        self.ba = None
        self.img_w = 0
        self.img_h = 0

        self.open_extern()

        self.editor.selectionChanged.connect(self.on_cursor_position_changed)
        self.editor.cursorPositionChanged.connect(self.set_footer)
        self.editor.textChanged.connect(self.editor_changed)
        self.editor.imageInserted.connect(self.insert_image)

    # #####################################
    # ####    OPEN FILE DOUBLE CLICK   ####
    # #####################################
    def open_extern(self):
        try:
            arg = sys.argv
            path = arg[1]
            with open(path, 'r') as f:
                text = f.read()
        except Exception as e:
            print(e)
        else:
            self.path = str(path).replace('\\', '/')
            self.n_chr = 'open'
            self.editor.setHtml(text)
            self.update_title()

    # ###############################
    # ####    CREATE MENU BAR    ####
    # ###############################

    def create_menu_bar(self):

        # file menu **
        self.file_menu = QMenu("Arquivo", self)
        self.file_menu.setStyleSheet(style_qmenu())
        self.menuBar.addMenu(self.file_menu)

        new_action = QAction('Novo', self)
        new_action.triggered.connect(self.fechar)
        self.file_menu.addAction(new_action)

        open_action = QAction('Abrir', self)
        open_action.triggered.connect(self.abrir)
        self.file_menu.addAction(open_action)

        save_action = QAction('Salvar', self)
        save_action.triggered.connect(self.file_save)
        self.file_menu.addAction(save_action)

        rename_action = QAction('Salvar como', self)
        rename_action.triggered.connect(self.file_saveas)
        self.file_menu.addAction(rename_action)

        self.file_menu.addSeparator()

        pdf_action = QAction("Gerar PDF", self)
        pdf_action.triggered.connect(self.save_pdf)
        self.file_menu.addAction(pdf_action)

        printer_action = QAction("Imprimir", self)
        printer_action.triggered.connect(self.page_printer)
        self.file_menu.addAction(printer_action)

        preview_action = QAction("Visualizar impressão", self)
        preview_action.triggered.connect(self.print_preview)
        self.file_menu.addAction(preview_action)

        self.file_menu.addSeparator()

        fechar_action = QAction('Fechar', self)
        fechar_action.triggered.connect(self.fechar)
        self.file_menu.addAction(fechar_action)

        # edit menu
        edit_menu = QMenu("Editar", self)
        edit_menu.setStyleSheet(style_qmenu())
        self.menuBar.addMenu(edit_menu)

        # font
        font_action = QAction('Font', self)
        font_action.triggered.connect(self.font_dialog)
        edit_menu.addAction(font_action)

        # color
        color_action = QAction("Cor da font", self)
        color_action.triggered.connect(self.show_color_dialog)
        edit_menu.addAction(color_action)

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

        # resize image
        resize_img_action = QAction('Redimensionar Imagem', self)
        resize_img_action.triggered.connect(self.img_size)
        edit_menu.addAction(resize_img_action)

        # table settings
        conf_tab_action = QAction('Configurar tabela', self)
        conf_tab_action.triggered.connect(self.config_tab)
        edit_menu.addAction(conf_tab_action)

        # insert menu **
        self.insert_menu = QMenu("Inserir", self)
        self.insert_menu.setStyleSheet(style_qmenu())
        self.menuBar.addMenu(self.insert_menu)

        # insert image
        insert_img_action = QAction('Inserir imagem', self)
        insert_img_action.triggered.connect(self.insert_image)
        self.insert_menu.addAction(insert_img_action)

        # insert link
        insert_link_action = QAction('Inserir link', self)
        insert_link_action.triggered.connect(self.insert_link)
        self.insert_menu.addAction(insert_link_action)

        # insert list bullet
        insert_list_action = QAction('Inserir lista', self)
        insert_list_action.triggered.connect(self.insert_list)
        self.insert_menu.addAction(insert_list_action)

        # insert list numerada
        insert_list_enum_action = QAction('Inserir lista numerada', self)
        insert_list_enum_action.triggered.connect(self.insert_list_num)
        self.insert_menu.addAction(insert_list_enum_action)

        # insert table
        insert_table_action = QAction('Inserir tabela', self)
        insert_table_action.triggered.connect(self.insert_table)
        self.insert_menu.addAction(insert_table_action)

        # window menu **
        window_menu = QMenu("Janela", self)
        window_menu.setStyleSheet(style_qmenu())
        self.menuBar.addMenu(window_menu)

        # minimize
        minscr_action = QAction('Minimizar', self)
        minscr_action.triggered.connect(self.show_minimized)
        window_menu.addAction(minscr_action)

        # maxmize
        maxscr_action = QAction('Maximizar', self)
        maxscr_action.triggered.connect(self.show_max_win)
        window_menu.addAction(maxscr_action)

        # fullscreen
        fullscr_action = QAction('Tela cheia', self)
        fullscr_action.triggered.connect(self.show_full_win)
        window_menu.addAction(fullscr_action)

        # normal screen
        normscr_action = QAction('Tela normal', self)
        normscr_action.triggered.connect(self.show_norm)
        window_menu.addAction(normscr_action)

        # About menu **
        about_menu = QMenu("Sobre", self)
        about_menu.setStyleSheet(style_qmenu())
        self.menuBar.addMenu(about_menu)

        # Help
        help_action = QAction('Ajuda', self)
        help_action.triggered.connect(self.abrir_help)
        about_menu.addAction(help_action)

        # App Settings
        config_action = QAction('Configurações', self)
        config_action.triggered.connect(self.open_config)
        about_menu.addAction(config_action)

        # About
        about_action = QAction('Sobre...', self)
        about_action.triggered.connect(DialogAbout)
        about_menu.addAction(about_action)

        self.lay_v.addWidget(self.menuBar)

    # ###############################
    # ####    CREATE TOOL BAR    ####
    # ###############################

    def create_toolbar(self):
        ToolBar = QToolBar("Tools", self)
        ToolBar.setContentsMargins(4, 0, 4, 0)
        ToolBar.setStyleSheet(style_tool_bar())

        # undo
        undo = Path(base_path, 'icons/undo.svg')
        undo_action = QAction(cor_icon(undo), 'Desfazer', self)
        undo_action.triggered.connect(self.editor.undo)
        ToolBar.addAction(undo_action)

        # redo
        redo = Path(base_path, 'icons/redo.svg')
        redo_action = QAction(cor_icon(redo), 'Refazer', self)
        redo_action.triggered.connect(self.editor.redo)
        ToolBar.addAction(redo_action)

        # separator
        ToolBar.addSeparator()

        # font color
        self.font_color.setToolTip('Cores')
        self.font_color.setFixedSize(QSize(18, 18))
        self.font_color.setStyleSheet(style_font_color('default'))
        self.font_color.clicked.connect(self.show_color_dialog)
        ToolBar.addWidget(self.font_color)

        # separator
        ToolBar.addSeparator()

        # font family
        fontDB = QFontDatabase()
        fontFamilies = fontDB.families()
        self.font_combo.setToolTip('Fonte')
        self.font_combo.addItems(fontFamilies)
        self.font_combo.activated.connect(self.set_font)
        self.font_combo.setStyleSheet(style_font_family())
        self.font_combo.setMaxVisibleItems(20)
        self.font_combo.setCurrentText('Arial')
        ToolBar.addWidget(self.font_combo)

        # separator
        ToolBar.addSeparator()

        # font size
        self.font_size.setToolTip('Tamanho')
        self.font_size.setValue(12)
        self.font_size.valueChanged.connect(self.set_font_size)
        self.font_size.setMinimumHeight(18)
        self.font_size.setStyleSheet(style_font_size())
        ToolBar.addWidget(self.font_size)

        ToolBar.addSeparator()

        # bold
        bold = Path(base_path, 'icons/bold.svg')
        bold_action = QAction(cor_icon(bold), 'Bold', self)
        bold_action.triggered.connect(self.bold_text)
        ToolBar.addAction(bold_action)

        # underline
        underline = Path(base_path, 'icons/underline.svg')
        underline_action = QAction(cor_icon(underline), 'Underline', self)
        underline_action.triggered.connect(self.underline_text)
        ToolBar.addAction(underline_action)

        # italic
        italic = Path(base_path, 'icons/italic.svg')
        italic_action = QAction(cor_icon(italic), 'Italic', self)
        italic_action.triggered.connect(self.italic_text)
        ToolBar.addAction(italic_action)

        # separator
        ToolBar.addSeparator()

        # alignment left
        left_align = Path(base_path, 'icons/left-align.svg')
        left_alignment_action = QAction(cor_icon(left_align), 'Esquerda', self)
        left_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        ToolBar.addAction(left_alignment_action)

        # alignment center
        center_align = Path(base_path, 'icons/center-align.svg')
        center_action = QAction(cor_icon(center_align), 'Centralizar', self)
        center_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        ToolBar.addAction(center_action)

        # alignment justify
        justify_align = Path(base_path, 'icons/justify-align.svg')
        justification_action = QAction(cor_icon(justify_align), 'Justificado', self)
        justification_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        ToolBar.addAction(justification_action)

        # alignment right
        right_align = Path(base_path, 'icons/right-align.svg')
        right_alignment_action = QAction(cor_icon(right_align), 'Direita', self)
        right_alignment_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        ToolBar.addAction(right_alignment_action)

        # separator
        ToolBar.addSeparator()

        # list
        list_bullet = Path(base_path, 'icons/list_bullet.svg')
        list_action = QAction(cor_icon(list_bullet), "Lista", self)
        list_action.triggered.connect(self.insert_list)
        ToolBar.addAction(list_action)

        # list enumerate
        list_enum = Path(base_path, 'icons/list_enum.svg')
        list_action = QAction(cor_icon(list_enum), "Lista numerada", self)
        list_action.triggered.connect(self.insert_list_num)
        ToolBar.addAction(list_action)

        # separator
        ToolBar.addSeparator()

        # insert image
        picture = Path(base_path, 'icons/picture.svg')
        image_action = QAction(cor_icon(picture), 'Imagem', self)
        image_action.triggered.connect(self.open_img)
        ToolBar.addAction(image_action)

        # insert link
        link_plus = Path(base_path, 'icons/link-plus.svg')
        link_action = QAction(cor_icon(link_plus), 'Link', self)
        link_action.triggered.connect(self.insert_link)
        ToolBar.addAction(link_action)

        # separator
        ToolBar.addSeparator()

        ToolBar.setIconSize(QSize(18, 18))
        ToolBar.setFixedHeight(36)

        self.lay_v.addWidget(ToolBar)

    # ###############################
    # ######  FONT  METHODS    ######
    # ###############################

    def show_color_dialog(self):
        cor = self.editor.textColor().name()
        color_dialog = QColorDialog()

        if cor != '#000000' and cor != '#ffffff':
            color = color_dialog.getColor(cor)
        else:
            color = color_dialog.getColor()

        if color.isValid():
            self.font_color.setStyleSheet("border: 0; background-color: %s" % color.name())
            self.editor.setTextColor(QColor(color.name()))

    def font_dialog(self):
        family = self.editor.fontFamily()
        if not family:
            family = 'Arial'
        font_init = QFont(family, int(self.editor.fontPointSize()))
        ok, font = QFontDialog().getFont(font_init)
        if font:
            self.editor.setCurrentFont(font)
            self.editor.setFontPointSize(font.pointSize())

    def set_font(self):
        font_family = self.font_combo.currentText()
        value = self.font_size.value()
        font = QFont(font_family, value)
        self.editor.setCurrentFont(font)

    def set_font_size(self):
        value = self.font_size.value()
        self.editor.setFontPointSize(value)

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

    # ###############################
    # ######   LISTs & TABLE   ######
    # ###############################

    def insert_list(self):
        cursor = self.editor.textCursor()
        cursor.createList(QTextListFormat.ListDisc)

    def insert_list_num(self):
        cursor = self.editor.textCursor()
        cursor.createList(QTextListFormat.ListDecimal)

    def insert_table(self):
        cursor = self.editor.textCursor()
        table_format = CustomTableFormat()
        table_format.setCellPadding(5)
        table_format.setCellSpacing(0)
        table_format.setBorderStyle(QTextFrameFormat.BorderStyle_Solid)

        set_tab = DialogTableConfig(None, None, None)

        if set_tab.resp:
            border = set_tab.border
            border_color = set_tab.border_color
            width = set_tab.width
            align = set_tab.align
            rows = set_tab.rows
            cols = set_tab.cols

            if width < 630:
                mrg = self.mm_to_pixel(20)
                table_format.setMargin(mrg)

            table_format.setBorder(border)
            table_format.setBorderBrush(border_color)
            table_format.setWidth(width)
            table_format.setAlignment(align)

            table_format.setBorderCollapse(True)
            cursor.insertTable(rows, cols, table_format)
            # self.editor.insertHtml('<br>')

    def config_tab(self):
        cursor = self.editor.textCursor()
        table = cursor.currentTable()
        if table is not None:
            table_format = table.format()
            border = int(table_format.border())
            border_color = table_format.borderBrush().color().name()

            set_tab = DialogTableConfig(border, border_color, True)

            if set_tab.resp:
                table_format.setBorderBrush(set_tab.border_color)
                table_format.setBorder(float(set_tab.border))
                table.setFormat(table_format)

        else:
            CustomDialog('Configurar tabela', 'Selecione primeiro a tabela que irá configurar.\n')

    # ###############################
    # ######  IMAGE  METHODS   ######
    # ###############################

    def insert_image(self, path):
        img = path
        document = self.editor.document()
        cursor = QTextCursor(document)
        pos = self.editor.textCursor().position()
        cursor.setPosition(pos)
        image = QPixmap(img)
        width = image.width()
        height = image.height()
        ba = QByteArray()
        buffer = QBuffer(ba)
        image.save(buffer, 'PNG', quality=95)
        binary = base64.b64encode(ba.data())
        tagImage = str("<img src= \"data:image/*;base64,{}\" " + f" width={width} height={height}></img>")
        HTMLBin = tagImage.format(str(binary, 'utf-8'))
        cursor.insertHtml(HTMLBin)

    def open_img(self):
        try:
            img, _ = QFileDialog.getOpenFileName(self, "Escolha uma imagem", "",
                                                 "Image Files(*.png *.gif *.jpg *jpeg *.svg)")
            self.insert_image(img)
        except Exception as e:
            print(e)

    def img_size(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
            if cursor.charFormat().isImageFormat():
                image_format = cursor.charFormat().toImageFormat()
                if image_format.isValid():
                    binary = image_format.name()
                    width = image_format.width()
                    height = image_format.height()
                    self.dialog_size(width, height, binary)
            else:
                CustomDialog('Redimensionar imagem',
                             'Redimensionar apenas imagem.\nPara texto, altere o tamanho da fonte.\n')
        else:
            CustomDialog('Redimensionar imagem', 'Selecione primeiro a imagem que irá redimensionar.\n')

    def dialog_size(self, w, h, binary):
        dlg = ResizeDialog(w, h)
        if dlg.res:
            self.ba = binary
            self.img_w = dlg.res[0]
            self.img_h = dlg.res[1]
            self.new_size_img()

    def new_size_img(self):
        width = self.img_w
        height = self.img_h
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            html = "<img src='{}' width={} height={}>".format(self.ba, width, height)
            cursor.insertHtml(html)

    # ###############################
    # ####      INSERT LINK      ####
    # ###############################

    def insert_link(self):
        if self.editor.textCursor().selectedText():
            nome = self.editor.textCursor().selectedText()
        else:
            nome = ''
        dg = DialogLink(nome)
        str_link = f'<a href="{dg.link_url}">{dg.link_nome}</a> '
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

    # ###############################
    # ####    FILE FUNCTIONS     ####
    # ###############################

    def fechar(self):
        if self.alter == '*' and self.editor.toPlainText() != '':
            self.dialog_save_open('fechar')
        else:
            self.new_file()

    def abrir(self):
        if self.alter == '*' and self.editor.toPlainText() != '':
            self.dialog_save_open('abrir')
        else:
            self.file_open()

    def new_file(self):
        self.editor.setHtml('')
        self.path = ''
        self.alter = ''
        self.update_title()

    def abrir_help(self):
        pass

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
                self.alter = ''
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
                self.alter = ''
                self.update_title()
        except Exception as e:
            print(e)

    # ###############################
    # ####    SAVE FUNCTIONS     ####
    # ###############################

    def closeEvent(self, event):
        if self.alter == '*':
            self.dialog_save_open(event)

    def dialog_save_close(self, event):
        print(event)
        if event.spontaneous():
            if type(self.evento).__name__ == 'QCloseEvent':
                self.evento.ignore()

    def dialog_save_open(self, ev):
        self.evento = ev
        self.dialog_save.setWindowTitle('Salvar')
        f_icon = str(Path(base_path, 'icons/save.svg'))
        self.dialog_save.setWindowIcon(cor_icon(f_icon))
        self.dialog_save.setMinimumSize(320, 90)
        lay_v = QVBoxLayout(self.dialog_save)
        nome = self.path
        if nome == '':
            nome = 'Documento sem nome'
        lbl1 = QLabel(nome)
        btn_yes = QPushButton('Salvar')
        btn_yes.clicked.connect(self.yes_save)
        btn_no = QPushButton('Não salvar')
        btn_no.clicked.connect(self.no_save)
        btn_cancel = QPushButton('Cancelar')
        btn_cancel.clicked.connect(self.cancel_save)
        lay_h = QHBoxLayout()
        lay_h.addWidget(btn_cancel)
        lay_h.addWidget(btn_no)
        lay_h.addWidget(btn_yes)
        lay_v.addWidget(lbl1)
        lay_v.addLayout(lay_h)
        self.dialog_save.exec()
        self.dialog_save.finished.connect(lambda: self.dialog_save.setAttribute(Qt.WA_DeleteOnClose))
        self.dialog_save.closeEvent = self.dialog_save_close

    def cancel_save(self):
        if type(self.evento).__name__ == 'QCloseEvent':
            self.evento.ignore()
        self.dialog_save.close()

    def no_save(self):
        if type(self.evento).__name__ == 'QCloseEvent':
            self.dialog_save.close()
        if self.evento == 'fechar':
            self.dialog_save.close()
            self.new_file()
        if self.evento == 'abrir':
            self.dialog_save.close()
            self.file_open()

    def yes_save(self):
        self.file_save()
        self.alter = ''
        self.update_title()
        if self.evento == 'fechar':
            self.new_file()
        if self.evento == 'abrir':
            self.file_open()
        self.dialog_save.close()

    # ###############################
    # ####   PRINTER FUNCTIONS   ####
    # ###############################

    def print_preview(self):
        self.print_page('')
        dialog = QDialog()
        dialog.setWindowTitle('Visualizar impressão')
        f_icon = str(Path(base_path, 'icons/printing.svg'))
        dialog.setWindowIcon(cor_icon(f_icon))
        dialog.setFixedSize(500, 400)
        lay_v = QVBoxLayout(dialog)
        # Create a new PDF document
        pdf_doc = QPdfDocument()
        # Load the PDF file
        file = QFile("output.pdf")
        file.open(QIODevice.ReadOnly)
        pdf_doc.load(file)
        # Create a new PDF view and set the document
        pdf_view = QPdfView()
        pdf_view.setDocument(pdf_doc)
        pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        pdf_view.setZoomFactor(0.5)
        lay_v.addWidget(pdf_view)
        file.close()
        dialog.finished.connect(self.dialog_preview_close)
        dialog.exec()

    def dialog_preview_close(self):
        os.remove("output.pdf")

    def print_page(self, f_name):
        if f_name == '':
            f_name = "output.pdf"
        printer = QPrinter()
        printer.setResolution(96)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPageMargins(QMargins(0, 0, 0, 0), QPageLayout.Millimeter)
        printer.setOutputFileName(f_name)
        text = self.editor.document()
        text.print_(printer)

    def page_printer(self):
        printer = QPrinter()
        printer.setResolution(96)
        printer.setPageMargins(QMargins(0, 0, 0, 0), QPageLayout.Millimeter)
        document = self.editor.document()
        dlg = QPrintDialog(printer)
        if dlg.exec():
            document.print_(printer)

    def save_pdf(self):
        if self.editor.toPlainText() != '':  # if name not empty
            f_name, _ = QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF files (*.pdf)")
            if f_name[-4:] != '.pdf':
                f_name = f_name + '.pdf'
            self.print_page(f_name)
            webbrowser.open(f_name)

    # ###############################
    # ####     CHANGE EDITOR     ####
    # ###############################

    def editor_changed(self):
        if self.editor.toPlainText() == '':
            self.alter = ''
            self.path = ''
            self.update_title()
        if self.n_chr != 'open' and self.editor.toPlainText() != '':
            self.alter = '*'
            self.update_title()
        if self.n_chr == 'open':
            self.n_chr = ''
            self.alter = ''
        self.set_footer()

    def on_cursor_position_changed(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            txt = cursor.selectedText()
            if txt.isascii():
                family = self.editor.fontFamily()
                size = self.editor.fontPointSize()
                color = self.editor.textColor().name()
                self.font_combo.setCurrentText(family)
                self.font_color.setStyleSheet(style_font_color(color))
                self.font_size.setValue(int(size))

    def set_footer(self):
        chrs = len(self.editor.toPlainText())
        cursor = self.editor.textCursor()
        row = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.lbl_footer.setText(f'{chrs} caracteres           posição:  linha {row} coluna {col}')

    # ###############################
    # ####     TITLE UPDATE      ####
    # ###############################

    def update_title(self):
        if self.path != '':
            part = self.path.split('/')
            n = len(part)
            title = str(self.title + ' - ' + part[n - 1] + self.alter)
            self.edit_title.emit(title)
        else:
            title = str(self.title + ' ' + self.alter)
            self.edit_title.emit(title)

    def mm_to_pixel(self, mm):
        px = mm / (25.4 / 96)
        return int(px)

    # ###############################
    # ####     CONFIG WINDOW     ####
    # ###############################

    def show_min_win(self):
        self.show_minimized.emit()

    def show_max_win(self):
        self.show_maximized.emit()

    def show_full_win(self):
        self.show_full_screen.emit()

    def show_norm(self):
        self.show_normal.emit()

    def open_config(self):
        self.get_config.emit('conf')
