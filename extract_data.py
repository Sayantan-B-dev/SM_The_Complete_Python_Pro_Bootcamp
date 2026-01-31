from bs4 import BeautifulSoup
import re


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_udemy_curriculum(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")

    output_lines = []

    # Section titles if present
    section_headers = soup.find_all(
        lambda tag: tag.name in ["h2", "h3"]
        and "Section" in tag.get_text()
    )

    if section_headers:
        for header in section_headers:
            section_title = clean_text(header.get_text())
            output_lines.append(section_title)

            ul = header.find_next("ul", class_="ud-unstyled-list")
            if not ul:
                continue

            for li in ul.find_all("li", recursive=False):
                title_span = li.find("span", attrs={"data-purpose": "item-title"})
                if not title_span:
                    continue

                title = clean_text(title_span.get_text())
                output_lines.append("  " + title)

    else:
        # Fallback when section headers are not present
        ul = soup.find("ul", class_="ud-unstyled-list")
        if not ul:
            return ""

        output_lines.append("Section")

        for li in ul.find_all("li", recursive=False):
            title_span = li.find("span", attrs={"data-purpose": "item-title"})
            if not title_span:
                continue

            title = clean_text(title_span.get_text())
            output_lines.append("  " + title)

    return "\n".join(output_lines)


def main():
    input_path = "input.html"
    output_path = "output.txt"

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    tree_text = extract_udemy_curriculum(html_content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tree_text)

    print("Curriculum tree extracted successfully")


if __name__ == "__main__":
    main()
