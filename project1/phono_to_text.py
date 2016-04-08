import sys
import argparse

def build_codebook(cb_file):
	cb_file = open(cb_file, 'r')
	codebook = {}
	for line in cb_file:
		sp = line.split()
		if len(sp) == 3: 
			code, message = sp[1], sp[0]
			code = code[1:]
			if code not in codebook:
				codebook[code] = message
			else:
				codebook[code] = message +'/'+ codebook[code]
		else:
			message = sp[0]
			codes = []
			i = 0
			for st in sp[1:]:
				if st != '-w':
					if sp[1:][i + 1] == '-w':
						codes.append(st[1:] + ' ')
					else:
						codes.append(st[1:])	
				i = i + 1
			code = ''
			for c in codes: 
					code = code + c
			code = code[:(len(code)-1)]
			if code not in codebook:
				codebook[code] = message
			else:
				codebook[code] = message + codebook[code]
	return codebook

def decode(input_file, codebook):
	 output_file = input_file + '_text.txt' 
	 output_file = open(output_file, 'w')
	 input_file = open(input_file, 'r')
	 for line in input_file:
	 	sp = line.split()
	 	output_line = []
	 	i = 0
	 	for w in sp:
			if i < (len(sp) - 3):
				mwe3 = w + ' ' + sp[i + 1] + ' ' + sp[i + 2]
	 			mwe4 = mwe3 + ' ' + sp[i + 3]
	 			if mwe4 in codebook:
	 				output_line.append(codebook[mwe4])
	 				sp.remove(sp[i + 1])
	 				sp.remove(sp[i + 2])
	 				sp.remove(sp[i + 3])
	 			elif mwe3 in codebook:
	 				output_line.append(codebook[mwe3])
	 				sp.remove(sp[i + 1])
	 				sp.remove(sp[i + 2])
	 			else:
	 				output_line.append(codebook[w])
	 		elif i >= (len(sp)-3) and i < (len(sp)-2):
				mwe3 = w + ' ' + sp[i + 1] + ' ' + sp[i + 2]
				if mwe3 in codebook:
	 				output_line.append(codebook[mwe3])
	 				sp.remove(sp[i + 1])
	 				sp.remove(sp[i + 2])
	 			else:
	 				output_line.append(codebook[w])
	 		else:
	 			output_line.append(codebook[w])
	 		i = i + 1
	 	i = 0
	 	for w in output_line:
	 		output_file.write(w)
	 		if i != (len(output_line) -1):
	 			output_file.write(' ')
	 		else:
	 			output_file.write('\n')
	 		i = i + 1
	 output_file.close() 
	 
def main():
    commandline_parser = argparse.ArgumentParser()   
    commandline_parser.add_argument("--input-file", nargs =1, help="Specify the path of the file to decode")  
    args = vars(commandline_parser.parse_args())
    input_file = args["input_file"][0]
    codebook = build_codebook("data/dict.txt")
    decode(input_file, codebook)
	 
if __name__ == '__main__':
	main()
	 

		