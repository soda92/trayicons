from trayicons.config import Config


def test_config():
    """
    Main function to demonstrate loading the TOML configuration.
    """
    # Create a sample TOML file
    toml_content = """
[[icon]]
src = "image1.kra"
dst = "./icons/image1.ico"

[[icon]]
src = "image2.png"
dst = "output/image2.ico"

[[icon]]
src = "image3.kra"
dst = "icons/image3.ico"
    """
    with open("config.toml", "w") as f:
        f.write(toml_content)

    # Load the configuration from the TOML file
    config = Config.from_toml("config.toml")

    # Print the icon configurations
    print("Loaded icon configurations:")
    for icon_config in config:
        print(icon_config)  # Uses the __repr__ method of IconConfig
        print(f"Source: {icon_config.src}, Destination: {icon_config.dst}")
    print(f"Number of icon configurations: {len(config)}")
