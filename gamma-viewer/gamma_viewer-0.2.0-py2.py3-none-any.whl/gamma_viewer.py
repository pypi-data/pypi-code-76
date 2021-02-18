"""Python wrapper that sends comms to React component."""
from __future__ import print_function
from jupyter_react import Component


class GammaViewer(Component):
    """Gamma Viewer class."""

    # This module needs to match the entry React component
    module = 'App'

    def __init__(self, **kwargs):
        """Initialize python wrapper and forward messages from notebook."""
        # This needs to match the name in the entry js file
        target_name = 'react.gamma_viewer'
        super(GammaViewer, self).__init__(target_name=target_name, **kwargs)
        self.on_msg(self._handle_msg)

    def _handle_msg(self, msg):
        print(msg)
