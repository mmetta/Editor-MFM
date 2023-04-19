<p align="center"><img src="https://github.com/mmetta/Editor-MFM/blob/main/icons/mfm_logo.png"/></p>
<h1 align="center"> Editor-MFM </h1>

 É um editor de texto desenvolvido em <b>Python 3</b>, compacto porém com muitos recursos para gerar textos formatados, com imagens e links. Pode ser salvo em PDF, HTML, sem extensão ou com uma extensão criada por você, neste caso usei *.mfm, as iniciais do meu nome.
 
 A ideia do projeto é disponibilizar um editor leve e fácil de usar para gerar documentos complexos e bonitos adicionando ao texto os recursos personalizáveis do HTML.

 <b>O projeto conta com diversos recursos do PySide6:</b><br/>

 QTextEdit<br/>
 QMenuBar<br/>
 QMenu<br/>
 QToolBar<br/>
 QAction<br/>
 QPaint<br/>
 QImage<br/>
 QPixmap<br/>
 QDialog<br/>
 QPrinter<br/>
 QPrintDialog<br/>
 QPrintPreviewDialog<br/>
 QProcess<br/>

 Essa grande quantidade de elementos pretende servir de exemplo de suas implementações e permitir configurações pessoais como a de esquema de cores e tema Dark ou Light.<br/>
 
 Reinicializa o editor para aplicação das configurações escolhidas pelo usuário.<br/>
 
 A <b>versão 0.0.3</b> traz correções e melhorias importantes além de implementar funcionalidades que faltavam.
 Vou listar abaixo as principais:
 
 <li>Correção do QColorDialog() que estava em conflito com a paleta de cores do dark theme;</li>
 <li>Troca do tema dark de darkstyle para qdarktheme do Pyqtdarktheme;</li>
 <li>Ajusta das cores secundárias para igualar a paleta do qdarktheme;</li>
 <li>Implementa lista comum (bullet) e lista numerada;</li>
 <li>Implementa QFontDialog() para customização de fontes do texto. Importa todas as fontes disponíveis no sistema do usuário;</li>
 <li>Implementa QTextTableFormat() para inserir e formatar tabelas no editor;</li>
 <li>Nova estratégia de impressão e geração de PDF com QPrinter();</li>
 <li>Novo print preview customizado, usando QpdfView() para uma visão real do arquivo que será impresso. O arquivo gerado para o viewer é removido aasim que o dialog é fechado;</li>
 <li>Ajustes de tamano de folha e margens para uma impressão fiel ao que está na tela;</li>

<p align="right"><b>MFMetta - abr/2023</b></p>

![Badge](https://img.shields.io/badge/Python-3.11.1-blue)
![Badge](https://img.shields.io/badge/PySide6-6.4.2-orange)
![Badge](https://img.shields.io/github/issues/mmetta/Editor-MFM)
<br/>
![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)
