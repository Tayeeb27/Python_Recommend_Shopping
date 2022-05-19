# Name: Tayeeb Islam
# Student Number: c2003538
# Module: CM1208
import numpy as np
import math

def calc_angle(a, b):
    A = np.array(a)
    B = np.array(b)
    norm_x = np.linalg.norm(A)
    norm_y = np.linalg.norm(B)
    cos_theta = (np.dot(A, B) / (norm_x * norm_y))
    # if statement used to avoid domain math error
    if 1.00001 > cos_theta > 1:
        cos_theta = 1
    theta = math.degrees(math.acos(cos_theta))
    return round(theta, 2)


hfile = ((open("history.txt", "r")).readlines())

firstLine = hfile[0].split()
Number_of_Customers = int(firstLine[0])
Number_of_Items = int(firstLine[1])
Number_of_Transactions = int(firstLine[2])
positive_entries = 0
history = {}

for i in range(Number_of_Items+1):
    # Creates a empty list for the the items a customer bought
    Customer_Purchase_List = [0] * Number_of_Items
    history[i] = Customer_Purchase_List


for i in range(Number_of_Transactions + 1):
    Customer_ID = int((hfile[i].split())[0])
    Item_ID = int((hfile[i].split())[1])
    # Gives the value 1 to which item was bought by the specific customer
    history[Item_ID][Customer_ID - 1] = 1

# creates the purchase history table in list format
Purchase_History_List = [history[i] for i in history]
# Counts the Positive Entries i.e all the ones
pos_entries = (np.count_nonzero(Purchase_History_List))
# Dictionary for Item with corresponding angles
Item_Angle_Dict = {}
for i in range(Number_of_Items + 1):
    # Creates an empty dictionary for each Customer and what they bought
    Customer_Purchase_Dict = [0] * Number_of_Customers
    Item_Angle_Dict[i] = Customer_Purchase_Dict

# List of angles with value and not repeating itself i.e (1 and 2) and (2 and 1)
List_Of_Angles = []
for x in range(1, Number_of_Items + 1):
    for y in range(1, Number_of_Items + 1):
        angle_calc = calc_angle(history[x], history[y])
        Item_Angle_Dict[x][y - 1] = angle_calc
        if x < y:
            List_Of_Angles.append(angle_calc)

print("Positive entries:", pos_entries)
print("Average angle:", round(sum(List_Of_Angles) / len(List_Of_Angles)))

qfile = ((open("queries.txt", "r")).readlines())
for i in range(len(qfile)):
    List_Of_Recommended_Items = []
    Item_Angles_Dict = {}
    angleList = []
    cart = qfile[i].split()
    print("Shopping cart:", *cart)
    for Item_ID in cart:
        # The specific Item's Angles
        Item_Angles_Dict[Item_ID] = (Item_Angle_Dict[int(Item_ID)])[:]
        for ids in cart:
            # Making the Other Items in the cart 0
            Item_Angles_Dict[Item_ID][int(ids) - 1] = 0
        Angle_Array = np.array(Item_Angles_Dict[Item_ID])
        # Finding the Minimum Angle excluding 0
        Min_Angle = np.min(Angle_Array[np.nonzero(Angle_Array)])
        # A list used to then find the Recommended Item
        angleList.append([Min_Angle, Item_ID])
        match_angles = Item_Angles_Dict[Item_ID][:]
        # Used to get the matching item number
        Match_ID = str(match_angles.index(Min_Angle) + 1)
        if Min_Angle < 90:
            print("Item:", Item_ID + "; match:", Match_ID + "; angle:", Min_Angle)
        else:
            print("Item:", Item_ID, "no match")
    # sort the list to have the smaller angle first
    angleList.sort()

    for angle in angleList:
        if angle[0] < 90:
            # Adds to the list for recommended items
            List_Of_Recommended_Items.append(Item_Angles_Dict[angle[1]].index(angle[0]) + 1)
    List_Of_Recommended_Items = list(dict.fromkeys(List_Of_Recommended_Items))
    print("Recommend:", *List_Of_Recommended_Items)
