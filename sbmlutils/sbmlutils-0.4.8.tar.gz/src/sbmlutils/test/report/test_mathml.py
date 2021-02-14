import libsbml
import pytest

from sbmlutils.report import mathml


formulas = [
    "1 dimensionless",
    "power(3, 5) / x * glc",
    "GK_Vmax * GK_gc_free * (atp/(GK_k_atp + atp)) * f_gly * "
    "(power(glc,GK_n)/(power(glc,GK_n) + power(GK_k_glc, GK_n)))",
    "piecewise(3, x>3, 5)",
]

cmathmls = [
    """
    <math xmlns="http://www.w3.org/1998/Math/MathML">
    <apply>
    <divide/>
    <apply>
        <times/>
        <cn>243</cn>
        <ci>glc</ci>
    </apply>
    <ci>x</ci>
    </apply>
    </math>
    """,
    """
    <math xmlns="http://www.w3.org/1998/Math/MathML">
      <apply>
        <times></times>
        <ci> f_gly </ci>
        <ci> GK_Vmax </ci>
        <ci> GK_gc_free </ci>
        <apply>
          <divide></divide>
          <ci> atp </ci>
          <apply>
            <plus></plus>
            <ci> GK_k_atp </ci>
            <ci> atp </ci>
          </apply>
        </apply>
        <apply>
          <divide></divide>
          <apply>
            <power></power>
            <ci> glc </ci>
            <ci> GK_n </ci>
          </apply>
          <apply>
            <plus></plus>
            <apply>
              <power></power>
              <ci> glc </ci>
              <ci> GK_n </ci>
            </apply>
            <apply>
              <power></power>
              <ci> GK_k_glc </ci>
              <ci> GK_n </ci>
            </apply>
          </apply>
        </apply>
      </apply>
    </math>
    """,
]


@pytest.mark.parametrize("formula", formulas)
def test_formula_to_astnode(formula):
    astnode = mathml.formula_to_astnode(formula)
    print(astnode)
    assert astnode
    assert isinstance(astnode, libsbml.ASTNode)


@pytest.mark.parametrize("cmathml", cmathmls)
def test_cmathml_to_astnode(cmathml):
    astnode = mathml.cmathml_to_astnode(cmathml)
    assert astnode
    assert isinstance(astnode, libsbml.ASTNode)
    return libsbml.readMathMLFromString(cmathml)


@pytest.mark.parametrize("formula", formulas)
def test_astnode_to_expression(formula):
    astnode = mathml.formula_to_astnode(formula)
    expr = mathml.astnode_to_expression(astnode)
    assert expr


@pytest.mark.parametrize("formula", formulas)
def test_formula_to_expression(formula):
    expr = mathml.formula_to_expression(formula)
    assert expr


@pytest.mark.parametrize("formula", formulas)
def test_astnode_to_mathml(formula):
    astnode = mathml.formula_to_astnode(formula)
    cmathml = mathml.astnode_to_mathml(astnode, printer="content")
    assert cmathml
    assert isinstance(cmathml, str)
    pmathml = mathml.astnode_to_mathml(astnode, printer="presentation")
    assert pmathml
    assert isinstance(pmathml, str)


@pytest.mark.parametrize("formula", formulas)
def test_formula_to_mathml(formula):
    cmathml = mathml.formula_to_mathml(formula, printer="content")
    assert cmathml
    assert isinstance(cmathml, str)
    pmathml = mathml.formula_to_mathml(formula, printer="content")
    assert pmathml
    assert isinstance(pmathml, str)


@pytest.mark.parametrize("cmathml", cmathmls)
def test_cmathml_to_pmathml(cmathml):
    pmathml = mathml.cmathml_to_pmathml(cmathml)
    assert pmathml
    assert isinstance(pmathml, str)


@pytest.mark.parametrize("formula", formulas)
def test_formula_to_latex(formula):
    latex = mathml.formula_to_latex(formula)
    assert latex
    assert isinstance(latex, str)


@pytest.mark.parametrize("formula", formulas)
def test_astnode_to_latex(formula):
    astnode = mathml.formula_to_astnode(formula)
    latex = mathml.astnode_to_latex(astnode)
    assert latex
    assert isinstance(latex, str)


@pytest.mark.parametrize("cmathml", cmathmls)
def test_cmathml_to_latex(cmathml):
    latex = mathml.cmathml_to_latex(cmathml)
    assert latex
    assert isinstance(latex, str)


def test_inline_unit_formula_to_expression():
    formula = "1 dimensionless"
    formula_new = mathml.formula_to_expression(formula)
    assert formula_new == 1
