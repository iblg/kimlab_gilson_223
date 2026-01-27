########################################################################
# ENV = gsioc-win-32 on 
########################################################################


#-----------------------------------------------------------------------
# GSIOC.py
#
# Demonstrates how to bind the Gsioc32.dll to a Python script running
#   under Windows 10.
# The Gsioc32.dll will need to be in the path and the Gsioc Server needs
#   to be installed.
# This requires the 32-bit version of Python.
#
# To run the script: py -3.7-32 GSIOC.py i 63 %
#   i is i (immediate) or b (buffered)
#   63 is the unit id (0..63)
#   % is the command to send over Gsioc
#-----------------------------------------------------------------------
import sys
import ctypes
from ctypes import *
from time import sleep

#-----------------------------------------------------------------------
# Returns the dll version from the Gsioc32.dll

def get_dll_version():
	try:
		# load the Gsioc32.dll and function
		lib = windll.gsioc32
		# interface -> void GetDllVersion(char* rsp, int maxrsp)
		getdllver = lib.GetDllVersion
		
		# setup the parameters
		rsp = ctypes.create_string_buffer(256)
		rsplen = ctypes.c_int(256)
		
		# execute the call into the Gsioc32.dll
		getdllver(rsp, rsplen)
		
		# return the response
		return rsp.value
	except OSError as ex:
		print("WARNING:", ex)
		return "Error"

#-----------------------------------------------------------------------
# Returns the result of an immediate command
#   unitid is the unit id of the instrument (0..63)
#   command is the command string to send to the instrument
def immediate(unitid, command):
	try:
		# load the Gsioc32.dll and function
		lib = windll.gsioc32
		# interface -> int ICmd(int unit, char const* cmd, char* rsp, int maxrsp)
		icmd = lib.ICmd
				
		# setup the parameters
		rsp = ctypes.create_string_buffer(256)
		rsplen = ctypes.c_int(256)

		# convert the incoming command to UTF-8 bytestring
		command = command.encode('utf-8')
		print(f"Unit ID: {unitid} received immediate command: {command}.")

		# execute the call into the Gsioc32.dll
		icmd(unitid, command, rsp, rsplen)

		# return the response
		return rsp.value
	except OSError as ex:
		print("WARNING:", ex)
		return "Error"

#-----------------------------------------------------------------------
# Returns the result of a buffered command
#   unitid is the unit id of the instrument (0..63)
#   command is the command string to send to the instrument
def buffered(unitid, command):
	try:
		# load the Gsioc32.dll and function
		lib = windll.gsioc32
		# interface -> int BCmd(int unit, char const* cmd, char* rsp, int maxrsp)
		bcmd = lib.BCmd
				
		# setup the parameters
		rsp = ctypes.create_string_buffer(256)
		rsplen = ctypes.c_int(256)

		# convert the incoming command to UTF-8 bytestring
		command = command.encode('utf-8')
		print(f"Unit ID: {unitid} received buffered command: {command}.")

		# execute the call into the Gsioc32.dll
		bcmd(unitid, command, rsp, rsplen)

		# return the response
		return rsp.value
	except OSError as ex:
		print("WARNING:", ex)
		return "Error"


#-----------------------------------------------------------------------
# Checks the command line values and tests communication through the 
# #   Gsioc32.dll.
# def main(commandType, unitid, command, verbose=False):
# 	# echo the version of the Gsioc32.dll
# 	if verbose:
# 		print("Gsioc32.dll version: " + str(get_dll_version()))

# 	# check to see if this is an immediate or buffered command and execute
# 	if commandType == 'i':
# 		print("ICmd Response: " + str(immediate(unitid, command)))
# 	else:
# 		print("BCmd Response: " + str(buffered(unitid, command)))

#-----------------------------------------------------------------------
# Run main
#   argv[1] is the command type - i for immediate, b for buffered
#   argv[2] is the uint id (0..63)
#   argv[3] is the command
# main(sys.argv[1], int(sys.argv[2]), sys.argv[3])

def run(cmd: str | tuple[str], 
		cmd_type: str = 'b', 
		unit_id: int = 10, 
		show_command_sent: bool = False, 
		show_response: bool = True, 
		sleep_before: float = 0.5):
	"""
	Run a command, or a tuple of commands

	cmd: str or tuple of str
	The commands that you want to pass to the instrument.

	cmd_type: str, default 'b'
	The command type. Should be 'b' or 'i' for buffered or immediate. Buffered commands are passed to the instrument to make it actually do something
	(such as move). Immediate commands are commands that return information about the current state of the instrument.

	unit_id: int, default 10
	The unit id is a unique number assigned to the instrument in GSIOC, which is the connection protocol provided by GIlson.
	By default, the 223 autosampler is 10. The Minipuls3 pump is 30. It is not recommended to change this default.

	show_command_sent: bool, default False
	If true, prompts the Python program to echo the command sent to the instruments.

	show_response: bool, default True
	If true, prompts the Python program to echo the response received from the instrument.

	sleep_before: float, default 0.5
	The time (in seconds) to wait before running the command. This is done to prevent crashes and miscommunications.
	"""
	sleep(sleep_before)

	def check_command_type(cmd_type):
		if cmd_type in ('i', 'b'):
			return True
		else:
			print('Incorrect command type. The only allowed command types are \'b\' for buffered commands and \'i\' for immediate commands.')
			print('Buffered commands tell the instrument to do something. Immediate commands tell the instrument to give diagnostic info like current location.')
			return False
	
	if check_command_type(cmd_type):
		pass
	else:
		return

	if isinstance(cmd, str):
		if cmd_type == 'i':
			resp = immediate(unit_id, cmd)
		else:
			resp = buffered(unit_id, cmd)

	elif isinstance(cmd, tuple):
		resp = []
		if cmd_type == 'i':
			for i in cmd:
				resp.append(immediate(unit_id, i))
		else:
			for i in cmd:
				resp.append(buffered(unit_id, i))
	else:
		pass

	if show_command_sent:
		print('Command input: cmd = {}, cmd_type: {}, unit_id: {}'.format(cmd, cmd_type, unit_id))
	
	if show_response:
		print(str(resp))

	return resp

def main():
	cmd_type = 'b'
	unit_id = 10

	cmd = 'H'
	cmd = 'X0300/0300'
	run(cmd, cmd_type=cmd_type, unit_id=unit_id)

	return


if __name__ == '__main__':
	main()
