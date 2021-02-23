template = """
\\documentclass[
    12pt,
    a4paper,
    oneside,
%   unicode,
]{article}

\\usepackage[utf8]{inputenc}

\\usepackage[
    margin=20mm,
]{geometry}

% Color support
\\usepackage{xcolor}

% Do not indent paragraphs
\\setlength{\\parindent}{0pt}

% Allow hyperlinks
\\usepackage{hyperref}

% Set font family to sans serif
\\renewcommand{\\familydefault}{\\sfdefault}

% Set default colors
((colors))

% Set PDF colors
\\usepackage[pagecolor={bg}]{pagecolor}
\\color{fg}

% Configure code blocks
\\usepackage[formats]{listings}
\\lstset{
    language=tex,
    basicstyle=\\ttfamily\\small\\color{fg},
% general settings
    captionpos=b,
    tabsize=4,
    inputencoding=utf8,
    columns=fixed,
    fontadjust=true,
% line numbers
    numbers=left,
    numbersep=1em,
    numberstyle=\\tiny\\color{keyword},
    frame=leftline,
%
    morekeywords = {acro, emph, texttt, textbf, textit, enquote, cite, ref, section, subsection, chapter, begin, end, textins},
% colors
    backgroundcolor=\\color{bg},
    commentstyle=\\color{comment},
    keywordstyle=\\color{keyword},
    rulecolor=\\color{keyword},
    stringstyle=\\color{comment},
% wrapping
    linewidth=\\textwidth,
    breaklines=true,
    breakatwhitespace=true,
    breakautoindent=true,
% character support
    extendedchars=true,
        literate=
        % acute
        {á}{{\\'a}}1   {é}{{\\'e}}1   {í}{{\\'i}}1   {ó}{{\\'o}}1   {ú}{{\\'u}}1   {ý}{{\\'y}}1
        {Á}{{\\'A}}1   {É}{{\\'E}}1   {Í}{{\\'I}}1   {Ó}{{\\'O}}1   {Ú}{{\\'U}}1   {Ý}{{\\'Y}}1
        % grave
        {à}{{\\`a}}1   {è}{{\\`e}}1   {ì}{{\\`i}}1   {ò}{{\\`o}}1   {ù}{{\\`u}}1   {ỳ}{{\\`x}}1
        {À}{{\\`A}}1   {È}{{\\'E}}1   {Ì}{{\\`I}}1   {Ò}{{\\`O}}1   {Ù}{{\\`U}}1   {Ỳ}{{\\`Y}}1
        % diaeresis
        {ä}{{\\"a}}1   {ë}{{\\"e}}1   {ï}{{\\"i}}1   {ö}{{\\"o}}1   {ü}{{\\"u}}1   {ÿ}{{\\"y}}1
        {Ä}{{\\"A}}1   {Ë}{{\\"E}}1   {Ï}{{\\"I}}1   {Ö}{{\\"O}}1   {Ü}{{\\"U}}1   {Ÿ}{{\\"Y}}1
        % circumflex
        {â}{{\\^a}}1   {ê}{{\\^e}}1   {î}{{\\^i}}1   {ô}{{\\^o}}1   {û}{{\\^u}}1   {ŷ}{{\\^y}}1
        {Â}{{\\^A}}1   {Ê}{{\\^E}}1   {Î}{{\\^I}}1   {Ô}{{\\^O}}1   {Û}{{\\^U}}1   {Ŷ}{{\\^Y}}1
        % caron
        {ǎ}{{\\v{a}}}1 {ě}{{\\v{e}}}1 {ǐ}{{\\v{i}}}1 {ǒ}{{\\v{o}}}1 {ǔ}{{\\v{u}}}1 {y̌}{{\\v{y}}}1
        {Ǎ}{{\\v{A}}}1 {Ě}{{\\v{E}}}1 {Ǐ}{{\\v{I}}}1 {Ǒ}{{\\v{O}}}1 {Ǔ}{{\\v{U}}}1 {Y̌}{{\\v{Y}}}1
        {č}{{\\v{c}}}1 {Č}{{\\v{C}}}1
        {ď}{{\\v{d}}}1 {Ď}{{\\v{D}}}1
        {ň}{{\\v{n}}}1 {Ň}{{\\v{N}}}1
        {ř}{{\\v{r}}}1 {Ř}{{\\v{R}}}1
        {š}{{\\v{s}}}1 {Š}{{\\v{S}}}1
        {ť}{{\\v{t}}}1 {Ť}{{\\v{T}}}1
        {ž}{{\\v{z}}}1 {Ž}{{\\v{Z}}}1
        % macron
        {ã}{{\\~a}}1   {ē}{{\\~e}}1   {ī}{{\\~i}}1   {õ}{{\\~o}}1   {ū}{{\\~u}}1   {ȳ}{{\\~y}}1
        {Ã}{{\\~A}}1   {Ē}{{\\~E}}1   {Ī}{{\\~I}}1   {Õ}{{\\~O}}1   {Ū}{{\\~U}}1   {Ȳ}{{\\~Y}}1
        % double acute
        {a̋}{{\\H{a}}}1 {e̋}{{\\H{e}}}1 {i̋}{{\\H{i}}}1 {ő}{{\\H{o}}}1 {ű}{{\\H{u}}}1 {ӳ}{{\\H{y}}}1
        {A̋}{{\\H{A}}}1 {E̋}{{\\H{E}}}1 {I̋}{{\\H{I}}}1 {Ő}{{\\H{O}}}1 {Ű}{{\\H{U}}}1 {Ӳ}{{\\H{Y}}}1
        % overring
        {å}{{\\r{a}}}1 {e̊}{{\\r{e}}}1 {i̊}{{\\r{i}}}1 {o̊}{{\\r{o}}}1 {ů}{{\\r{u}}}1 {ẙ}{{\\r{y}}}1
        {Å}{{\\r{A}}}1 {E̊}{{\\r{E}}}1 {I̊}{{\\r{I}}}1 {O̊}{{\\r{O}}}1 {Ů}{{\\r{U}}}1 {Y̊}{{\\r{Y}}}1
        % other letter modifications
        {ç}{{\\c c}}1 {Ç}{{\\c C}}1 {ø}{{\\o}}1
        % joined letters
        {œ}{{\\oe}}1 {Œ}{{\\OE}}1 {æ}{{\\ae}}1 {Æ}{{\\AE}}1 {ß}{{\\ss}}1
        % destructive: quotes
        {“}{"}1
        {„}{"}1
        {‘}{'}1
        {’}{'}1
        {»}{"}1
        {«}{"}1
        {›}{'}1
        {‹}{'}1
        % destructive: some formatting characters
        {…}{...}3
        {←}{<-}2
        {→}{->}2
        {↔}{<->}3
        {–}{--}2
        {‒}{--}2
        {—}{--}2
        {―}{--}2
}
"""


