import argparse
import os
import toml


class IconConfig:
    """
    Represents a single icon configuration.
    """

    def __init__(self, src, dst):
        """
        Initializes an IconConfig object.

        Args:
            src (str): The source file path.
            dst (str): The destination file path.
        """
        self.src = src
        self.dst = dst

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
        self.icons = []  # List to store IconConfig objects

    def add_icon_config(self, icon_config):
        """
        Adds an IconConfig object to the configuration.

        Args:
            icon_config (IconConfig): The IconConfig object to add.
        """
        self.icons.append(icon_config)

    @classmethod
    def from_toml(cls, toml_file_path):
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
                            icon_config = IconConfig(icon_data["src"], icon_data["dst"])
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

    if args.config:
        config = Config.from_toml(args.config)
    elif args.config_file:
        config = Config.from_toml(args.config_file)
    else:
        default_config_path = "icons.toml"
        if os.path.exists(default_config_path):
            config = Config.from_toml(default_config_path)
        else:
            print(f"Default config '{default_config_path}' not found.")
            exit(-1)
            config = {}  # Or handle the absence of default config as needed

    if config:
        print("Loaded Configuration:", config)

    return config
