import subprocess
import os

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def convert_with_pandoc(input_text):
    # Write input to a temporary file
    with open('temp_input.wiki', 'w', encoding='utf-8') as f:
        f.write(input_text)

    # Run pandoc
    try:
        result = subprocess.run(
            ['pandoc', '-f', 'mediawiki', '-t', 'markdown', 'temp_input.wiki'],
            capture_output=True,
            text=True,
            check=True
        )
        converted_text = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e}")
        converted_text = ""
    finally:
        # Clean up temporary file
        os.remove('temp_input.wiki')

    return converted_text

def main():
    input_file_path = "data/article.txt"  # Update this path to your MediaWiki file
    mediawiki_content = read_file(input_file_path)

    # Write original MediaWiki content to a file
    mediawiki_output_path = "output_mediawiki.txt"
    write_file(mediawiki_output_path, mediawiki_content)
    print(f"Original MediaWiki content written to: {mediawiki_output_path}")

    # Convert and write Markdown content to a file
    markdown_content = convert_with_pandoc(mediawiki_content)
    markdown_output_path = "output_markdown.md"
    write_file(markdown_output_path, markdown_content)
    print(f"Converted Markdown content written to: {markdown_output_path}")

if __name__ == "__main__":
    main()
