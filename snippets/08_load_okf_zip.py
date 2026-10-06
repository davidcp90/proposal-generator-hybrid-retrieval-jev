import pathlib, zipfile
from google.colab import files

OKF = pathlib.Path("okf")
if not OKF.exists():
    uploaded = files.upload()                    # select okf.zip
    zipfile.ZipFile(next(iter(uploaded))).extractall(".")
print(len(list(OKF.rglob("*.md"))), "OKF files")
!find okf -name '*.md' | sort
