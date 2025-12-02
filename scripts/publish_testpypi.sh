#!/bin/bash
set -e

echo "📤 Publishing greenmining to TestPyPI..."
echo ""
echo "⚠️  This will publish to TEST PyPI (test.pypi.org)"
echo ""

# Build package
echo "🔨 Building package..."
bash scripts/build_package.sh

# Upload to TestPyPI
echo ""
echo "📤 Uploading to TestPyPI..."

# Determine python to use
if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "${VIRTUAL_ENV}/bin/python" ]; then
    PYTHON="$VIRTUAL_ENV/bin/python"
else
    PYTHON="python3"
fi

"$PYTHON" -m pip install --upgrade twine
"$PYTHON" -m twine upload --repository testpypi dist/*

echo ""
echo "✅ Published to TestPyPI!"
echo "🔗 View at: https://test.pypi.org/project/greenmining/"
echo ""
echo "📦 Test installation with:"
echo "   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ greenmining"
echo ""
echo "   # The --extra-index-url is needed for dependencies"
