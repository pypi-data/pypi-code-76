try:
  import pint
  u = pint.UnitRegistry()
  Q_ = u.Quantity
except:
  def Q_(*args):
    raise RuntimeError("Quantities are not supported because the pint module could not be imported. Please make sure it is installed and try again.")

quant = Q_
