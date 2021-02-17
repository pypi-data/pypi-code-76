#!/usr/bin/env python3


__all__ = ["PyFileReader"]


import ast
import copy
import io
import itertools
import logging
import sys

import raisin
from ..tools import improve_recursion_decorateur, identity


def _jump(chaine, start_rank):
    """
    'chaine' est une ligne de code ou un bout de ligne de code (STR)
    'start_rank' est le rang a partir d'ou l'analise commence
    retourne le rang du dernier caractere qui fait parti du groupe
    en cas de paquet posiblement incomplet, retourne -1
    ex:
    >>>_jump("les (orties sont belles) et verte", 4)
    24
    >>>chaine[4:24]
    '(orties sont belles et vertes)'
    >>>_jump("les (orties sont belles) et verte", 5)
    23
    >>>chaine[5:23]
    'orties sont belles'
    """
    def count_backslash(chaine):
        """
        retourne le nombre de \\ concecutif present
        a la fin de 'chaine'
        """
        nbr = 0
        for i in range(len(chaine)):
            if chaine[-1-i] != "\\":
                return nbr
            nbr += 1
        return nbr

    parentheses = 0                                                     # nombre de parentheses ouvertes
    crochets = 0                                                        # nombre de crochets ouverts
    accolades = 0                                                       # nombre d'accolades ouvertes
    guillemets = [0, 0, 0, 0]                                           # c'est tous les types de guillemets [''', ', """, "]

    var_re = r"(?:[a-zA-Z_\x7f-\U000fffff][a-zA-Z0-9_\x7f-\U000fffff]*)"# model regex d'une variable python

    # verif
    if start_rank < 0:
        raise ValueError("the start rank must to be >= 0")
    if start_rank >= len(chaine):
        raise ValueError("the start rank must to be < len(chaine)")


    chaine = chaine[start_rank:]                                        # on se place au debut

    # cas (...), [...], {...}, "...", '...', """...""", '''...'''
    if chaine[0] in ("'", '"', "(", "[", "{"):                      # dans le cas ou l'on est sur le debut d'un paquet on ne peu plus clair
        ref_ouvrante = chaine[0]
        if ref_ouvrante == "'":
            if chaine[:3] == "'''":
                ref_ouvrante = "'''"
        elif ref_ouvrante =='"':
            if chaine[:3] == '"""':
                ref_ouvrante = '"""'

        i_veritable = len(ref_ouvrante) - 1                         # on se place bien pour le debut de l'analyse
        while i_veritable+1 < len(chaine):                          # on va analyser chaque caractere
            i_veritable += 1                                        # c'est le rang a partir du tout debut de la chaine
            if (ref_ouvrante in ("'", '"', "'''", '"""')) and \
               (chaine[i_veritable:i_veritable + len(ref_ouvrante)] != ref_ouvrante):# si on est pas au bout
                continue
            elif (ref_ouvrante in ("'", '"', "'''", '"""')) and \
                 (chaine[i_veritable:i_veritable + len(ref_ouvrante)] == ref_ouvrante) and \
                 (count_backslash(chaine[:i_veritable]) % 2 == 0):
                return i_veritable + len(ref_ouvrante) + start_rank
            elif (ref_ouvrante in ("(", "[", "{")) and (chaine[i_veritable] in "([{'\""):#si on rentre dans un autre bloc
                i_veritable = _jump(chaine, i_veritable)-1
                continue
            elif (ref_ouvrante in ("(", "[", "{")) and \
                 (chaine[i_veritable] == {"(":")", "[":"]", "{":"}"}.get(ref_ouvrante, "")):
                return i_veritable + 1 + start_rank
        return -1

    # cas de caractere inimprimable, si on est
    if chaine[0] in " \t\n\r\f\v":                                  # si ca semble bien parti
        for i_veritable in range(1, len(chaine)):                   # pour tous les caractere suivants
            if not(chaine[i_veritable] in " \t\n\r\f\v"):           # si le caractere en cours n'est pas un espace
                return i_veritable + start_rank                     # alors le dernier en etait un
        return -1                                                   # si il y a que des espaces, on ne peu pas dire avoir trouver la fin de la chaine

    # cas d'un mot clef ou d'un nom de variable
    recherche = raisin.re.match(var_re, chaine)                     # si c'est une variable simple, ne contenant pas de "." au milieu
    if recherche:                                                   # alors on donne tout le travail a regex
        i_veritable = recherche.end()                               # possible et nous retourne la position du dernier caractere qui coincide
        return i_veritable + start_rank                             # puis on retourne la nouvelle position

    # cas des nombres
    model = raisin.re.compile(r"""
        (?: #     binary                octal                   hexadecimal
            0 (?: b [01]+ (?:_[01]+)* | o [0-7]+ (?:_[0-7]+)* | x [0-9a-f]+ (?:_[0-9a-f]+)* )
          | # decimal
            \. [0-9]+ (?:_[0-9]+)*
            (?: e [+-]? [0-9]+ (?:_[0-9]+)* )?
          |
            [0-9]+ (?:_[0-9]+)* \.? (?: [0-9]+ (?:_[0-9]+)* )?
            (?: e [+-]? [0-9]+ (?:_[0-9]+)* )?
        )j?""", raisin.re.VERBOSE | raisin.re.IGNORECASE)
    recherche = raisin.re.match(model, chaine)
    if recherche:
        i_veritable = recherche.end()                               # on l'extrait
        return i_veritable + start_rank                             # puis on le retourne aussi-tot

    #cas + - * ** / // % & | ^ < << > >> @ = += -= *= **= /= //= %= &= |= ^= <= <<= >= >>= @= == , != : ~ .
    model = r"(?:(?:\+|-|\*{1,2}|/{1,2}|%|&|\||\^|<{1,2}|>{1,2}|@|=)=?)|,|!=|:|~|\."
    recherche = raisin.re.match(model, chaine)
    if recherche:
        i_veritable = recherche.end()
        return i_veritable + start_rank

    raise SyntaxError("The position of depature is not correct:\nchaine: %s.\n" % chaine.__repr__())

def _get_l_jump(chaine, simplify=True):
    """
    decompose la chaine en plusieurs entitees qui sont retournees dans une liste l
    ainsi, " ".join(l) == chaine (a peu pres, aux espaces pres...)
    """
    def all_permutations(iterable):
        """
        cede tout les agencement possible de l'iterable
        """
        iterable_liste = []
        for element in iterable:
            iterable_liste.append(element)
            yield (element,)
        for i in range(2, len(iterable) + 1):
            for combination in itertools.combinations(iterable, i):
                yield from itertools.permutations(combination)

    def index_list(liste, elements, debut):
        rangs = []
        for element in elements:
            try:
                rangs.append(liste.index(element, debut))
            except ValueError:
                pass
        if rangs:
            return min(rangs)
        raise ValueError

    d_brute = []
    start_rank = 0
    while 1:
        suivant = _jump(chaine, start_rank)
        if suivant == -1:
            d_brute.append(chaine[start_rank:])
            break
        d_brute.append(chaine[start_rank:suivant])
        if suivant == len(chaine):
            break
        start_rank = suivant
    if not simplify:
        return d_brute
        
    d_simplify = [e for e in d_brute if not raisin.re.fullmatch(r"\s*", e)] # suppression des caracteres inimprimables
    
    i = 1                                                               # on raboute la signature des fonction avec leur identifiant
    while i < len(d_simplify):                                          # pour cela on parcours chaque element de la d_simplify
        if (d_simplify[i] == "not") and (d_simplify[i-1] == "is"):
            d_simplify = d_simplify[:i-1] + ["is not"] + d_simplify[i+1:]
            continue
        if (d_simplify[i] == "def") and (d_simplify[i-1] == "async"):
            d_simplify = d_simplify[:i-1] + ["async def"] + d_simplify[i+1:]
            continue
        if (d_simplify[i] == "for") and (d_simplify[i-1] == "async"):
            d_simplify = d_simplify[:i-1] + ["async for"] + d_simplify[i+1:]
            continue
        if (d_simplify[i] == "with") and (d_simplify[i-1] == "async"):
            d_simplify = d_simplify[:i-1] + ["async with"] + d_simplify[i+1:]
            continue
        if (d_simplify[i] == "from") and (d_simplify[i-1] == "yield"):
            d_simplify = d_simplify[:i-1] + ["yield from"] + d_simplify[i+1:]
            continue
        if (d_simplify[i-1] == "not") and (d_simplify[i] == "in"):
            d_simplify = d_simplify[:i-1] + ["not in"] + d_simplify[i+1:]
            continue
        if "f" in d_simplify[i-1].lower() and d_simplify[i-1].lower() != "f":
            if tuple(d_simplify[i-1].lower()) in all_permutations("bruf"):# si c'est une chaine formatee
                if raisin.re.search(r"^(?:(?:\".*\")|(?:\'.*\')).*$", d_simplify[i]):# qui est donc obligatoirement suivie d'une chaine de caractere
                    d_simplify[i-1] = d_simplify[i-1].lower().replace("f", "")# on separe alors le f du reste
                    d_simplify.insert(i-1, "f")                         # en le faisant sortir devant
                    continue                                            # puis on passe a la suite
        if "b" in d_simplify[i-1].lower() or "r" in d_simplify[i-1].lower() or "u" in d_simplify[i-1].lower():
            if tuple(d_simplify[i-1].lower()) in all_permutations("bruf"):# si on tombe sur un "r", un "b", un "u", un "f" ou une combinaison de tous ca
                if raisin.re.search(r"^(?:(?:\".*\")|(?:\'.*\')).*$", d_simplify[i]):# qui est suivit d'une chaine de caractere
                    d_simplify = d_simplify[:i-1] + [d_simplify[i-1] + d_simplify[i]] + d_simplify[i+1:]# alors on les raboute
                    i = 1                                               # pour faire fonctionner le test suivant dans par example: b'truc' b'machin'
                    continue
        if raisin.re.search(r"^((r)|(b)|(u)|(br)|(rb))?[\'\"]", d_simplify[i-1].lower()) \
           and raisin.re.search(r"^((r)|(b)|(u)|(br)|(rb))?[\'\"]", d_simplify[i].lower()):# si deux chaine se suivent
            d_simplify[i-1] = repr(eval(d_simplify[i-1]) + eval(d_simplify[i]))
            del d_simplify[i]                                           # il s'agit en fait d'un concatenation de chaine
            continue
        if raisin.re.search(r"^((r)|(b)|(u)|(br)|(rb))?[\'\"]", d_simplify[i-1].lower()) \
           and d_simplify[i].lower() == "f":                            # si il y a un + implicite entre 2 chaines
            d_simplify.insert(i, "+")                                   # on l'ajoute
            continue
        i+=1

    i = 2
    while i < len(d_simplify):
        if (d_simplify[i-1] == "<") and (d_simplify[i] == ">"):
            del d_simplify[i-1]
            d_simplify[i-1] = "!="
            continue
        if d_simplify[i-2:i+1] == ["."]*3:
            del d_simplify[i-2]
            del d_simplify[i-2]
            d_simplify[i-2] = "Ellipsis"
            continue
        i+=1

    while "lambda" in d_simplify:                                       # la fonction lambda va etre colle en un seul bloc
        rang_lambda = d_simplify.index("lambda")                        # car elle peut comporter des virgules qui peuvent preter a confusion
        rang_deux_points = rang_lambda                                  # rang ou se trouvent le ':'
        to_jump = 0                                                     # nombre de : a sauter
        while 1:                                                        # on va parcourir pour aller explorer les caracteres suivants
            rang_deux_points += 1                                       # on passe au caractere suivant
            if rang_deux_points >= len(d_simplify):                     # si on s'aprete a faire un indexe out of range
                raise SyntaxError("Un lambda doit comporter un ':', ici il n'y en a pas.")
            if d_simplify[rang_deux_points] == "lambda":                # si un lambda est imbrique dans un lambda
                to_jump += 1                                            # alors on va voir la suite
            elif d_simplify[rang_deux_points] == ":":                   # si c'est veritablement un ":"
                to_jump -= 1                                            # alors on decremente le compteur
                if to_jump < 0:                                         # si on est arrive sur les ':' qui nous interresses
                    break                                               # alors on s'arrete la
        try:
            rang_fin_lambda = index_list(d_simplify, [",", ":"], rang_deux_points + 1)
            d_simplify = d_simplify[:rang_lambda] + [" ".join(d_simplify[rang_lambda:rang_fin_lambda])] \
                       + d_simplify[rang_fin_lambda:]                   # puis on en fait qu'un seul bloc
        except ValueError:
            d_simplify = d_simplify[:rang_lambda] + [" ".join(d_simplify[rang_lambda:])]

    return d_simplify.copy()

