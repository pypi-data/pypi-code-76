#!/usr/bin/env python3
#-*- coding: utf-8 -*-

__all__ = ["Function"]

import inspect
import logging
import re

import raisin

def _domain(expression, signature, restriction=None):
    """
    cherche pour quelles valeurs l'expression est definie
    retourne un dictionnaire qui a chaque variable (free_symbols), associe son domaine de definition
    cette fonction nessecite raisin.sympy
    en cas d'echec du solveur, le domaine renvoye peut etre plus grand que le vrai domaine
    """
    def inter_d(d1, d2, signature):
        """
        retourne l'intersection de 2 domaines
        d1 et d2 sont les 2 domaine sous forme de dictionaire
        """
        with raisin.Printer("Intersection of %s and %s..." % (d1, d2), signature=signature) as p:
            nouveau_domaine = d1.copy()
            for var, inter in d2.items():
                nouveau_domaine[var] = raisin.sympy.simplify(d1.get(var, inter) & inter)
            p.show(nouveau_domaine)
        return nouveau_domaine

    def union_d(d1, d2, signature):
        """
        retourne l'union de 2 domaines
        d1 et d2 sont les 2 domaines sous forme de dictionaire
        """
        with raisin.Printer("Union of %s and %s..." % (d1, d2), signature=signature) as p:
            nouveau_domaine = d1.copy()
            for var, uni in d2.items():
                nouveau_domaine[var] = raisin.sympy.simplify(d1.get(var, uni) | uni)
            p.show(nouveau_domaine)
        return nouveau_domaine

    def complement_d(d1, set1, signature):
        """
        retourne le domaine set1-d2
        """
        with raisin.Printer("Complement of %s in %s..." % (d1, set1), signature=signature) as p:
            d = {v: raisin.sympy.simplify(set1-d) for v, d in d1.items()}
            p.show(d)
        return d

    def get_symbol_domain(s, signature):
        """
        retourne le dommaine de definition du symbole
        """
        _n = raisin.sympy.Symbol("n", integer=True)
        d = raisin.sympy.Complexes
        with raisin.Printer("Search for the %s domain..." % s, signature=signature) as p:
            if s.is_real:
                d = raisin.sympy.Reals
            elif s.is_imaginary:
                d = raisin.sympy.ComplexRegion(raisin.sympy.FiniteSet(0)*raisin.sympy.Reals, polar=False)
            elif s.is_integer:
                d = raisin.sympy.Integers
            elif s.is_zero:
                d = raisin.sympy.FiniteSet(0)
            if s.is_nonzero:
                d = d - raisin.sympy.FiniteSet(0)
            if s.is_odd: # pair
                d = raisin.sympy.ImageSet(raisin.sympy.Lambda(_n, 2*_n), raisin.sympy.Integers)
            elif s.is_even: # impaire
                d = raisin.sympy.ImageSet(raisin.sympy.Lambda(_n, 2*_n + 1), raisin.sympy.Integers)

            if s.is_negative or s.is_nonpositive:
                d &= raisin.sympy.ImageSet(raisin.sympy.Lambda(_n, -abs(_n)), raisin.sympy.Reals)
            elif s.is_positive or s.is_nonnegative:
                d &= raisin.sympy.ImageSet(raisin.sympy.Lambda(_n, abs(_n)), raisin.sympy.Reals)

            d = raisin.sympy.simplify(d)
            p.show(d)
        return d

    if restriction is None:
        restriction = {}
    assert type(restriction) is dict, "'restriction' doit etre un dictionaire, et non pas un %s." % type(restriction)
    restriction = {str(s):restriction.get(str(s), get_symbol_domain(s, signature)) for s in expression.free_symbols}

    with raisin.Printer("Search for the definition domain of %s..." % expression, signature=signature) as p:
        if type(expression) in [raisin.sympy.numbers.Zero, raisin.sympy.numbers.One, raisin.sympy.numbers.Half, raisin.sympy.numbers.Infinity, raisin.sympy.numbers.NegativeOne, raisin.sympy.numbers.NegativeInfinity]:
            p.show(raisin.sympy.Complexes)
            return {}
        if type(expression) in [raisin.sympy.Integer, raisin.sympy.Rational, raisin.sympy.Float]:
            p.show(raisin.sympy.Complexes)
            return {}
        if type(expression) in [raisin.sympy.numbers.Exp1, raisin.sympy.numbers.Pi, raisin.sympy.numbers.ImaginaryUnit]:
            p.show(raisin.sympy.Complexes)
            return {}
        if type(expression) in [raisin.sympy.Add, raisin.sympy.Mul]:
            terms = expression.as_two_terms()
            restriction = inter_d(_domain(terms[0], signature, restriction=restriction), _domain(terms[1], signature, restriction=restriction), signature)
            p.show(restriction)
            return restriction
        if type(expression) is raisin.sympy.Pow:
            base, exposant = expression.as_base_exp()
            for s in base.free_symbols | exposant.free_symbols:                 # pour chaque variable
                with raisin.Printer("Base risk domain of %s..." % s, signature=signature):
                    try:
                        zonne_a_risque = raisin.sympy.solveset(raisin.sympy.Equality(base, 0), s, domain=restriction[str(s)]) & restriction[str(s)]# on fait en sorte que la base soit non nule
                        p.show(zonne_a_risque)
                    except KeyboardInterrupt as e:
                        raise e from e
                    except:
                        zonne_a_risque = raisin.sympy.EmptySet
                        p.show("Evaluation failed.")
                if zonne_a_risque != raisin.sympy.EmptySet:
                    with raisin.Printer("Reduction of the risk zone...", signature=signature):
                        try:
                            zonne_ok_en_fait = raisin.sympy.solveset(raisin.sympy.Equality(raisin.sympy.arg(exposant), 0), s, domain=zonne_a_risque) & zonne_a_risque
                            p.show(zonne_ok_en_fait)
                        except KeyboardInterrupt as e:
                            raise e from e
                        except:
                            zonne_ok_en_fait = raisin.sympy.EmptySet
                            p.show("Evaluation failed")
                    zonne_a_risque = raisin.sympy.simplify(zonne_a_risque - zonne_ok_en_fait)
                restriction[str(s)] = restriction[str(s)] - zonne_a_risque
            p.show(restriction)
            return restriction
        if type(expression) is raisin.sympy.Symbol:
            p.show(restriction)
            return restriction
        if type(expression) is raisin.sympy.Derivative:
            raise NotImplementedError("Je ne sais pas trouver quand est-ce qu'une derivee est definie.")
        if type(expression) is raisin.sympy.Integral:
            raise NotImplementedError("Je ne sais pas trouver quand est-ce qu'une integrale existe.")
        if type(expression) is raisin.sympy.Piecewise:
            paquets = expression.as_expr_set_pairs()
            d_union = {}
            while paquets:
                d_local = {str(v):paquets[0][1] for v in paquets[0][0].free_symbols}
                d_local = inter_d(_domain(paquets[0][0], signature, restriction=restriction), d_local, signature=signature)
                d_uni = raisin.sympy.simplify(union_d(d_local, d_union, signature=signature))
                del paquets[0]
            restriction = {str(v):d_uni.get(str(v), _domain(v, signature)) for v in expression.free_symbols}
            p.show(restriction)
            return restriction

        raise TypeError("Unable to find the definition domain of an expression of type: %s." % type(expression))

