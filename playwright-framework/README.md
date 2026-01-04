Playwright pytest framework for SauceDemo

Usage

1. Create a venv and activate it:

python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies:

pip install -r requirements.txt
python -m playwright install chromium

3. Run tests (headed):

pytest -q

Outputs
- reports/order_details.txt will contain the purchased items and total.

