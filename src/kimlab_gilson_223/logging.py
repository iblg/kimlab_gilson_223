# logger.py
import csv
import datetime
import functools

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
            'response': response
        }
        
        # Append the log entry to the global log entries list
        log_entries.append(log_entry)
        
        save_log_entries(filename)
        return response
    
    return wrapper_log_command

def save_log_entries(filename, verbose: bool = False):
    """Save the log entries to a CSV file."""
    # Get the current date and time for the filename
    # if filename == None:
    #     now = datetime.datetime.now()
    #     filename = 'C:/Users/uvcom/OneDrive/Desktop/gilson223_logs/'+ now.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    
    # Write the log entries to a CSV file
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['timestamp', 'command', 'response']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in log_entries:
            writer.writerow(entry)
    
    if verbose:
        (f"Log saved to {filename}")