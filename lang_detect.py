from langdetect import detect

with open("trends.txt", "r", encoding='UTF-8') as f:
    lines = f.readlines()

english_lines = [line.strip() for line in lines if detect(line) == 'en']

with open("required_trends.txt", "w", encoding='UTF-8') as f:
    f.writelines('\n'.join(english_lines))




