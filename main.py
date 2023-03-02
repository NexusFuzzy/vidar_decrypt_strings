#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

def xor(part_1, part_2):
   output = ""
   c = 0

   if len(str(part_2[c])) == 1:
       for s in part_1:
           output += chr(int(s) ^ ord(str(part_2[c])))
           c+=1
   else:
       for s in part_1:
           output += chr(int(s) ^ int(part_2[c]))
           c+=1
   return output

def get_string(addr, size):
    try:
        output = []
        for offset in range(size):
            output.append(getByte(addr))
	    addr = addr.add(1)
        return output
    except:
        # Sometimes we try to read bytes where there aren't any.
        # We return an empty array if this is the case
        output = []
        return output

for x in getReferencesTo(toAddr("func_decrypt_string")):
    length = 0
    xor_values = []
    print("[*] Found function call at " + x.getFromAddress().toString())
    ref_addr = x.getFromAddress().toString()
    prev_instr = getInstructionBefore(toAddr(ref_addr))
    instr_addr = prev_instr.getAddress()

    counter = 0
    xor_values = []
    while counter <= 3:

        value_found = False
        try:
            if "ECX" in prev_instr.getOpObjects(0)[0].toString():
                length = int(prev_instr.getOpObjects(1)[0].toString(), 16)
                print("Found length: " + str(length))
                value_found = True 
        except:
            pass

        if not value_found:
            try:
                key_addr = prev_instr.getOpObjects(0)[0].toString()
                print("Possible string is at: " + key_addr )
                output = get_string(toAddr(key_addr), length)
                if len(output) == length and length != 0:
                    xor_values.append(output)
            except Exception as ex:
                pass
        

        prev_instr = getInstructionBefore(prev_instr.getAddress())
        counter += 1
    
    if len(xor_values) == 2:
        decrypted = xor(xor_values[0], xor_values[1])
        comment_addr = (getInstructionAfter(getInstructionAfter(x.getFromAddress()))).getAddress()
        listing = currentProgram.getListing()
	codeUnit = listing.getCodeUnitAt(comment_addr)
	codeUnit.setComment(codeUnit.EOL_COMMENT, '[*] ' + decrypted)
    else:
        print("xor_values has wrong size " + str(len(xor_values)))
    print("\n")
    

