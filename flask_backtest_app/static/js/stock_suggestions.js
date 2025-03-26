document.addEventListener('DOMContentLoaded', function() {
    const stockTickerInput = document.getElementById('stock_ticker');
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.id = 'stock_suggestions';
    suggestionsContainer.style.position = 'absolute';
    suggestionsContainer.style.zIndex = '1000';
    stockTickerInput.parentNode.appendChild(suggestionsContainer);

    stockTickerInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length >= 3) {
            fetchStockSuggestions(query);
        } else {
            clearSuggestions();
        }
    });

    function fetchStockSuggestions(query) {
        fetch(`/stock_suggestions?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (Array.isArray(data)) {
                    if (data.length > 0) {
                        displaySuggestions(data);
                    } else {
                        const message = document.createElement('div');
                        message.className = 'no-results';
                        message.textContent = 'No matching stocks found. Try a different search term.';
                        suggestionsContainer.appendChild(message);
                    }
                } else {
                    console.error('Invalid response format:', data);
                    clearSuggestions();
                }
            })
            .catch(error => {
                console.error('Error fetching stock suggestions:', error);
                clearSuggestions();
                // Show error to user
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger';
                errorDiv.textContent = `Error: ${error.message}`;
                document.querySelector('.container').prepend(errorDiv);
            });
    }

    function displaySuggestions(suggestions) {
        clearSuggestions();
        if (suggestions.length > 0) {
            const list = document.createElement('ul');
            list.style.listStyleType = 'none';
            list.style.padding = '0';
            list.style.margin = '0';
            suggestions.forEach(suggestion => {
                const item = document.createElement('li');
                item.style.padding = '5px';
                item.style.cursor = 'pointer';
                item.textContent = `${suggestion.ticker} - ${suggestion.name} (${suggestion.exchange})`;
                item.addEventListener('click', function() {
                    stockTickerInput.value = suggestion.ticker;
                    clearSuggestions();
                });
                list.appendChild(item);
            });
            suggestionsContainer.appendChild(list);
        } else {
            const message = document.createElement('div');
            message.textContent = 'No suggestions found.';
            suggestionsContainer.appendChild(message);
        }
    }

    function clearSuggestions() {
        suggestionsContainer.innerHTML = '';
    }
});