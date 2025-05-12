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
        try:
            with open(toml_file_path, "r") as f:
                toml_data = toml.load(f)  # Load the TOML data
                # print(toml_data) #for debugging
                if "icon" in toml_data:
                    for icon_data in toml_data["icon"]:
                        # print(icon_data) # for debugging
                        if "src" in icon_data and "dst" in icon_data:
                            icon_config = IconConfig(
                                icon_data["src"], icon_data["dst"], toml_file_path
                            )
                            config.add_icon_config(icon_config)
                        else:
                            print(
                                f"Warning: Incomplete icon configuration: {icon_data}"
                            )
                else:
                    print(
                        f"Warning: No 'icon' table found in TOML file: {toml_file_path}"
                    )

        except FileNotFoundError:
            print(f"Error: TOML file not found at {toml_file_path}")
            # You might want to raise an exception here depending on your application's needs
        except toml.TomlDecodeError as e:
            print(f"Error decoding TOML: {e}")
            #  Handle TOML decoding errors
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


def load_config() -> Config:
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

    config = None

    cr = os.getcwd()
    if args.config:
        config_path = os.path.join(cr, args.config)
        config = Config.from_toml(config_path)
    elif args.config_file:
        config_path = os.path.join(cr, args.config_file)
        config = Config.from_toml(config_path)
    else:
        default_config_path = os.path.join(cr, "icons.toml")
        if os.path.exists(default_config_path):
            config = Config.from_toml(default_config_path)
        else:
            print(f"Default config '{default_config_path}' not found.")
            print("creating...")
            Path(default_config_path).write_text(
                encoding="utf8",
                data="""
[[icon]]
src = "demo.kra"
dst = "./demo.ico"
""",
            )
            print("please correct the config then run the tool again.")
            exit(-1)
            config = {}  # Or handle the absence of default config as needed

    if config:
        print("Loaded Configuration:", config)

    return config
