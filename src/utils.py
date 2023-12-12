from const import table_prompt_initial, text_containing_tags
import requests
import re


def process_table(soup_table):
    """
    Function to convert an HTML table to a 2D Python list
    :param soup_table: The BeautifulSoup table element
    :return: A 2D Python list containing the tabular data
    """
    # This will contain our Table data
    data = []

    # See if this table has a header, and if so, add it to our data as the first row
    header = soup_table.find('thead')
    # grab all the headers, extract and clean the text, and add it to our data
    if header is not None:
        data.append([h.text.strip().replace('\xa0', ' ') for h in header.find_all('th')])

    # grab the main table body
    tbody = soup_table.find('tbody')
    if tbody is None:
        tbody = soup_table

    # get all rows
    rows = tbody.find_all('tr')

    # loop through every row
    for row in rows:
        # this will hold the data for this column
        col_data = []
        # check if there is a header, and if so, add it to the column data
        header = row.find('th')
        if header is not None:
            col_data.append(header.text.strip().replace('\xa0', ' '))

        # get al of the data columns for this row
        cols = row.find_all('td')

        # loop through each element in the column, clean it, and append to col_data
        for element in cols:
            element = element.text.strip()
            if element is None:
                col_data.append("N/A")
            else:
                element = element.replace('\xa0', ' ')
                col_data.append(element)
        # add the row to our data
        data.append(col_data)
    return data


def table2text(table):
    """
    This function formats a table into a more human-readable format
    :param table: The table loaded from html, a 2D Python list
    :return: Formatted string
    """
    table_str = ""
    # loop through every row
    for i, row in enumerate(table):
        # indicate which row we are in
        table_str += "R{}: ".format(i)
        # loop through every column
        for j, column in enumerate(row):
            # indicate which column we are in
            table_str += 'C{}: "{}" '.format(j, column)
        # let's add a newline after the last column (probably not necessary)
        if i != len(table) - 1:
            table_str += '\n'
    return table_prompt_initial.format(table=table_str)


def in_table(element):
    """
    Check if the current element is contained in a table, in which case, it has already been processed
    :param element: Soup element
    :return: True if in table, False otherwise
    """
    table_parents = element.find_parents('table')
    if len(table_parents) > 1:
        return True
    else:
        return False


def element_contains_text_children(element):
    """
    Checks if the element contains children that are text-containing children
    :param element:
    :return:
    """
    for child in element.find_all():
        if child.name in text_containing_tags:
            return True
    return False


def clean_text(text):
    text = re.sub(r'\[\d+\]', '', text)
    # text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('[edit]', '')
    return text


class BreakException(Exception):
    pass


def process_element(element, text: str = "", verbose: bool = False, break_string: str = "See also[edit]"):
    """
    Recursive function that iterates over all elements in the Soup HTML structure
    and extracts and formats text as prescribed for each type of HTML structure.

    NOTE: This function needs to be optimized.

    :param element: The soup element (typically the top-level element)
    :param text: The string that the function appends the results to
    :param verbose: True for verbosity, False otherwise
    :return: The extracted text as a String
    """
    # check if element has the name attribute. If it doesn't, it is a nonstandard tag that we want to ignore
    if element.name:
        # handle tables independently
        if element.name == 'table':
            if verbose:
                print("Handling table...")
            table_data = table2text(process_table(element))
            text += table_data
# handle plain text tags
        elif element.name in text_containing_tags:
            # check if this was in a table and thus already processed
            if not in_table(element):
                if element.name == 'strong':
                    text += '\n\n\n'
                if verbose:
                    print("Handling text...")
                element_text = element.get_text()
                # ignore any text that is one character or less
                if len(element_text) > 1:
                    if break_string in element_text:
                        raise BreakException()
                    if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        text += '\n'
                        if element.name == 'h1':
                            text += '\n\n'
                        text += 'Heading<{0}>: {1}:'.format(element.name, clean_text(element_text))
                    else:
                        # only process the element if it is the bottom-level text element
                        # this handles the issue embedded text tags
                        if not element_contains_text_children(element):
                            if element.name == 'li':
                                text += ' - '
                            text += clean_text(element_text)
                            text += '\n'
        # if we encountered a list item, then add in the list text (-, bullet point, etc.)
        elif element.name == 'li':
            if 'data-list-text' in element.attrs:
                text += element.attrs['data-list-text']
        # ignore table elements because they are already handled in the table handler
        elif element.name in ['td', 'tr']:
            pass
        # ignore the rest
        else:
            if verbose:
                print("Tag type not considered in loop: " + element.name)
    # recursively loop through the children of every element
    for child in element.find_all(recursive=False):
        try:
            text = process_element(child, text, verbose=verbose)
        except BreakException:
            break
    if verbose:
        print("Done.")

    return text
