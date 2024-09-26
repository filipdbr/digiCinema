# **This is a Draft**

## How to Set Up the Project
1. Open your terminal and navigate to the project directory.
2. Install the dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Info for Analytics
- `year = 0` means that no year was provided while entering the data into the system.

## Info About the Data
### Data Pre-Cleaning:
1. **Duplicates Removed**: 
    - Movies with the same title but different directors are considered distinct.
2. **Whitespaces Trimmed**: 
    - Any leading or trailing whitespaces in the data have been removed.

### Data Normalization:
1. **Consistent Formatting**:
    - Titles and director names are capitalized for uniformity.
2. **Consistent Data Types**:
    - Data types are standardized across all records.

## What Hasn't Been Done
- Verification of outliers.