def _is_complex(grandeur):
    """
    retourne True si la grandeur peut etre vue comme une grandeur appartenant a C.
    c'est a dire si cet objet est un reel, un entier, un complexe ou une expression raisin.sympy
    qui reflete un complexe
    retourne False sinon
    """
    if type(grandeur) is float:             # si la grandeur est un flotant
        return True                         # alors elle est complexe comme tout reel est complexe
    if type(grandeur) is int:               # si la grandeur est un entier
        return True                         # de meme tous entier est un complexe
    if type(grandeur) is complex:           # si c'est de type complexe
        return True                         # alors c'est evidement un complexe
    if type(grandeur) is str:               # si la grandeur est une chaine de caractere
        try:                                # on va essayer d'en faire une expression raisin.sympy
            return _is_complex(_to_sympy(grandeur))# puis si on y arrive, on regarde si cette expression donne bien un complexe
        except KeyboardInterrupt as e:
            raise e from e
        except:                             # si on arrive pas a convertir la chaine en expression raisin.sympy
            return False                    # ca ne risque pas d'etre un complexe
    if raisin.sympy:                                # si raisin.sympy est bien importer
        # singleton numbers
        if type(grandeur) in [raisin.sympy.numbers.Zero, raisin.sympy.numbers.One, raisin.sympy.numbers.Half, raisin.sympy.numbers.Infinity, raisin.sympy.numbers.NegativeOne, raisin.sympy.numbers.NegativeInfinity]:# si la grandeur est un nombre
            return True                     # alors c'est un complexe
        # numbers
        if type(grandeur) in [raisin.sympy.Integer, raisin.sympy.Rational, raisin.sympy.Float]:# si c'est un rationel
            return True                     # alors c'est aussi un complexe
        # singleton symbols
        if type(grandeur) in [raisin.sympy.numbers.Exp1, raisin.sympy.numbers.Pi, raisin.sympy.numbers.ImaginaryUnit]:# si c'est un complexe particulier
            return True                     # alors c'est un complexe en general

        # arithmetic operations
        if type(grandeur) in [raisin.sympy.Add, raisin.sympy.Mul, raisin.sympy.Pow]:# si c'est une operation
            if type(grandeur) is raisin.sympy.Pow:
                terms = grandeur.as_base_exp()
            else:
                terms = grandeur.as_two_terms()# on extrai le membre de droite et le membre de gauche de l'opperation
            return _is_complex(terms[0]) and _is_complex(terms[1])# il faut que tous les membres soient complexe

        # symbols
        if type(grandeur) is raisin.sympy.Symbol:   # si l'objet est une variable
            return True                     # alors c'est bon vu que toutes variable est un objet raisin.sympy

        # function values
        if type(grandeur) in [raisin.sympy.Derivative, raisin.sympy.Integral]:# si il s'agit de la derive ou de la primitive d'une fonction
            return True                     # alors on dit que c'est complexe car toutes fonction raisin.sympy est une fonction complexe et que la derive et l'integrale conservent le typage
    
        if type(grandeur) is raisin.sympy.Piecewise:# si l'expression est une expression conditionelle
            for expression, condition in grandeur.as_expr_set_pairs():# il faut allors
                if not _is_complex(expression):# que chaque expression
                    return False            # soit complexe
            return True

        #fonctions
        try:                                # on va voir l'expression est une fonction
            if grandeur.is_Function:        # si c'est le cas
                return True                 # alors comme c'est une fonction au sens raisin.sympy, elle renvoi forcement un complexe
        except AttributeError:              # si ce n'est pas une fonction
            pass

    return False                            # si c'est un autre objet, alors on dit d'office que ce n'est pas un complexe

def _is_numerical(grandeur):
    """
    retourne True si 'grandeur' represente un
    entier, un flottant ou un complexe mais pas litteral
    """
    try:
        nouveau = grandeur.evalf()
    except AttributeError:
        nouveau = grandeur
    try:
        complex(grandeur)
        return True
    except (ValueError, TypeError):
        return False

# def _is_symbol(grandeur):
#     """
#     retourne True si grandeur represente
#     un symbol au sens symbol raisin.sympy
#     """
#     if raisin.sympy is not None:
#         if type(_to_sympy(grandeur)) is raisin.sympy.Symbol:
#             return True
#     elif type(grandeur) is str:
#         with raisin.Printer("Is '%s' a raisin.sympy symbol?..." % grandeur) as p:
#             return raisin.data_manager.pyreader._PyLineDecompozer("", None).is_var(grandeur, p)
#     return False

def _symbolic(func):
    """
    retourne une expression raisin.sympy si l'objet 'func' (un CALLABLE)
    fait du calcul symbolique (ie exact, formel). En cas de doute, retourne None
    l'expression retournee correspondant a la valeur de sortie
    """
    @raisin.timeout_decorator(30)
    def func_bis(*args, **kwargs):
        return func(*args, **kwargs)

    with raisin.Printer("Looking for a formal expression for '%s'..." % func) as p:
        #verification
        try:                        # on s'assure que la fonction soit bien une fonction
            func.__call__           # pour cela on regarde qu'elle soit callable
        except AttributeError as e: # si elle n'est pas calable
            raise TypeError("The function '%s' is not callable." % func) from e# on genere une erreur

        #cas des objets _Simple_Function
        if type(func) is _Simple_Function:
            if func.symbolic is not None:
                p.show("The test is already done.")
                return func.symbolic
            else:
                func = func.func
        
        #cas des objet sympy_Callable
        if type(func) is type(_sympy_to_func("")):
            p.show("It is already a formal equation.")
            return func.expression
        
        #premiere tentative jolie
        try:
            args_signature = func.args
        except AttributeError:
            args_signature = [p.name for p in inspect.signature(func).parameters.values() if p.kind not in [p.VAR_POSITIONAL, p.VAR_KEYWORD]]# recuperation des parametres
        try:                        # pour trouver l'equation formelle d'une fonction
            with raisin.Printer("Trying to make a symbolic computation..."):
                return _to_sympy(func_bis(**{a:raisin.sympy.Symbol(str(a)) for a in args_signature}))# il suffit de l'evaluer partout a la fois
        except KeyboardInterrupt as e:
            raise e from e
        except:                     # mais bon on arrive pas toujours a le faire
            pass

        #autres cas
        return None
        raise NotImplementedError   # pour ne pas oublier de terminer cette fonction

def _sympy_to_func(expression):
    """
    'expression' est une expression raisin.sympy
    """
    class sympy_Callable:
        """
        objet callable travaillant sur une expression raisin.sympy
        """
        def __init__(self, expression):
            self.expression = expression    # expression raisin.sympy

        def __call__(self, **kwargs):
            """
            aucune verification n'est effectuee a ce niveau
            toute verification doit etre faite en amont
            """
            dico_replacement = {s: kwargs[str(s)] for s in self.expression.free_symbols}
            return self.expression.subs(dico_replacement, simultaneous=True)

    return sympy_Callable(expression)

def _to_sympy(chaine):
    """
    convertit cette chaine de caractere ou cet objet deja de type raisin.sympy en expression raisin.sympy
    retourne l'expression raisin.sympy
    si raisin.sympy n'est pas installe, ou qu'il y a un probleme de conversion renvoie une erreur
    """
    if raisin.sympy:                                # si le module raisin.sympy est present
        try:                                # on va tenter de convertir l'expression en graph raisin.sympy
            return raisin.sympy.sympify(chaine) # on ne fait aucune simplification de facon a aller le plus vite possible
        except raisin.sympy.SympifyError as e:      # si la convertion a echouee
            if raisin.giacpy is not None:           # si raisin.giacpy est importe
                return raisin.sympy.sympify(str(raisin.giacpy.giac(chaine)))# on tente avec lui car il connait les operations implicites
            else:
                raise e
    raise ImportError("The 'raisin.sympy' module is not installed, it is therefore impossible to convert a 'str' into a 'raisin.sympy' expression!")#si il n'y a pas raisin.sympy, on ne tente rien du tout

