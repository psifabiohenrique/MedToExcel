from typing import Dict, List, Union
from PySide6.QtGui import QClipboard
from med_to_excel.core.utils.correct_sequence_time import clear_data


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


def calculate_response_time(time_data: str, consequences_data: str, use_comma: bool) -> str:
    """
    Calculate and format response time data based on time and consequences data.
    
    Args:
        time_data: String containing time measurements
        consequences_data: String containing consequence data
        use_comma: Whether to use comma as decimal separator
        
    Returns:
        str: Formatted response time data
    """
    clipboard = QClipboard()
    
    # Process input data
    processed_time_data = process_time_data(clear_data(time_data))
    processed_consequences = clear_data(consequences_data)
    
    reinforcement_number = 1
    result: Dict[str, List[int]] = {}
    
    # Process data for each consequence
    for i in range(len(processed_consequences)):
        reinforcement_key = f"Reinforcement: {reinforcement_number}"
        
        if reinforcement_key in result:
            result[reinforcement_key].append(processed_time_data[i])
        else:
            result[reinforcement_key] = [processed_time_data[i]]
            
        # Update reinforcement number based on consequence
        if processed_consequences[i] == '1':
            reinforcement_number += 1
    
    # Format output
    output = "RESPONSE TIME (Time between trial start and correct response)\n\n"
    
    for reinforcement, times in result.items():
        output += f"{reinforcement}:\t"
        for time in times:
            if use_comma:
                output += f"{str(time).replace('.', ',')}\t"
            else:
                output += f"{time}\t"
        output += "\n"
    
    try:
        clipboard.setText(output)
        return "Done"
    except:
        return "Error"
            