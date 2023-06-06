from graphics import Canvas
import random

PLAYER_NAME                     = 'Guybrush Threepwood'
ENEMY_NAME                      = 'Sword Master'

FILE_INSULTS                    = 'monkey_island_pirate_insults.txt'
FILE_COMEBACKS                  = 'monkey_island_pirate_comebacks.txt'

FILE_IMAGE_1                    = 'monkey_island_1.png'
FILE_IMAGE_2                    = 'monkey_island_2.png'

FILE_IMAGE_LIKE                 = 'like.png'
FILE_IMAGE_DISLIKE              = 'dislike.png'

NUM_MAX_HITS                    = 3
NUM_MAX_ROUNDS                  = 10
NUM_COMEBACKS                   = 10

CANVAS_WIDTH                    = 575
CANVAS_HEIGHT                   = 350

def get_lines_from_file(file, multiple_possibilities):
    f = open(file)
    
    lines = []
    for line in f:
        # removes whitespace characters (\n) from the start and end of the line
        line = line.strip()
        
        # if the line was only whitespace characters, skip it 
        if line != "":
            if (multiple_possibilities):
                lines.append(line.split(";"))
            else:
                lines.append(line)
                
    return lines

def insult(insults):
    insult_index = random.randint(0, (len(insults) - 1))
    
    insult_selected = [ insult_index, insults[insult_index] ]
    
    return insult_selected
    
def comeback(insult_selected, comebacks):
    # Select a random position on the correct comeback answer
    max_comebacks = NUM_COMEBACKS
    
    if (max_comebacks > len(comebacks)):
        max_comebacks = len(comebacks)
    
    comeback_correct_position = random.randint(1, max_comebacks)
    insult_index = insult_selected[0]
    
    comeback_correct = [ insult_index, comebacks[insult_index] ]

    comeback_subindex_print = 0
    comebacks_sublist = [ comeback_correct ]

    for i in range(1, (max_comebacks + 1)):
        if (i == comeback_correct_position):
            comeback_current = comeback_correct
        else:
            # Discard all the answers that may be correct, due to the fact 
            # that it has been processed previously and the possible repeated answers.
            comeback_incorrect = True
            
            while (comeback_incorrect):
                comeback_index = random.randint(0, (len(comebacks) - 1))
                
                comeback_subindex = random.randint(0, (len(comebacks[comeback_index]) - 1))
                
                comeback_find = False
                for comeback_sublist in comebacks_sublist:
                    if (comebacks[comeback_index][comeback_subindex] in comeback_sublist[1]):
                        comeback_find = True
                        break
                
                if (not comeback_find):
                    comeback_incorrect = False
                    
            comeback_current = [ comeback_index, [ comebacks[comeback_index][comeback_subindex] ] ] 
            
        comebacks_sublist.append(comeback_current)

        comeback_subindex = random.randint(0, (len(comeback_current[1]) - 1))
        
        if (i == comeback_correct_position):
            comeback_subindex_print = comeback_subindex
            
        print(str(i) + ") " + comeback_current[1][comeback_subindex])
    
    choose_comeback_index = 0
    while (not (1 <= int(choose_comeback_index) <= max_comebacks)):    
        choose_comeback_index = input("\r\n>>> " + PLAYER_NAME + ", choose the correct answer: ");
        
        if (not (choose_comeback_index.isdigit())):
            choose_comeback_index = 0

    #Remove the first element, it has helped us to search for repetitions, 
    #but the correct answer is duplicated in the correct position.
    comebacks_sublist.pop(0)
    comeback_selected = comebacks_sublist[(int(choose_comeback_index) - 1)]
    
    print("\r")
    
    #Remove correct answer multiple possibilities, and get only the print answer
    if (insult_index == (int(choose_comeback_index) - 1)):
        comeback_selected = [ comeback_selected[0], [ comeback_selected[1][comeback_subindex_print] ] ]
    
    return comeback_selected

def print_round(canvas, round, hits, only_canvas = False):
    game_status_canvas = canvas.create_text(10, 10, font='courier', text="ROUND: " + str(round) + " of " + str(NUM_MAX_ROUNDS) + " / CORRECT ANSWERS: " + str(hits) + " of " + str(NUM_MAX_HITS), color='darkgreen')
    
    if (not only_canvas):
        print("################################################################################\r\n")
        print("                       ROUND: " + str(round) + " of " + str(NUM_MAX_ROUNDS) + " / CORRECT ANSWERS: " + str(hits) + " of " + str(NUM_MAX_HITS) + "\r\n")
        print("################################################################################\r\n")
        
    return game_status_canvas
    
def get_and_print_game_init_elements(canvas, image_canvas, round, hits):
    canvas.delete(image_canvas)
    image_canvas = canvas.create_image(0, 90, FILE_IMAGE_1)
    
    game_status_canvas = print_round(canvas, round, hits)
    
    return [ game_status_canvas, image_canvas ]
    