def to_set(expr):
    """
    renvoi l'expression sous la forme d'un interval raisin.sympy
    """
    assert raisin.sympy is not None, "The 'raisin.sympy' module is necessary to convert an expression to an interval"
    assert sympy is not None, "The 'sympy' module is necessary to convert an expression to an interval."
    if _is_complex(expr):
        return raisin.sympy.FiniteSet(expr)
    elif type(expr) in [
        raisin.sympy.Complement, raisin.sympy.EmptySet, raisin.sympy.FiniteSet, raisin.sympy.Intersection,
        raisin.sympy.Interval, raisin.sympy.ProductSet, raisin.sympy.SymmetricDifference, raisin.sympy.Union,
        raisin.sympy.UniversalSet, raisin.sympy.ImageSet, raisin.sympy.ComplexRegion, raisin.sympy.ConditionSet,
        raisin.sympy.Naturals, raisin.sympy.Naturals0, raisin.sympy.Integers, raisin.sympy.Reals, raisin.sympy.Complexes]:
        return expr
    elif type(expr) is list:
        return list(map(to_set, expr))
    elif type(expr) is tuple:
        return tuple(map(to_set, expr))
    elif type(expr) is set:
        return set(map(to_set, expr))
    elif type(expr) is dict:
        return {v: to_set(e) for v,e in expr.items()}
    raise ValueError("Impossible to convert %s (type %s) into a raisin.sympy set." % (expr, type(expr)))

def _regressi(func):
    """
    cherche un modele qui semble s'approcher au plus pres
    de 'func'
    'func' est une fonction de C dans C
    """
    with raisin.Printer("Looking for a model for '%s'..." % func):
        if raisin.sympy is None:
            raise ImportError("'raisin.sympy' is required to search for an approximate expression.")
        raise NotImplementedError

# class _Simple_Function:
#     """
#     c'est une fonction allant de C**n dans C
#     """
#     def __init__(self, func, name=None, fixed=set(), domain={}, formal=None, signature=None, **kwargs):
#         """
#         examples:
#         >>> def g(x, y):
#         ...     return x**2 + y**2
#         >>> def h(x, y, a=0):
#         ...     return g(x, y) + a

#         >>> _Simple_Function(g)
#         g : (x, y) ↦ g(x, y)
#         >>> _Simple_Function(h)
#         h : (a=0, x, y) ↦ h(a, x, y)

#         >>> _Simple_Function(g, name="f", fixed="x")
#         fₓ : y ↦ fₓ(y)
#         >>> _Simple_Function(h, name="fonc4D", fixed=("a","x"))
#         fonc4Dₓˏₐ₌₀ : y ↦ fonc4Dₓˏₐ₌₀(y)

#         >>> _Simple_Function(h, x=3)
#         h : (a=0, x=3, y) ↦ h(a, x, y)
#         >>> _Simple_Function(h, x=3, a=1)
#         h : (a=1, x=3, y) ↦ h(a, x, y)

#         >>> _Simple_Function("a+b")
#         f : (a, b) ↦ a + b
#         >>> _Simple_Function(1)
#         f : x ↦ 1
#         """
#         self.func = func                # objet pouvant etre vu comme un callable.
#         self.name = name                # nom de cet objet (pour la methode __str__).
#         self.fixed = set(fixed)         # ensemble qui recence tous les parametres fixes en STR, non pas en 'raisin.sympy'.
#         self.domain = domain            # dictionaire qui a chaque variable (STR), associ l'expression raisin.sympy de son domaine de definition.
#         self.kwargs = kwargs            # sauvegrade de tous nessesaire lorsqu'on fait une copie vrai de l'objet
#         self.args = []                  # tous les parametres (STR) dans l'ordre de la signature de self.func ou dans l'ordre alphabetique sinon. les *args et **kargs n'apparaissent pas ici.
#         self.default = {}               # dictionaire qui a chaque variable (STR), associ ca valeur par defaut.
#         self.symbolic = None            # expression raisin.sympy de la fonction si celle si peut etre vue comme une fonction formelle.
#         self.var_positional = False     # est True si la methode __call__ de func contient un argument du type *args
#         self.var_keyword = False        # est True si la methode __call__ de func contient un kargs du genre **kwargs
#         self.signature = signature

#         with raisin.Printer("Converting '%s' to simple function..." % self.func):
#             # mise en forme de func
#             if callable(self.func):     # on teste si l'objet est un 'callable'
#                 if formal is True or formal is None:# si rien ne nous interdit de tenter de faire un peu de calcul formel
#                     self.symbolic = _symbolic(self.func)# on tente de comprendre le mecanisme de self.func afin d'en extraire une equation formelle
#                 elif formal is False:# si par contre il ne faut rien faire du tout en formel
#                     self.symbolic = None# on ne cherche pas a en faire du coup
#                 else:               # si le message n'est pas clair
#                     raise ValueError("'formal' can only be 'True', 'False' or 'None', no %s." % formal)# on rouspette
#                 self.var_positional = True if [p for p in inspect.signature(self.func).parameters.values() if p.kind is p.VAR_POSITIONAL] else False# on regarde si il y a une *args
#                 self.var_keyword = True if [p for p in inspect.signature(self.func).parameters.values() if p.kind is p.VAR_KEYWORD] else False# on regarde si il y a une **kwargs
#                 args_signature = [p.name for p in inspect.signature(self.func).parameters.values() if p.kind not in [p.VAR_POSITIONAL, p.VAR_KEYWORD]]# ajout des parametres issue de __call__
#                 if self.symbolic is None:# si on ne connait pas l'equation formelle qui regit self.func
#                     args_expression = {}# alors il n'y a pas dautre parametres
#                 else:                   # par contre, si on connait l'equation formelle
#                     args_expression = sorted(map(str, self.symbolic.free_symbols))# on va regarder qu'il n'y ai pas des arguments en plus
#                 self.args = [a for a in args_expression if a not in args_signature] + args_signature# on raboute les 2 afin d'avoir tous les arguments
#                 default_signature = {p.name: p.default for p in inspect.signature(self.func).parameters.values() if p.default is not inspect._empty}# valeur par defaut inscrite dans self.func.__call__
#                 default_given = {a: kwargs[a] for a in self.args if a in kwargs}# recuperations des valeurs par defaut
#                 self.default = {**default_given, **{a: v for a, v in default_signature.items() if a not in default_given}}# on raboute les deux en donnant priorite au valeurs par defaut passe en parametre plutot que celle definie dans la signature de self.func.__call__
#                 if raisin.sympy is not None:    # si raisin.sympy est installe
#                     given_domain = {a: self.domain.get(a, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) for a in self.args}# domaine de definition impose par l'utilisateur
#                     if self.symbolic is not None:# si on connait l'equation qui regit la fonction
#                         sympy_domain = _domain(self.symbolic)# on regarde aussi le domaine de definition donne par l'equation
#                         self.domain = {a: sympy_domain.get(a, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) & given_domain[a] for a in self.args}# on raboutte alors les 2 domaines
#                     else:               # si la fonction est trop complique pour en extraire une equation formelle
#                         self.domain = given_domain# on se contente de faire confience a ce que nous impose l'utilisateur
#                 if type(self.func) is _Simple_Function:# si l'objet que l'on manipule depuis toute a l'heure contient d'autres infos interressantes
#                     self.fixed |= self.func.fixed# on recupere ces informations
#                     self.var_positional = self.func.var_positional# donc le fait que les parametres soit
#                     self.var_keyword = self.func.var_keyword# plus ou moins bien specifies
#                     if self.func.domain and raisin.sympy is not None:# si l'objet callable contient un domaine de definition
#                         self.domain = {a: self.domain[a] & self.func.domain.get(a, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) for a in self.args}# on le prend en compte
#             else:                       # si l'objet n'est pas callable
#                 try:                    # on va essayer d'en faire un callable
#                     self.symbolic = _to_sympy(self.func)# on passe donc par raisin.sympy, on tente de convertir l'expression en objet raisin.sympy
#                     self.func = _sympy_to_func(self.symbolic)# puis on fait de cette expression un callable
#                     self.args = sorted(map(str, self.symbolic.free_symbols))# recuperation de tous le parametres
#                     self.default = {a: kwargs[a] for a in self.args if a in kwargs}# ce sont les parametres par defaut
#                     sympy_domain = _domain(self.symbolic, self.signature)# domaine maximum de definition
#                     given_domain = {a: self.domain.get(a, raisin.sympy.Complexes) for a in self.args}# domaine de definition impose
#                     self.domain = {a: sympy_domain[a] & given_domain[a] for a in self.args}# recuperation du domaine de definition
#                     if formal is False: # si l'on ne veut pas faire de calcul formel
#                         self.symbolic = None# alors on cache le fait que l'on est entrain d'en faire
#                     elif formal is True or formal is None:# simple verification pour la loie de meurfi
#                         pass
#                     else:
#                         raise ValueError("'formal' can only be 'True', 'False' or 'None', no %s." % formal)# on rouspette
#                 except KeyboardInterrupt as e:
#                     raise e from e
#                 except Exception as e:  # si ca non plus ca ne fonctionne pas
#                     raise Exception("'%s' ne peut pas etre vu comme une fonction de C**k dans C." % self.func) from e# alors on renvoi la cause de l'erreur
#             if not self.args:           # si aucun argument n'est nessecaire
#                 self.args = ["x"]       # on en met quand meme un hitoire de dire quoi...

