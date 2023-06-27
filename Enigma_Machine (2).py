# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 12:39:49 2023

@author: ajord
"""
import copy
# The 'copy' module is imported to be able to make a copy of the rotors more efficiently.

## CERTAMEN 2 MAQUINA ENIGMA

## PART 1 'READ THE CSV ARCHIVE'.

route = '## ENTER A ROUTE ##'

archive = '## ENTER FILE NAME ##'

# The functions that read the delivered csv file.
def read_archive(route,archive):
      
    with open(route+archive, 'r') as enigma_messages:
        
        enigma_messages.readline()
        archive_list = []
        for m in enigma_messages:
            mess_list = m.split(';')
            mess_list[2] = mess_list[2].strip('\n')
            archive_list.append(mess_list)
                       
    return archive_list

# The function that reads the file is called before anything else to avoid any kind of problem later.
# It also separates the file by rows and stores them in this variable. (what is a list)
archive_list = read_archive(route, archive)

# Function that adds the processed messages to the file.
def add_new_messages(route, archive, new_messages,new_column):
    
    
    with open(route + archive, 'r') as enigma_messages:
        
        archive_cont = enigma_messages.readlines()
        
    archive_cont[0] = archive_cont[0].strip() + ';' + new_column + '\n'
        
    for i in range(1, len(archive_cont)):
    
        archive_cont[i] = archive_cont[i].strip() + ';' + new_messages[i-1] + '\n'
    
    with open(route + archive, 'w') as enigma_messages:
        enigma_messages.writelines(archive_cont)
        

## PART 2  'CREATE AND ORDER THE ROTORS'

# The keyboard, the reflector and the rotors are defined. They are all stored in lists and the latter in lists within lists.
       
right_rotor = [['A', 'B'], ['B', 'D'], ['C', 'F'], ['D', 'H'], ['E', 'J'], ['F', 'L'], ['G', 'C'], ['H', 'P'], ['I', 'R'], ['J', 'T'], ['K', 'X'], ['L', 'V'], ['M', 'Z'], ['N', 'N'], ['O', 'Y'], ['P', 'E'], ['Q', 'I'], ['R', 'W'], ['S', 'G'], ['T', 'A'], ['U', 'K'], ['V', 'M'], ['W', 'U'], ['X', 'S'], ['Y', 'Q'], ['Z', 'O']]

middle_rotor = [['A', 'A'], ['B', 'J'], ['C', 'D'], ['D', 'K'], ['E', 'S'], ['F', 'I'], ['G', 'R'], ['H', 'U'], ['I', 'X'], ['J', 'B'], ['K', 'L'], ['L', 'H'], ['M', 'W'], ['N', 'T'], ['O', 'M'], ['P', 'C'], ['Q', 'Q'], ['R', 'G'], ['S', 'Z'], ['T', 'N'], ['U', 'P'], ['V', 'Y'], ['W', 'F'], ['X', 'V'], ['Y', 'O'], ['Z', 'E']]

left_rotor = [['A', 'E'], ['B', 'K'], ['C', 'M'], ['D', 'F'], ['E', 'L'], ['F', 'G'], ['G', 'D'], ['H', 'Q'], ['I', 'V'], ['J', 'Z'], ['K', 'N'], ['L', 'T'], ['M', 'O'], ['N', 'W'], ['O', 'Y'], ['P', 'H'], ['Q', 'X'], ['R', 'U'], ['S', 'S'], ['T', 'P'], ['U', 'A'], ['V', 'I'], ['W', 'B'], ['X', 'R'], ['Y', 'C'], ['Z', 'J']]

keyboard = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

reflector = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'D', 'I', 'J', 'K', 'G', 'M', 'K', 'M', 'I', 'E', 'B', 'F', 'T', 'C', 'V', 'V', 'J', 'A', 'T']

# A copy of each rotor is made with the copy module so as not to alter the order of the originals and thus avoid problems later.

right_rotor_copy = copy.deepcopy(right_rotor)

middle_rotor_copy = copy.deepcopy(middle_rotor)

left_rotor_copy = copy.deepcopy(left_rotor)

# Function that prints the rotors vertically and side by side including the keyboard and the reflector. (Visually simulating the enigma machine)
def print_rotors(r1, r2, r3):
    for i in range(26):
        print(f"{reflector[i]}   {r1[i][0]}-{r1[i][1]}   {r2[i][0]}-{r2[i][1]}   {r3[i][0]}-{r3[i][1]}   {keyboard[i]}")
    
    print()

print_rotors(left_rotor,middle_rotor,right_rotor)

# Function that rotates the rotors using the slicing method.
def spin_rotor(rotor,pos):

    cont1 = 0
    while cont1 < pos:
        
        rotor = rotor[1:] + rotor[:1]
        cont1 += 1
    return rotor

# Function that obtains the initial order of the rotors depending on the entered key.
def rotors_initial_pos(left_rotor, middle_rotor, right_rotor, key):
    lf_initial_pos = None
    md_initial_pos = None
    rr_initial_pos = None
    
    for pos_l, l in enumerate(left_rotor):
        if l[0] == key[0]:
            lf_initial_pos = pos_l
            break
    
    for pos_m, m in enumerate(middle_rotor):
        if m[0] == key[1]:
            md_initial_pos = pos_m
            break
    
    for pos_r, r in enumerate(right_rotor):
        if r[0] == key[2]:
            rr_initial_pos = pos_r
            break
    
    return lf_initial_pos, md_initial_pos, rr_initial_pos


## PART 3  'GET IN AND OUT POSITIONS OF LETTERS'

# To obtain these positions we will create different functions, some for the input positions, others for the output ones, and these same ones but inverted. (For when the machine makes the 'way back')

# Function that receives the position of the letter entered by keyboard and returns the letter corresponding to the input section of the rotor.
def rotor_input_letter(rotor,pos):
    
    for l in rotor:
        input_letter = rotor[pos][1]
        
    return input_letter

# Function that receives the input letter of the rotor and returns the output position of the same rotor.
def rotor_output_position(rotor, input_letter):
    
    for pos,pair in enumerate(rotor):
        
        if pair[0] == input_letter:               
            rotor_output_pos = pos
        
    return rotor_output_pos

# Function that does the same as input_letter but in reverse.
def rotor_input_letter_invert(rotor,pos):
    
    for l in rotor:
        input_letter = rotor[pos][0]
        
    return input_letter

# Function that does the same as output_pos but in reverse.
def rotor_output_position_invert(rotor, input_letter):
    
    for pos,pair in enumerate(rotor):
        
        if pair[1] == input_letter:               
            rotor_output_pos = pos
        
    return rotor_output_pos

# Function that receives the output position of the rotor next to the reflector and that looks for the position of the repeated letter in it and returns its position
def reflector_output_position(reflector, rotor_output_pos):
    
    for r in reflector:
        
        let = reflector[rotor_output_pos]
        try:
            r_output_pos = reflector.index(let,0,rotor_output_pos)
        except ValueError:
            r_output_pos = reflector.index(let,rotor_output_pos+1)
            
        return r_output_pos
    
# Function that looks for the outout position of the letter entered on the keyboard.
def keyboard_letter_position(keyboard, letter):
        
    kb_let_pos = keyboard.index(letter)
     
    return kb_let_pos
    
# Function that receives the exit position of the rotor next to the keyboard when it comes back and returns the corresponding letter on the keyboard.    
def final_letter(keyboard, r_output_pos):

    for l in keyboard:
        
        final_let = keyboard[r_output_pos]

    return final_let    


## PART 4  'JOIN ALL THE PARTS'

# To make the machine work, we will begin to define variables making use of the previously created functions and defining conditions to be fulfilled.


# List that stores all the messages already processed.
new_messages = []

# To make the machine work, a general while loop will be used, started by a counter and which will work as long as it is less than the length of the list that contains the rows of the csv file.
a = 0
# The counter is also used to indicate the positions of the key, message, and task variables as the code progresses.
while a < len(archive_list):
    
    # With this condition you are verifying which task you want to do, Encrypt or Decrypt.
    if archive_list[a][2] == 'Desencriptar':
        
        # Variables key, message and task according to the position.
        key = archive_list[a][0]
        message = archive_list[a][1]  
        mes_list = list(message)
        
        # The initial position of the rotors is defined depending on the key and using the function defined above.
        rotor_ini_pos = rotors_initial_pos(left_rotor, middle_rotor, right_rotor, key)
        
        # The 3 rotors are turned until they reach the previously defined configuration.
        
        lf_initial_position = spin_rotor(left_rotor_copy, rotor_ini_pos[0])
        
        md_initial_position = spin_rotor(middle_rotor_copy, rotor_ini_pos[1])
        
        rr_initial_position = spin_rotor(right_rotor_copy, rotor_ini_pos[2])
        
        # The rotors are printed on the screen using the previously defined function.
        print_rotors(lf_initial_position, md_initial_position, rr_initial_position)
        
       
        
        # An empty list is created to store the processed message.
        final_message = []
        i = 0
        # To process each message, another while loop will be used, initialized by a counter that will go through each letter of the message and stop when the counter is equal to the length of the message.
        # As in the other while loop, the counter also serves as an index into some variables.
        while i < len(mes_list):
            
            # This variable stores the letter to be processed and changes its position as the counter advances.           
            letter = mes_list[i]
            # Exception handling for when trying to process a 'space'. Since it is not found on the keyboard.
            try:
                kb_let_pos = keyboard_letter_position(keyboard, letter)
            # If the function gives ValueError certain conditions are executed and it is laughed
            except ValueError:
                
                lf_initial_position = spin_rotor(left_rotor_copy, rotor_ini_pos[0])
        
                md_initial_position = spin_rotor(middle_rotor_copy, rotor_ini_pos[1])
        
                rr_initial_position = spin_rotor(right_rotor_copy, rotor_ini_pos[2])
                # The 'space' is added to the final message in order to make it easier to read and understand.
                final_message.append(' ')
                
                i += 1
                
                continue
            # With this condition it is verified if the first row of the ordered column of the right rotor is equal to 'V'. If so, the middle rotor advances one position. 
            if rr_initial_position[0][0] == 'V':
                md_initial_position = spin_rotor(md_initial_position, 1)
            # With this condition it is verified if the first row of the ordered column of the middle rotor is equal to 'Q'. If so, the left rotor advances one position.       
            if md_initial_position[0][0] == 'Q':
                lf_initial_position = spin_rotor(lf_initial_position, 1)
                
            # The right rotor is rotated simulating the real enigma machine.       
            rr_initial_position = spin_rotor(rr_initial_position, 1)
            # The rotors are printed since the right rotor was rotated once and the configuration changed.
            print_rotors(lf_initial_position, md_initial_position, rr_initial_position)
            
            # In the following block of code, the message is processed following the encryption logic of the enigma machine. This is done using the functions defined above.
            
            rr_input_let = rotor_input_letter(rr_initial_position, kb_let_pos)
            
            rr_output_pos = rotor_output_position(rr_initial_position, rr_input_let)
                
            md_input_let = rotor_input_letter(md_initial_position, rr_output_pos)
                
            md_output_pos = rotor_output_position(md_initial_position, md_input_let)
                
            lf_input_let = rotor_input_letter(lf_initial_position, md_output_pos)
                
            lf_output_pos = rotor_output_position(lf_initial_position, lf_input_let)
                
            rf_output_pos = reflector_output_position(reflector, lf_output_pos)
                
            lf_input_let_invert = rotor_input_letter_invert(lf_initial_position, rf_output_pos)
                
            lf_output_pos_invert = rotor_output_position_invert(lf_initial_position, lf_input_let_invert)
                
            md_input_let_invert = rotor_input_letter_invert(md_initial_position, lf_output_pos_invert)
                
            md_output_pos_invert = rotor_output_position_invert(md_initial_position, md_input_let_invert)
                
            rr_input_let_invert = rotor_input_letter_invert(rr_initial_position, md_output_pos_invert)
                
            rr_output_pos_invert = rotor_output_position_invert(rr_initial_position, rr_input_let_invert)
                
            final_let = final_letter(keyboard, rr_output_pos_invert)
                
            final_message.append(final_let)
                                              
            i += 1
        # The list containing the processed message is transformed into a string and then the latter is added to the list containing all messages.   
        str_message = "".join(final_message)           
        new_messages.append(str_message)
            
                            
           
        
        
            
        
    # This condition verifies what task you want to perform with the message. In this case it is not very relevant since the process is the same.  
    
    # The code that comes after it is the same as the one in the previous block but it is left the same in case you want to make any modifications in the encryption logic in the future.
    
    if archive_list[a][2] == 'Encriptar':
            
        key = archive_list[a][0]
        message = archive_list[a][1]  
        mes_list = list(message)
            
        rotor_ini_pos = rotors_initial_pos(left_rotor, middle_rotor, right_rotor, key)
        
        lf_initial_position = spin_rotor(left_rotor_copy, rotor_ini_pos[0])
            
        md_initial_position = spin_rotor(middle_rotor_copy, rotor_ini_pos[1])
            
        rr_initial_position = spin_rotor(right_rotor_copy, rotor_ini_pos[2])
            
            
        print_rotors(lf_initial_position, md_initial_position, rr_initial_position)
            
       
            
        final_message = []               
        i = 0
        while i < len(mes_list):
            
            
            letter = mes_list[i]
            try:
                kb_let_pos = keyboard_letter_position(keyboard, letter)
                
            except ValueError:
                    
                lf_initial_position = spin_rotor(left_rotor_copy, rotor_ini_pos[0])
            
                md_initial_position = spin_rotor(middle_rotor_copy, rotor_ini_pos[1])
            
                rr_initial_position = spin_rotor(right_rotor_copy, rotor_ini_pos[2])
                    
                final_message.append(' ')
                    
                i += 1
                continue
                   
            if rr_initial_position[0][0] == 'V':
                md_initial_position = spin_rotor(md_initial_position, 1)
                        
            if md_initial_position[0][0] == 'Q':
                lf_initial_position = spin_rotor(lf_initial_position, 1)
                        
            rr_initial_position = spin_rotor(rr_initial_position, 1)
            print_rotors(lf_initial_position, md_initial_position, rr_initial_position)
                
            rr_input_let = rotor_input_letter(rr_initial_position, kb_let_pos)
                
            rr_output_pos = rotor_output_position(rr_initial_position, rr_input_let)
                    
            md_input_let = rotor_input_letter(md_initial_position, rr_output_pos)
                    
            md_output_pos = rotor_output_position(md_initial_position, md_input_let)
                    
            lf_input_let = rotor_input_letter(lf_initial_position, md_output_pos)
                    
            lf_output_pos = rotor_output_position(lf_initial_position, lf_input_let)
                    
            rf_output_pos = reflector_output_position(reflector, lf_output_pos)
                    
            lf_input_let_invert = rotor_input_letter_invert(lf_initial_position, rf_output_pos)
                    
            lf_output_pos_invert = rotor_output_position_invert(lf_initial_position, lf_input_let_invert)
                    
            md_input_let_invert = rotor_input_letter_invert(md_initial_position, lf_output_pos_invert)
                    
            md_output_pos_invert = rotor_output_position_invert(md_initial_position, md_input_let_invert)
                    
            rr_input_let_invert = rotor_input_letter_invert(rr_initial_position, md_output_pos_invert)
                    
            rr_output_pos_invert = rotor_output_position_invert(rr_initial_position, rr_input_let_invert)
                    
            final_let = final_letter(keyboard, rr_output_pos_invert)
                    
            final_message.append(final_let)
            
                        
            i += 1
                                
        str_message = "".join(final_message)            
        new_messages.append(str_message)       
            
    a += 1
            

## PART 5 'ADD THE NEW MESSAGES TO THE ARCHIVE'

            
new_column = 'mensaje procesado'  

# To add the messages to the file, the function defined at the beginning is used.
add_new_messages(route, archive, new_messages, new_column)


# Finally, a message is printed on the screen to notify that the process has finished.
print('Se ha actualizado el archivo con los mensajes procesados')


##################################################### BONUS ########################################################################3

# KEY = XFA
# MESSAGE = 'BT BTZTDLV HC KSAES ADZ ZIMT MDXME'


    
    
    
    
    
    


    

    
    
        
        




