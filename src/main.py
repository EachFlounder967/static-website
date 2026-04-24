import os
import shutil
from copystatic import copy_dir_recursive


def main():
    src = "static"
    dst = "public"

    if os.path.exists(dst):
        shutil.rmtree(dst)

    copy_dir_recursive(src, dst)


if __name__ == "__main__":
    main()