#             #identifiant
#             if self.name is None:       # si il n'y a aucun identifiant de specifie
#                 try:                    # on va tenter de prendre le nom de l'argument callable
#                     self.name = self.func.__name__# on recupere donc le nom de l'objet
#                     assert self.name not in [None, "<lambda>"]#seulement si il n'est pas trop pourris
#                 except:                 # si le nom est vraiment trop mausvais
#                     if self.symbolic:
#                         # self.name = [varname for varname, value in globals().items() if value is self][0]
#                         self.name = str(self.symbolic) if re.match(r"(?:(?P<complex>[\+\-\s]*(?:(?:[0-9]+\.?[0-9]*)|(?:[0-9]*\.?[0-9]+))(?:e[\+\-]?[0-9]+)*j)|(?:[a-zA-Z_\x7f-\U000fffff][a-zA-Z0-9_\x7f-\U000fffff]*)|(?P<flotant>[\+\-\s]*(?:(?:(?:\.[0-9]+)|(?:[0-9]+\.[0-9]*))(?:e[\+\-]?[0-9]+)*|(?:[0-9]+e[\+\-]?[0-9]+)))|(?P<entier>[\+\-\s]*(?:0b[01]+)|(?:0o[0-7]+)|(?:0x[0-9a-fA-F]+)|(?:[0-9]+)))", str(self.symbolic)) else "f"# on met 'f', car f ca fait bien pensser a une fonction
#                     else:
#                         self.name = str(self.func) if re.match(r"(?:(?P<complex>[\+\-\s]*(?:(?:[0-9]+\.?[0-9]*)|(?:[0-9]*\.?[0-9]+))(?:e[\+\-]?[0-9]+)*j)|(?:[a-zA-Z_\x7f-\U000fffff][a-zA-Z0-9_\x7f-\U000fffff]*)|(?P<flotant>[\+\-\s]*(?:(?:(?:\.[0-9]+)|(?:[0-9]+\.[0-9]*))(?:e[\+\-]?[0-9]+)*|(?:[0-9]+e[\+\-]?[0-9]+)))|(?P<entier>[\+\-\s]*(?:0b[01]+)|(?:0o[0-7]+)|(?:0x[0-9a-fA-F]+)|(?:[0-9]+)))", str(self.func)) else "f"
#             self.__name__ = self.name

#             #forcage a faire du formel
#             if formal is True and self.symbolic is None:# si l'on doit faire du formel mais que l'on a pas reussi a en faire
#                 with raisin.Printer("Pseudoformal calculation interpolation..."):
#                     self.symbolic = _regressi(self)

#     def __abs__(self):
#         """
#         returne abs(self)
#         """
#         class Abs:
#             def __init__(self, f):
#                 self.f = f
#             def __call__(self, **f_kwargs):
#                 """
#                 ne fait aucune verification
#                 toute verification doit etre faite en amont
#                 """
#                 return abs(self.f(**f_kwargs))

#         with raisin.Printer("Calculation of abs(%s)..." % self):
#             name = "Abs(%s)" % self.__name__
#             if self.symbolic is not None:   # si on connait l'expression formelle
#                 return _Simple_Function(abs(self.symbolic), name=name, fixed=self.fixed, domain=self.domain, **self.kwargs)
#             return _Simple_Function(Abs(self), name=name, fixed=self.fixed, domain=self.domain, **self.kwargs)

#     def __add__(self, other):
#         """
#         permet d'ajouter other a self
#         appelle par 'self + other'
#         """
#         class Sum:
#             def __init__(self, f, g):
#                 self.f = f
#                 self.g = g
#                 self.correspondance = {f.args[i]: g.args[i] for i in range(len(f.args))}
#             def __call__(self, **f_kwargs):
#                 """
#                 ne fait aucune verifications
#                 toute verification doit etre faite en amont
#                 """
#                 g_kwargs = {self.correspondance[a]:v for a, v in f_kwargs.items()}
#                 return self.f(**f_kwargs) + self.g(**g_kwargs)

#         with raisin.Printer("Calculation of %s + %s..." % (self, other)):

#             if type(other) is not _Simple_Function:
#                 logging.warning("The sum expressions are not homogeneous, %s will be converted to a function." % other)
#                 try:
#                     name = other.__name__
#                 except AttributeError:
#                     name = str(other) if " " not in str(other) else "f"
#                 return self + _Simple_Function(other, name=name)

#             #egalisation du nombre de parametres
#             moi = self
#             if len(self.args) > len(other.args):
#                 other = _Simple_Function(other)
#                 other.args += sorted(set(self.args)-set(other.args))[:len(self.args)-len(other.args)]
#             elif len(self.args) < len(other.args):
#                 moi = _Simple_Function(self)
#                 moi.args += sorted(set(other.args)-set(self.args))[:len(other.args)-len(self.args)]
            
#             #preparation
#             correspondance = {other.args[i]: moi.args[i] for i in range(len(moi.args))}# a chaque variable dans other, on lui associ un non dans self
#             bij_correspondance = {moi.args[i]: other.args[i] for i in range(len(moi.args))}
#             nouveau_name = "Sum(%s, %s)" % (moi.__name__, other.__name__)# cela va etre le nouveau nom de la fonction
#             nouveau_fixed = moi.fixed & {correspondance[a] for a in other.fixed}# on recupere toutes les informations de la nouvelle fonction
#             nouveau_args = sorted(set(moi.args) | set([correspondance[a] for a in other.args]))# c'est vrai pour les arguments
#             if raisin.sympy is not None:
#                 nouveau_domain = {a: moi.domain.get(a, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) & other.domain.get(bij_correspondance[a], raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) for a in nouveau_args}# car la fonction f(g) herite en grosse partie des caracteristiques de g
#             else:
#                 nouveau_domain = {}
#             nouveau_default = {a: moi.default.get(a, other.default.get(bij_correspondance[a], None)) for a in nouveau_args if moi.default.get(a, None) != other.default.get(bij_correspondance[a], None) and a in moi.default or bij_correspondance[a] in other.default}# et leur valeurs
#             nouveau_var_positional = moi.var_positional and other.var_positional
#             nouveau_var_keyword = moi.var_keyword and other.var_keyword
#             if moi.symbolic is not None and other.symbolic is not None:# si on a affaire a 2 fonctions dont on connait l'expression
#                 nouveau_func = moi.symbolic + other.symbolic.subs(correspondance, simultaneous=True)# c'est un jeu d'enfant
#             else:               # par contre si l'une des 2 au moin n'est pas formelle
#                 nouveau_func = Sum(moi, other)# et bien on fait une fonction qui calcul point par point
                    