class ExtendNode:
    """
    permet une surcharge factorise
    de chacun des noeud de l'arbre syntaxique
    """
    def overload(self, ast_node):
        """
        retourne le meme noeud ayant subit une extension de class
        """
        if type(ast_node) in self.grammar:
            raisin_node = self.grammar[type(ast_node)](ast_node)
            raisin_node.grammar = self.grammar
            raisin_node.priorites = self.priorites
            raisin_node.signature = self.signature
            raisin_node.father = self # cela permet de remonter l'arbre
            return raisin_node
        elif type(ast_node) is ast.Num:
            return ast_node.n
        elif type(ast_node) is ast.NameConstant:
            return ast_node.value
        elif type(ast_node) is ast.Str:
            return repr(ast_node.s)
        elif type(ast_node) is ast.Bytes:
            return repr(ast_node.s)
        elif type(ast_node) is ast.Ellipsis:
            class RaisinEllipsis:
                def __init__(self):
                    self.value = Ellipsis
                def __str__(self):
                    return "..."
            return RaisinEllipsis()
        raise TypeError("'%s' n'est pas un heritier de la classe ast.AST." % type(ast_node))

    def get_origin(self):
        """
        retourne la ligne du code d'origine
        """
        master = self
        while True:
            try:
                lineno = master.lineno
                break
            except AttributeError:
                master = master.father
        while master.father is not None:
            master = master.father
        return master.file_content.split("\n")[lineno-1] # les numeros de lignes commencent a 1, pas a 0

    def get_modules(self):
        """
        retourne l'ensemble des modules
        qui sont importes dans ce module
        dons le module lui-meme et les sous modules des modules.
        """
        # with raisin.Printer("Search modules in '%s'..." % str(type(self))[1:-1].split(".")[-1]) as p:
        if self._type == "Import":
            return set([alias.name for alias in ast.iter_child_nodes(self)])
        elif self._type == "ImportFrom":
            return {self.module} if not self.level else set()
        else:
            modules = set()
            for child in ast.iter_child_nodes(self):
                try:
                    modules |= self.overload(child).get_modules()
                except AttributeError:
                    pass
            return modules

    def _indent(self, code):
        """
        Indente de 4 espaces l'entierte du code
        'code', qui bien sur, est de type str
        """
        assert type(code) is str, "Le code 'code' doit etre de type str, pas %s." % type(code)
        return "    " + "\n    ".join(code.split("\n")).replace("\n    \n", "\n\n")

    def _body_str(self, ast_body):
        """
        retourne le code humainement comprehenssible
        de l'enfant body.
        Si le contenu est vide, renvoi pass.
        """
        body_str = "\n".join((
                    str(self.overload(bod))
                    + ("\n" if type(bod) in (ast.FunctionDef,
                                            ast.AsyncFunctionDef,
                                            ast.ClassDef)
                                         and i + 1 != len(ast_body)
                            else "")
                    for i, bod in enumerate(ast_body))
                        )
        return body_str if ast_body else "pass"

    def _is_monobloc(self, ast_node):
        """
        Renvoi True si le bloc n'est pas secable. C'est a dire
        si le fait de l'encadrer de parenthese est toujours inutile
        """
        return type(ast_node) in (ast.Dict, ast.Set, ast.ListComp,
            ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.Name,
            ast.List, ast.Tuple, ast.Num, ast.Subscript, ast.Attribute,
            ast.Call, ast.NameConstant, ast.Str, ast.Bytes, ast.Ellipsis,
            ast.JoinedStr, ast.Constant)

    def _prio(self, my_op, ast_node, side_other):
        """
        retourne '"%s"'' si l'objet 'ast_node' sera
        evalue avant l'operateur 'op' quelque soit sa position.
        retourn '"(%s)"' si l'objet 'ast_node' sera evalue apres 'op'
        quel que soit ca position.
        En cas de prioritee equivalente des 2 opperateurs, retourne "'%s'" si 'side_other' == "left",
        "'(%s)'" si 'side_other' == "right".
        """
        assert side_other == "left" or side_other == "right", "'side_other ne peut valoir que 'left' ou 'right', pas %s" % side_other
        if self._is_monobloc(ast_node):  # si il n'y a meme pas de question d'operateurs
            return "%s"             # alors inutile de s'encombrer de parentheses
        comparison = False
        if type(ast_node) in [ast.BoolOp, ast.BinOp, ast.UnaryOp]:
            comparison = True
            other_priorities = self.priorites[type(ast_node.op)]
        elif type(ast_node) is ast.Compare:
            comparison = True
            other_priorities = min([self.priorites[type(my_op)] for op in ast_node.ops])
        if comparison:
            my_priorites = self.priorites[type(my_op)] # mon taux de priorite
            if my_priorites < other_priorities:
                return "%s"
            elif my_priorites > other_priorities:
                return "(%s)"
            return "%s" if side_other == "left" else "(%s)"
        return "(%s)" # dans le doute, il vaut mieu metre des parentheses

