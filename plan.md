# Backtesting Application Plan (Python/Flask Implementation)

This document outlines the architecture of the Python/Flask backtesting application.

## Project Setup

1. Create a Python virtual environment:
```bash
conda create -n backtest_env python=3.11
conda activate backtest_env
```

2. Install required packages:
```bash
pip install flask pyyaml
```

## Application Structure

The application uses Flask with the following key components:

* **app.py:** Main application file with Flask routes
* **templates/index.html:** Jinja2 template for the UI
* **static/css/style.css:** CSS styling
* **strategies.yaml:** Strategy definitions

## Key Features

* Form for entering tickers, selecting strategy and year
* Backtesting results display
* Investment resources sidebar
* Responsive design with modern styling

## Data Flow

1. User submits form data (tickers, strategy, year)
2. Flask processes the request and runs backtest logic
3. Results are rendered in the template
4. Transactions and profit summary are displayed

## strategies.yaml

The strategy definitions file remains the same:

```yaml
- Strategy1
- Strategy2
- Strategy3
```

## UI Design

The UI features:
* Gradient background
* Card-based layout
* Responsive tables
* Hover effects on buttons
* Consistent color scheme

## Architecture Diagram

```mermaid
graph TD
    A[Flask App] --> B[Routes];
    B --> C[Templates];
    B --> D[Static Files];
    C --> E[Form Handling];
    C --> F[Results Display];