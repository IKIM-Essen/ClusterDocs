# IKIM Cluster Documentation

Welcome to the IKIM cluster documentation! If you are interested in the documentation, please refer to the website: <https://ikim-essen.github.io/ClusterDocs/>

## Introduction

- All documentation is written in markdown which makes it easy to contribute to the docs (see below)
- Website is rendered with [mkdocs](https://www.mkdocs.org) and the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme and is hosted on GitHub pages
- New commits to `main` are automatically built and deployed to the `gh-pages` branch
- For consistent formatting of markdown sources we use [markdownlint](https://github.com/DavidAnson/markdownlint)

## Contributing

You are welcome to open a pull request for changes to the documentation. If you want to make larger changes and you would like to see how they would appear on the rendered site, you can run mkdocs locally.

```sh
# Install dependencies
conda create -n cluster-docs -c conda-forge python=3.8 mkdocs mkdocs-material
conda activate cluster-docs

# Build and serve documentation
mkdocs serve
```

You can run markdownlint and fix basic errors as follows:

```sh
npm install -g markdownlint-cli

markdownlint docs/
markdownlint --fix docs/
```
