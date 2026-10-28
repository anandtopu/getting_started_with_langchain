"""Keep identity in the host and reject overlapping work on the same thread.

Run: uv run --extra apps python modules/18_apps/examples/05_session_isolation.py --offline
Expected: Cross-customer access and overlapping work are denied.
Cost: No API calls; deterministic local checks. Requires: apps
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from common.budget import Admission
from common.config import Settings
from common.errors import run_cli
from common.lesson import lesson_settings
from common.pretty import print_text
from common.security import Principal
from common.service import SupportService


def main() -> None:
    lesson_settings()
    with TemporaryDirectory() as directory:
        service = SupportService(Path(directory), Settings(course_offline=True))
        thread = service.new_thread(Principal("C001", "customer"))
        try:
            service.session(thread, Principal("C002", "customer"))
        except PermissionError:
            print_text("Cross-customer access denied.")
    admission = Admission(maximum=1)
    with admission.slot("thread-a", "C001"):
        try:
            # KEY IDEA: a thread identifier is neither a credential nor a lock.
            with admission.slot("thread-a", "C001"):
                raise AssertionError("Overlapping request was admitted")
        except BlockingIOError:
            print_text("Concurrent request rejected; outer slot will be released.")


if __name__ == "__main__":
    run_cli(main)
