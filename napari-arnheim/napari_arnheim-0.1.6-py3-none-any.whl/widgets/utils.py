

def replaceWidgetInLayout(layout, widget, replacement):
    index = layout.indexOf(widget)
    layout.removeWidget(widget)
    widget.close()
    widget = replacement
    layout.insertWidget(index, widget)