#!/bin/bash
set -e

echo "⚠️  Publishing greenmining to PRODUCTION PyPI..."
echo ""
echo "🚨 This will publish to REAL PyPI (pypi.org) - package will be public!"
echo ""
read -p "Are you absolutely sure? Type 'yes' to continue: " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Cancelled"
    exit 1
fi

# Build package
echo ""
echo "🔨 Building package..."
# Determine python to use (prefer active virtualenv)
if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "${VIRTUAL_ENV}/bin/python" ]; then
    PYTHON="$VIRTUAL_ENV/bin/python"
    echo "Using active virtualenv python: $PYTHON"
else
    # Create a temporary venv for the publish process and reuse it
    PUBLISH_VENV=".publish_env"
    if [ ! -d "$PUBLISH_VENV" ]; then
        echo "No active virtualenv detected. Creating temporary venv: $PUBLISH_VENV"
        python3 -m venv "$PUBLISH_VENV"
    fi
    PYTHON="$PWD/$PUBLISH_VENV/bin/python"
    echo "Using temporary venv python: $PYTHON"
fi
export PYTHON
"$PYTHON" -m pip install --upgrade pip setuptools wheel build
bash scripts/build_package.sh

# Final confirmation
echo ""
echo "📦 Ready to publish:"
ls -lh dist/
echo ""
read -p "Proceed with upload? (yes/no): " final_confirm

if [ "$final_confirm" != "yes" ]; then
    echo "❌ Cancelled"
    exit 1
fi

# Upload to PyPI
echo ""
echo "📤 Uploading to PyPI..."
"$PYTHON" -m pip install --upgrade twine
"$PYTHON" -m twine upload dist/*

echo ""
echo "✅ Published to PyPI!"
echo "🔗 View at: https://pypi.org/project/greenmining/"
echo ""
echo "📦 Users can now install with:"
echo "   pip install greenmining"
echo ""
echo "🎉 Congratulations on publishing your package!"
