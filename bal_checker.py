import easyocr, argparse
import cv2
import re
import csv
from enum import IntEnum
import file_utils
import numpy
import time

class Position(IntEnum):
  GK=1
  CB=2
  LRB=3
  DMF=4
  CMF=5
  AMF=6
  LRMF=7
  LRWF=8
  SS=9
  CF=10
  
class Stats(IntEnum):
  Offensive_Awareness=1
  Ballcontrol=2
  Dribbling=3
  Tight_Possession=4
  Low_Pass=5
  Lofted_Pass=6
  Finishing=7
  Heading=8
  Set_Piece_Taking=9
  Curl=10
  Speed=11
  Accleration=12
  Kicking_Power=13
  Jump=14
  Physical_Contact=15
  Balance=16
  Stamina=17
  Defensive_Awareness=18
  Ball_winning=19
  Aggression=20
  GK_Awareness=21
  GK_Catching=22
  GK_Clearing=23
  GK_Reflexes=24
  GK_Reach=25

with open("tables/min_rules.csv") as f:
  minimums = list(csv.reader(f))
with open("tables/max_rules.csv") as f:
  maximums = list(csv.reader(f))


def check_stats(response_string, stats_list, player_position, max_speed, max_phys, max_jump="95", max_reflex="95", max_reach="90"):

  illegal_flag = False

  for index, stat_value in enumerate(stats_list):

    current_stat = Stats(index+1).name

    if current_stat == "Speed":
      speed = stat_value
      if speed > max_speed: 
        print(current_stat," is higher than maximum for your height")
        response_string.append(current_stat+" is higher than maximum for your height<br>")
        illegal_flag = True
    
    elif current_stat == "Physical_Contact":
      phys = stat_value
      if phys > max_phys: 
        print(current_stat," is higher than maximum for your height")
        response_string.append(current_stat+" is higher than maximum for your height<br>")
        illegal_flag = True

    elif current_stat == "Jump":
      jump = stat_value
      if jump > max_jump:
        print(current_stat," is higher than maximum for your height")
        response_string.append(current_stat+" is higher than maximum for your height<br>")
        illegal_flag = True

    elif current_stat == "GK_Reflexes":
      reflexes = stat_value
      if reflexes > max_reflex:
        print(current_stat," is higher than maximum for your height")
        response_string.append(current_stat+" is higher than maximum for your height<br>")
        illegal_flag = True

    elif current_stat == "GK_Reach":
      reach = stat_value
      if reach > max_reach:
        print(current_stat," is higher than maximum for your height")
        response_string.append(current_stat+" is higher than maximum for your height<br>")
        illegal_flag = True
        
    if stat_value < minimums[index+1][player_position]:
      print(current_stat," lower than minimum")
      response_string.append(current_stat+" lower than minimum<br>")
      illegal_flag = True

    elif stat_value > maximums[index+1][player_position]:
      print(current_stat," higher than maximum")
      response_string.append(current_stat+" higher than maximum<br>")
      illegal_flag = True
    print(current_stat, stat_value)
    response_string.append(current_stat+" "+stat_value+"<br>")


  if int(speed) + int(phys) > 154: 
    print("Your BAL is illegal, Speed + Phys is bigger than 154!")
    response_string.append("Your BAL is illegal, Speed + Phys is bigger than 154!<br>")
    illegal_flag = True

  if not illegal_flag:
    print("Your BAL is legal, have fun!")
    response_string.append("Your BAL is legal, have fun!")
  
  else: 
    print("Your BAL is illegal, unlucky!") 
    response_string.append("Your BAL is illegal, unlucky!") 


def bal_checker(image_list, selected_position):

  reader = easyocr.Reader(['en'], gpu=False) # need to run only once to load model into memory

  start_time = time.time()

  first_page_pattern = re.compile("([2]{1,2}[/|\\|][4-5])") # regex pattern for overall/stats and page number
  second_page_pattern = re.compile("([3]{1,2}[/|\\|][4-5])") # regex pattern for overall/stats and page number
  stat_pattern = re.compile("^([4-9][0-9])$") # regex pattern for overall/stats and page number
  height_pattern = re.compile("^[1-2][0-9][0-9]")

  with open("tables/"+selected_position+".csv") as f:
    height_limits = list(csv.reader(f))
    heights = [row[0] for row in height_limits]

  player_position = Position[selected_position]

  is_first_page = True

  first_page_stats = []
  second_page_stats = []

  # image_list = file_utils.get_files(args.in_folder)

  response_string = []

  for k, image_path in enumerate(image_list):

    image = cv2.imread(image_path)
    # will pass the grayscale image for better detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # margin for better number detection, threshold lowered to pass some color/number combinations
    res = reader.readtext(gray_image, text_threshold=0.4, add_margin=0.15)  

    for (bbox, text, prob) in res: 

      if first_page_pattern.search(text):
        is_first_page=True

      elif second_page_pattern.search(text):
        is_first_page=False
    
      elif height_pattern.search(text):
        height = ''.join(filter(str.isdigit, text))
        height_index = heights.index(height)
        max_speed = height_limits[height_index][1]
        max_phys = height_limits[height_index][2]
        if selected_position == "GK":
          max_jump = height_limits[height_index][3]
          max_reflex = height_limits[height_index][4]
          max_reach = height_limits[height_index][5]

        print("Height:", height, "Max Speed:", max_speed, "Max Phys:", max_phys)
        response_string.append("Height: "+height+ " Max Speed: "+ max_speed+ " Max Phys: "+ max_phys+"<br>")

      elif stat_pattern.search(text):

        if is_first_page:
          first_page_stats.append(text)
        else:
          second_page_stats.append(text)      
      #unpack the bounding box
      # (tl, tr, br, bl) = bbox
      # tl = (int(tl[0]), int(tl[1]))
      # tr = (int(tr[0]), int(tr[1]))
      # br = (int(br[0]), int(br[1]))
      # bl = (int(bl[0]), int(bl[1]))
      # cv2.rectangle(image, tl, br, (0, 255, 0), 2)
      # cv2.putText(image, text, (tl[0], tl[1] - 10),
      # cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    #image = cv2.resize(image, (1920, 1080))
    # cv2.imshow("Title", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

  # if len(first_page_stats) > 17: 
  #   overall = first_page_stats.pop(3)
  #   print("Overall:", overall)
  #   response_string.append("Overall: "+overall+"<br>")
  #   second_page_stats.pop(3)


  all_stats = first_page_stats + second_page_stats

  if selected_position=="GK":
    check_stats(response_string, all_stats, player_position, max_speed, max_phys, max_jump, max_reflex, max_reach)
  else:
    check_stats(response_string, all_stats, player_position, max_speed, max_phys)

  print("--- %s seconds ---" % (time.time() - start_time))

  return ''.join(response_string)


