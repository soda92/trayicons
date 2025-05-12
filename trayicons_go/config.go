package main

import (
	"fmt"
	"os"

	"path/filepath"

	"github.com/pelletier/go-toml/v2"
)

type MyConfig struct {
	Icons []Icon
}

type Icon struct {
	Src string
	Dst string
}

func ParseConfig(config string) MyConfig {
	var cfg MyConfig
	err := toml.Unmarshal([]byte(config), &cfg)
	if err != nil {
		panic(err)
	}
	return cfg
}

func MustFindDefaultConfig() string {
	path, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	configFile := filepath.Join(path, "icons.toml")

	if _, err := os.Stat(configFile); err == nil {
	} else if os.IsNotExist(err) {
		fmt.Printf("File '%s' does not exist\n", configFile)
		// Create or open the file
		file, err := os.OpenFile(configFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			fmt.Println("Error opening or creating file:", err)
			panic("")
		}
		defer file.Close()

		// Write to the file
		_, err = file.WriteString(`[[icons]]
src = "demo.kra"
dst = "./demo.ico"
`)
		if err != nil {
			fmt.Println("Error writing to file:", err)
			panic("")
		}
		panic("default config created. please correct the config and re-run this tool.")
	} else {
		fmt.Printf("Error checking file '%s': %v\n", configFile, err)
		panic(err)
	}

	data, err := os.ReadFile(configFile)
	if err != nil {
		panic(err)
	}

	return string(data)
}
