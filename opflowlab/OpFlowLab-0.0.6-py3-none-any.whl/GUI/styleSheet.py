invalid_stylesheet = "background-color: rgb(255, 216, 216);"
valid_stylesheet = "background-color: rgb(255, 255, 255);"
stop_button_stylesheet = "background-color: #BF2B56;"
start_button_stylesheet = "background-color: #20639B;"
qss = """
QWidget:window {					/* Borders around the code editor and debug window */
	background-color: #DDDDDD;
}

/* === QTabBar === */
QTabBar {
	background: white;
	font-weight: bold;
}

QTabWidget::pane {
	background: transparent;
	border: 0px solid transparent;
    border-radius: 7px;
}

QTabBar::tab {
	background: transparent;
	border: 0px solid transparent;
	border-bottom: 3px solid transparent;
	color: #20639B;
	padding: 10px 15px;
}

QTabBar::tab:hover {
	background-color: white;
	border: 0px solid transparent;
	border-bottom: 1px solid #20639B;
	color: #20639B;
}

QTabBar::tab:!selected { font-weight: normal; }

QTabBar::tab:selected {
	background-color: #E8F0FF;
	border: 0px solid transparent;
	border-top: none;
	border-bottom: 3px solid #20639B;
	color: #20639B;
	font-weight: bold;
}

QStackedWidget {
	background: #FFFFFF;
	border-radius: 7px;
	margin: 7px;
}

/* === QGroupBox === */
QGroupBox {
    border: 1px solid #20639B;
    margin-top: 1em;
    border-radius: 5px;
}

QGroupBox::title {
	color: #20639B;
    subcontrol-origin: top left;
    left: 12px;
    top: -7px;
}

QComboBox {
	color: #000000;
	outline: 0;
}

QComboBox QAbstractItemView
{
	outline: 1;
	outline-color: gray;
}

/* === QCheckBox === */
QCheckBox, QRadioButton {
	color: #000000;
	padding: 5px;
}

/* === QScrollBar:horizontal === */
QScrollBar:horizontal {
	background: #DDDDDD;				/* Background where slider is not */
	height: 10px;
	margin: 0;
}

QScrollBar:vertical {
	background: #DDDDDD;				/* Background where slider is not */
	width: 10px;
	margin: 0;
}

QScrollBar::handle:horizontal {
    background: #20639B;					/* Slider color */
    min-width: 16px;
	border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #20639B;					/* Slider color */
    min-height: 16px;
	border-radius: 5px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background: none;												/* Removes the dotted background */
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {	/* Hides the slider arrows */
      border: none;
      background: none;
}

QPushButton {
	background-color: #20639B;
	color: #FFFFFF;
	border: 0px solid transparent;
	padding: 10px;
	border-radius: 7px;
	font: bold;
}

QPushButton:hover {
    background-color: #3073AB;
}

QPushButton:pressed {
    background-color: #5093CB;
}

QPushButton:disabled{
    background-color: #DDDDDD;
    color: #888888;
}

QLineEdit {
	background: transparent;
	border: 0px solid transparent;
	border-top: none;
	border-bottom: 1px solid #20639B;
	padding: 5px;
}

QLineEdit:disabled {
    background: #DDDDDD;
}

QLabel {
    padding: 5px 0;
    color: #000000;		/* Text at the bottom right corner of the screen */
}

QTextBrowser {
    margin: 0 7px 10px 7px;
    border: 7px solid white;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
}

QProgressBar {
    text-align: right;
    margin-right: 12ex;
    margin-top: 3px;
    background-color: #DDDDDD;
    height: 20px;
    border-radius: 5px;
}

QProgressBar::chunk {
    background-color: #20639B;
    border: 1px solid transparent;
    border-radius: 5px;
}

QComboBox {
    background: white;
	border: 1px solid transparent;
	border-top: none;
	border-bottom: 1px solid #20639B;
	padding: 5px;
}

QComboBox QAbstractItemView {
    border: 1px solid lightgray;
    selection-background-color: #80C3FB;
    selection-color: black;
    outline: 1px;
}

QComboBox QAbstractItemView::item {
    padding: 5px;
}

/* === QToolButton === */
QToolButton:hover, QToolButton:pressed {
	background-color: transparent;
}

QToolButton::menu-button:hover, QToolButton::menu-button:pressed {
	background-color: #263238;
}

QStatusBar {
	background-color: #263238;
}

QToolButton {	/* I don't like how the items depress */
	color: #546E7A;
}

QToolButton:hover, QToolButton:pressed, QToolButton:checked {
	background-color: #263238;
}

QToolButton:hover {
	color: #AFBDC4;

}

QToolButton:checked, QToolButton:pressed {
	color: #FFFFFF;
}

QToolButton {
	border: 1px solid transparent;
	margin: 1px;
}

QToolButton:hover {
	background-color: transparent;				/* I don't like how the down arrows in the top menu bar move down when clicked */
	border: 1px solid transparent;
}

QToolButton[popupMode="1"] { /* only for MenuButtonPopup */
	padding-right: 20px; /* make way for the popup button */
}

QToolButton::menu-button {
	border-left: 1px solid transparent;
	background: transparent;
    width: 16px;
}

QToolButton::menu-button:hover {
	border-left: 1px solid transparent;
	background: transparent;
    width: 16px;
}

/* Play around with these settings */
/* Force the dialog's buttons to follow the Windows guidelines. */
QDialogButtonBox {
    button-layout: 0;
}

QTabWidget::tab-bar {
	left: 0px; /* Test this out on OS X, it will affect the tabs in the Options Dialog, on OS X they are centered */
}
"""