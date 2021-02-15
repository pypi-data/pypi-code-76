
from typing import Any, Callable, Mapping
from PyQt5.QtWidgets import QLabel, QLineEdit
from bergen.extenders.base import BaseExtender
import logging

logger = logging.getLogger(__name__)

class PortExtender(BaseExtender):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._widget = None

    def buildWidget(self, **kwargs):
        from bergen.extenders.ui.widgets.base import BaseWidgetMixin
        from bergen.extenders.ui.widgets.querywidget import QueryWidget
        from bergen.extenders.ui.widgets.sliderwidget import SliderWidget
        from bergen.extenders.ui.widgets.void import VoidWidget
        from bergen.extenders.ui.widgets.intwidget import IntWidget

        typeWidgetMap: Mapping[str, Callable[[Any], BaseWidgetMixin]] = {
            "QueryWidgetType": lambda port: QueryWidget.fromPort(port, **kwargs),
            "SliderWidgetType": lambda port: SliderWidget.fromPort(port, **kwargs),
            "IntWidgetType": lambda port: IntWidget.fromPort(port, **kwargs),
        }

        widgetBuilder = typeWidgetMap.get(self.widget.TYPENAME, lambda port: VoidWidget.fromPort(port, **kwargs))
        self._widget = widgetBuilder(self)
        
        return self._widget
    
    def __call__(inputs: dict, provider="vard"):
        logger.info("Called with inputs")

        logger.info("Serializing Inputs")


    def _repr_html_(self):
        string = f"{self.TYPENAME} with {self.key}"

        return string

