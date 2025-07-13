from time import time

print("Press Enter to start typing or to break a new line")
print("Press Enter twice to finish typing")
input("-----------------------------------------------")

#record timestamp when user starts typing
start = time()

text = [] 
while True:
    line = input()
    if not line:
        break
    text.append(line)

#record timestamp when user finishes typing
end = time()

print("The text user typed in:")
for line in text:
    print(line)

#calculate and pint timing and speed
total_time = end - start
print(f"\nTotal time taken:{total_time:.2f} second")

total_words = sum(len(line.split()) for line in text)
print(f"Total words typed:{total_words}")

if total_time > 0:
    wpm = (total_words / total_time)*60
    print(f"typing speed:{wpm:.2f} words per minute")
else:
    print("typing speed:0 words per minute (too fast or invalid timing)")



