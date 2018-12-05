#!/usr/bin/python

import sys

CONTROL_KEYS = {
	'KEY_LEFT_CTRL':  0x80,
	'KEY_LEFT_SHIFT':  0x81,
	'KEY_LEFT_ALT':  0x82,
	'KEY_LEFT_GUI':  0x83,
	'KEY_RIGHT_CTRL':  0x84,
	'KEY_RIGHT_SHIFT' : 0x85,
	'KEY_RIGHT_ALT':  0x86,
	'KEY_RIGHT_GUI':  0x87,
	'KEY_UP_ARROW':  0xDA,
	'KEY_DOWN_ARROW':  0xD9,
	'KEY_LEFT_ARROW' : 0xD8,
	'KEY_RIGHT_ARROW':  0xD7,
	'KEY_BACKSPACE':  0xB2,
	'KEY_TAB':  0xB3,
	'KEY_RETURN' : 0xB0,
	'KEY_ESC':  0xB1,
	'KEY_INSERT':  0xD1,
	'KEY_DELETE':  0xD4,
	'KEY_PAGE_UP':  0xD3,
	'KEY_PAGE_DOWN': 0xD6,
	'KEY_HOME':  0xD2,
	'KEY_END':  0xD5,
	'KEY_CAPS_LOCK':  0xC1,
	'KEY_F1':  0xC2,
	'KEY_F2':  0xC3,
	'KEY_F3':  0xC4,
	'KEY_F4':  0xC5,
	'KEY_F5':  0xC6,
	'KEY_F6':  0xC7,
	'KEY_F7':  0xC8,
	'KEY_F8': 0xC9,
	'KEY_F9': 0xCA,
	'KEY_F10': 0xCB,
	'KEY_F11': 0xCC,
	'KEY_F12': 0xCD
}

COMMANDS = {
	'DELAY':0xE0,
	'STRING':0xE1,
	'PRESS':0xE2,
	'RELEASE':0xE3,
	'WRITE':0xE4,
	'FILE':0xE5,
	'UKNOWN': 0xE6
}

def encode_int(number, b_array)
	b_array.append((number>>24) & 0xff)
	b_array.append((number>>16) & 0xff)
	b_array.append((number>>8) & 0xff)
	b_array.append((number) & 0xff)

def encode_delay(tokens, b_array):
	delay_time = int(tokens[1])
	b_array.append(COMMANDS['DELAY'])
	encode_int(delay_time, b_array)

def encode_control_keys(tokens, b_array):
	for tok in tokens:
		if(tok in CONTROL_KEYS):
			b_array.append(COMMANDS['PRESS'])
			b_array.append(CONTROL_KEYS[tok])
		else:
			for c in tok:
				b_array.append(COMMANDS['PRESS'])
				b_array.append(c)

	b_array.append(COMMANDS['RELEASE'])

def encode_print(line, b_array):
	line = line.replace('STRING ', '')
	line_len = len(line)

	b_array.append(COMMANDS['STRING'])
	encode_int(line_len, b_array)
	b_array += line

def encode_print_file(line, b_array):
	line = line.replace('FILE ', '')
	line_len = len(line)

	b_array.append(COMMANDS['FILE'])
	encode_int(line_len, b_array)
	b_array += line

def encode_script(file_name):
	script_file = open(file_name, 'r')
	b_array = bytearray()

	for line in script_file:
		tokens = line.rstrip().split(' ')
	
		if(tokens>0):
			head_command = tokens[0]

			if(head_command in CONTROL_KEYS):
				encode_control_keys(tokens, b_array)
			elif(head_command == "STRING"):
				encode_print(line.rstrip(), b_array)
			elif(head_command == "FILE"):
				encode_print_file(line.rstrip(), b_array)
			elif(head_command == "DELAY"):
				encode_delay(tokens, b_array)
			elif(head_command == "REM"):
				pass

	return b_array

def encode():
	file_name_flag = sys.argv.index("-f")

	if(file_name_flag):
		file_name = sys.argv[file_name_flag + 1]
		byteArray = encode_script(file_name)
		sys.stdout.write(byteArray)

encode()