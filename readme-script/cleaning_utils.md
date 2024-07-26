# `cleaning_utils.py` - Explanation

## Overview

The `cleaning_utils.py` script provides utility functions for processing housing market data. It includes functions for extracting weekly prices from text and calculating the number of months between a given date and a reference date.

## Step-by-Step Explanation

### 1. Import Required Libraries

The script starts by importing essential libraries:
- **`re`**: The regular expression library used for pattern matching in strings.
- **`datetime`**: Provides classes for manipulating dates and times.

### 2. Define Regular Expression Pattern

A regular expression (regex) pattern is defined to identify weekly prices within text. This pattern is designed to handle various formats of price listings.

- **Pattern Breakdown**:
  - **`\$\s*`**: Matches a dollar sign followed by any number of whitespace characters.
  - **`(\d{1,3}(?:,\d{3})*)`**: Captures the numeric price amount, allowing for commas as thousand separators.
  - **`(?:\s*\+\s*.*|(?:\s*(?:per\s*week|pw|incl\s*water|week|wk|w)))`**: Matches optional text that may follow the price, such as "+", "per week", "pw", "incl water", and other variations.

### 3. Define `extract_weekly_price` Function

The `extract_weekly_price` function extracts and converts a weekly price from a text string.

- **Function Steps**:
  1. **Search for Price**: Applies the regex pattern to find a price within the text.
  2. **Extract Price**: If a match is found, the function extracts the price string from the matched group.
  3. **Format Price**: Removes commas from the extracted price string for easier conversion.
  4. **Convert Price**: Converts the cleaned price string to a float, then to an integer.
  5. **Error Handling**: If the conversion fails, the function returns `None`.
  6. **Return Value**: Returns the price as an integer or `None` if no valid price is found.

### 4. Define `get_relative_month` Function

The `get_relative_month` function calculates the number of months between a given date and a fixed reference date.

- **Function Steps**:
  1. **Parse Date**: Converts the input text, which should be in "Month Year" format (e.g., "Jun 2023"), into a `datetime` object.
  2. **Calculate Differences**: Computes the difference in years and months between the fixed reference date and the parsed date.
  3. **Calculate Relative Months**: Converts these differences into a total month count.
  4. **Return Value**: Returns the total number of months between the two dates.

## Additional Notes

- **Regular Expression**: The regex pattern is flexible to accommodate various price formats. Adjustments may be necessary if different formats are encountered.
- **Error Handling**: Basic error handling is included for conversion operations. Ensure the input text follows expected formats to avoid errors.
- **Date Format**: The `get_relative_month` function expects dates in "Month Year" format. Verify that input dates conform to this format to prevent parsing errors.

For more information on regular expressions and date handling, refer to the [Python `re` documentation](https://docs.python.org/3/library/re.html) and [Python `datetime` documentation](https://docs.python.org/3/library/datetime.html).
