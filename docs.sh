#!/bin/bash

case "$1" in
  "serve")
    echo "Starting local documentation server..."
    mkdocs serve
    ;;
  "deploy")
    echo "Deploying documentation to GitHub Pages..."
    mkdocs gh-deploy
    ;;
  *)
    echo "Usage: ./docs.sh [command]"
    echo "Commands:"
    echo "  serve   - Start local documentation server with live reload"
    echo "  deploy  - Deploy documentation to GitHub Pages"
    ;;
esac