#             #restitution
#             fonction = _Simple_Function(nouveau_func, name=nouveau_name, fixed=nouveau_fixed, domain=nouveau_domain)
#             fonction.args = nouveau_args# on injecte de force les parametres que l'on viens de sauver
#             fonction.default = nouveau_default
#             fonction.var_positional = nouveau_var_positional
#             fonction.var_keyword = nouveau_var_keyword
#             return fonction

#     def __bool__(self):
#         """
#         retourne True si la fonction n'est pas la fonction nulle
#         de partout en cas de doute, retourne True
#         """
#         if self.symbolic is not None:
#             return bool(self.symbolic)
#         return True

#     def __call__(self, *args, **kwargs):
#         """
#         Il y a 3 fonctionalites a cette methode:
#             -Evaluer en un point numerique la fonction afin de resortir un complexe numerique.
#             -Evaluer la fonction en une autre fonction, fait donc une loie de composition et retourne une nouvelle fonction.
#             -Changer les parametres de la fonction. Ils peuvent etre renomes, ajoutes ou supprimes.
#         examples:
#         si ils ne sont pas specifier explicitement, les arguments sont classe par ordre alphabetique
#         >>> def f(x, y, z=0):
#         ...     return x**2+y**2-z
#         >>> g = _Simple_Function(f, name="g")
#         >>> g(2, 2)
#         8
#         >>> g(2, 2, 1)
#         7
#         >>> g(2, 2, z=1)
#         7
#         >>> g(x=2, y=2)
#         8

#         >>> f = _Simple_Function((lambda x : x**2), name="f")
#         >>> h = _Simple_Function((lambda y : 2*y), name="h")
#         >>> r1 = f(h)
#         >>> r2 = h(f)
#         >>> print(r1, r2)
#         (f o h) : y ↦ (f o h)(y)
#         (h o f) : x ↦ (h o f)(x)
#         >>> r1(10)
#         400
#         >>> r2(10)
#         200
#         """
#         class Composition:
#             def __init__(self, f, g):
#                 self.f = f
#                 self.g = g
#             def __call__(self, *args, **kwargs):
#                 return self.f(self.g(*args, **kwargs))

#         class Change_Args:
#             def __init__(self, old_func, correspondance, nouveau_args):
#                 self.old_func = old_func
#                 self.correspondance = correspondance# encien vers nouveau
#                 self.nouveau_args = nouveau_args
#                 self.args = self.nouveau_args# pour l'avaluation formelle

#             def __call__(self, *args, **kwargs):
#                 return self.old_func(*args, **{oa: self.correspondance[oa] if self.correspondance[oa] not in kwargs else kwargs[self.correspondance[oa]] for oa in self.correspondance})

#         with raisin.Printer("Evaluation of %s with args:%s and kwargs:%s..." % (self, args, kwargs)):

#             # loie de composition f(g)
#             if len(args) == 1 and not kwargs:# si il y a juste un parametre et rien d'autre
#                 if type(args[0]) is _Simple_Function:# et que ce parametre est une fonction
#                     with raisin.Printer("Internal composition law..."):
#                         assert len(self.args) == 1, "'%s' requires %d input parameters, but '%s' returns only one parameter.\nSo it is impossible to do%s(%s)." % (self.__name__, len(self.args), args[0].__name__, self.__name__, args[0].__name__)
#                         nouveau_name = "(%s o %s)" % (self.__name__, args[0].__name__)# cela va etre le nouveau nom de la fonction
#                         nouveau_fixed = args[0].fixed# on recupere toutes les informations de la nouvelle fonction
#                         nouveau_domain = args[0].domain# car la fonction f(g) herite en grosse partie des caracteristiques de g
#                         nouveau_args = args[0].args# c'est vria pour les arguments
#                         nouveau_default = args[0].default# et leur valeurs
#                         nouveau_var_positional = args[0].var_positional
#                         nouveau_var_keyword = args[0].var_keyword
#                         if self.symbolic is not None and args[0].symbolic is not None:# si on a affaire a 2 fonctions dont on connait l'expression
#                             nouveau_func = self(args[0].symbolic)# c'est un jeu d'enfant
#                         else:               # par contre si l'une des 2 au moin n'est pas formelle
#                             nouveau_func = Composition(self, args[0])# et bien on fait une fonction qui calcul point par point
#                         fonction = _Simple_Function(nouveau_func, name=nouveau_name, fixed=nouveau_fixed, domain=nouveau_domain)
#                         fonction.args = nouveau_args# on injecte de force les parametres que l'on viens de sauver
#                         fonction.default = nouveau_default
#                         fonction.var_positional = nouveau_var_positional
#                         fonction.var_keyword = nouveau_var_keyword
#                         return fonction

#             # protection contre la loi de meurfi
#             change_args = False
#             for i,a in enumerate(args):
#                 if _is_symbol(a):
#                     change_args = True
#                     continue
#                 if not _is_numerical(a):
#                     raise TypeError("Arguments must be a symbol or a numeric value, not %s!" % a)
#             for a in self.args:
#                 if a in kwargs:
#                     if _is_symbol(a):
#                         change_args = True
#                         continue
#                     if not _is_numerical(a):
#                         raise TypeError("Arguments must be a symbol or a numeric value, not %s!" % a)

#             if change_args:
#                 with raisin.Printer("Changing parameters configuration..."):
#                     correspondance = {}     # a chaque non de variable, on associ le nouveau nom
#                     nouveau_args = []       # liste de tous les nouveaux arguments
#                     generator_given_args = iter(args)
#                     for a in self.args:     # pour chacun des arguments actuels
#                         if a in kwargs:     # si cet argument est specialement specifie
#                             correspondance[a] = str(kwargs[a]) if not _is_numerical(kwargs[a]) else eval(str(kwargs[a])) # on le recupere
#                             if _is_symbol(kwargs[a]):
#                                 nouveau_args.append(str(kwargs[a]))
#                             continue
#                         try:
#                             suivant = next(generator_given_args)
#                         except StopIteration:
#                             suivant = None
#                         if suivant is not None:
#                             correspondance[a] = str(suivant) if not _is_numerical(suivant) else eval(str(suivant))
#                             if _is_symbol(suivant):
#                                 nouveau_args.append(str(suivant))
#                             continue
#                         elif a in self.default:
#                             correspondance[a] = self.default[a]
#                         raise Exception("Argument %s is not specified." % a)
#                     surplus_args = sorted(set((str(a) for a in generator_given_args if _is_symbol(a) and str(a) not in nouveau_args)))
                    
#                     fixed = {correspondance[a] for a in self.fixed}
#                     domain = {correspondance[a]:d for a, d in self.domain.items()}
#                     new_callable = Change_Args(self.func, correspondance, nouveau_args)
#                     nouvelle_func = _Simple_Function(new_callable, name=self.__name__, fixed=fixed, domain=domain, formal=False)
#                     nouvelle_func.args = nouveau_args+surplus_args
#                     nouvelle_func.var_positional = self.var_positional
#                     nouvelle_func.var_keyword = self.var_keyword
#                     nouvelle_func.symbolic = _symbolic(nouvelle_func)
#                     return nouvelle_func