def get_and_print_insult(canvas, insult_selected):
    insult_canvas = canvas.create_text(10, 40, font='courier', text=ENEMY_NAME + ": " + insult_selected[1], color='purple')
    
    print("--------------------------------------------------------------------------------\r\n")
    print(ENEMY_NAME + ": " + insult_selected[1] + "\r\n")
    print("--------------------------------------------------------------------------------\r\n")
    
    return insult_canvas
    
def get_and_print_comeback(canvas, comeback_selected):
    comeback_canvas = canvas.create_text(10, 60, font='courier', text=PLAYER_NAME + ": " + comeback_selected[1][0], color='blue')
    
    print(PLAYER_NAME + ": " + comeback_selected[1][0] + "\r\n")
    
    return comeback_canvas
    
def get_and_print_result(canvas, image_canvas, insult_selected, comeback_selected, hits):
    time.sleep(1)
    
    if (insult_selected[0] == comeback_selected[0]):
        image_canvas_tmp = canvas.create_image(0, 90, FILE_IMAGE_2)
        
        time.sleep(0.5)
        
        canvas.delete(image_canvas)
        
        image_canvas = image_canvas_tmp
        
        image_like_dislike = canvas.create_image(160, (CANVAS_HEIGHT / 2), FILE_IMAGE_LIKE)
        
        print("[ Correct answer! You're a great pirate! ]\r\n")
    else:
        image_like_dislike = canvas.create_image(160, (CANVAS_HEIGHT / 2), FILE_IMAGE_DISLIKE)
        
        print("[ Wrong answer! You should practice a little more ]\r\n")
    
    time.sleep(2)

    return [ (insult_selected[0] == comeback_selected[0]), image_canvas, image_like_dislike ]

def delete_canvas_objects(canvas, canvas_objects_delete):
    for canvas_object_delete in canvas_objects_delete:
        canvas.delete(canvas_object_delete)
            
def print_end_game(canvas, round, hits):
    print_round(canvas, (round - 1), hits, True)
    
    if (hits >= NUM_MAX_HITS):
        print("################################################################################\r\n")
        print("                           CONGRATULATIONS!, You Win!\r\n")
        print("You're a formidable pirate, ready to face any challenge that comes your way.")
        print("With your unwavering determination and skills honed through countless battles,")
        print("you're a true force to be reckoned with on the open waters.")
        print("Together, we make a fearsome team, ready to conquer the seven seas!\r\n")
        print("################################################################################\r")
    else:
        print("################################################################################\r\n")
        print("                                OMG!, You Lose!\r\n")
        print("You're still honing your skills as a pirate, yet to fully embrace the life of")
        print("adventure and battle on the high seas. With more experience and training, you'll")
        print("become a formidable force ready to face any challenge that comes your way.")
        print("Take heart, for your journey towards becoming a pirate has only just begun!\r\n")
        print("################################################################################\r")
        
def main():
    round     = 1
    hits      = 0
    insults   = get_lines_from_file(FILE_INSULTS, False)
    comebacks = get_lines_from_file(FILE_COMEBACKS, True)
    canvas    = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, color='#F5F5F5')
    image_canvas = canvas.create_image(0, 90, FILE_IMAGE_1)
    
    if ((len(insults) > 0) and (len(comebacks) > 0) and (len(insults) == len(comebacks))):
        while ((round <= NUM_MAX_ROUNDS) and (hits < NUM_MAX_HITS)):
            # Print round
            [ game_status_canvas, image_canvas ] = get_and_print_game_init_elements(canvas, image_canvas, round, hits)
            
            # Select an insult
            insult_selected = insult(insults)
            insult_canvas   = get_and_print_insult(canvas, insult_selected)
            
            # Select a comeback
            comeback_selected = comeback(insult_selected, comebacks)
            comeback_canvas   = get_and_print_comeback(canvas, comeback_selected)
            
            # Print result
            [ num_hits, image_canvas, image_like_dislike ] = get_and_print_result(canvas, image_canvas, insult_selected, comeback_selected, hits)
            
            hits += num_hits
            
            round += 1
            
            # Delete all canvas elements
            if ((round <= NUM_MAX_ROUNDS) and (hits < NUM_MAX_HITS)):
                delete_canvas_objects(canvas, [ game_status_canvas, image_canvas, insult_canvas, comeback_canvas, image_like_dislike ])
            else:
                delete_canvas_objects(canvas, [ game_status_canvas ])
                
        # Print end game    
        print_end_game(canvas, round, hits)
        
    else:
        if (len(insults) != len(comebacks)):
            print("Wrong files.")
        else:
            print("Files cannot be empty.")

if __name__ == '__main__':
    main()