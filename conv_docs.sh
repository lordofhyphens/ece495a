#!/bin/bash
# Script to convert OpenDocument formats to XLS. 

# Basic concepts pulled from
# http://www.xml.com/pub/a/2006/01/11/from-microsoft-to-openoffice.html?page=2
# http://www.xml.com/pub/a/2004/02/04/tr-xml.html

# switch statement here to tell us to which we want to do our conversions.

ooffice2 -invisible 
  "macro:///Standard.MyConversions.SaveAsOOO(`pwd $1`/$1)"