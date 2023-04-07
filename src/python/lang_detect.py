from langdetect import detect

with open("../../go/files/trends.txt", "r", encoding='UTF-8') as f:
    lines = f.readlines()

english_lines = [line.strip() for line in lines if detect(line) == 'en']

with open("../../go/files/required_trends.txt", "w", encoding='UTF-8') as f:
    f.writelines('\n'.join(english_lines))