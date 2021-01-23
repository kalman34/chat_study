from __future__ import division
import csv
import re

## Builds concreteness dictionary
conc_dict = {} #difference between this and dict()?
with open("concreteness.csv", "r") as conc_file:  # change name of file and put in here #what is "r"
    reader = csv.reader(conc_file)
    next(reader)  # .next skips header
    for row in reader:
        conc_dict[row[0]] = float(row[2])

with open("chat_text_2021.01.19.csv", "r") as raw_file:
    with open("scores_chat_2021.01.22.csv", "w") as g:
        reader = csv.reader(raw_file, quotechar='"')
        writer = csv.writer(g, lineterminator = '\n')
        writer.writerow(["id", "chat_sum", "chat_avg", "chat_word_count"])
        reader.__next__()
        for row in reader:
            dyad_ = row[0]
            print(dyad_)
            id_ = row[1]
            print(id_)
            chat = row[2].split()
            to_write = [id_]

            # If a value is missing in a cell, skip this row
            if chat == []:
                writer.writerow(["chat is empty"])
                continue

            chat_sum = 0
            chat_word_count = 0
            for i in range(0, len(chat) - 1): #
                word1 = re.sub("[\.,-/\\?!;: ]", "", chat[i]).lower()
                word2 = re.sub("[\.,-/\\?!;: ]", "", chat[i + 1]).lower()
                phrase = word1 + " " + word2

                if phrase in conc_dict: #do we need to deal with spaces in concretness file?
                    chat_sum += conc_dict[phrase]
                    chat_word_count += 1 #word_count as in matches
                else:
                    if i == 0 and word1 in conc_dict:
                        chat_sum += conc_dict[word1]
                        chat_word_count += 1
                    if word2 in conc_dict:
                        chat_sum += conc_dict[word2]
                        chat_word_count += 1

            to_write.append(str(chat_sum))
            if chat_word_count != 0:
                to_write.append(str(chat_sum/float(chat_word_count)))
            else:
                to_write.append('0')


        
            to_write.append(str(chat_word_count))
            writer.writerow(to_write)
