# logger.py
import csv
import datetime
import functools
import re
# Global log entries list
log_entries = []
now = datetime.datetime.now()
filename = 'C:/Users/uvcom/OneDrive/Desktop/gilson223_logs/'+ now.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
print(f"\nLog will be saved to \n{filename}\n")



# Define the decorator
def log_command(func):
    @functools.wraps(func)
    def wrapper_log_command(*args, **kwargs):
        # Get the current date and time
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Call the original function and get the response
        response = func(*args, **kwargs)
        
        # Log the command, response, and timestamp
        log_entry = {
            'timestamp': timestamp,
            'command': args[0],  # Assuming the command is the first argument
            'response': response,
            'description':parse_command(args[0])
        }
        
        # Append the log entry to the global log entries list
        log_entries.append(log_entry)
        
        save_log_entries(filename)
        return response
    
    return wrapper_log_command

def parse_command(cmd: str)-> str:
    if cmd == 'H':
        description = 'Moving needle to home position.'
    elif cmd == 'KH':
        description = 'Stopping pump.'
    elif cmd == 'K<':
        description = 'Running pump in counterclockwise direction.'
    elif cmd == 'K>':
        description = 'Running pump in clockwise direction.'
    elif cmd == 'V0':
        description = 'Valve set to position zero.'
    elif cmd == 'V1':
        description = 'Valve set to position one.' 
    elif cmd == 'SR':
        description = 'Setting pump to remote mode.'
    elif cmd == 'SK':
        description = 'Setting pump to keypad mode.'
    elif re.search(r'Z\d+', cmd):
        z = cmd.split('Z')[1]
        if ',' in z:
            speed = z.split(',')[1]
            z = z.split(',')[0]
            speed_addendum = f' at speed {speed}.'
        else:
            speed_addendum = '.'
        z = int(z) / 10 # convert to mm
        z = str(z)
        description = f'Moving z to position {z}' + speed_addendum
    elif re.search(r'X\d+/\d+', cmd):
        xy = cmd.strip('X')
        if ',' in xy:
            speed = xy.split(',')[1]
            xy = xy.split(',')[0]
            speed_addendum = f' at speed {speed}.'
        else:
            speed_addendum = '.'
        x = xy.split('/')[0]
        y = xy.split('/')[1]
        x = int(x)/10 # convert into mm
        y = int(y)/10 # convert into mm
        description = f'Moving to position xy = ({x},{y})' + speed_addendum
    else:
        print(f'Command could not be translated into human-friendly format for logging. Command was {cmd}')
        print('Command was still executed\n')
        return ''

    print(description + '\n')

    return description

def save_log_entries(filename, verbose: bool = False):
    """Save the log entries to a CSV file."""
    # Get the current date and time for the filename
    # if filename == None:
    #     now = datetime.datetime.now()
    #     filename = 'C:/Users/uvcom/OneDrive/Desktop/gilson223_logs/'+ now.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    
    # Write the log entries to a CSV file
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['timestamp', 'command', 'response', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in log_entries:
            writer.writerow(entry)
    
    if verbose:
        (f"Log saved to {filename}")