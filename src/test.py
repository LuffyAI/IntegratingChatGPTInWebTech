from helperFunctions import php_code_sniffer

# Example usage
php_code = """
<?php
if (true)
    $variable = "Hello, world!";
"""

is_valid, message, output = php_code_sniffer(php_code)
print(f"Is valid? {is_valid}")
print("Message:")
print(message)
print("Output Message:")
print(output)
