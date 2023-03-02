#TODO write a description for this script
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

debug_counter = 0
debug_entries_to_show = 2

def xor(part_1, part_2):   
   output = ""
   c = 0
   for s in part_1:
       output += chr(int(s) ^ ord(str(part_2[c])))
       c+=1
   return output
   

def get_string(addr, size):
    output = []
    for offset in range(size):
        output.append(getByte(addr))
        #print("get_string: " + chr(getByte(addr)))
	addr = addr.add(1)
    return output

print("[*] Deobfuscating strings")

for x in getReferencesTo(toAddr("func_decrypt_string")):

    length = 0
    val_1 = []
    val_2 = []

    ref_addr = x.getFromAddress().toString()
    prev_instr = getInstructionBefore(toAddr(ref_addr))
    instr_addr = prev_instr.getAddress()
    
    # Vidar uses multiple possibilities to pass the length of the string
    # to the decryption function so we have to make some destinctions
    if prev_instr.getOpObjects(0)[0].toString() == "ECX":
       length = int(prev_instr.getOpObjects(1)[0].toString(), 16)
       print("[*] Got length for string: " + str(length))

    # Now we get the first part for the decryption routine
    prev_instr = getInstructionBefore(toAddr(instr_addr.toString()))
    instr_addr = prev_instr.getAddress()
    print("[*] Address of string 1: " + prev_instr.getOpObjects(0)[0].toString())
    # The first string can be passed in different varieties so we try some of them
    string_extracted = False
    try:
        val_1 = getDataAt(prev_instr.getOpObjects(0)[0].toString()).getValue()
        string_extracted = True
    except:
        pass

    if not string_extracted:
        try:
            key_addr = toAddr(prev_instr.getDefaultOperandRepresentation(0))
            output = get_string(key_addr, length)
            if len(output) == length:
                val_1 = output
                string_extracted = True
        except Exception as ex:
            pass    
    
    #print("[*] Extracted string 1: " + str(val_1))

    # Now we get the second part for the decryption routine
    prev_instr = getInstructionBefore(toAddr(instr_addr.toString()))
    instr_addr = prev_instr.getAddress()
    print("[*] Address of string 2: " + prev_instr.getOpObjects(0)[0].toString())
    val_2 = list(getDataAt(toAddr(prev_instr.getOpObjects(0)[0].toString())).getValue())
    #print("[*] Extracted string 2: " + str(val_2))

    print("[*] Decrypted string: " + xor(val_1, val_2))
    
    debug_counter += 1
    if debug_counter > debug_entries_to_show:
        break
    