# Flask Backtesting App

## Description

A web application for backtesting stock trading strategies using historical data from the OpenBB platform.
Allows users to select a stock ticker, strategy, and starting year to run a backtest and view the results.

## Installation

*   Prerequisites: Python 3.7+, pip
*   Clone the repository: `git clone <repository_url>`
*   Navigate to the project directory: `cd backtest`
*   Create a conda environment: `conda create -n backtest_env python=3.9`
*   Activate the conda environment: `conda activate backtest_env`
*   Install dependencies: `pip install -r flask_backtest_app/requirements.txt`
*   Set the FMP API key in a `.env` file:
    ```
    FMP_API_KEY=your_api_key_here
    ```

## Usage

*   Run the Flask application: `python flask_backtest_app/app.py`
*   Open the application in your web browser: `http://localhost:5001`
*   Select a stock ticker, strategy, and year from the dropdown menus.
*   Click the "Run Backtest" button to view the results.
*   Click on a stock ticker to view stock details.

## Configuration

*   **Strategies:**
    *   Strategies are defined in the `backtest-app/public/strategies.yaml` file.
    *   To add a new strategy, add a new entry to the `strategies.yaml` file and implement the corresponding logic in the `run_backtest` function in `flask_backtest_app/app.py`.
*   **OpenBB Integration:**
    *   The application uses the OpenBB platform to fetch stock data.
    *   The `openbb_integration.py` module handles the integration with OpenBB.
    *   An FMP API key is required for the OpenBB integration.
    *   The API key can be configured in the `.env` file.
*   **Caching:**
    *   Stock data is cached locally in the `flask_backtest_app/data/cache` directory.
    *   The cache has a TTL of 24 hours.
*   **Error Logging:**
    *   Errors are logged to the `flask_backtest_app/data/logs/openbb_errors.log` file.

## Contributing

*   Fork the repository.
*   Create a new branch for your feature or bug fix.
*   Commit your changes.
*   Create a pull request.

## License

[Specify the license here]