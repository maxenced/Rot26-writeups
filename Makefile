publish: build
	git subtree push --prefix _site --squash github gh-pages

build: prepare
	git diff --exit-code > /dev/null; \
	if [ $$? -ne 0 ]; then \
		echo "Can't build with unclean tree, please commit all your changes"; \
		exit 1; \
	fi;
	./generate_index.sh
	bundle exec jekyll build
	git add _site/*
	git commit -m "Generate Github Pages" _site
	git commit -am "Update pages"

prepare:
	bundle install
.PHONY: prepare build publish



