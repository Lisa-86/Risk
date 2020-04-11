import random

# territories { 'territory': {'location': [x, y], 'neighbours': [a, b, c], 'playerno': playerNo, 'troopno': troopNo}}

territories = {
    # Oceania
    'Eastern Australia': {'loc' : [1461, 864], 'neighbours': ['Western Australia', 'New Guinea']},
    'Western Australia': {'loc' : [1324, 854], 'neighbours': ['Eastern Australia', 'New Guinea', 'Indonesia']},
    'New Guinea': {'loc' : [1444, 725], 'neighbours': ['Eastern Australia', 'Western Australia', 'Indonesia']},
    'Indonesia': {'loc' : [1313, 673], 'neighbours': ['Western Australia', 'New Guinea', 'Siam']},
    # Asia
    'Siam': {'loc' : [1228, 554], 'neighbours': ['Indonesia', 'India', 'China']},
    'India': {'loc' : [1110, 557], 'neighbours': ['Siam', 'China', 'Afghanistan', 'Middle East']},
    'China': {'loc' : [1266, 450], 'neighbours': ['Siam', 'India','Afghanistan', 'Ural', 'Siberia', 'Mongolia']},
    'Middle East': {'loc' : [944, 544], 'neighbours': ['India', 'Afghanistan', 'Ukraine', 'Southern Europe', 'Egypt']},
    'Afghanistan': {'loc' : [1029, 401], 'neighbours': ['Ukraine', 'Middle East', 'India', 'China', 'Ural']},
    'Mongolia': {'loc' : [1263, 350], 'neighbours': ['China', 'Siberia', 'Irkutsk', 'Kamchatka', 'Japan']},
    'Irkutsk': {'loc' : [1240, 256], 'neighbours': ['Mongolia', 'Siberia', 'Yakutsk', 'Kamchatka']},
    'Ural': {'loc' : [1046, 230], 'neighbours': ['Siberia', 'China', 'Afghanistan', 'Ukraine']},
    'Siberia': {'loc' : [1129, 228], 'neighbours': ['Yakutsk', 'Irkutsk', 'Mongolia', 'China', 'Ural']},
    'Yakutsk': {'loc' : [1268, 166], 'neighbours': ['Kamchatka', 'Irkutsk', 'Siberia']},
    'Kamchatka': {'loc' : [1404, 179], 'neighbours': ['Yakutsk', 'Irkutsk', 'Mongolia', 'Japan', 'Alaska']},
    'Japan': {'loc' : [1404, 386], 'neighbours': ['Mongolia', 'Kamchatka']},
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

# replacing absolute location with relative to the natural image size (normalised to 0-1 range)
for ter in territories:
    pointWidth = territories[ter]['loc'][0]
    pointWScaler = pointWidth / imgnaturalWidth
    territories[ter]['loc'][0] = pointWScaler

    pointHeight = territories[ter]['loc'][1]
    pointHScaler = pointHeight / imgnaturalHeight
    territories[ter]['loc'][1] = pointHScaler

print(territories)



def teralloc(territories, troopNo=3):
    playerno = 2
    ter_no = int(len(territories) / playerno)

    # just the territories
    ters = list(territories)

    p1ters = random.sample(ters, ter_no)

    for ter in ters:
        territories[ter]['troopNo'] = troopNo
        if ter in p1ters:
            territories[ter]['playerNo'] = 1
        else:
            territories[ter]['playerNo'] = 2

    return territories

# p1ters, p2ters = teralloc(ters)
#
# for ter in territories:
#     if ter in p1ters:
#         territories[ter]
