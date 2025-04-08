from bs4 import BeautifulSoup

class HTMLSimpleParser:
    """
    A class to parse HTML content and extract specific values.
    """

    def __init__(self, html_string):
        """
        Initializes the HTMLParser with the given HTML string.

        Args:
            html_string (str): The HTML content as a string.
        """
        self.soup = BeautifulSoup(html_string, "html.parser")




    def extract_title_tags(self, join_str="|", max_count=-1):
        """
        Extracts the values of <title> tags from the HTML content.

        Args:
            join_str (str): The string used to join multiple <title> values. Default is a single space.
            max_count (int): The maximum number of <title> values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted <title> values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        titles = [title.get_text(strip=True) for title in self.soup.find_all("title")]

        if not titles:
            return ""

        if max_count > 0:
            titles = titles[:max_count]

        return join_str.join(titles)
    
    
    
    
    
    def extract_og_meta_tags(self, property_name: str | None = None, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the values of Open Graph (og) meta tags from the HTML content.

        Args:
            property_name (str | None, optional): The specific Open Graph property to extract (e.g., 'og:title').
                                                  If None, all Open Graph meta tags are extracted and joined into a single string.
            join_str (str): The string used to join multiple values if `property_name` is None. Default is '|'.
            max_count (int): The maximum number of values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted Open Graph meta tag values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        if property_name:
            meta_tag = self.soup.find("meta", property=f"og:{property_name}")
            return meta_tag.get("content", "").strip() if meta_tag else ""

        og_meta_values = [
            meta.get("content", "").strip() for meta in self.soup.find_all("meta")
            if meta.get("property", "").startswith("og:")
        ]

        if not og_meta_values:
            return ""

        if max_count > 0:
            og_meta_values = og_meta_values[:max_count]

        return join_str.join(og_meta_values)
    
    
    
    def extract_meta_tags(self, name: str | None = None, selector: str | None = None, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the values of meta tags from the HTML content.

        Args:
            name (str | None, optional): The specific meta tag name to extract (e.g., 'description').
                                         If None, all meta tags with a 'name' attribute are extracted and joined into a single string.
            selector (str | None, optional): A CSS selector to narrow down the search for meta tags.
                                             If provided, it overrides the `name` parameter.
            join_str (str): The string used to join multiple values if `name` or `selector` is None. Default is '|'.
            max_count (int): The maximum number of values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted meta tag values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        if selector:
            meta_tags = self.soup.select(selector)
            meta_values = [meta.get("content", "").strip() for meta in meta_tags]
        elif name:
            meta_tag = self.soup.find("meta", attrs={"name": name})
            return meta_tag.get("content", "").strip() if meta_tag else ""
        else:
            meta_values = [
                meta.get("content", "").strip() for meta in self.soup.find_all("meta", attrs={"name": True})
            ]

        if not meta_values:
            return ""

        if max_count > 0:
            meta_values = meta_values[:max_count]

        return join_str.join(meta_values)

    def extract_h_tags(self, level: int | None = None, selector: str | None = None, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the text content of <h1>, <h2>, ..., <h6> tags from the HTML content.

        Args:
            level (int | None, optional): The specific heading level to extract (e.g., 1 for <h1>, 2 for <h2>).
                                          If None, all heading levels are extracted and joined into a single string.
            selector (str | None, optional): A CSS selector to narrow down the search for heading tags.
                                             If provided, it overrides the `level` parameter.
            join_str (str): The string used to join multiple heading values. Default is '|'.
            max_count (int): The maximum number of values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted heading values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        if selector:
            headings = [h.get_text(strip=True) for h in self.soup.select(selector)]
        elif level:
            headings = [h.get_text(strip=True) for h in self.soup.find_all(f"h{level}")]
        else:
            headings = [h.get_text(strip=True) for h in self.soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]

        if not headings:
            return ""

        if max_count > 0:
            headings = headings[:max_count]

        return join_str.join(headings)


    def extract_links(self, selector: str | None = None, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the href attributes of <a> tags from the HTML content.

        Args:
            selector (str | None, optional): A CSS selector to narrow down the search for <a> tags.
                                             If provided, it overrides the default behavior.
            join_str (str): The string used to join multiple href values. Default is '|'.
            max_count (int): The maximum number of href values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted href values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        if selector:
            links = [a.get("href", "").strip() for a in self.soup.select(selector)]
        else:
            links = [a.get("href", "").strip() for a in self.soup.find_all("a", href=True)]

        if not links:
            return ""

        if max_count > 0:
            links = links[:max_count]

        return join_str.join(links)


    def extract_meta_description(self, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the values of meta tags with the 'description' name from the HTML content.

        Args:
            join_str (str): The string used to join multiple values. Default is '|'.
            max_count (int): The maximum number of values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted meta tag values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        meta_values = [
            meta.get("content", "").strip()
            for meta in self.soup.find_all("meta", attrs={"name": "description"})
        ]

        if not meta_values:
            return ""

        if max_count > 0:
            meta_values = meta_values[:max_count]

        return join_str.join(meta_values)


    def extract_meta_keywords(self, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the values of meta tags with the 'keywords' name from the HTML content.

        Args:
            join_str (str): The string used to join multiple values. Default is '|'.
            max_count (int): The maximum number of values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted meta tag values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        meta_values = [
            meta.get("content", "").strip()
            for meta in self.soup.find_all("meta", attrs={"name": "keywords"})
        ]

        if not meta_values:
            return ""

        if max_count > 0:
            meta_values = meta_values[:max_count]

        return join_str.join(meta_values)
    
    def extract_meta_author(self, join_str: str = "|", max_count: int = -1) -> str:
        """
        Extracts the values of meta tags with the 'author' name from the HTML content.

        Args:
            join_str (str): The string used to join multiple values. Default is '|'.
            max_count (int): The maximum number of values to return. 
                             -1 for all, 0 for an empty string, 1 for a single value. Default is -1.

        Returns:
            str: The extracted meta tag values joined by `join_str`, or an empty string if none are found.
        """
        if max_count == 0:
            return ""

        meta_values = [
            meta.get("content", "").strip()
            for meta in self.soup.find_all("meta", attrs={"name": "author"})
        ]

        if not meta_values:
            return ""

        if max_count > 0:
            meta_values = meta_values[:max_count]

        return join_str.join(meta_values)
    
    def extract_html_lang(self) -> str:
        """
        Extracts the value of the 'lang' attribute from the <html> tag in the HTML content.

        Returns:
            str: The value of the 'lang' attribute, or 'en' if not found.
        """
        html_tag = self.soup.find("html")
        return html_tag.get("lang", "en").strip() if html_tag else "en"
    
    
    
