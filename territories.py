import random

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
    'Ukraine': {'loc' : [905, 261], 'neighbours': ['Scandinavia', 'Northern Europe', 'Southern Europe', 'Middle East', 'Afghanistan', 'Ural']},
    'Scandinavia': {'loc' : [776, 221], 'neighbours': ['Ukraine', 'Northern Europe', 'Great Britain', 'Iceland']},
    'Northern Europe': {'loc' : [766, 315], 'neighbours': ['Southern Europe', 'Western Europe', 'Great Britain', 'Scandinavia', 'Ukraine']},
    'Southern Europe': {'loc' : [800, 381], 'neighbours': ['North Africa', 'Egypt', 'Middle East', 'Ukraine', 'Northern Europe', 'Western Europe']},
    'Western Europe': {'loc' : [715, 385], 'neighbours': ['North Africa', 'Great Britain', 'Northern Europe', 'Southern Europe']},
    'Great Britain': {'loc' : [697, 305], 'neighbours': ['Iceland', 'Scandinavia', 'Northern Europe', 'Western Europe']},
    'Iceland': {'loc' : [660, 221], 'neighbours': ['Greenland', 'Scandinavia', 'Great Britain']},
    # North America
    'Alaska': {'loc' : [112,162], 'neighbours': ['Northwest Territory', 'Alberta', 'Kamchatka']},
    'Northwest Territory': {'loc' : [261,167], 'neighbours': ['Greenland', 'Ontario', 'Alberta', 'Alaska']},
    'Alberta': {'loc' : [258,250], 'neighbours': ['Western United States', 'Ontario', 'Northwest Territory', 'Alaska']},
    'Ontario': {'loc' : [352,261], 'neighbours': ['Quebec', 'Eastern United States', 'Western United States', 'Alberta', 'Northwest Territory', 'Greenland']},
    'Greenland': {'loc' : [603,94], 'neighbours': ['Quebec', 'Iceland', 'Ontario', 'Northwest Territory']},
    'Quebec': {'loc' : [495,266], 'neighbours': ['Greenland', 'Eastern United States', 'Ontario']},
    'Western United States': {'loc' : [271,330], 'neighbours': ['Central America', 'Eastern United States', 'Ontario', 'Alberta']},
    'Eastern United States': {'loc' : [390,377], 'neighbours': ['Western United States', 'Central America', 'Ontario', 'Quebec']},
    'Central America': {'loc' : [270,448], 'neighbours': ['Venezuela', 'Eastern United States', 'Western United States']},
    # South America
    'Venezuela': {'loc' : [389,548], 'neighbours': ['Brazil', 'Peru', 'Central America']},
    'Brazil': {'loc' : [490,643], 'neighbours': ['Argentina', 'Peru', 'Venezuela', 'North Africa']},
    'Peru': {'loc' : [377,686], 'neighbours': ['Argentina', 'Brazil', 'Venezuela']},
    'Argentina': {'loc' : [424,790], 'neighbours': ['Brazil', 'Peru']},
    # Africa
    'North Africa': {'loc' : [708,554], 'neighbours': ['Congo', 'East Africa', 'Egypt', 'Brazil', 'Southern Europe', 'Western Europe']},
    'Egypt':{'loc' : [828,506], 'neighbours': ['East Africa', 'North Africa', 'Southern Europe', 'Middle East']},
    'East Africa': {'loc' : [880,625], 'neighbours': ['Madagascar', 'South Africa', 'Congo', 'North Africa', 'Egypt']},
    'Congo': {'loc' : [825,683], 'neighbours': ['South Africa', 'East Africa', 'North Africa']},
    'South Africa': {'loc' : [834,824], 'neighbours': ['Madagascar', 'Congo', 'East Africa']},
    'Madagascar':{'loc' : [950,826], 'neighbours': ['South Africa', 'East Africa']},
    }

# This checks that all the territories are correctly included
for ter in territories:
    for n in territories[ter]['neighbours']:
        if ter not in territories[n]['neighbours']:
            print("PROBLEMU")
            raise Exception (ter, n)


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

#print("this is ters", territories)



def teralloc(territories, troopNo=3, testWin=False):
    playerno = 2
    ter_no = int(len(territories) / playerno)
    if testWin:
        ter_no = 1

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


def teralloc_db(territories, players, troopNo=3, test_winning=False):
    playerno = 2
    ter_no = int(len(territories) / playerno)
    if test_winning:
        ter_no = 1

    # just the territories
    p1ters = random.sample(territories, ter_no)

    for ter in territories:
        ter.troopNo = troopNo
        if ter in p1ters:
            ter.currentOwner = players[0].id
        else:
            ter.currentOwner = players[1].id


#test = teralloc(territories)
#
# for ter in territories:
#     if ter in p1ters:
#         territories[ter]


