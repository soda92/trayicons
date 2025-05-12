import argparse
import os
import toml
from pathlib import Path


class IconConfig:
    """
    Represents a single icon configuration.
    """

    def __init__(self, src, dst, toml_file_path):
        """
        Initializes an IconConfig object.

        Args:
            src (str): The source file path.
            dst (str): The destination file path.
        """
        p = Path(toml_file_path).resolve().parent
        self.src = p.joinpath(src).resolve()
        if not self.src.exists():
            print(f"config error: path {self.src} not exists.")
            exit(-1)
        self.dst = p.joinpath(dst).resolve()

    def __repr__(self):
        """
        Returns a string representation of the IconConfig object.
        """
        return f"IconConfig(src='{self.src}', dst='{self.dst}')"


class Config:
    """
    Represents the overall application configuration, including a list of icon configurations.
    """

    def __init__(self):
        """
        Initializes a Config object.
        """
        self.icons: list[IconConfig] = []  # List to store IconConfig objects

    def add_icon_config(self, icon_config):
        """
        Adds an IconConfig object to the configuration.

        Args:
            icon_config (IconConfig): The IconConfig object to add.
        """
        self.icons.append(icon_config)

    @classmethod
    def from_toml(cls, toml_file_path: str):
        """
        Loads the configuration from a TOML file.

        Args:
            toml_file_path (str): The path to the TOML file.

        Returns:
            Config: A Config object containing the loaded configuration.
        """
        config = cls()  # Create an instance of Config
        content = Path(toml_file_path).read_text(encoding="utf8")
        toml_data = dict()
        try:
            toml_data = toml.loads(content)  # Load the TOML data
            # print(toml_data) #for debugging
        except toml.TomlDecodeError as e:
            print(f"Error decoding TOML: {e}")
            #  Handle TOML decoding errors

        if "icon" in toml_data:
            for icon_data in toml_data["icon"]:
                # print(icon_data) # for debugging
                if "src" in icon_data and "dst" in icon_data:
                    icon_config = IconConfig(
                        icon_data["src"], icon_data["dst"], toml_file_path
                    )
                    config.add_icon_config(icon_config)
                else:
                    print(f"Warning: Incomplete icon configuration: {icon_data}")
            print("converting icon to icons...")
            for icon_data in toml_data["icon"]:
                import copy

                toml_data["icons"] = copy.deepcopy(toml_data["icon"])
                del toml_data["icon"]
                Path(toml_file_path).write_text(toml.dumps(toml_data))
        elif "icons" in toml_data:
            for icon_data in toml_data["icons"]:
                # print(icon_data) # for debugging
                if "src" in icon_data and "dst" in icon_data:
                    icon_config = IconConfig(
                        icon_data["src"], icon_data["dst"], toml_file_path
                    )
                    config.add_icon_config(icon_config)
                else:
                    print(f"Warning: Incomplete icon configuration: {icon_data}")
        else:
            print(
                f"Warning: No 'icon/icons' table found in TOML file: {toml_file_path}"
            )

        return config

    def __iter__(self):
        """
        Makes the Config object iterable, allowing iteration over the icon configurations.
        """
        return iter(self.icons)

    def __len__(self):
        """
        Returns the number of icon configurations.
        """
        return len(self.icons)


def get_config_path() -> Path:
    parser = argparse.ArgumentParser(
        description="A program that loads configuration files."
    )

    # Optional argument for specifying the config file
    parser.add_argument(
        "--config",
        "-c",  # Short option
        type=str,
        help="Path to the configuration file.",
        metavar="FILE",
    )

    # Positional argument for the config file (optional)
    parser.add_argument(
        "config_file",
        nargs="?",  # Allows 0 or 1 positional arguments
        type=str,
        help="Optional path to the configuration file (can also use --config).",
        metavar="FILE",
    )

    args = parser.parse_args()

    cr = Path(os.getcwd()).resolve()

    config_path = None

    if args.config:
        config_path = cr.joinpath(args.config)
    elif args.config_file:
        config_path = cr.joinpath(args.config_file)

    if config_path is None:
        config_path = cr.joinpath("icons.toml")
        if not config_path.exists():
            print(f"Default config '{config_path}' not found.")
            print("creating...")
            Path(config_path).write_text(
                encoding="utf8",
                data="""
[[icons]]
src = "demo.kra"
dst = "./demo.ico"
""",
            )
            print("please correct the config then run the tool again.")
            exit(-1)

    return config_path
