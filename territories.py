import random

territories = {
    # Oceania
    'Alaska': [112, 160],
    'Eastern Australia': [1461, 864],
    'Western Australia': [1324, 854],
    'New Guinea': [1444, 725],
    'Indonesia': [1313, 673],
    # Asia
    'Siam': [1228, 554],
    'India': [1110, 557],
    'China': [1266, 450],
    'Middle East': [944, 544],
    'Afghanistan': [1029, 401],
    'Mongolia': [1263, 350],
    'Irkutsk': [1240, 256],
    'Ural': [1046, 230],
    'Siberia': [1129, 228],
    'Yakutsk': [1268, 166],
    'Kamchatka': [1404, 179],
    'Japan': [1404, 386],
    # Europe
    'Ukraine': [905, 261],
    'Scandinavia': [776, 221],
    'Northern Europe': [766, 315],
    'Southern Europe': [800, 381],
    'Western Europe': [715, 385],
    'Great Britain': [697, 305],
    'Iceland': [660, 221],
    # North America
    'Alaska': [112,162],
    'Northwest Territory': [261,167],
    'Alberta': [258,250],
    'Ontario': [352,261],
    'Greenland': [603,94],
    'Quebec': [495,266],
    'Western United States': [271,330],
    'Eastern United States': [390,377],
    'Central America': [270,448],
    # South America
    'Venezuela': [389,548],
    'Brazil': [490,643],
    'Peru': [377,686],
    'Argentina': [424,790],
    # Africa
    'North Africa': [708,554],
    'Egypt':[828,506],
    'East Africa': [880,625],
    'Congo': [825,683],
    'South Africa': [834,824],
    'Madagascar':[950,826],
    }

imgnaturalWidth = 1536
imgnaturalHeight = 999

for ter in territories:
    pointWidth = territories[ter][0]
    pointWScaler = pointWidth / imgnaturalWidth
    territories[ter][0] = pointWScaler

    pointHeight = territories[ter][1]
    pointHScaler = pointHeight / imgnaturalHeight
    territories[ter][1] = pointHScaler

ters = list(territories.items())

def teralloc(ters):
    playerno = 2
    troopno = int(len(ters) / playerno)

    p1ters = random.sample(ters, troopno)
    p2ters = []

    for ter in ters:
        if ter not in p1ters:
            p2ters.append(ter)



    return p1ters, p2ters

p1ters, p2ters = teralloc(ters)