#             with raisin.Printer("Numerical evaluation..."):
#                 # recuperation des **kwargs
#                 if self.var_keyword:        # si la fonction que l'on s'apprete appeller contient un argument du genre **kwargs
#                     kwargs_only = {**kwargs, **{a: v for a, v in self.default.items() if a not in kwargs}}# on ajoute aux mot clef donne en parametre, la valeur par default des variables, si celle ci n'est pas ecraser par une nouvelle valeur specifiee
#                 else:                       # dans le cas ou self.func axcepte un nombre fini de parametre assigne (avec le =)
#                     given_util_kwargs = {a:kwargs[a] for a in self.args if a in kwargs}# on recupere les kwargs qui vont servir a queqlque chose
#                     if len(kwargs) > len(given_util_kwargs):# si tous les parametres specifier ne servent pas
#                         surplus_kwargs = {a: v for a, v in kwargs.items() if a not in given_util_kwargs}# on met de cote tous les parametre ignores
#                         logging.warning("Arguments %s are specified but are ignored" % surplus_kwargs)# afin de le crier haut et fort et de ne pas le cacher sous le tapis
#                     kwargs_only = {**given_util_kwargs, **{a: v for a, v in self.default.items() if a not in given_util_kwargs}}# c'est l'ensemble exaustif des kwargs

#                 #recuperation des *args
#                 surplus = len(args) - len(self.args) + len(kwargs_only)# c'est le nombre d'argument en trop
#                 assert surplus >= 0, "%d argument(s) missing." % -surplus# si il manque des arguments, on revoi une erreur
#                 default = {a:v for a, v in self.default.items() if a not in kwargs}# on recupere tous les arguments que l'on s'aprete a fixer arbitrairement
#                 if surplus > 0 and not self.var_positional:# si au contraire, il y a des arguments en trop et qu'il n'y a pas de place pour les acceullir
#                     if surplus > len(default):  # si il y a plus d'argument que de place
#                         raise Exception("%d arguments are specified: %s\n%d key arguments are specified %s.\nSo there are %d extra arguments for 3 default parameters only: %d." % (len(args), args, len(kwargs_only), kwargs_only, surplus, len(default), default))
#                     if surplus < len(default):  # si il n'y a pas suffisement d'arguments pour emplacer tous les parametre par defaut
#                         raise Exception("%d arguments are specified: %s\n%d key arguments are specified %s.\nSo there are only %d arguments while there are %d default parameters: %s." % (len(args), args, len(kwargs_only), kwargs_only, surplus, len(default), default))
#                 generator_given_args = iter(args)# on transforme les arguments donnes en parametre par un iterateur
#                 if surplus:
#                     all_kwargs = {**kwargs_only, **{a:next(generator_given_args) for a in self.args if a not in kwargs_only or a in default}}
#                 else:
#                     all_kwargs = {**kwargs_only, **{a:next(generator_given_args) for a in self.args if a not in kwargs_only}}
#                 all_args = tuple(generator_given_args)# on recupere l'exedent d'arguments

#                 #evaluation de la fonction
#                 return self.func(*all_args, **all_kwargs)# on evalue la fonction avec les parametres fraichement fixes

#     def __contains__(self, other):
#         """
#         retourne la condition pour que
#         other soit contenu dans self.
#         retourne True ou false si c'est toujours ou jamais le cas
#         """
#         raise NotImplementedError

#     def __eq__(self, other):
#         """
#         retourne True si la fonction
#         other est egale en tous points a self
#         et que les intervalles de definitions sont les memes
#         en cas de doute, retourne False
#         """
#         raise NotImplementedError

#     def __mul__(self, other):
#         """
#         permet de multiplier self a other
#         appele par 'self * other'
#         """
#         class Mul:
#             def __init__(self, f, g):
#                 self.f = f
#                 self.g = g
#                 self.correspondance = {f.args[i]: g.args[i] for i in range(len(f.args))}
#             def __call__(self, **f_kwargs):
#                 """
#                 ne fait aucune verifications
#                 toute verification doit etre faite en amont
#                 """
#                 g_kwargs = {self.correspondance[a]:v for a, v in f_kwargs.items()}
#                 return self.f(**f_kwargs) * self.g(**g_kwargs)

#         if type(other) is not _Simple_Function:
#             try:
#                 name = other.__name__
#             except AttributeError:
#                 name = str(other) if " " not in str(other) else "constant"
#             return self * _Simple_Function(other, name=name)

#         with raisin.Printer("Calculation of '%s' * '%s'..." % (self, other)):

#             #egalisation du nombre de parametres
#             moi = self
#             if len(self.args) > len(other.args):
#                 other = _Simple_Function(other)
#                 other.args += sorted(set(self.args)-set(other.args))[:len(self.args)-len(other.args)]
#             elif len(self.args) < len(other.args):
#                 moi = _Simple_Function(self)
#                 moi.args += sorted(set(other.args)-set(self.args))[:len(other.args)-len(self.args)]

#             #preparation
#             correspondance = {other.args[i]: moi.args[i] for i in range(len(moi.args))}# a chaque variable dans other, on lui associ un non dans self
#             bij_correspondance = {moi.args[i]: other.args[i] for i in range(len(moi.args))}
#             nouveau_name = "Mul(%s, %s)" % (moi.__name__, other.__name__)# cela va etre le nouveau nom de la fonction
#             nouveau_fixed = moi.fixed & {correspondance[a] for a in other.fixed}# on recupere toutes les informations de la nouvelle fonction
#             nouveau_args = sorted(set(moi.args) | set([correspondance[a] for a in other.args]))# c'est vrai pour les arguments
#             if raisin.sympy is not None:
#                 nouveau_domain = {a: moi.domain.get(a, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) & other.domain.get(bij_correspondance[a], raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) for a in nouveau_args}# car la fonction f(g) herite en grosse partie des caracteristiques de g
#             else:
#                 nouveau_domain = {}

#             nouveau_default = {a: moi.default.get(a, other.default.get(bij_correspondance[a], None)) for a in nouveau_args if moi.default.get(a, None) != other.default.get(bij_correspondance[a], None) and a in moi.default or bij_correspondance[a] in other.default}# et leur valeurs
#             nouveau_var_positional = moi.var_positional and other.var_positional
#             nouveau_var_keyword = moi.var_keyword and other.var_keyword
#             if moi.symbolic is not None and other.symbolic is not None:# si on a affaire a 2 fonctions dont on connait l'expression
#                 nouveau_func = moi.symbolic * other.symbolic.subs(correspondance, simultaneous=True)# c'est un jeu d'enfant
#             else:               # par contre si l'une des 2 au moin n'est pas formelle
#                 nouveau_func = Mul(moi, other)# et bien on fait une fonction qui calcul point par point

#             #restitution
#             fonction = _Simple_Function(nouveau_func, name=nouveau_name, fixed=nouveau_fixed, domain=nouveau_domain)
#             fonction.args = nouveau_args# on injecte de force les parametres que l'on viens de sauver
#             fonction.default = nouveau_default
#             fonction.var_positional = nouveau_var_positional
#             fonction.var_keyword = nouveau_var_keyword
#             return fonction

#     def __neg__(self):
#         """
#         return -self
#         """
#         class Neg:
#             def __init__(self, f):
#                 self.f = f
#             def __call__(self, **f_kwargs):
#                 """
#                 ne fait aucune verifications
#                 toute verification doit etre faite en amont
#                 """
#                 return -self.f(**f_kwargs)
        
