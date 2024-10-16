# Firstmail Password Changer

## Overview 🚀
**Firstmail Password Changer** is a powerful, high-speed tool designed to change passwords for Firstmail accounts. It supports various formats of email-password combinations and leverages multithreading to deliver exceptional performance. Whether you're handling single or bulk requests, this tool provides smooth, error-handled execution with beautiful log output.

---

### ✨ Features
- **Multithreading Support**: Lightning-fast password changing, even for large batches.
- **Flexible Email Format Handling**: Supports various formats including `mail|pass`, `mail:pass`, and `mail:pass:value`. The `value` field allows the user to add random or custom data as needed.
- **Detailed Console Logs**: Clear, easy-to-read logs to keep track of operations.
- **Smart Error Handling**: Thoughtful error messages and recovery mechanisms to ensure smooth operation.
- **Password Options**: You can choose to generate a random password or set a custom one.

---

### ⚙️ Setup & Usage

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Get your **X-Api-Key**:
   - Head over to [Firstmail API Dashboard](https://firstmail.ltd/lk/api) to generate your API key.

3. Configure your API key and settings in `config.json`:
    ```json
    {
        "Main": {
            "Threads": 1,
            "X-Api-Key": ""
        },
        "Password": {
            "Generate_password": true,
            "new_password": ""
        }
    }
    ```

   - In the `Password` section:
     - Set `"Generate_password"` to `true` if you want to generate a random password.
     - Set `"Generate_password"` to `false` and provide your desired password in `"new_password"` if you want to use a custom one.

4. Run the tool:
    ```bash
    python main.py
    ```

---

### 📄 Supported Input Formats
| Format             | Example                                  |
|--------------------|------------------------------------------|
| `mail:pass`        | `user@example.com:password123`          |
| `mail:pass:value`  | `user@example.com:password123:random_value` |

---

### 🔧 Configuration
Modify `config.json` to add your API key and set the number of threads as needed:
```json
{
    "Main": {
        "Threads": 1,
        "X-Api-Key": "your-api-key"
    },
    "Password": {
        "Generate_password": true,
        "new_password": ""
    }
}
