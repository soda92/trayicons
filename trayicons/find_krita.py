from pathlib import Path


def get_krita() -> Path:
    scoop_krita = Path.home().joinpath("scoop/apps/krita/current/bin")
    if scoop_krita.exists():
        return scoop_krita
    print("cannot find krita")
    exit(-1)