def get_grammar(signature):
    """
    retourne un dictionaire qui a chaque classe definie
    dans le module ast, associ une class etendue de cette class.
    Le dictionaire retourne et les objets qu'ils contient sont en adequation avec la version de python
    """
    def update_to_3_7(grammar_dico):
        """
        ajoute les nouveaux elements apparus entre
        python 3.6 et 3.7
        """
        return grammar_dico

    def update_to_3_8(grammar_dico):
        """
        ajoute les nouveaux elements apparus entre
        python 3.7 et 3.8
        """
        class NamedExpr(ast.NamedExpr, ExtendNode):
            """
            expr target, expr value
            """
            def __init__(self, ast_namedexpr):
                assert type(ast_namedexpr) is ast.NamedExpr, "Cet objet permet une extension d'une instance de type ast.NamedExpr"
                self.__dict__ = ast_namedexpr.__dict__ # permet de faire un heritage sur des instances d'objets

            def __str__(self):
                """
                represente une assignation de la forme truc := machin
                """
                return "(" + str(self.overload(self.target)) + " := " + str(self.overload(self.value)) + ")"

        class FunctionType(ast.FunctionType, ExtendNode):
            """
            expr* argtypes, expr returns
            """
            def __init__(self, ast_functiontype):
                assert type(ast_functiontype) is ast.FunctionType, "Cet objet permet une extension d'une instance de type ast.FunctionType"
                self.__dict__ = ast_functiontype.__dict__ # permet de faire un heritage sur des instances d'objets

        class type_ignore(ast.type_ignore, ExtendNode):
            """
            int lineno, string tag
            """
            def __init__(self, ast_type_ignore):
                assert type(ast_type_ignore) is ast.type_ignore, "Cet objet permet une extension d'une instance de type ast.type_ignore"
                self.__dict__ = ast_type_ignore.__dict__ # permet de faire un heritage sur des instances d'objets

        grammar_dico[ast.NamedExpr] = NamedExpr
        grammar_dico[ast.FunctionType] = FunctionType
        grammar_dico[ast.type_ignore] = type_ignore

        return grammar_dico

    grammar_dico = {} # initialisation du dictionaire

    #######
    # mod #
    #######

    class Module(ast.Module, ExtendNode):
        """
        stmt* body, type_ignore *type_ignores
        """
        def __init__(self, ast_module, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_module) is ast.Module, "Cet objet permet une extension d'une instance de type ast.Module"
            self.__dict__ = ast_module.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Module"

        @improve_recursion_decorateur(50)
        def __str__(self):
            """
            retourne le code complet du module
            presente de la facon suivante:
                -duner_list
                -import_list
                -def_list
                -class_list
                -body_list
            """
            if not self.body:
                return "\n"
            
            content_str = "# !/usr/bin/env python3\n# -*- coding: utf-8 -*-"
            duner_list = []
            import_list = []
            def_class_list = []
            body_list = []
            start = True # False des que l'on sort du champs 'dunner'
            
            for node in ast.iter_child_nodes(self):
                if type(node) is ast.Import or type(node) is ast.ImportFrom:
                    start = False
                    import_list.append(node)
                elif type(node) is ast.FunctionDef or \
                     type(node) is ast.AsyncFunctionDef or \
                     type(node) is ast.ClassDef:
                    start = False
                    def_class_list.append(node)
                elif start and type(node) is ast.Assign:
                    duner_list.append(node)
                else:
                    start = False
                    body_list.append(node)

            # cas ou le module est bien trie
            if duner_list + import_list + def_class_list + body_list == self.body:
                if duner_list:
                    content_str += "\n\n\n"+"\n".join(map(lambda el: str(self.overload(el)), duner_list))
                if import_list:
                    content_str += "\n\n\n"+"\n".join(map(lambda el: str(self.overload(el)), import_list))
                if def_class_list:
                    content_str += "\n\n\n"+"\n\n".join(map(lambda el: str(self.overload(el)), def_class_list))
                if body_list:
                    content_str += "\n\n\n"+"\n".join(map(lambda el: str(self.overload(el)), body_list))
            else:
                content_str += "\n\n\n" + str(self.overload(self.body[0]))
                for i in range(1, len(self.body)):
                    if type(self.body[i-1]) in [ast.Import, ast.ImportFrom] \
                        and type(self.body[i]) in [ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef] \
                        or type(self.body[i-1]) in [ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef] \
                        and type(self.body[i]) not in [ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]:
                        content_str += "\n\n"
                    elif type(self.body[i-1]) in [ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]:
                        content_str += "\n"
                    content_str += "\n" + str(self.overload(self.body[i]))
            content_str += "\n"
            return content_str

    class Interactive(ast.Interactive, ExtendNode):
        """
        stmt* body
        """
        def __init__(self, ast_interactive, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_interactive) is ast.Interactive, "Cet objet permet une extension d'une instance de type ast.Interactive"
            self.__dict__ = ast_interactive.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Interactive"

    class Expression(ast.Expression, ExtendNode):
        """
        expr body
        """
        def __init__(self, ast_expression, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_expression) is ast.Expression, "Cet objet permet une extension d'une instance de type ast.Expression"
            self.__dict__ = ast_expression.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Expression"

    class Suite(ast.Suite, ExtendNode):
        """
        stmt* body
        """
        def __init__(self, ast_suite, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_suite) is ast.Suite, "Cet objet permet une extension d'une instance de type ast.Suite"
            self.__dict__ = ast_suite.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Suite"

    ########
    # stmt #
    ########

    class FunctionDef(ast.FunctionDef, ExtendNode):
        """
        identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment
        """
        def __init__(self, ast_functiondef, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_functiondef) is ast.FunctionDef, "Cet objet permet une extension d'une instance de type ast.FunctionDef"
            self.__dict__ = ast_functiondef.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "FunctionDef"

        @improve_recursion_decorateur(20)
        def __str__(self):
            """
            affiche joliment une definition de fonction
            {   'name': '__init__',
                'args': <_ast.arguments object at 0x7fa552cc9f98>,
                'body': [...],
                'decorator_list': [],
                'returns': None}"
            """
            decorator_str = "\n".join(("@" + str(self.overload(dec)) for dec in self.decorator_list))
            header_str = "def " + self.name + "(" + str(self.overload(self.args)) + ")"
            if self.returns: # donne des informations sur le type retournee def foo() -> returns
                header_str += " -> " + str(self.overload(self.returns))
            header_str += ":"
            body_str = self._body_str(self.body)

            code = ""
            if decorator_str:
                code += decorator_str + "\n"
            code += header_str + "\n"
            code += self._indent(body_str)
            return code

    class AsyncFunctionDef(ast.AsyncFunctionDef, ExtendNode):
        """
        identifier name, arguments args, stmt* body, expr* decorator_list, expr? returns, string? type_comment
        """
        def __init__(self, ast_asyncfunctiondef, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_asyncfunctiondef) is ast.AsyncFunctionDef, "Cet objet permet une extension d'une instance de type ast.AsyncFunctionDef"
            self.__dict__ = ast_asyncfunctiondef.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AsyncFunctionDef"

        @improve_recursion_decorateur(20)
        def __str__(self):
            """
            se rapporte a la methode str de FunctionDef
            """
            f = ast.FunctionDef()
            f.__dict__ = self.__dict__
            f.decorator_list = []
            return "\n".join(("@" + str(self.overload(dec)) for dec in self.decorator_list)) \
                + "async " + str(FunctionDef(f))

    class ClassDef(ast.ClassDef, ExtendNode):
        """
        identifier name, expr* bases, keyword* keywords, stmt* body, expr* decorator_list
        """
        def __init__(self, ast_classdef, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_classdef) is ast.ClassDef, "Cet objet permet une extension d'une instance de type ast.ClassDef"
            self.__dict__ = ast_classdef.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "ClassDef"

        @improve_recursion_decorateur(20)
        def __str__(self):
            """
            correspond a une definition de class
            retourne la class sous forme de code executable
            """
            decorator_str = "\n".join(("@" + str(self.overload(dec)) for dec in self.decorator_list))
            header_str = "class " + self.name
            if self.bases:
                header_str += "(" + ", ".join((str(self.overload(base)) for base in self.bases + self.keywords)) + ")"
            header_str += ":"
            body_str = self._body_str(self.body)

            code = ""
            if decorator_str:
                code += decorator_str + "\n"
            code += header_str + "\n"
            code += self._indent(body_str)
            return code

    class Return(ast.Return, ExtendNode):
        """
        expr? value
        """
        def __init__(self, ast_return, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_return) is ast.Return, "Cet objet permet une extension d'une instance de type ast.Return"
            self.__dict__ = ast_return.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Return"

        def __str__(self):
            code = "return"
            if self.value:
                prio = "%s"
                if type(self.value) in (ast.YieldFrom, ast.Yield):
                    prio = "(%s)"
                code += " " + prio % str(self.overload(self.value))
            return code

    class Delete(ast.Delete, ExtendNode):
        """
        expr* targets
        """
        def __init__(self, ast_delete, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_delete) is ast.Delete, "Cet objet permet une extension d'une instance de type ast.Delete"
            self.__dict__ = ast_delete.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Delete"

        def __str__(self):
            return "del " + ", ".join((str(self.overload(tar)) for tar in self.targets))

    class Assign(ast.Assign, ExtendNode):
        """
        expr* targets, expr value, string? type_comment
        """
        def __init__(self, ast_assign, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_assign) is ast.Assign, "Cet objet permet une extension d'une instance de type ast.Assign"
            self.__dict__ = ast_assign.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Assign"

        def __str__(self):
            return " = ".join((
                       ", ".join((str(self.overload(elt)) for elt in var.elts)) if type(var) is ast.Tuple
                        else str(self.overload(var))
                        for var in self.targets)) \
                + " = " + str(self.overload(self.value))

    class AugAssign(ast.AugAssign, ExtendNode):
        """
        expr target, operator op, expr value
        """
        def __init__(self, ast_augassign, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_augassign) is ast.AugAssign, "Cet objet permet une extension d'une instance de type ast.AugAssign"
            self.__dict__ = ast_augassign.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AugAssign"

        def __str__(self):
            """
            represente une assignation 'recursive'
            """
            return str(self.overload(self.target))          \
                + " " + str(self.overload(self.op)) + "= "   \
                + str(self.overload(self.value))

    class AnnAssign(ast.AnnAssign, ExtendNode):
        """
        expr target, expr annotation, expr? value, int simple
        """
        def __init__(self, ast_annassign, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_annassign) is ast.AnnAssign, "Cet objet permet une extension d'une instance de type ast.AnnAssign"
            self.__dict__ = ast_annassign.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AnnAssign"

        def __str__(self):
            """
            ne sert pas a grand chose, a part a typer une variable
            comme par example x: int
            """
            return str(self.overload(self.target)) + ": " + str(self.overload(self.annotation)) + (" = " + str(self.overload(self.value)) if self.value else "")

    class For(ast.For, ExtendNode):
        """
        expr target, expr iter, stmt* body, stmt* orelse, string? type_comment
        """
        def __init__(self, ast_for, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_for) is ast.For, "Cet objet permet une extension d'une instance de type ast.For"
            self.__dict__ = ast_for.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "For"

        def __str__(self):
            target_str = str(self.overload(self.target)) \
                        if type(self.target) not in (ast.Tuple, ast.List) \
                        else ", ".join((str(self.overload(elt)) for elt in self.target.elts))
            code = "for " + target_str \
                    + " in " + str(self.overload(self.iter)) + ":\n" \
                    + self._indent(self._body_str(self.body))
            if self.orelse:
                code += "\nelse:\n" + self._indent(self._body_str(self.orelse))
            return code

    class AsyncFor(ast.AsyncFor, ExtendNode):
        """
        expr target, expr iter, stmt* body, stmt* orelse, string? type_comment
        """
        def __init__(self, ast_asyncfor, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_asyncfor) is ast.AsyncFor, "Cet objet permet une extension d'une instance de type ast.AsyncFor"
            self.__dict__ = ast_asyncfor.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AsyncFor"

        def __str__(self):
            """
            se base sur la syntaxe de For
            """
            f = ast.For()
            f.__dict__ = self.__dict__
            return "async " + str(self.overload(f))

    class While(ast.While, ExtendNode):
        """
        expr test, stmt* body, stmt* orelse
        """
        def __init__(self, ast_while, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_while) is ast.While, "Cet objet permet une extension d'une instance de type ast.While"
            self.__dict__ = ast_while.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "While"

        def __str__(self):
            prio = "(%s)" if type(self.test) is ast.Yield else "%s"
            code = "while " + prio % str(self.overload(self.test)) + ":\n" \
                + self._indent(self._body_str(self.body))
            if self.orelse:
                code += "\nelse:\n" + self._indent(self._body_str(self.orelse))
            return code

    class If(ast.If, ExtendNode):
        """
        expr test, stmt* body, stmt* orelse
        """
        def __init__(self, ast_if, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_if) is ast.If, "Cet objet permet une extension d'une instance de type ast.If"
            self.__dict__ = ast_if.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "If"

        def __str__(self):
            """
            permet de metre en forme un bloc conditionel
            """
            prio = "%s" if type(self.test) is not ast.YieldFrom else "(%s)"
            code = "if " + prio % str(self.overload(self.test)) + ":\n" \
                    + self._indent(self._body_str(self.body))
            if self.orelse:
                if type(self.orelse[0]) is ast.If:
                    code += "\nel" + self._body_str(self.orelse)
                else:
                    code += "\nelse:\n" + self._indent(self._body_str(self.orelse))
            return code

    class With(ast.With, ExtendNode):
        """
        withitem* items, stmt* body, string? type_comment
        """
        def __init__(self, ast_with, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_with) is ast.With, "Cet objet permet une extension d'une instance de type ast.With"
            self.__dict__ = ast_with.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "With"

        def __str__(self):
            """
            represente le bloc comencant par le mot clef 'with'
            """
            return "with " + ", ".join((str(self.overload(item)) for item in self.items)) \
                    + ":\n" + self._indent(self._body_str(self.body))

    class AsyncWith(ast.AsyncWith, ExtendNode):
        """
        withitem* items, stmt* body, string? type_comment
        """
        def __init__(self, ast_asyncwith, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_asyncwith) is ast.AsyncWith, "Cet objet permet une extension d'une instance de type ast.AsyncWith"
            self.__dict__ = ast_asyncwith.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AsyncWith"

        def __str__(self):
            """
            se base sur la syntaxe de With
            """
            f = ast.With()
            f.__dict__ = self.__dict__
            return "async " + str(self.overload(f))

    class Raise(ast.Raise, ExtendNode):
        """
        expr? exc, expr? cause
        """
        def __init__(self, ast_raise, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_raise) is ast.Raise, "Cet objet permet une extension d'une instance de type ast.Raise"
            self.__dict__ = ast_raise.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Raise"

        def __str__(self):
            """
            represente un raise
            """
            code = "raise"
            if self.exc:
                code += " " + str(self.overload(self.exc))
            if self.cause:
                code += " from " + str(self.overload(self.cause))
            return code

    class Try(ast.Try, ExtendNode):
        """
        stmt* body, excepthandler* handlers, stmt* orelse, stmt* finalbody
        """
        def __init__(self, ast_try, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_try) is ast.Try, "Cet objet permet une extension d'une instance de type ast.Try"
            self.__dict__ = ast_try.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Try"

        def __str__(self):
            """
            renvoi un code qui correspond a la syntaxe du try
            """
            code = "try:\n" + self._indent(self._body_str(self.body))
            for handler in self.handlers:
                code += "\n" + str(self.overload(handler))
            if self.orelse:
                code += "\nelse:\n" + self._indent(self._body_str(self.orelse))
            if self.finalbody:
                code += "\nfinally:\n" + self._indent(self._body_str(self.finalbody))
            return code

    class Assert(ast.Assert, ExtendNode):
        """
        expr test, expr? msg
        """
        def __init__(self, ast_assert, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_assert) is ast.Assert, "Cet objet permet une extension d'une instance de type ast.Assert"
            self.__dict__ = ast_assert.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Assert"

        def __str__(self):
            code = "assert " + str(self.overload(self.test))
            if self.msg:
                code += ", " + str(self.overload(self.msg))
            return code

    class Import(ast.Import, ExtendNode):
        """
        alias* names
        """
        def __init__(self, ast_import, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_import) is ast.Import, "Cet objet permet une extension d'une instance de type ast.Import"
            self.__dict__ = ast_import.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Import"

        def __str__(self):
            """
            ecrit la syntaxe du import
            """
            return "import %s" % ", ".join((str(self.overload(alias)) for alias in ast.iter_child_nodes(self)))

    class ImportFrom(ast.ImportFrom, ExtendNode):
        """
        identifier? module, alias* names, int? level
        """
        def __init__(self, ast_importfrom, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_importfrom) is ast.ImportFrom, "Cet objet permet une extension d'une instance de type ast.ImportFrom"
            self.__dict__ = ast_importfrom.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "ImportFrom"

        def __str__(self):
            """
            represent un import de module avec la syntaxe:
            from truc import *machins
            """
            return "from " + "."*self.level + (self.module if self.module else "") + " import " \
                + ", ".join((str(self.overload(a)) for a in self.names))

    class Global(ast.Global, ExtendNode):
        """
        identifier* names
        """
        def __init__(self, ast_global, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_global) is ast.Global, "Cet objet permet une extension d'une instance de type ast.Global"
            self.__dict__ = ast_global.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Global"

        def __str__(self):
            return "global " + ", ".join(self.names)

    class Nonlocal(ast.Nonlocal, ExtendNode):
        """
        identifier* names
        """
        def __init__(self, ast_nonlocal, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_nonlocal) is ast.Nonlocal, "Cet objet permet une extension d'une instance de type ast.Nonlocal"
            self.__dict__ = ast_nonlocal.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Nonlocal"

        def __str__(self):
            return "nonlocal " + ", ".join(self.names)

    class Expr(ast.Expr, ExtendNode):
        """
        expr value
        """
        def __init__(self, ast_expr, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_expr) is ast.Expr, "Cet objet permet une extension d'une instance de type ast.Expr"
            self.__dict__ = ast_expr.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Expr"

        def __str__(self):
            return str(self.overload(self.value))

    class Pass(ast.Pass, ExtendNode):
        def __init__(self, ast_pass, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_pass) is ast.Pass, "Cet objet permet une extension d'une instance de type ast.Pass"
            self.__dict__ = ast_pass.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Pass"

        def __str__(self):
            return "pass"

    class Break(ast.Break, ExtendNode):
        def __init__(self, ast_break, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_break) is ast.Break, "Cet objet permet une extension d'une instance de type ast.Break"
            self.__dict__ = ast_break.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Break"

        def __str__(self):
            return "break"

    class Continue(ast.Continue, ExtendNode):
        def __init__(self, ast_continue, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_continue) is ast.Continue, "Cet objet permet une extension d'une instance de type ast.Continue"
            self.__dict__ = ast_continue.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Continue"

        def __str__(self):
            return "continue"

    ########
    # expr #
    ########

    class BoolOp(ast.BoolOp, ExtendNode):
        """
        boolop op, expr* values
        """
        def __init__(self, ast_boolop, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_boolop) is ast.BoolOp, "Cet objet permet une extension d'une instance de type ast.BoolOp"
            self.__dict__ = ast_boolop.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "BoolOp"

        def __str__(self):
            """
            represente les opperateurs:
                -or, and
            """
            return (" " + str(self.overload(self.op)) + " ").join(
                self._prio(self.op, value, "left") % str(self.overload(value))
                for value in self.values)

    class BinOp(ast.BinOp, ExtendNode):
        """
        expr left, operator op, expr right
        """
        def __init__(self, ast_binop, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_binop) is ast.BinOp, "Cet objet permet une extension d'une instance de type ast.BinOp"
            self.__dict__ = ast_binop.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "BinOp"

        def __str__(self):
            """
            represente les opperateurs:
                -+, -, *, @, /, %, **, <<, >>, |, ^, &, //
            """
            space = "%s" if type(self.op) in [ast.Mult, ast.Div, ast.Pow, ast.FloorDiv] else " %s "
            return self._prio(self.op, self.left, "left") % str(self.overload(self.left)) \
                   + space % str(self.overload(self.op)) \
                   + self._prio(self.op, self.right, "right") % str(self.overload(self.right))

    class UnaryOp(ast.UnaryOp, ExtendNode):
        """
        unaryop op, expr operand
        """
        def __init__(self, ast_unaryop, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_unaryop) is ast.UnaryOp, "Cet objet permet une extension d'une instance de type ast.UnaryOp"
            self.__dict__ = ast_unaryop.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "UnaryOp"

        def __str__(self):
            """
            represente un operateur qui agit sur la gauche d'un objet
            """
            space = "" if type(self.op) in [ast.UAdd, ast.USub, ast.Invert] else " "
            return str(self.overload(self.op)) + space \
                   + self._prio(self.op, self.operand, "right") % str(self.overload(self.operand))

    class Lambda(ast.Lambda, ExtendNode):
        """
        arguments args, expr body
        """
        def __init__(self, ast_lambda, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_lambda) is ast.Lambda, "Cet objet permet une extension d'une instance de type ast.Lambda"
            self.__dict__ = ast_lambda.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Lambda"

        def __str__(self):
            """
            represente une expression 'lambda'
            """
            code = "lambda"
            args_str = str(self.overload(self.args))
            if args_str:
                code += " " + args_str + " :"
            else:
                code += ":"
            prio = "%s"
            if type(self.body) in (ast.YieldFrom, ast.Yield):
                prio = "(%s)"
            code += " " + prio % str(self.overload(self.body))
            return code

    class IfExp(ast.IfExp, ExtendNode):
        """
        expr test, expr body, expr orelse
        """
        def __init__(self, ast_ifexp, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_ifexp) is ast.IfExp, "Cet objet permet une extension d'une instance de type ast.IfExp"
            self.__dict__ = ast_ifexp.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "IfExp"

        def __str__(self):
            return str(self.overload(self.body)) \
                + " if " + str(self.overload(self.test)) \
                + " else " + str(self.overload(self.orelse))

    class Dict(ast.Dict, ExtendNode):
        """
        expr* keys, expr* values
        """
        def __init__(self, ast_dict, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_dict) is ast.Dict, "Cet objet permet une extension d'une instance de type ast.Dict"
            self.__dict__ = ast_dict.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Dict"

        def __str__(self):
            encapsule = (lambda elt: "%s" if self._is_monobloc(elt) else "(%s)")
            return "{" \
                + ", ".join((
                    encapsule(k) % str(self.overload(k)) + ": " + encapsule(v) % str(self.overload(v)) if k
                    else "**" + encapsule(k) % str(self.overload(v))
                    for k, v in zip(self.keys, self.values)
                    )) \
                + "}"

    class Set(ast.Set, ExtendNode):
        """
        expr* elts
        """
        def __init__(self, ast_set, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_set) is ast.Set, "Cet objet permet une extension d'une instance de type ast.Set"
            self.__dict__ = ast_set.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Set"

        def __str__(self):
            if self.elts:
                return "{" + ", ".join((("(%s)" if type(elt) in (ast.Yield, ast.YieldFrom) else "%s") \
                        % str(self.overload(elt)) for elt in self.elts)) + "}"
            return "set()"

    class ListComp(ast.ListComp, ExtendNode):
        """
        expr elt, comprehension* generators
        """
        def __init__(self, ast_listcomp, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_listcomp) is ast.ListComp, "Cet objet permet une extension d'une instance de type ast.ListComp"
            self.__dict__ = ast_listcomp.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "ListComp"

        def __str__(self):
            return "[" + str(self.overload(self.elt)) + " " \
                + " ".join((str(self.overload(gen))
                    for gen in self.generators)) + "]"

    class SetComp(ast.SetComp, ExtendNode):
        """
        expr elt, comprehension* generators
        """
        def __init__(self, ast_setcomp, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_setcomp) is ast.SetComp, "Cet objet permet une extension d'une instance de type ast.SetComp"
            self.__dict__ = ast_setcomp.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "SetComp"

        def __str__(self):
            return "{" + str(self.overload(self.elt)) + " " \
                + " ".join((str(self.overload(gen))
                    for gen in self.generators)) + "}"

    class DictComp(ast.DictComp, ExtendNode):
        """
        expr key, expr value, comprehension* generators
        """
        def __init__(self, ast_dictcomp, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_dictcomp) is ast.DictComp, "Cet objet permet une extension d'une instance de type ast.DictComp"
            self.__dict__ = ast_dictcomp.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "DictComp"

        def __str__(self):
            return "{" + str(self.overload(self.key)) + ": " + str(self.overload(self.value)) \
                + " " + " ".join((str(self.overload(gen))
                    for gen in self.generators)) + "}"

    class GeneratorExp(ast.GeneratorExp, ExtendNode):
        """
        expr elt, comprehension* generators
        """
        def __init__(self, ast_generatorexp, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_generatorexp) is ast.GeneratorExp, "Cet objet permet une extension d'une instance de type ast.GeneratorExp"
            self.__dict__ = ast_generatorexp.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "GeneratorExp"

        def __str__(self):
            return "(" + str(self.overload(self.elt)) + " " \
                + " ".join((str(self.overload(gen))
                    for gen in self.generators)) + ")"

    class Await(ast.Await, ExtendNode):
        """
        expr value
        """
        def __init__(self, ast_await, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_await) is ast.Await, "Cet objet permet une extension d'une instance de type ast.Await"
            self.__dict__ = ast_await.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Await"

        def __str__(self):
            prio = "%s" if type(self.value) is not ast.Await else "(%s)"
            return "await " + prio % str(self.overload(self.value))

    class Yield(ast.Yield, ExtendNode):
        """
        expr? value
        """
        def __init__(self, ast_yield, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_yield) is ast.Yield, "Cet objet permet une extension d'une instance de type ast.Yield"
            self.__dict__ = ast_yield.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Yield"

        def __str__(self):
            code = "yield"
            prio = "(%s)" if type(self.value) is ast.Lambda else "%s"
            if self.value:
                code += " " + prio % str(self.overload(self.value))
            return code

    class YieldFrom(ast.YieldFrom, ExtendNode):
        """
        expr value
        """
        def __init__(self, ast_yieldfrom, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_yieldfrom) is ast.YieldFrom, "Cet objet permet une extension d'une instance de type ast.YieldFrom"
            self.__dict__ = ast_yieldfrom.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "YieldFrom"

        def __str__(self):
            return "yield from " + str(self.overload(self.value))

    class Compare(ast.Compare, ExtendNode):
        """
        expr left, cmpop* ops, expr* comparators
        """
        def __init__(self, ast_compare, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_compare) is ast.Compare, "Cet objet permet une extension d'une instance de type ast.Compare"
            self.__dict__ = ast_compare.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Compare"

        def __str__(self):
            """
            comparaison multiple entre n elements avec les opperateurs:
                -==, !=, >, <, >=, <=
            """
            code = self._prio(self.ops[0], self.left, "left") % str(self.overload(self.left))
            if self.ops:
                code += " " + " ".join((
                    str(self.overload(op)) + " " + self._prio(op, comp, "right") % str(self.overload(comp))
                    for op, comp in zip(self.ops, self.comparators)
                    ))
            return code

    class Call(ast.Call, ExtendNode):
        """
        expr func, expr* args, keyword* keywords
        """
        def __init__(self, ast_call, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_call) is ast.Call, "Cet objet permet une extension d'une instance de type ast.Call"
            self.__dict__ = ast_call.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Call"

        def __str__(self):
            """
            affiche joliment un appel de fonction
            """
            args_str = None
            if self.args:
                args_str = ", ".join((("(%s)" if type(arg) in [ast.Yield, ast.YieldFrom] else "%s") % str(self.overload(arg))
                    for arg in self.args))
            keywords_str = None
            if self.keywords:
                keywords_str = ", ".join((str(self.overload(keyword)) for keyword in self.keywords))
            params = ", ".join((t for t in (args_str, keywords_str) if t))
            prio = "%s" if self._is_monobloc(self.func) else "(%s)"
            return prio % str(self.overload(self.func)) + "(%s)" % params

    class FormattedValue(ast.FormattedValue, ExtendNode):
        """
        expr value, int? conversion, expr? format_spec
        """
        def __init__(self, ast_formattedvalue, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_formattedvalue) is ast.FormattedValue, "Cet objet permet une extension d'une instance de type ast.FormattedValue"
            self.__dict__ = ast_formattedvalue.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "FormattedValue"

        def __str__(self):
            """
            represente une paquet {...} dans une chaine formattee
            """
            var_str = str(self.overload(self.value))
            if self.conversion == -1:
                pass
            elif self.conversion == 97:
                var_str += "!a"
            elif self.conversion == 114:
                var_str += "!r"
            elif self.conversion == 115:
                var_str += "!s"
            else:
                raise ValueError("C'est cence donner quoi? %d, %s." % (self.conversion, self.get_origin()))
            if self.format_spec: # si dans l'accolade, on apporte des precisions sur le formattage de la variable
                if type(self.format_spec) is ast.JoinedStr:
                    var_str += ":" + "".join(
                        [str(self.overload(v)) if type(v) is ast.FormattedValue
                         else eval(str(self.overload(v)))
                         for v in self.format_spec.values])
                else:
                    raise TypeError("Dans les chaine formattee, apres les:, on doit trouver un type ast.JoinedStr, pas %s." % type(self.format_spec))
            return "{" + var_str + "}"

    class JoinedStr(ast.JoinedStr, ExtendNode):
        """
        expr* values
        """
        def __init__(self, ast_joinedstr, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_joinedstr) is ast.JoinedStr, "Cet objet permet une extension d'une instance de type ast.JoinedStr"
            self.__dict__ = ast_joinedstr.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "JoinedStr"

        def __str__(self):
            """
            Represente une chaine formattee, par example: f'{sup.module}.{sname}'
            donne [<_ast.FormattedValue object at 0x7fcad1091940>, <_ast.Constant object at 0x7fcad1091790>, <_ast.FormattedValue object at 0x7fcad10916d0>]
            pour python 3.8
            donne [<_ast.FormattedValue object at 0x7f0a77fbf620>, <_ast.Str object at 0x7f0a77fbf588>, <_ast.FormattedValue object at 0x7f0a77fbf470>]
            pour python 3.6 et 3.7
            """
            def smart_repr(chaine):
                """
                retourne la meme chose que repr(chaine) a une difference pres
                c'est que contreoblique n'est pas duplique.
                De plus, contrairement a repr, l'ajout de caractere d'echappement
                y est encore plus minimise
                """
                if "\n" in chaine or "\r" in chaine:
                    if "'''" not in chaine:
                        return "'''" + chaine + "'''"
                    elif '"""' not in chaine:
                        return '"""' + chaine + '"""'
                else:
                    if "'" not in chaine:
                        return "'" + chaine + "'"
                    elif '"' not in chaine:
                        return '"' + chaine + '"'
                    elif "'''" not in chaine:
                        return "'''" + chaine + "'''"
                    elif '"""' not in chaine:
                        return '"""' + chaine + '"""'
                return repr(chaine).replace(r"\\", "\\")

            if ast.FormattedValue not in map(type, self.values):    # si cette chaine formattee n'en est pas une:
                return repr("".join([eval(str(self.overload(v))) for v in self.values]))# on renvoi une chaine normale, pas formattee
            
            return "f" + smart_repr("".join(
                [str(self.overload(v)) if type(v) is ast.FormattedValue # il manque les f'' autour des {...} mais c'est normal, c'est pour mieu les rassembler
                 else eval(str(self.overload(v))).replace("{", "{{").replace("}", "}}").replace("\\", r"\\") # il manque aussi les '' autour des chaine normales, la raison est la meme
                 for v in self.values]))
            
    class Constant(ast.Constant, ExtendNode):
        """
        constant value, string? kind
        """
        def __init__(self, ast_constant, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_constant) is ast.Constant, "Cet objet permet une extension d'une instance de type ast.Constant"
            self.__dict__ = ast_constant.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Constant"

        def __str__(self):
            """
            represente une grandeur python qui ne change pas
            que ce soit un str, un entier, un booleen...
            """
            prefixe = ""
            if self.kind:
                prefixe = self.kind
            return prefixe + repr(self.value)

    class Attribute(ast.Attribute, ExtendNode):
        """
        expr value, identifier attr, expr_context ctx
        """
        def __init__(self, ast_attribute, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_attribute) is ast.Attribute, "Cet objet permet une extension d'une instance de type ast.Attribute"
            self.__dict__ = ast_attribute.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Attribute"

        def __str__(self):
            """
            represente la syntaxe truc.machin
            """
            prio = "%s" if self._is_monobloc(self.value) and type(self.value) is not ast.Num else "(%s)"
            if type(self.value) is ast.Constant:
                if type(self.value.value) in (int, float, complex, ast.Num):
                    prio = "(%s)"
            return prio % str(self.overload(self.value)) + "." + self.attr

    class Subscript(ast.Subscript, ExtendNode):
        """
        expr value, slice slice, expr_context ctx
        """
        def __init__(self, ast_subscript, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_subscript) is ast.Subscript, "Cet objet permet une extension d'une instance de type ast.Subscript"
            self.__dict__ = ast_subscript.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Subscript"

        def __str__(self):
            """
            represente la stimulation d'un objet grace a objet[truc]
            """
            prio = "%s" if self._is_monobloc(self.value) else "(%s)"
            return prio % str(self.overload(self.value)) + "[" + str(self.overload(self.slice)) + "]"

    class Starred(ast.Starred, ExtendNode):
        """
        expr value, expr_context ctx
        """
        def __init__(self, ast_starred, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_starred) is ast.Starred, "Cet objet permet une extension d'une instance de type ast.Starred"
            self.__dict__ = ast_starred.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Starred"

        def __str__(self):
            """
            dans un appel de fonction, c'est
            pour passer n parametres
            """
            prio = "%s" if self._is_monobloc(self.value) else "(%s)"
            return "*" + prio % str(self.overload(self.value))

    class Name(ast.Name, ExtendNode):
        """
        identifier id, expr_context ctx
        """
        def __init__(self, ast_name, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_name) is ast.Name, "Cet objet permet une extension d'une instance de type ast.Name"
            self.__dict__ = ast_name.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Name"

        def __str__(self):
            """
            retourne le nom de la variable qu'il represente
            """
            return self.id

    class List(ast.List, ExtendNode):
        """
        expr* elts, expr_context ctx
        """
        def __init__(self, ast_list, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_list) is ast.List, "Cet objet permet une extension d'une instance de type ast.List"
            self.__dict__ = ast_list.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "List"

        def __str__(self):
            return "[" + ", ".join((("(%s)" if type(elt) in (ast.Yield, ast.YieldFrom) else "%s") \
                    % str(self.overload(elt)) for elt in self.elts)) + "]"

    class Tuple(ast.Tuple, ExtendNode):
        """
        expr* elts, expr_context ctx
        """
        def __init__(self, ast_tuple, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_tuple) is ast.Tuple, "Cet objet permet une extension d'une instance de type ast.Tuple"
            self.__dict__ = ast_tuple.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Tuple"

        def __str__(self):
            if len(self.elts) == 0:
                return "()"
            if len(self.elts) == 1:
                return "(" + ("(%s)" if type(self.elts[0]) in (ast.Yield, ast.YieldFrom) else "%s") \
                       % str(self.overload(self.elts[0])) + ",)"
            return "(" + ", ".join((("(%s)" if type(elt) in (ast.Yield, ast.YieldFrom) else "%s") \
                    % str(self.overload(elt)) for elt in self.elts)) + ")"

    ################
    # expr_context #
    ################

    class Load(ast.Load, ExtendNode):
        def __init__(self, ast_load, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_load) is ast.Load, "Cet objet permet une extension d'une instance de type ast.Load"
            self.__dict__ = ast_load.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Load"

    class Store(ast.Store, ExtendNode):
        def __init__(self, ast_store, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_store) is ast.Store, "Cet objet permet une extension d'une instance de type ast.Store"
            self.__dict__ = ast_store.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Store"

    class Del(ast.Del, ExtendNode):
        def __init__(self, ast_del, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_del) is ast.Del, "Cet objet permet une extension d'une instance de type ast.Del"
            self.__dict__ = ast_del.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Del"

    class AugLoad(ast.AugLoad, ExtendNode):
        def __init__(self, ast_augload, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_augload) is ast.AugLoad, "Cet objet permet une extension d'une instance de type ast.AugLoad"
            self.__dict__ = ast_augload.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AugLoad"

    class AugStore(ast.AugStore, ExtendNode):
        def __init__(self, ast_augstore, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_augstore) is ast.AugStore, "Cet objet permet une extension d'une instance de type ast.AugStore"
            self.__dict__ = ast_augstore.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "AugStore"

    class Param(ast.Param, ExtendNode):
        def __init__(self, ast_param, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_param) is ast.Param, "Cet objet permet une extension d'une instance de type ast.Param"
            self.__dict__ = ast_param.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Param"

    #########
    # slice #
    #########

    class Slice(ast.Slice, ExtendNode):
        """
        expr? lower, expr? upper, expr? step
        """
        def __init__(self, ast_slice, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_slice) is ast.Slice, "Cet objet permet une extension d'une instance de type ast.Slice"
            self.__dict__ = ast_slice.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Slice"

        def __str__(self):
            return "%s:%s%s" % (
                str(self.overload(self.lower)) if self.lower else "",
                str(self.overload(self.upper)) if self.upper else "",
                ":" + str(self.overload(self.step)) if self.step else "")

    class ExtSlice(ast.ExtSlice, ExtendNode):
        """
        slice* dims
        """
        def __init__(self, ast_extslice, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_extslice) is ast.ExtSlice, "Cet objet permet une extension d'une instance de type ast.ExtSlice"
            self.__dict__ = ast_extslice.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "ExtSlice"

        def __str__(self):
            """
            Represente une succession de slice multidimenssionel, par example:
            X[:, 3]
            """
            return ", ".join((str(self.overload(dim)) for dim in self.dims))

    class Index(ast.Index, ExtendNode):
        """
        expr value
        """
        def __init__(self, ast_index, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_index) is ast.Index, "Cet objet permet une extension d'une instance de type ast.Index"
            self.__dict__ = ast_index.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Index"

        def __str__(self):
            """
            represente un inex d'objet, comme un slice en moin evolue
            """
            return "[" + str(self.overload(self.value)) + "]"

    ##########
    # boolop #
    ##########

    class And(ast.And, ExtendNode):
        def __init__(self, ast_and, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_and) is ast.And, "Cet objet permet une extension d'une instance de type ast.And"
            self.__dict__ = ast_and.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "And"

        def __str__(self):
            return "and"

    class Or(ast.Or, ExtendNode):
        def __init__(self, ast_or, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_or) is ast.Or, "Cet objet permet une extension d'une instance de type ast.Or"
            self.__dict__ = ast_or.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Or"

        def __str__(self):
            return "or"

    ############
    # operator #
    ############

    class Add(ast.Add, ExtendNode):
        def __init__(self, ast_add, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_add) is ast.Add, "Cet objet permet une extension d'une instance de type ast.Add"
            self.__dict__ = ast_add.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Add"

        def __str__(self):
            return "+"

    class Sub(ast.Sub, ExtendNode):
        def __init__(self, ast_sub, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_sub) is ast.Sub, "Cet objet permet une extension d'une instance de type ast.Sub"
            self.__dict__ = ast_sub.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Sub"

        def __str__(self):
            return "-"

    class Mult(ast.Mult, ExtendNode):
        def __init__(self, ast_mult, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_mult) is ast.Mult, "Cet objet permet une extension d'une instance de type ast.Mult"
            self.__dict__ = ast_mult.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Mult"

        def __str__(self):
            return "*"

    class MatMult(ast.MatMult, ExtendNode):
        def __init__(self, ast_matmult, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_matmult) is ast.MatMult, "Cet objet permet une extension d'une instance de type ast.MatMult"
            self.__dict__ = ast_matmult.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "MatMult"

        def __str__(self):
            return "@"

    class Div(ast.Div, ExtendNode):
        def __init__(self, ast_div, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_div) is ast.Div, "Cet objet permet une extension d'une instance de type ast.Div"
            self.__dict__ = ast_div.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Div"

        def __str__(self):
            return "/"

    class Mod(ast.Mod, ExtendNode):
        def __init__(self, ast_mod, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_mod) is ast.Mod, "Cet objet permet une extension d'une instance de type ast.Mod"
            self.__dict__ = ast_mod.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Mod"

        def __str__(self):
            return "%"

    class Pow(ast.Pow, ExtendNode):
        def __init__(self, ast_pow, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_pow) is ast.Pow, "Cet objet permet une extension d'une instance de type ast.Pow"
            self.__dict__ = ast_pow.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Pow"

        def __str__(self):
            return "**"

    class LShift(ast.LShift, ExtendNode):
        def __init__(self, ast_lshift, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_lshift) is ast.LShift, "Cet objet permet une extension d'une instance de type ast.LShift"
            self.__dict__ = ast_lshift.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "LShift"

        def __str__(self):
            return "<<"

    class RShift(ast.RShift, ExtendNode):
        def __init__(self, ast_rshift, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_rshift) is ast.RShift, "Cet objet permet une extension d'une instance de type ast.RShift"
            self.__dict__ = ast_rshift.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "RShift"

        def __str__(self):
            return ">>"

    class BitOr(ast.BitOr, ExtendNode):
        def __init__(self, ast_bitor, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_bitor) is ast.BitOr, "Cet objet permet une extension d'une instance de type ast.BitOr"
            self.__dict__ = ast_bitor.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "BitOr"

        def __str__(self):
            return "|"

    class BitXor(ast.BitXor, ExtendNode):
        def __init__(self, ast_bitxor, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_bitxor) is ast.BitXor, "Cet objet permet une extension d'une instance de type ast.BitXor"
            self.__dict__ = ast_bitxor.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "BitXor"

        def __str__(self):
            return "^"

    class BitAnd(ast.BitAnd, ExtendNode):
        def __init__(self, ast_bitand, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_bitand) is ast.BitAnd, "Cet objet permet une extension d'une instance de type ast.BitAnd"
            self.__dict__ = ast_bitand.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "BitAnd"

        def __str__(self):
            return "&"

    class FloorDiv(ast.FloorDiv, ExtendNode):
        def __init__(self, ast_floordiv, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_floordiv) is ast.FloorDiv, "Cet objet permet une extension d'une instance de type ast.FloorDiv"
            self.__dict__ = ast_floordiv.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "FloorDiv"

        def __str__(self):
            return "//"

    ###########
    # unaryop #
    ###########

    class Invert(ast.Invert, ExtendNode):
        def __init__(self, ast_invert, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_invert) is ast.Invert, "Cet objet permet une extension d'une instance de type ast.Invert"
            self.__dict__ = ast_invert.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Invert"

        def __str__(self):
            return "~"

    class Not(ast.Not, ExtendNode):
        def __init__(self, ast_not, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_not) is ast.Not, "Cet objet permet une extension d'une instance de type ast.Not"
            self.__dict__ = ast_not.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Not"

        def __str__(self):
            return "not"

    class UAdd(ast.UAdd, ExtendNode):
        def __init__(self, ast_uadd, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_uadd) is ast.UAdd, "Cet objet permet une extension d'une instance de type ast.UAdd"
            self.__dict__ = ast_uadd.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = 'UAdd'

        def __str__(self):
            return "+"

    class USub(ast.USub, ExtendNode):
        def __init__(self, ast_usub, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_usub) is ast.USub, "Cet objet permet une extension d'une instance de type ast.USub"
            self.__dict__ = ast_usub.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "USub"

        def __str__(self):
            return "-"

    #########
    # cmpop #
    #########

    class Eq(ast.Eq, ExtendNode):
        def __init__(self, ast_eq, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_eq) is ast.Eq, "Cet objet permet une extension d'une instance de type ast.Eq"
            self.__dict__ = ast_eq.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Eq"

        def __str__(self):
            return "=="

    class NotEq(ast.NotEq, ExtendNode):
        def __init__(self, ast_noteq, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_noteq) is ast.NotEq, "Cet objet permet une extension d'une instance de type ast.NotEq"
            self.__dict__ = ast_noteq.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "NotEq"

        def __str__(self):
            return "!="

    class Lt(ast.Lt, ExtendNode):
        def __init__(self, ast_lt, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_lt) is ast.Lt, "Cet objet permet une extension d'une instance de type ast.Lt"
            self.__dict__ = ast_lt.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Lt"

        def __str__(self):
            return "<"

    class LtE(ast.LtE, ExtendNode):
        def __init__(self, ast_lte, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_lte) is ast.LtE, "Cet objet permet une extension d'une instance de type ast.LtE"
            self.__dict__ = ast_lte.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "LtE"

        def __str__(self):
            return "<="

    class Gt(ast.Gt, ExtendNode):
        def __init__(self, ast_gt, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_gt) is ast.Gt, "Cet objet permet une extension d'une instance de type ast.Gt"
            self.__dict__ = ast_gt.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Gt"

        def __str__(self):
            return ">"

    class GtE(ast.GtE, ExtendNode):
        def __init__(self, ast_gte, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_gte) is ast.GtE, "Cet objet permet une extension d'une instance de type ast.GtE"
            self.__dict__ = ast_gte.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "GtE"

        def __str__(self):
            return ">="

    class Is(ast.Is, ExtendNode):
        def __init__(self, ast_is, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_is) is ast.Is, "Cet objet permet une extension d'une instance de type ast.Is"
            self.__dict__ = ast_is.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "Is"

        def __str__(self):
            return "is"

    class IsNot(ast.IsNot, ExtendNode):
        def __init__(self, ast_isnot, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_isnot) is ast.IsNot, "Cet objet permet une extension d'une instance de type ast.IsNot"
            self.__dict__ = ast_isnot.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "IsNot"

        def __str__(self):
            return "is not"

    class In(ast.In, ExtendNode):
        def __init__(self, ast_in, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_in) is ast.In, "Cet objet permet une extension d'une instance de type ast.In"
            self.__dict__ = ast_in.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "In"

        def __str__(self):
            return "in"

    class NotIn(ast.NotIn, ExtendNode):
        def __init__(self, ast_notin, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_notin) is ast.NotIn, "Cet objet permet une extension d'une instance de type ast.NotIn"
            self.__dict__ = ast_notin.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "NotIn"

        def __str__(self):
            return "not in"

    #########
    # other #
    #########

    class comprehension(ast.comprehension, ExtendNode):
        """
        expr target, expr iter, expr* ifs, int is_async
        """
        def __init__(self, ast_comprehension, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_comprehension) is ast.comprehension, "Cet objet permet une extension d'une instance de type ast.comprehension"
            self.__dict__ = ast_comprehension.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "comprehension"

        def __str__(self):
            return ("async " if self.is_async else "") + "for " \
                + (str(self.overload(self.target)) if type(self.target) is not ast.Tuple else ", ".join((str(self.overload(elt)) for elt in self.target.elts))) \
                + " in " + ("%s" if self._is_monobloc(self.iter) else "(%s)") % str(self.overload(self.iter)) \
                + (" if " + " if ".join((("(%s)" if type(if_) is ast.IfExp else "%s") % str(self.overload(if_))
                    for if_ in self.ifs)) if self.ifs else "")

    class ExceptHandler(ast.ExceptHandler, ExtendNode):
        """
        expr? type, identifier? name, stmt* body
        """
        def __init__(self, ast_exceptHandler, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_exceptHandler) is ast.ExceptHandler, "Cet objet permet une extension d'une instance de type ast.ExceptHandler"
            self.__dict__ = ast_exceptHandler.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "ExceptHandler"

        def __str__(self):
            """
            represente unbloc 'Except'
            """
            code = "except"
            if self.type:
                code += " " + str(self.overload(self.type))
            if self.name:
                code += " as " + self.name
            code += ":\n" + self._indent(self._body_str(self.body))
            return code

    class arguments(ast.arguments, ExtendNode):
        """
        arg* posonlyargs, arg* args, arg? vararg, arg* kwonlyargs, expr* kw_defaults, arg? kwarg, expr* defaults
        """
        def __init__(self, ast_arguments, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_arguments) is ast.arguments, "Cet objet permet une extension d'une instance de type ast.arguments"
            self.__dict__ = ast_arguments.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "arguments"

        def __str__(self):
            """
            represente les argument d'une definition de fonction par example.
            C'est donc de la forme: (...){
                'args': [], # les arguments normaux que l'on trouve au debut
                'vararg': None, # l'argument multiple de type: *args
                'kwonlyargs': [], # tous les arguments precedent une *, ceux que l'on doit appeller en toute lettre
                'posonlyargs': [], # tous les arguments succedant un /, ceux que l'on ne peut pas nommer
                'kw_defaults': [], # les valeurs par defaut des kwonlyargs
                'kwarg': None, # l'argument multiple de type: **kwargs
                'defaults': []} # tous les autre valeurs par defaut
            """
            args_list = []
            # creation des arguments sans les valeurs par defaut
            args_list.extend([str(self.overload(a)) for a in self.args])    # ajout des arguments vraiment classiques
            if "posonlyargs" in self._fields:                               # ajout des argument succedant /
                if self.posonlyargs:
                    args_list.extend([str(self.overload(a)) for a in self.posonlyargs] + ["/"])
            if self.vararg:                                                 # ajout des parametres *args
                args_list.append("*" + str(self.overload(self.vararg)))
            if "kwonlyargs" in self._fields:                                # ajout des arguments precedent *
                if self.kwonlyargs:
                    args_list.extend((["*"] if not self.vararg else []) + [str(self.overload(a)) for a in self.kwonlyargs])
            if self.kwarg:                                                  # ajout des parametres **kwargs
                args_list.append("**" + str(self.overload(self.kwarg)))

            # ajout de valeurs par defaut
            decalage = 1
            for i, defaut in enumerate([d for d in self.kw_defaults + self.defaults if d][::-1]):   # ajout des valeurs par defaut (=truc)
                while "*" in args_list[-i - decalage] or args_list[-i - decalage] == "/":
                    decalage += 1
                args_list[-i - decalage] += "=" + str(self.overload(defaut))

            code = ", ".join(args_list)
            return code

    class arg(ast.arg, ExtendNode):
        """
        identifier arg, expr? annotation, string? type_comment
        """
        def __init__(self, ast_arg, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_arg) is ast.arg, "Cet objet permet une extension d'une instance de type ast.arg"
            self.__dict__ = ast_arg.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "arg"

        def __str__(self):
            """
            represente un argument
            """
            return self.arg

    class keyword(ast.keyword, ExtendNode):
        """
        identifier? arg, expr value
        """
        def __init__(self, ast_keyword, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_keyword) is ast.keyword, "Cet objet permet une extension d'une instance de type ast.keyword"
            self.__dict__ = ast_keyword.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "keyword"

        def __str__(self):
            """
            c'est dans un appel de fonction l'orsque l'on impose la valeur
            """
            if self.arg:
                return self.arg + "=" + str(self.overload(self.value))
            prio = "%s" if self._is_monobloc(self.value) else "(%s)"
            return "**" + prio % str(self.overload(self.value))

    class alias(ast.alias, ExtendNode):
        """
        identifier name, identifier? asname
        """
        def __init__(self, ast_alias, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_alias) is ast.alias, "Cet objet permet une extension d'une instance de type ast.alias"
            self.__dict__ = ast_alias.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "alias"

        def __str__(self):
            """
            permet de metre en forme une variable et son alias
            """
            return self.name + (" as %s" % self.asname if self.asname else "")

    class withitem(ast.withitem, ExtendNode):
        """
        expr context_expr, expr? optional_vars
        """
        def __init__(self, ast_withitem, *args, **kwargs):
            super().__init__(*args, **kwargs)
            assert type(ast_withitem) is ast.withitem, "Cet objet permet une extension d'une instance de type ast.withitem"
            self.__dict__ = ast_withitem.__dict__ # permet de faire un heritage sur des instances d'objets
            self._type = "withitem"

        def __str__(self):
            """
            represente un seul bloc truc [as machin] dans une expression with
            """
            prio = "(%s)" if type(self.context_expr) in [ast.Yield, ast.YieldFrom] else "%s"
            code = prio % str(self.overload(self.context_expr))
            if self.optional_vars:
                code += " as " + str(self.overload(self.optional_vars))
            return code

    grammar_dico[ast.Module] = Module
    grammar_dico[ast.Interactive] = Interactive
    grammar_dico[ast.Expression] = Expression
    grammar_dico[ast.Suite] = Suite

    grammar_dico[ast.FunctionDef] = FunctionDef
    grammar_dico[ast.AsyncFunctionDef] = AsyncFunctionDef
    grammar_dico[ast.ClassDef] = ClassDef
    grammar_dico[ast.Return] = Return
    grammar_dico[ast.Delete] = Delete
    grammar_dico[ast.Assign] = Assign
    grammar_dico[ast.AugAssign] = AugAssign
    grammar_dico[ast.AnnAssign] = AnnAssign
    grammar_dico[ast.For] = For
    grammar_dico[ast.AsyncFor] = AsyncFor
    grammar_dico[ast.While] = While
    grammar_dico[ast.If] = If
    grammar_dico[ast.With] = With
    grammar_dico[ast.AsyncWith] = AsyncWith
    grammar_dico[ast.Raise] = Raise
    grammar_dico[ast.Try] = Try
    grammar_dico[ast.Assert] = Assert
    grammar_dico[ast.Import] = Import
    grammar_dico[ast.ImportFrom] = ImportFrom
    grammar_dico[ast.Global] = Global
    grammar_dico[ast.Nonlocal] = Nonlocal
    grammar_dico[ast.Expr] = Expr
    grammar_dico[ast.Pass] = Pass
    grammar_dico[ast.Break] = Break
    grammar_dico[ast.Continue] = Continue

    grammar_dico[ast.BoolOp] = BoolOp
    grammar_dico[ast.BinOp] = BinOp
    grammar_dico[ast.UnaryOp] = UnaryOp
    grammar_dico[ast.Lambda] = Lambda
    grammar_dico[ast.IfExp] = IfExp
    grammar_dico[ast.Dict] = Dict
    grammar_dico[ast.Set] = Set
    grammar_dico[ast.ListComp] = ListComp
    grammar_dico[ast.SetComp] = SetComp
    grammar_dico[ast.DictComp] = DictComp
    grammar_dico[ast.GeneratorExp] = GeneratorExp
    grammar_dico[ast.Await] = Await
    grammar_dico[ast.Yield] = Yield
    grammar_dico[ast.YieldFrom] = YieldFrom
    grammar_dico[ast.Compare] = Compare
    grammar_dico[ast.Call] = Call
    grammar_dico[ast.FormattedValue] = FormattedValue
    grammar_dico[ast.JoinedStr] = JoinedStr
    grammar_dico[ast.Constant] = Constant
    grammar_dico[ast.Attribute] = Attribute
    grammar_dico[ast.Subscript] = Subscript
    grammar_dico[ast.Starred] = Starred
    grammar_dico[ast.Name] = Name
    grammar_dico[ast.List] = List
    grammar_dico[ast.Tuple] = Tuple

    grammar_dico[ast.Load] = Load
    grammar_dico[ast.Store] = Store
    grammar_dico[ast.Del] = Del
    grammar_dico[ast.AugLoad] = AugLoad
    grammar_dico[ast.AugStore] = AugStore
    grammar_dico[ast.Param] = Param

    grammar_dico[ast.Slice] = Slice
    grammar_dico[ast.ExtSlice] = ExtSlice
    grammar_dico[ast.Index] = Index

    grammar_dico[ast.And] = And
    grammar_dico[ast.Or] = Or

    grammar_dico[ast.Add] = Add
    grammar_dico[ast.Sub] = Sub
    grammar_dico[ast.Mult] = Mult
    grammar_dico[ast.MatMult] = MatMult
    grammar_dico[ast.Div] = Div
    grammar_dico[ast.Mod] = Mod
    grammar_dico[ast.Pow] = Pow
    grammar_dico[ast.LShift] = LShift
    grammar_dico[ast.RShift] = RShift
    grammar_dico[ast.BitOr] = BitOr
    grammar_dico[ast.BitXor] = BitXor
    grammar_dico[ast.BitAnd] = BitAnd
    grammar_dico[ast.FloorDiv] = FloorDiv

    grammar_dico[ast.Invert] = Invert
    grammar_dico[ast.Not] = Not
    grammar_dico[ast.UAdd] = UAdd
    grammar_dico[ast.USub] = USub

    grammar_dico[ast.Eq] = Eq
    grammar_dico[ast.NotEq] = NotEq
    grammar_dico[ast.Lt] = Lt
    grammar_dico[ast.LtE] = LtE
    grammar_dico[ast.Gt] = Gt
    grammar_dico[ast.GtE] = GtE
    grammar_dico[ast.Is] = Is
    grammar_dico[ast.IsNot] = IsNot
    grammar_dico[ast.In] = In
    grammar_dico[ast.NotIn] = NotIn

    grammar_dico[ast.comprehension] = comprehension
    grammar_dico[ast.ExceptHandler] = ExceptHandler
    grammar_dico[ast.arguments] = arguments
    grammar_dico[ast.arg] = arg
    grammar_dico[ast.keyword] = keyword
    grammar_dico[ast.alias] = alias
    grammar_dico[ast.withitem] = withitem


    if identity["python_version"] >= "3.7":
        grammar_dico = update_to_3_7(grammar_dico)
    if identity["python_version"] >= "3.8":
        grammar_dico = update_to_3_8(grammar_dico)
    return grammar_dico

