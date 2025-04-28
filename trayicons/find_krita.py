from pathlib import Path


def get_krita() -> Path:
    scoop_krita = Path.home().joinpath("scoop/apps/krita/current/bin/krita.exe")
    normal_krita = Path(r"C:\Program Files\Krita (x64)\bin\krita.exe")
    steam_krita = Path(
        r"c:\Program Files (x86)\Steam\steamapps\common\Krita\krita\bin\krita.exe"
    )
    if scoop_krita.exists():
        return scoop_krita
    elif normal_krita.exists():
        return normal_krita
    elif steam_krita.exists():
        return steam_krita

    print("cannot find krita")
    exit(-1)
