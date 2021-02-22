# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from ipywidgets import IntProgress, HTML, VBox
from IPython.core.display import display


class _ProgressBar(object):
    def __init__(self, total):
        """Init the progress bar instance."""
        self.total_tasks = total
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.progress_bar = None
        self.label = None
        self.footer = None
        self.box = None
        self.progress_text = ""
        self.job_status_text = ""

    def display(self):
        """Display the progress bar in the notebook."""
        self.progress_bar = IntProgress(min=0, max=self.total_tasks, value=0)
        self.progress_text = "Completed 0 / {}".format(self.total_tasks)
        self.job_status_text = ""
        self.label = HTML(self.progress_text)
        self.footer = HTML()
        self.box = VBox(children=[self.label, self.progress_bar, self.footer])
        display(self.box)

    def update(
        self,
        completed_tasks,
        failed_tasks,
        scheduled_tasks=None,
        elapsed_time=None,
        estimated_remaining_time=None,
    ):
        """Update the progress bar."""
        if scheduled_tasks:
            self.total_tasks = scheduled_tasks
        self.completed_tasks = completed_tasks
        self.failed_tasks = failed_tasks

        self.progress_bar.max = scheduled_tasks
        self.progress_bar.value = completed_tasks

        self.progress_text = "Completed {} / {}".format(
            self.completed_tasks, self.total_tasks
        )
        # TODO: Highlight the failed items
        if self.failed_tasks:
            self.progress_text += " ({} failed)".format(failed_tasks)
        self._update_label()

        self.footer.value = "Elapsed time: {}".format(elapsed_time)
        if estimated_remaining_time:
            self.footer.value += "; Estimated remaining time: {}".format(
                estimated_remaining_time
            )

    def _update_label(self):
        """Update the label of the progress bar."""
        self.label.value = self.progress_text
        if self.job_status_text:
            self.label.value += " - {}".format(self.job_status_text)

    def set_job_not_started(self):
        """Set the progress bar to display job not started."""
        self.job_status_text = "Job NotStarted"
        self._update_label()

    def set_job_queued(self):
        """Set the progress bar to display job queued."""
        self.job_status_text = "Job Queued"
        self._update_label()

    def set_job_running(self):
        """Set the progress bar to display job running."""
        self.job_status_text = "Job Running"
        self._update_label()

    def set_job_completed(self):
        """Set the progress bar to display job completed."""
        self.job_status_text = "Job Completed"
        self._update_label()
        self.progress_bar.bar_style = "success"

    def set_job_failed(self):
        """Set the progress bar to display job failed."""
        self.job_status_text = "Job Failed"
        self._update_label()
        self.progress_bar.bar_style = "danger"

    def set_job_canceled(self):
        """Set the progress bar to display job canceled."""
        self.job_status_text = "Job Canceled"
        self._update_label()
        self.progress_bar.bar_style = "warning"
