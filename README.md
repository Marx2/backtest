![Build Status](https://github.com/Marx2/backtest/actions/workflows/build.yml/badge.svg)
![Code Coverage](https://img.shields.io/codecov/c/github/Marx2/backtest)
![License](https://img.shields.io/github/license/Marx2/backtest)
![Stars](https://img.shields.io/github/stars/Marx2/backtest?style=social)
![Forks](https://img.shields.io/github/forks/Marx2/backtest?style=social)
![Issues](https://img.shields.io/github/issues/Marx2/backtest)
![Dependencies](https://img.shields.io/david/Marx2/backtest)
![Dev Dependencies](https://img.shields.io/david/dev/Marx2/backtest)

# Flask Backtesting App

## Description

A web application for backtesting stock trading strategies using historical data from the OpenBB platform.
Allows users to select a stock ticker, strategy, and starting year to run a backtest and view the results.

This project has been vibe coded using RooCode, and LLMs: Google Gemini Flash 2.0, Deepseek V3 0324, and local model qwen2.5-coder-cline via Ollama.

## Installation

*   Prerequisites: Python 3.7+, pip
*   Clone the repository: `git clone <repository_url>`
*   Navigate to the project directory: `cd backtest`
*   Create a conda environment: `conda create -n backtest_env python=3.9`
*   Activate the conda environment: `conda activate backtest_env`
*   Install dependencies: `pip install -r flask_backtest_app/requirements.txt`

## Usage

*   Run the Flask application: `python flask_backtest_app/app.py`
*   Open the application in your web browser: `http://localhost:5001`
*   Select a stock ticker, strategy, and year from the dropdown menus.
*   Click the "Run Backtest" button to view the results.
*   Click on a stock ticker to view stock details.

## Contributing

*   Fork the repository.
*   Create a new branch for your feature or bug fix.
*   Commit your changes.
*   Create a pull request.

## License

[Specify the license here]

## Star Graph

[![GitHub stars](https://starchart.cc/Marx2/backtest.svg)](https://starchart.cc/Marx2/backtest)