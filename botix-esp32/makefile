.PHONY: snapshot s

include ./.pio/libdeps/esp32dev/KiraFlux-Toolkit/examples/common.mak

erase:
	pio run --target erase

snapshot:
	python snapshot.py

s: snapshot