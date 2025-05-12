package main

import "testing"

func TestConfig(t *testing.T) {
	config := `[[icons]]
src = "demo.kra"
dst = "./demo.ico"
`
	cfg := ParseConfig(config)

	if len(cfg.Icons) != 1 {
		t.Fatal("parse error")
	}
}