#         with raisin.Printer("Calculation of -('%s')..." % self):
#             name = "Neg(%s)" % self.__name__
#             if self.symbolic is not None:   #si on connait l'expression formelle
#                 return _Simple_Function(-self.symbolic, name=name, fixed=self.fixed, domain=self.domain, **self.kwargs)
#             return _Simple_Function(Neg(self), name=name, fixed=self.fixed, domain=self.domain, **self.kwargs)

#     def __pos__(self):
#         """
#         retourne la valeur positive de cette fonction, c'est a dire elle meme. (appelle par '+self')
#         retourne self directement, en faisant une copie tout de meme
#         """
#         return self.copy()

#     def __pow__(self, other):
#         """
#         retourne self**other
#         """
#         return NotImplementedError

#     def __radd__(self, other):
#         """
#         permet d'ajouter other a self
#         appele par 'other + self'
#         """
#         return self + other     #on profite de la commutativite de la loie + chez les complexes

#     def __repr__(self):
#         fixe = raisin.str(",".join((f if f not in self.default else "%s=%s" % (f, self.default[f]) for f in self.fixed))).indice()
#         if self.var_positional or self.var_keyword:
#             args = ", ".join(sorted(set(self.args)-self.fixed)+["..."])
#         else:
#             args = ", ".join(sorted(set(self.args) - self.fixed))
#         if args == "":
#             args = "x"
#         if ", " in args:
#             tuple_args = "(%s)" % ", ".join((f if f not in self.default else "%s=%s" % (f, self.default[f]) for f in sorted(set(self.args)-self.fixed)))
#         else:
#             tuple_args = ", ".join((f if f not in self.default else "%s=%s" % (f, self.default[f]) for f in sorted(set(self.args)-self.fixed)))
#         if tuple_args == "":
#             tuple_args = "x"
#         if self.symbolic is None:
#             return "{nom}{fixe} : {tuple_args} ↦ {nom}{fixe}({args})".format(nom=self.__name__, fixe=fixe, args=args, tuple_args=tuple_args)
#         return "{nom}{fixe} : {tuple_args} ↦ {expression}".format(nom=self.__name__, fixe=fixe, tuple_args=tuple_args, expression=self.symbolic)

#     def __rmul__(self, other):
#         """
#         permet de multiplier other a self
#         appelle par 'other * self'
#         """
#         return self * other     #on profite que la loi '*' soit commutative chez les complexes

#     def __rtruediv__(self, other):
#         """
#         permet de diviser other par self
#         appelle par 'other / self'
#         """
#         return _Simple_Function(other) / self

#     def __str__(self):
#         return repr(self)

#     def __sub__(self, other):
#         """
#         permet de soustraire other a self
#         appelle par 'self - other'
#         """
#         with raisin.Printer("Calculation of '%s' - '%s'..." % (self, other)):
#             return self + (-other)  #on se rapporte a la loie '+'

#     def __truediv__(self, other):
#         """
#         permet de diviser self par other
#         appelle par 'self / other'
#         """
#         class Div:
#             def __init__(self, f, g):
#                 self.f = f
#                 self.g = g
#                 self.correspondance = {f.args[i]: g.args[i] for i in range(len(f.args))}
#             def __call__(self, **f_kwargs):
#                 """
#                 ne fait aucune verifications
#                 toute verification doit etre faite en amont
#                 """
#                 g_kwargs = {self.correspondance[a]:v for a, v in f_kwargs.items()}
#                 return self.f(**f_kwargs) / self.g(**g_kwargs)

#         with raisin.Printer("Calculation of '%s' / '%s'..." % (self, other)):

#             if type(other) is not _Simple_Function:
#                 try:
#                     name = other.__name__
#                 except AttributeError:
#                     name = str(other) if " " not in str(other) else "constant"
#                 return self / _Simple_Function(other, name=name)

#             #egalisation du nombre de parametres
#             moi = self
#             if len(self.args) > len(other.args):
#                 other = _Simple_Function(other)
#                 other.args += sorted(set(self.args)-set(other.args))[:len(self.args)-len(other.args)]
#             elif len(self.args) < len(other.args):
#                 moi = _Simple_Function(self)
#                 moi.args += sorted(set(other.args)-set(self.args))[:len(other.args)-len(self.args)]

#             #preparation
#             correspondance = {other.args[i]: moi.args[i] for i in range(len(moi.args))}# a chaque variable dans other, on lui associ un non dans self
#             bij_correspondance = {moi.args[i]: other.args[i] for i in range(len(moi.args))}
#             nouveau_name = "Div(%s, %s)" % (moi.__name__, other.__name__)# cela va etre le nouveau nom de la fonction
#             nouveau_fixed = moi.fixed & {correspondance[a] for a in other.fixed}# on recupere toutes les informations de la nouvelle fonction
#             nouveau_args = sorted(set(moi.args) | set([correspondance[a] for a in other.args]))# c'est vrai pour les arguments
#             if raisin.sympy is not None:
#                 nouveau_domain = {a: moi.domain.get(a, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) & other.domain.get(bij_correspondance[a], raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) for a in nouveau_args}# car la fonction f(g) herite en grosse partie des caracteristiques de g
#                 #il est inutil de reduire le domaine en enlevant les valeur pour lequelles le denominateur est nul puisque
#                 #ces valeur sont calculer des que l'on initialise la nouvelle fonction
#             else:
#                 nouveau_domain = {}

#             nouveau_default = {a: moi.default.get(a, other.default.get(bij_correspondance[a], None)) for a in nouveau_args if moi.default.get(a, None) != other.default.get(bij_correspondance[a], None) and a in moi.default or bij_correspondance[a] in other.default}# et leur valeurs
#             nouveau_var_positional = moi.var_positional and other.var_positional
#             nouveau_var_keyword = moi.var_keyword and other.var_keyword
#             if moi.symbolic is not None and other.symbolic is not None:# si on a affaire a 2 fonctions dont on connait l'expression
#                 nouveau_func = moi.symbolic / other.symbolic.subs(correspondance, simultaneous=True)# c'est un jeu d'enfant
#             else:               # par contre si l'une des 2 au moin n'est pas formelle
#                 nouveau_func = Mul(moi, other)# et bien on fait une fonction qui calcul point par point

#             #restitution
#             fonction = _Simple_Function(nouveau_func, name=nouveau_name, fixed=nouveau_fixed, domain=nouveau_domain)
#             fonction.args = nouveau_args# on injecte de force les parametres que l'on viens de sauver
#             fonction.default = nouveau_default
#             fonction.var_positional = nouveau_var_positional
#             fonction.var_keyword = nouveau_var_keyword
#             return fonction

#     def atoms(self, *types):
#         """
#         extension de la methode atoms de raisin.sympy
#         """
#         assert self.symbolic is not None, "The function %s is not symbolic, it is impossible to excecute the 'atoms' method." % self
#         return self.symbolic.atoms(*types)

#     def copy(self):
#         """
#         retourne une copie vrai de self
#         """
#         with raisin.Printer("Copy function %s ..." % self):
#             if self.symbolic is not None:
#                 return _Simple_Function(self.symbolic.copy(), name=self.__name__+"_copy", fixed=self.fixed, domain=self.domain, **self.kwargs)
#             return _Simple_Function(raisin.copy(self.func), name=self.__name__+"_copy", fixed=self.fixed, domain=self.domain, **self.kwargs)

