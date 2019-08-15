import sys

from background_task import background


@background()
def task():  # pragma: no cover
    """
    Function to register a new task in the background.

    """
    pass


if 'process_tasks' in sys.argv:  # pragma: no cover
    task(verbose_name='task')
