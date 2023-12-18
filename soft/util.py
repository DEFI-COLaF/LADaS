import os.path as op


def rel_path(path: str) -> str:
    return op.join(
        op.dirname(__file__),
        "..",
        path
    )
