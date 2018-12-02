from bashplotlib.histogram import plot_hist
import matplotlib.pyplot as plt

with open('guardian.freq', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(lines)
    freq = []
    words = []
    for line in lines:
        line = line.replace('\n', '')
        print(line)
        wf = line.split()
        if len(wf) == 2:
            freq.append(int(line.split()[0]))
            words.append(line.split()[1])

    print(freq)
    print(words)

    plt.bar(words[:50], freq[:50])
    plt.xticks(words[:50], rotation='vertical')
    plt.show()