class Schemes:
    def __init__(self):
        self.dark = """
        \\definecolor{bg}{HTML}{111111} % black
        \\definecolor{fg}{HTML}{FFFFFF} % white
        \\definecolor{comment}{HTML}{97C681} % green
        \\definecolor{keyword}{HTML}{DEC3E2} % red
        """

        self.light = """
        \\definecolor{bg}{HTML}{FFFFFF} % White
        \\definecolor{fg}{HTML}{111111} % Black
        \\definecolor{comment}{HTML}{2BAF4F} % Green
        \\definecolor{keyword}{HTML}{AD54AD} % Purple
        """

        self.mariana = """
        \\definecolor{bg}{HTML}{343D46} % Grey blue
        \\definecolor{fg}{HTML}{FDFFFD} % White-ish
        \\definecolor{comment}{HTML}{A6ACB7} % Grey
        \\definecolor{keyword}{HTML}{C695C6} % Purple
        """

        self.marianne = """
        \\definecolor{bg}{HTML}{242D36} % Grey blue
        \\definecolor{fg}{HTML}{FDFFFD} % White-ish
        \\definecolor{comment}{HTML}{a2abbc} % Grey
        \\definecolor{keyword}{HTML}{d88fd8} % Purple
        """

        self.plain = """
        \\definecolor{bg}{HTML}{FFFFFF} % White
        \\definecolor{fg}{HTML}{111111} % Black
        \\definecolor{comment}{HTML}{111111} % Black
        \\definecolor{keyword}{HTML}{111111} % Black
        """

    def get(self, scheme: str):
        return getattr(self, scheme, None)


def get(scheme: str):
    colors = Schemes().get(scheme)
    if colors is None:
        raise ValueError

    return template.replace("((colors))", colors)
