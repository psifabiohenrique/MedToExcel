from typing import Dict, List, TextIO
from PySide6.QtGui import QClipboard


def _create_index_dict() -> Dict[str, List[str]]:
    """Creates a dictionary with empty lists for each index."""
    return {
        'A:': [], 'B:': [], 'C:': [], 'D:': [],
        'E:': [], 'F:': [], 'G:': [], 'H:': [],
        'I:': [], 'J:': [], 'K:': [], 'L:': [],
        'M:': [], 'N:': [], 'O:': [], 'P:': [],
        'Q:': [], 'R:': [], 'S:': [], 'T:': [],
        'U:': [], 'V:': [], 'X:': [], 'Z:': [],
        'Y:': [], 'W:': [], 'date': None
    }


def _get_column_indexes() -> List[str]:
    """Returns a list of column indexes."""
    return ['A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 
            'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'X:', 'Z:', 
            'Y:', 'W:']


def _get_number_indexes() -> List[str]:
    """Returns a list of number indexes."""
    return [f"{i}:" for i in range(0, 1300, 5)]


def process_row_data(archive: TextIO, sieve: TextIO, is_column: bool, use_comma: bool) -> str:
    """
    Process the data from archive and sieve files to generate formatted output.
    
    Args:
        archive: File object containing the main data
        sieve: File object containing the filter data
        is_column: Whether to format output as columns (True) or rows (False)
        use_comma: Whether to use comma as decimal separator
        
    Returns:
        str: Formatted output string
    """
    sieve_list = []
    row_data = _create_index_dict()
    column_indexes = _get_column_indexes()
    number_indexes = _get_number_indexes()
    current_index = None
    full_column = None

    # Process sieve data
    for line in sieve:
        if 'FULL' in line:
            temp = line.split('-')
            full_column = temp[0]
        else:
            sieve_list.append(line.split())

    # Process archive data
    for line in archive:
        if "File" in line:
            line = line.replace('C:\\', '')
            
        temp = line.split()
        
        # Extract date
        if len(temp) == 3 and temp[0] == 'Start' and temp[1] == 'Date:':
            row_data['date'] = temp[2]
            
        # Find current index
        if len(temp) > 1 and temp[0] in column_indexes:
            current_index = temp[0]
        elif temp and temp[0][:2] in column_indexes:
            current_index = temp[0][:2]
            
        # Process data for current index
        for item in temp:
            if item in column_indexes or item in number_indexes:
                continue
            if current_index in column_indexes:
                row_data[current_index].append(item)

    # Format output data
    formatted_data = []
    for item in sieve_list:
        try:
            if item:
                column, index = item[0].split('-')
                value = row_data[f"{column}:"][int(index)]
                if use_comma:
                    value = value.replace('.', ',')
                formatted_data.append(value)
        except IndexError:
            return 'Incorrect Index'

    # Generate final output
    if full_column:
        result = str(row_data['date'])
        for value in row_data[f'{full_column}:']:
            if use_comma:
                value = value.replace('.', ',')
            result += f'\t{str(value)}'
    else:
        result = str(row_data['date'])
        separator = '\t' if is_column else '\n'
        for value in formatted_data:
            result += f'{separator}{str(value)}'

    # Reset file pointers
    archive.seek(0)
    sieve.seek(0)
    
    return result


def copy_to_clipboard(archive: TextIO, sieve: TextIO, is_column: bool, use_comma: bool) -> str:
    """
    Process data and copy it to clipboard.
    
    Args:
        archive: File object containing the main data
        sieve: File object containing the filter data
        is_column: Whether to format output as columns (True) or rows (False)
        use_comma: Whether to use comma as decimal separator
        
    Returns:
        str: "Done" if successful, "Error" if failed
    """
    clipboard = QClipboard()
    data = process_row_data(archive, sieve, is_column, use_comma)
    
    try:
        clipboard.setText(data)
        return "Done"
    except:  # noqa: E722
        return "Error"
    