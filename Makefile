# Makefile for source rpm: netpbm
# $Id$
NAME := netpbm
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
