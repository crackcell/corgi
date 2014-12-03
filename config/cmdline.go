/***************************************************************
 *
 * Copyright (c) 2014, Menglong TAN <tanmenglong@gmail.com>
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GPL licence
 *
 **************************************************************/

/**
 *
 *
 * @file cmdline.go
 * @author Menglong TAN <tanmenglong@gmail.com>
 * @date Sun Nov 23 20:59:30 2014
 *
 **/

package config

import (
	"flag"
	_ "fmt"
)

//===================================================================
// Public APIs
//===================================================================

var (
	Help      bool
	Verbose   bool
	WorkPath  string
	MetaPath  string
	NodeName  string
	EntryFile string
)

func InitFlags() {
	flag.BoolVar(&Help, "help", false, "Print help message")
	flag.BoolVar(&Help, "h", false, "Print help message")
	flag.BoolVar(&Verbose, "verbose", false, "Use verbose output")
	flag.BoolVar(&Verbose, "v", false, "Use verbose output")
	flag.StringVar(&NodeName, "name", "noname", "Node name")
	flag.StringVar(&NodeName, "n", "noname", "Node name")
	flag.StringVar(&WorkPath, "work", "", "Root path of the flow")
	flag.StringVar(&WorkPath, "w", "", "Work root of the flow")
	flag.StringVar(&MetaPath, "meta", "", "Path for meta data")
	flag.StringVar(&MetaPath, "m", "", "Path for meta data")
	flag.StringVar(&EntryFile, "flow", "", "Entry of the flow")
	flag.StringVar(&EntryFile, "f", "", "Entry of the flow")
}

func Parse() {
	flag.Parse()
}

//===================================================================
// Private
//===================================================================