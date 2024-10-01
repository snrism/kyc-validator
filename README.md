# KYC Validator

A sample demo app that validates whether an uploaded document, such as a passport or driver's license, is legitimate. The tool extracts key information from the document and checks its authenticity.

## Features

- Supports document types: **Passport** and **Driver's License**.
- Extracts key information such as name, date of birth, and document number.
- Provides a basic legitimacy check for uploaded documents.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/snrism/kyc-validator.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Anthropic API key:
   - Sign up (https://console.anthropic.com/settings/keys) for an Anthropic account and obtain an API key
   - Set the API key as an environment variable or update it in the script

4. Run the application
    ```
    streamlit run kyc-processor.py
    ```

5. Upload your document (passport or driver's license) for validation and check the response.

## Limitations

- The current implementation is limited to processing US license and passport.
- The quality of the feedback depends on the capabilities of the Anthropic AI model.

## Contributing

Contributions to improve the KYC input validator app are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

This project is licensed under the MIT License.

