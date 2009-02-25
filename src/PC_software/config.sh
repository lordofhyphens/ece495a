#!/bin/bash
curr_path=` pwd | sed -e 's#/c/#C:\\\\\\\\#' -e 's_/_\\\\\\\\_g' `
sed -e "s/#PATH#/$curr_path/" displaydata_base.m > display_data.m 