#     def diff(self, var=None, **options):
#         """
#         retourne la fonction derivee
#         """
#         #verification
#         if var is None:
#             reste = [a for a in self.args if a not in self.fixed]
#             if len(reste) == 1:
#                 var = reste[0]
#             else:
#                 raise ValueError("Since there is more than one variable in the expression, the variable of differentiation must be supplied to differentiate %s." % self)
#         assert str(var) in self.args, "The variable %s must belong to one of the following arguments: %s." % (var, self.args)

#         #entrage dans le dur
#         if self.symbolic is not None:
#             nouvelle = self.copy()
#             nouvelle.symbolic = nouvelle.symbolic.diff(str(var), **options)
#             nouvelle.__name__ = "Diff(%s, %s)" % (self.__name__, var)
#             nouvelle.domain = {c:v & nouvelle.domain.get(c, raisin.sympy.Interval(-raisin.sympy.oo, raisin.sympy.oo)) for c, v in _domain(nouvelle.symbolic).items()}
#             return nouvelle
#         raise NotImplementedError

#     def diffs(self, var=None, n=None, **options):
#         """
#         est un generateur qui cede les derivees successives
#         """
#         raise NotImplementedError

#     def doit(self):
#         """
#         applique la methode doit a self ce qui a pour concequence de modifier self
#         retourne self
#         """
#         with raisin.Printer("Doitation of %s..." % self):
#             assert self.symbolic is not None, "The function %s is not symbolic, it is impossible to excecute the 'doit' method." % self
#             self.symbolic.doit()
#             return self

#     def equals(self, other):
#         """
#         retourne True si self et la other sont egaux.
#         retourne False si ce n'est jamais le cas.
#         retourne un systeme d'equation si des variables sont en jeux. (appelle par '==')
#         """
#         raise NotImplementedError

#     def evalf(self, n=15, subs=None, maxn=1000, chap=False, strict=False, quad=None, verbose=False):
#         """
#         retourne le point ou cette fonction est appliquee a chacune des coordonnees
#         """
#         raise NotImplementedError

#     def _eval_simplify(self, ratio=1.7, measure=raisin.count_ops, rational=False, inverse=False):
#         """
#         methode appelle par raisin.sympy.simplify
#         modifie self
#         retourne self
#         """
#         if self.symbolic is not None:
#             self.symbolic.simplify(ratio, measure, rational, inverse)
#         return self

#     def get_expr_free_symbols(self):
#         """
#         retourne la liste de tous les parametres, symbol, que ce soit des lettres, des mots ou des chiffres...
#         la liste est triee par ordre alphabetique
#         """
#         if self.symbolic is not None:
#             return sorted(self.symbolic.expr_free_symbols, key=(lambda s:str(s)))
#         return self.args

#     def get_free_symbols(self):
#         """
#         retourne la liste de tous les parametres non muets, c'est a dire les variables
#         la liste est triee par ordre alphabetique
#         """
#         if self.symbolic is not None:
#             return sorted(self.symbolic.free_symbols, key=(lambda s:str(s)))
#         return self.args

#     def limit(self, x, xlim, dir="+"):
#         """
#         applique cette methode a self
#         retourne une nouvelle instance de l'objet
#         cela n'affecte donc par self
#         """
#         if self.symbolic is not None:
#             return _Simple_Function(self.symbolic.limit(x, xlim, dir), name=self.id+"_lim", fixed=self.fixed, domain=self.domain, **self.kwargs)
#         raise NotImplementedError

#     def n(self, *args, **kargs):
#         """
#         applique la methode evalf
#         """
#         return self.evalf(*args, **kargs)

#     def plot(self, ax, label=None, color=None, border={}, dim=None):
#         """
#         prepare l'affichage graphique de cette fonction
#         'ax' est l'objet matplotlib qui permet de tout plotter au meme endroit
#         'label' est la legende de cette fonction
#         'color' est le code rgb de la forme '#ffee00'
#         'border' est le dictionnaire qui a chaque variables associe au minimum la valeur minimum, maximum du parametre,
#         et accessoirement le nombre de point qu'il doit balayer.
#         """
#         raise NotImplementedError

#     def pprint(self):
#         """
#         affiche joliment l'objet
#         """
#         raise NotImplementedError

#     def replace(self, query, value, map=False, simultaneous=True, exact=False):
#         """
#         retourne la nouvelle fonction ou chaque coordonnees subit cette methode
#         """
#         raise NotImplementedError

#     def round(self, p=0):
#         """
#         retourne la fonction arrondi
#         """
#         raise NotImplementedError

#     def show(self, label="automatic", color=None, border={}, dim=None):
#         """
#         affiche la fonction dans un graphique en 2d ou 3d
#         'label' est la legende de cette fonction (par defaut le str de cet objet)
#         'color' est le code rgb de la forme '#ffee00'
#         'border' est le dictionnaire qui a chaque variable associe au minimum la valeur minimum, maximum du parametre,
#         et le nombre de point qu'il doit balayer.
#         """
#         raise NotImplementedError

#     def subs(self, *args, **kwargs):
#         """
#         retourne la nouvelle fonction ou la methode subs a ete applique a chaque coordonnees
#         """
#         raise NotImplementedError


# class Function:
#     """
#     c'est une fonction allant de C**n dans C**k
#     """
#     def __init__(self, *funcs, name=None, fixed=set(), domain={}, **kwargs):
#         """
#         s'appui tres fortement sur class _Simple_Function
#         example:
#         >>> def f(x, y):
#         ...     return x + y
#         >>> def g(a, b):
#         ...     return a - b
#         """
#         self.funcs = funcs          # liste d'objets pouvant chacun etre vu comme une fonctions
#         self.name = name            # nom de cet objet (pour la methode __str__).
#         self.fixed = set(fixed)     # ensemble qui recence tous les parametres fixes en STR, non pas en 'raisin.sympy'.
#         self.domain = domain        # dictionaire qui a chaque variable (STR), associ l'expression raisin.sympy de son domaine de definition.
#         self.kwargs = kwargs        # sauvegrade de tous nessesaire lorsqu'on fait une copie vrai de l'objet
#         self.args = {}              # tous les parametres (STR) dans l'ordre alphabetique. les *args et **kargs n'apparaissent pas ici. chaque parametre associe la liste des parametres des sous fonctions
#         self.default = {}           # dictionaire qui a chaque variable (STR), associ ca valeur par defaut.
#         self.symbolics = []         # liste des expressions raisin.sympy de chacunes des fonctions si celles ci peuvent etre vue comme des fonctions formelles.
#         self.var_positional = False # est True si la methode __call__ de func contient un argument du type *args
#         self.var_keyword = False    # est True si la methode __call__ de func contient un kargs du genre **kwargs

#         with raisin.Printer("Making %s as a function of C**n into C**k..." % str(funcs)):
#             #self.funcs
#             self.funcs = [_Simple_Function(func, fixed=self.fixed, domain=self.domain, **kwargs) for func in self.funcs]# on essai d'ajouter des methodes sympatiques a chaqune des fonctions
#             #self.domain
#             for f in self.funcs:
#                 self.domain = {var: self.domain[var] & f.domain[var] for var in self.domain}
#             #self.args
#             for i in range(max((len(f.args) for f in self.funcs))):
#                 self.args["x%d" % i] = []
#                 for f in self.funcs:
#                     if len(f.args) >= i+1:
#                         self.args["x%d" % i].append(f.args[i])
#                     else:
#                         self.args["x%d" % i].append(None)
#             #self.symbolics
#             self.symbolics = [f.symbolic for f in self.funcs]
#             #self.var_positional
#             self.var_positional = bool([f.var_positional for f in self.funcs if f.var_positional])
#             #self.var_keyword
#             self.var_keyword = bool([f.var_keyword for f in self.funcs if f.var_keyword])

