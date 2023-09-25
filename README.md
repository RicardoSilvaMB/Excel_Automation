
# AWS Calculator Excel Automation

This script enables you to optimize your time when you finish your pricing in AWS Calculator.

### Pre-requisites

1. **Python**: Before anything, this script was written in Python. Ensure you have Python installed on your PC. If not, just google "install Python" and follow an installation guide.

### Installation

2. **Packages Installation**: Open your terminal and navigate to the directory containing the script. Then, run the following command to install all necessary packages:

```bash
pip install -r requirements.txt
```

### Usage

3. **Script Execution**: Run the command below from the main directory. Replace the placeholders `<path_to_json>`, `<output_directory>`, and `<project_name>` with your values:

```bash
python3 excel_automation.py --json-dir <path_to_json> --output-dir <output_directory> --project-name <project_name>
```

**Example**:

```bash
python3 excel_automation.py --json-dir ~/Downloads/My\ Estimate\ \(1\).json --output-dir ./ --project-name test
```

Note:
- For `--json-dir`, specify both the directory and the *FILENAME*.json.
- For `--output-dir`, specify the directory where you want to save the generated Excel file.
- For `--project-name`, provide the project name, which will be used to name the generated Excel file.
