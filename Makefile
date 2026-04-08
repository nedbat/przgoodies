SLUG = paramfunc

SLIDE_HTML = $(SLUG).html
ZIP_FILE = $(SLUG).zip

SUPPORT = lineselect.js slides.js slides.css typogr.min.js
IMAGES = *.jpg *.png
VENDOR = slippy highlight

.PHONY: $(SLIDE_HTML) extract slides

SAMPLES = $(wildcard samples/*)

slides: $(SLIDE_HTML)

extract:
	sed -n -e '/^##: run/,/^## end/p' < $(SLIDE_HTML) | bash

$(SLIDE_HTML): $(SAMPLES) extract
	python -m cogapp -c -r $@

.PHONY: april

april: make_april.py
	python make_april.py > april_out.txt
	python -m cogapp -c -r april.html

PNG_DIR = png

clean:
	rm -f *.pyc $(PX)
	rm -rf __pycache__ samples/__pycache__
	rm -rf .*_cache samples/.*_cache
	rm -rf .coverage .coverage.*
	rm -rf $(PNG_DIR)
	rm -f $(ZIP_FILE)

sterile: clean
	python -m cogapp -x -r $(SLIDE_HTML)

test:
	coverage run --branch -m pytest test_*.py samples/test_*.py
	coverage report -m

pngs: $(SLIDE_HTML)
	phantomjs phantom-slippy-to-png.js $(SLIDE_HTML) $(PNG_DIR)/

pdf: pngs
	magick png/*.png $(SLUG).pdf

PX = $(SLUG).px

px $(PX): $(SLIDE_HTML)
	python slippy_to_px.py $(SLIDE_HTML) $(PX) $(SLUG)

WEBHOME = ~/web/stellated/pages/text
WEBPREZHOME = $(WEBHOME)/$(SLUG)
WEBPIXHOME = $(WEBHOME)/$(SLUG)_pix

publish: $(PX) pngs
	mkdir -p $(WEBPREZHOME) $(WEBPIXHOME)
	cp -f $(PX) $(WEBHOME)
	cp -f $(PNG_DIR)/* $(WEBPIXHOME)
	cp -f $(SLIDE_HTML) $(WEBPREZHOME)/$(SLUG).html
	cp -f $(SUPPORT) $(WEBPREZHOME)
	cp -f $(IMAGES) $(WEBPREZHOME)
	cp -rf $(VENDOR) $(WEBPREZHOME)

ZIP_EXTRA = 

zip $(ZIP_FILE): $(SLIDE_HTML)
	zip -r $(ZIP_FILE) $(SLIDE_HTML) $(SUPPORT) $(IMAGES) $(ZIP_EXTRA) $(VENDOR)
