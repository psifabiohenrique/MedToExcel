from typing import Dict, List
from PySide6.QtGui import QClipboard
from med_to_excel.core.utils.recorrence import remover_data


def process_time_data(time_data: str) -> List[int]:
    """
    Process time data by converting string values to integers.
    
    Args:
        time_data: String containing time values
        
    Returns:
        List[int]: List of processed time values
    """
    processed_data = []
    for value in time_data:
        processed_data.append(int(value.split('.')[0]))
    return processed_data


def clear_data(input_string: str) -> List[str]:
    """
    Clean and process input string data.
    
    Args:
        input_string: String containing data to be processed
        
    Returns:
        List[str]: Cleaned and processed data
    """
    row_data = input_string.split()
    
    # Replace commas with dots
    if ',' in input_string:
        row_data = [value.replace(',', '.') for value in row_data]
    
    # Remove data if needed
    if '/' in input_string:
        row_data = remover_data(row_data)
    
    # Remove zero values
    return [value for value in row_data if value != '0.000']


def calculate_sequence_time(time_data: str, consequences_data: str, use_comma: bool, individual: bool = False) -> str:
    """
    Calculate and format sequence time data based on time and consequences data.
    
    Args:
        time_data: String containing time measurements
        consequences_data: String containing consequence data
        use_comma: Whether to use comma as decimal separator
        individual: Whether to process individual responses (True) or sequences (False)
        
    Returns:
        str: Formatted sequence time data
    """
    clipboard = QClipboard()
    
    # Process input data
    processed_time_data = process_time_data(clear_data(time_data))
    processed_consequences = clear_data(consequences_data)
    
    # Initialize data structures
    reinforcement_number = 1
    secondary_reinforcement_number = 0
    result: Dict[str, List[List[int]]] = {}
    
    # Process data for each consequence
    for i in range(len(processed_consequences)):
        reinforcement_key = f"Reinforcement: {reinforcement_number}"
        num_responses = 12 if individual else 4
        
        if reinforcement_key in result:
            result[reinforcement_key][secondary_reinforcement_number].append(processed_time_data[i])
        else:
            result[reinforcement_key] = [[] for _ in range(num_responses)]
            result[reinforcement_key][secondary_reinforcement_number].append(processed_time_data[i])
        
        # Update reinforcement numbers
        if processed_consequences[i][0] == '1':
            reinforcement_number += 1
            secondary_reinforcement_number = 0
        elif processed_consequences[i][0] == '2':
            secondary_reinforcement_number += 1
    
    # Generate output
    output = generate_output(result, individual, use_comma)
    
    try:
        clipboard.setText(output)
        return "Done"
    except:
        return "Error"


def generate_output(result: Dict[str, List[List[int]]], individual: bool, use_comma: bool) -> str:
    """
    Generate formatted output string from processed data.
    
    Args:
        result: Dictionary containing processed data
        individual: Whether to process individual responses (True) or sequences (False)
        use_comma: Whether to use comma as decimal separator
        
    Returns:
        str: Formatted output string
    """
    # Initialize output
    if individual:
        output = "CORRECT RESPONSE TIME (Time between trial start and correct response)\n\n"
    else:
        output = "CORRECT SEQUENCE TIME (Time between trial start and 3rd correct response)\n\n"
    
    # Process blocks
    for block in range(5):
        output += process_block(block, result, individual, use_comma)
    
    # Add session means
    output += calculate_session_means(result, individual, use_comma)
    
    # Format decimal separator if needed
    if use_comma:
        output = output.replace('.', ',')
    
    return output


def process_block(block: int, result: Dict[str, List[List[int]]], individual: bool, use_comma: bool) -> str:
    """
    Process a single block of data.
    
    Args:
        block: Block number
        result: Dictionary containing processed data
        individual: Whether to process individual responses (True) or sequences (False)
        use_comma: Whether to use comma as decimal separator
        
    Returns:
        str: Formatted block data
    """
    output = f"Block {block + 1}:\t"
    num_responses = 12 if individual else 4
    
    # Add response headers
    for i in range(num_responses):
        output += f"{i+1}ª {'response' if individual else 'sequence'} correct\t"
    output += "Mean\n"
    
    # Process each reinforcement
    for reinforcement in range(1, 11):
        output += f"{reinforcement}° SR:\t"
        reinforcement_key = f"Reinforcement: {reinforcement}"
        
        if reinforcement_key in result:
            total = 0
            count = 0
            for response in result[reinforcement_key]:
                if response:
                    total += sum(response)
                    count += 1
                    output += f"{sum(response)}\t"
                else:
                    output += "0\t"
            
            if count > 0:
                output += f"{total/count}\n"
            else:
                output += "0\n"
        else:
            output += "0\t" * (num_responses + 1) + "\n"
    
    return output


def calculate_session_means(result: Dict[str, List[List[int]]], individual: bool, use_comma: bool) -> str:
    """
    Calculate and format session means.
    
    Args:
        result: Dictionary containing processed data
        individual: Whether to process individual responses (True) or sequences (False)
        use_comma: Whether to use comma as decimal separator
        
    Returns:
        str: Formatted session means
    """
    output = "\nSession Means:\t"
    num_responses = 12 if individual else 4
    
    # Calculate means for each response position
    for i in range(num_responses):
        total = 0
        count = 0
        for reinforcement in result.values():
            if i < len(reinforcement) and reinforcement[i]:
                total += sum(reinforcement[i])
                count += len(reinforcement[i])
        
        if count > 0:
            output += f"{total/count}\t"
        else:
            output += "0\t"
    
    return output