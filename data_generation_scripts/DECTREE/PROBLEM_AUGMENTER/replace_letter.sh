#!/bin/bash
src_let=$1
dst_let=$2
src_file=$3
dst_file=$4


sed "s/$src_let/$dst_let/g" src_file > dst_file
