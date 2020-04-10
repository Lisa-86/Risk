import random

# territories { 'territory': {'location': [x, y], 'playerno': playerNo, 'troopno': troopNo}}

territories = {
    # Oceania
    'Alaska': {'loc' : [112, 160]},
    'Eastern Australia': {'loc' : [1461, 864]},
    'Western Australia': {'loc' : [1324, 854]},
    'New Guinea': {'loc' : [1444, 725]},
    'Indonesia': {'loc' : [1313, 673]},
    # Asia
    'Siam': {'loc' : [1228, 554]},
    'India': {'loc' : [1110, 557]},
    'China': {'loc' : [1266, 450]},
    'Middle East': {'loc' : [944, 544]},
    'Afghanistan': {'loc' : [1029, 401]},
    'Mongolia': {'loc' : [1263, 350]},
    'Irkutsk': {'loc' : [1240, 256]},
    'Ural': {'loc' : [1046, 230]},
    'Siberia': {'loc' : [1129, 228]},
    'Yakutsk': {'loc' : [1268, 166]},
    'Kamchatka': {'loc' : [1404, 179]},
    'Japan': {'loc' : [1404, 386]},
    # Europe
    'Ukraine': {'loc' : [905, 261]},
    'Scandinavia': {'loc' : [776, 221]},
    'Northern Europe': {'loc' : [766, 315]},
    'Southern Europe': {'loc' : [800, 381]},
    'Western Europe': {'loc' : [715, 385]},
    'Great Britain': {'loc' : [697, 305]},
    'Iceland': {'loc' : [660, 221]},
    # North America
    'Alaska': {'loc' : [112,162]},
    'Northwest Territory': {'loc' : [261,167]},
    'Alberta': {'loc' : [258,250]},
    'Ontario': {'loc' : [352,261]},
    'Greenland': {'loc' : [603,94]},
    'Quebec': {'loc' : [495,266]},
    'Western United States': {'loc' : [271,330]},
    'Eastern United States': {'loc' : [390,377]},
    'Central America': {'loc' : [270,448]},
    # South America
    'Venezuela': {'loc' : [389,548]},
    'Brazil': {'loc' : [490,643]},
    'Peru': {'loc' : [377,686]},
    'Argentina': {'loc' : [424,790]},
    # Africa
    'North Africa': {'loc' : [708,554]},
    'Egypt':{'loc' : [828,506]},
    'East Africa': {'loc' : [880,625]},
    'Congo': {'loc' : [825,683]},
    'South Africa': {'loc' : [834,824]},
    'Madagascar':{'loc' : [950,826]},
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

print(territories)

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

for ter in territories:
    if ter in p1ters:
        territories[ter]