class PyFileReader:
    """
    permet de lire un fichier python pour en extraire un arbre syntaxique
    """
    def __init__(self, file, encoding):
        self.signature = None
        self.file_path = file if type(file) is not io.StringIO else "virtual_file"
        self.encoding = encoding if encoding is not None else "utf-8"
        with open(self.file_path, "r", encoding=self.encoding, errors="replace") as file_pointer:
            self.file_content = file_pointer.read()
        self.grammar = get_grammar(self.signature)

    def __enter__(self):
        """
        permet d'utiliser le mot clef 'with'
        """
        return self

    def __exit__(self, *args):
        return self.close()

    @staticmethod
    def close():
        return None

    def read(self):
        """
        lit le code dans le fichier python met ce
        code dans un objet qui comprend et interagit avec ce code
        l'objet retourne contient de nombreuse fonctionalitees pour
        faire des etudes sur le code
        la representation de l'objet est un code qui fait exactement la meme chose
        que le code lu dans le fichier python
        """
        tree_ast = ast.parse(self.file_content, self.file_path)
        tree_raisin = self.grammar[type(tree_ast)](tree_ast)
        tree_raisin.grammar = self.grammar
        tree_raisin.priorites = { # un nombre eleve represente un fort taux de priorites
                    ast.Or : 1,
                    ast.And : 2,
                    ast.Not : 3,
                    ast.Is : 4,
                    ast.IsNot : 4,
                    ast.In : 4,
                    ast.NotIn : 4,
                    ast.IfExp : 5,
                    ast.Eq : 6,
                    ast.NotEq : 6,
                    ast.Gt : 6,
                    ast.Lt : 6,
                    ast.GtE : 6,
                    ast.LtE : 6,
                    ast.BitXor : 7,
                    ast.BitOr : 7,
                    ast.BitAnd : 8,
                    ast.LShift : 9,
                    ast.RShift : 9,
                    ast.Add : 10,
                    ast.Sub : 10,
                    ast.Mult : 11,
                    ast.Div : 11,
                    ast.FloorDiv : 11,
                    ast.Mod : 11,
                    ast.MatMult : 11,
                    ast.Pow : 12,
                    ast.Invert : 13,
                    ast.UAdd : 13,
                    ast.USub : 13}
        tree_raisin.signature = self.signature
        tree_raisin.father = None
        tree_raisin.file_content = self.file_content

        return tree_raisin
