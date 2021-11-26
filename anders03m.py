from pathlib import Path
from numpy import mean as mean
import traci, os, datetime, json, sys, csv
programstart = datetime.datetime.now()
filesuffix = programstart.isoformat().replace('-', '_').replace(':', '_').replace('.', '_').replace('/', '_')

sumoBinary = "/usr/local/opt/sumo/share/sumo/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "simu_traci_02.sumocfg"] #simu_traci_01.sumocfg, simu_v5-6orig2-1.sumocfg
folder = 'REPORT/'
reportFile = "summary" + filesuffix + ".txt"
detectorFile = "pcuReport" + filesuffix + ".json"
dataFile = "data" + filesuffix + ".csv"

start, end = 0, 8100
process_time = [int(arg) for arg in sys.argv[1:]]
if len(process_time) > 1:
    start = min(process_time)
    end = max(process_time)
print(start, end)
warning = False

streets = {
"s1_s3" : ["-gneE406", "-gneE290", "-gneE291", "-gneE293", "-gneE294", "-gneE295", "-gneE296", "gneE252", "gneE253", "gneE255", "gneE297", "gneE396", "gneE611"],
"s1_s6" : ["gneE17", "gneE413", "gneE440", "gneE443", "gneE469", "gneE470", "gneE471"],
"s3_s1" : ["-gneE297", "gneE256", "gneE257", "gneE261", "gneE290", "gneE291", "gneE293", "gneE294", "gneE295", "gneE296", "gneE406", "gneE425", "gneE428", "gneE430", "gneE434", "gneE618", "gneE621"],
"s3_s5" : ["gneE262", "gneE270", "gneE274", "gneE279", "gneE320", "gneE321"],
"s3_s9" : ["-gneE131", "gneE248", "gneE374", "gneE375", "gneE628", "gneE629"],
"s5_s3" : ["gneE263", "gneE268", "gneE269", "gneE271", "gneE272", "gneE273", "gneE311", "gneE322", "gneE688"],
"s5_s11" : ["-gneE555", "gneE210", "gneE331", "gneE332", "gneE333", "gneE334", "gneE336", "gneE648", "gneE649", "gneE651"],
"s6_s1" : ["-gneE413", "-gneE440", "-gneE441", "gneE20", "gneE414", "gneE415", "gneE436", "gneE444"],
"s6_s9" : ["-gneE71", "gneE115", "gneE116", "gneE120", "gneE121", "gneE25", "gneE26", "gneE70", "gneE72", "gneE73", "gneE79"],
"s9_s3" : ["gneE131", "gneE376", "gneE377", "gneE378", "gneE626", "gneE627"],
"s9_s6" : ["-gneE115", "-gneE116", "-gneE120", "-gneE121", "-gneE25", "-gneE26", "-gneE70", "-gneE72", "-gneE73", "-gneE79", "gneE71"],
"s9_s11" : ["-gneE136", "gneE128", "gneE137", "gneE140", "gneE142", "gneE552"],
"s11_s5" : ["-gneE210", "gneE337", "gneE343", "gneE344", "gneE346", "gneE399", "gneE400", "gneE404", "gneE555"],
"s11_s9" : ["-gneE128", "-gneE137", "-gneE140", "-gneE142", "-gneE552", "gneE136"]
}

detectors = ["e2Detector_s1eOut1", "e2Detector_s1eOut2", "e2Detector_s1en", "e2Detector_s1es1", "e2Detector_s1es2", "e2Detector_s1ew1", "e2Detector_s1ew2", "e2Detector_s1ew3", "e2Detector_s1nOut1", "e2Detector_s1nOut2", "e2Detector_s1nOut3", "e2Detector_s1ne1", "e2Detector_s1ne2", "e2Detector_s1ne3", "e2Detector_s1ns1", "e2Detector_s1ns2", "e2Detector_s1nw1", "e2Detector_s1nw2", "e2Detector_s1sOut1", "e2Detector_s1sOut2", "e2Detector_s1se", "e2Detector_s1sn1", "e2Detector_s1sn2", "e2Detector_s1sw1", "e2Detector_s1sw2", "e2Detector_s1wOut1", "e2Detector_s1wOut2", "e2Detector_s1wOut3", "e2Detector_s1we1", "e2Detector_s1we2", "e2Detector_s1wn1", "e2Detector_s1wn2", "e2Detector_s1ws", "e2Detector_s3eOut1", "e2Detector_s3eOut2", "e2Detector_s3eOut3", "e2Detector_s3es1", "e2Detector_s3es2", "e2Detector_s3ew1", "e2Detector_s3ew2", "e2Detector_s3ew3", "e2Detector_s3nOut", "e2Detector_s3ne", "e2Detector_s3ns1", "e2Detector_s3ns2", "e2Detector_s3ns3", "e2Detector_s3nw1", "e2Detector_s3nw2", "e2Detector_s3sOut1", "e2Detector_s3sOut2", "e2Detector_s3se", "e2Detector_s3sn1", "e2Detector_s3sn2", "e2Detector_s3sw1", "e2Detector_s3sw2", "e2Detector_s3wOut1", "e2Detector_s3wOut2", "e2Detector_s3wOut3", "e2Detector_s3we", "e2Detector_s3we1", "e2Detector_s3we2", "e2Detector_s3we3", "e2Detector_s3ws", "e2Detector_s5busnws", "e2Detector_s5nOut1", "e2Detector_s5nOut2", "e2Detector_s5nbusOut", "e2Detector_s5ns1", "e2Detector_s5ns2", "e2Detector_s5nw", "e2Detector_s5sOut1", "e2Detector_s5sOut2", "e2Detector_s5sOut3", "e2Detector_s5sbusOut", "e2Detector_s5sn1", "e2Detector_s5sn2", "e2Detector_s5sn3", "e2Detector_s5sw", "e2Detector_s5wOut1", "e2Detector_s5wOut2", "e2Detector_s5wOut3", "e2Detector_s5wn1", "e2Detector_s5wn2", "e2Detector_s5wn3", "e2Detector_s5ws", "e2Detector_s6eOut1", "e2Detector_s6eOut2", "e2Detector_s6eOut3", "e2Detector_s6en", "e2Detector_s6es1", "e2Detector_s6es2", "e2Detector_s6ew1", "e2Detector_s6ew2", "e2Detector_s6nOut1", "e2Detector_s6nOut2", "e2Detector_s6nOut3", "e2Detector_s6ne1", "e2Detector_s6ne2", "e2Detector_s6ns1", "e2Detector_s6ns2", "e2Detector_s6nw", "e2Detector_s6sOut1", "e2Detector_s6sbusOut", "e2Detector_s6se", "e2Detector_s6sn1", "e2Detector_s6sn2", "e2Detector_s6sw1", "e2Detector_s6sw2", "e2Detector_s6wOut1", "e2Detector_s6wOut2", "e2Detector_s6wOut3", "e2Detector_s6we1", "e2Detector_s6we2", "e2Detector_s6wn1", "e2Detector_s6wn2", "e2Detector_s6ws", "e2Detector_s9eOut1", "e2Detector_s9eOut2", "e2Detector_s9eOut3", "e2Detector_s9en", "e2Detector_s9es1", "e2Detector_s9es2", "e2Detector_s9ew1", "e2Detector_s9ew2", "e2Detector_s9nOut1", "e2Detector_s9nOut2", "e2Detector_s9ne", "e2Detector_s9ns", "e2Detector_s9nw", "e2Detector_s9sOut1", "e2Detector_s9sOut2", "e2Detector_s9se", "e2Detector_s9sn", "e2Detector_s9sw", "e2Detector_s9wOut1", "e2Detector_s9wOut2", "e2Detector_s9wOut3", "e2Detector_s9we1", "e2Detector_s9we2", "e2Detector_s9wn1", "e2Detector_s9wn2", "e2Detector_s9ws1", "e2Detector_s11nwBus", "e2Detector_s11eOut1", "e2Detector_s11eOut2", "e2Detector_s11en", "e2Detector_s11es", "e2Detector_s11ew", "e2Detector_s11nBusOut", "e2Detector_s11nOut1", "e2Detector_s11nOut2", "e2Detector_s11ne", "e2Detector_s11ns1", "e2Detector_s11ns2", "e2Detector_s11sBusOut", "e2Detector_s11sOut1", "e2Detector_s11sOut2", "e2Detector_s11se", "e2Detector_s11sn1", "e2Detector_s11sn2", "e2Detector_s11snbus", "e2Detector_s11sw", "e2Detector_s11wOut1", "e2Detector_s11wOut2", "e2Detector_s11wOut3", "e2Detector_s11we1", "e2Detector_s11we2", "taz_s1n0", "taz_s1n1", "taz_s1n3", "taz_s1r0", "taz_s1w0", "taz_s1w1", "taz_s1w2", "taz_s1w3", "taz_s1w4", "taz_s3n0", "taz_s3n1", "taz_s5n0", "taz_s5n1", "taz_s5n2", "taz_s5n3", "taz_s5r0", "taz_s6w0", "taz_s6w1", "taz_s6w2", "taz_s6s0", "taz_s6s1", "taz_s6s2", "taz_s9s0", "taz_s9s1", "taz_s9s2", "taz_s11s0", "taz_s11s1", "taz_s11s2" , "taz_s11e0", "taz_s11e1", "taz_s11e2"]

fringeEdges = {'s1n': ["taz_s1n0", "taz_s1n1", "taz_s1n3"], 's1r': ["taz_s1r0"], 's1w': ["taz_s1w0", "taz_s1w1", "taz_s1w2", "taz_s1w3", "taz_s1w4"], 's3n': ["taz_s3n0", "taz_s3n1"], 's5n': ["taz_s5n0", "taz_s5n1", "taz_s5n2", "taz_s5n3"], 's5r': ["taz_s5r0"], 's6w': ["taz_s6w0", "taz_s6w1", "taz_s6w2"], 's6s': ["taz_s6s0", "taz_s6s1", "taz_s6s2"], 's9s': ["taz_s9s0", "taz_s9s1", "taz_s9s2"], 's11s': ["taz_s11s0", "taz_s11s1", "taz_s11s2"], 's11e': ["taz_s11e0", "taz_s11e1", "taz_s11e2"]}
pcuOnStreets = {'s1_s3': [[], []], 's1_s6': [[], []], 's3_s1': [[], []], 's3_s5': [[], []], 's3_s9': [[], []], 's5_s3': [[], []], 's5_s11': [[], []], 's6_s1': [[], []], 's6_s9': [[], []], 's9_s3': [[], []], 's9_s6': [[], []], 's9_s11': [[], []], 's11_s5': [[], []], 's11_s9': [[], []]}
collisions = {'s1_s3': 0, 's1_s6': 0, 's3_s1': 0, 's3_s5': 0, 's3_s9': 0, 's5_s3': 0, 's5_s11': 0, 's6_s1': 0, 's6_s9': 0, 's9_s3': 0, 's9_s6': 0, 's9_s11': 0, 's11_s5': 0, 's11_s9': 0}
statistics = {'sumLoaded': 0, 'sumDeparted': 0, 'sumArrived': 0, 'sumTeleports': 0, 'sumCollisions': 0, 'collisions': []}
csv_header = {'fringe' : True, 'pending' : True, 'occupancy' : True}
map, intervals, streetLanes = {}, {}, {} # [pcu, avg_occupancy], {t: {detector: pcu, ...}, ...}, [laneID, ...]
csv_fringe, csv_pending, csv_occupancy = {}, {}, {}
fringe, laneStreets = {}, {}
old = {'t': start}
for entry in fringeEdges.keys():
    fringe[entry] = 0

def resetDetected(detected):
    for detector in detectors:
        detected.update({detector: set()})
    return detected

def resetDictionary(iterable, value):
    for item in iterable:
        iterable[item] = value

def countVehicleTypes(idList, count_pcu):
    randoms, commuters, buses = [0, 0, 0]
    if count_pcu:
        busFactor = 3
    else:
        busFactor = 1
    for id in idList:
        if 'bus' in id:
            buses += busFactor
        elif 'commuter' in id:
            commuters += 1
        else:
            randoms += 1
    return [randoms, commuters, buses]

def countPCUsOnDetector(vhcLeftDetector):
    PCU = {}
    for detector in vhcLeftDetector:
        PCU[detector] = sum(countVehicleTypes(vhcLeftDetector[detector], True))
    return PCU

def setStreetLanes(streetLanes):
    for street in streets:
        streetLanes[street] = []
        for edge in streets[street]:
            lanes = traci.edge.getLaneNumber(edge)
            for lane in range(lanes):
                laneID = edge + '_' + str(lane)
                allowed = traci.lane.getAllowed(laneID)
                unprotected = ['moped', 'bicycle', 'pedestrian']
                if not any(category in allowed  for category in unprotected):
                    streetLanes[street].append(laneID)

def setLaneStreets(streetLanes, laneStreets):
    for street in streetLanes:
        for laneID in streetLanes[street]:
            laneStreets[laneID] = street

def update_pcuOnStreets(streetLanes):
    for street in streetLanes:
        vehicles = []
        occupancy = []
        for laneID in streetLanes[street]:
            vehicles.extend(traci.lane.getLastStepVehicleIDs(laneID))
            occupancy.append(traci.lane.getLastStepOccupancy(laneID))
        if sum(occupancy) != 0:
            pcuOnStreets[street][0].append(sum(countVehicleTypes(vehicles, True)))
            pcuOnStreets[street][1].append(mean(occupancy))

def pop_pcuOnStreets(street):
    vhc, occ = pcuOnStreets[street]
    pcuOnStreets[street] = [[], []]
    return int(mean(vhc)), mean(occ)

def getFringeVehicles(intervals, t):
    vhcAtFringe = {}
    entriesAtFringe = ''
    period = t - old['t']
    for entry in fringeEdges:
        nbr = 0
        for detector in fringeEdges[entry]:
            nbr += intervals[detector]
        vhcAtFringe[entry] = nbr
        fringe[entry] += nbr
    values = vhcAtFringe.values()
    entriesAtFringe += 'Number of PCUs that entered thru fringe from {} s to {} s ({} s).\n'.format(old['t'], t, period)
    entriesAtFringe += '{0:^5s} {1:^5s} {2:^5s} {3:^5s} {4:^5s} {5:^5s} {6:^5s} {7:^5s} {8:^5s} {9:^5s} {10:^5s} {11:^5s}\n'.format('sum', *vhcAtFringe.keys())
    entriesAtFringe += '{0:^5.0f} {1:^5.0f} {2:^5.0f} {3:^5.0f} {4:^5.0f} {5:^5.0f} {6:^5.0f} {7:^5.0f} {8:^5.0f} {9:^5.0f} {10:^5.0f} {11:^5.0f}\n'.format(sum(values), *values)
    old['t'] = t
    if csv_header['fringe']:
        csv_fringe[0] = ['time', 'sum', *vhcAtFringe.keys()]
        csv_header['fringe'] = False
    csv_fringe[t] = [t, sum(values), *values]
    return entriesAtFringe

def findConfig(sumoCfg):
    configFiles = {}
    values = ['<net-file', '<lateral-resolution', '<gui-settings-file', '<route-files', '<additional-files']
    with open(sumoCfg, 'r', encoding='utf-8') as aFile:
        cfgText = aFile.read()
    for value in values:
        i = cfgText.find(value)
        if i > 0:
            j = cfgText.find('/>', i)
        configFiles[value[1:]] = cfgText[i+1:j]
    return configFiles

def getPendings(t):
    origins = {
    's1n':['gneE660'], 's1ramp':['-gneE659'], 's1w':['-gneE411', 'gneE412'],
    's3n':['gneE532'], 's5n':['gneE666', 'gneE667'], 's5ramp':['-gneE675'],
    's6w':['-gneE10'], 's6s':['-gneE657'], 's9s':['-gneE133'],
    's11s':['-gneE669'], 's11e':['-gneE553']
    }
    M = [[0] * 12 for i in range(3)]
    col = 1
    thisMap = {}
    for entry in origins:
        for edge in origins[entry]:
            idList = traci.edge.getPendingVehicles(edge)
            thisMap[entry] = len(idList)
            M[0][col], M[1][col], M[2][col] = countVehicleTypes(idList, False)
        col +=1
    map[t].update(thisMap)
    headline = '{0:^5s} {1:^5s} {2:^5s} {3:^5s} {4:^5s} {5:^5s} {6:^5s} {7:^5s} {8:^5s} {9:^5s} {10:^5s} {11:^5s}\n'
    resultline = '{0:^5s} {1:^5.0f} {2:^5.0f} {3:^5.0f} {4:^5.0f} {5:^5.0f} {6:^5.0f} {7:^5.0f} {8:^5.0f} {9:^5.0f} {10:^5.0f} {11:^5.0f} \n'
    sumOfPenders = [sum(M[0]), sum(M[1]), sum(M[2])]
    pendings = 'At t = {} min {} vehicles are pending to enter via the fringe. \n'.format(t/60, sum(sumOfPenders))
    pendings += headline.format('vTyp', 's1n', 's1r', 's1w', 's3n', 's5n', 's5r', 's6w', 's6s', 's9s', 's11s', 's11e')
    pendings += resultline.format('rand', *M[0][1:12])
    pendings += resultline.format('comm', *M[1][1:12])
    pendings += resultline.format('bus', *M[2][1:12])
    if csv_header['pending']:
        csv_pending[0] = ['time', 'vTyp', 's1n', 's1r', 's1w', 's3n', 's5n', 's5r', 's6w', 's6s', 's9s', 's11s', 's11e']
        csv_header['pending'] = False
    csv_pending[t] = [[t, 'rand', *M[0][1:12]], [t, 'comm', *M[1][1:12]], [t, 'bus', *M[2][1:12]]]
    return pendings

def getSystemOccupancy(streetLanes):
    streetKeys = streets.keys()
    systemOccupancy = 'System occupancy:\n'
    systemOccupancy += '{0:5s} {1:5s} {2:5s} {3:5s} {4:5s} {5:5s} {6:5s} {7:6s} {8:5s} {9:5s} {10:5s} {11:5s} {12:6s} {13:6s} {14:6s}\n'.format('avg', *streetKeys)
    streetOccupancy = {}
    for street in streetLanes:
        streetOccupancy[street] = pop_pcuOnStreets(street)
        if streetOccupancy[street][0] == 0:
            warning = True
    map[t].update(streetOccupancy)
    occupancy_format = [mean([v[1] for v in streetOccupancy.values()]), *[streetOccupancy[street][1] for street in streetKeys]]
    systemOccupancy += '{0:^5.1%} {1:^5.1%} {2:^5.1%} {3:^5.1%} {4:^5.1%} {5:^5.1%} {6:^5.1%} {7:^6.1%} {8:^5.1%} {9:^5.1%} {10:^5.1%} {11:^5.1%} {12:^6.1%} {13:^6.1%} {14:^6.1%}\n'.format(*occupancy_format)
    if csv_header['occupancy']:
        csv_occupancy[0] = ['time', 'avg', *streetKeys]
        csv_header['occupancy'] = False
    csv_occupancy[t] = [t, mean([v[1] for v in streetOccupancy.values()]), *[streetOccupancy[street][1] for street in streetKeys]]
    return systemOccupancy

def updateStatistics(t, summarize):
    statistics['sumLoaded'] += traci.simulation.getLoadedNumber()
    statistics['sumDeparted'] += traci.simulation.getDepartedNumber()
    statistics['sumArrived'] += traci.simulation.getArrivedNumber()
    statistics['sumTeleports'] += traci.simulation.getEndingTeleportNumber()
    statistics['sumCollisions'] += traci.simulation.getCollidingVehiclesNumber()
    statistics['collisions'].extend(traci.simulation.getCollisions())
    if summarize:
        for collision in statistics.pop('collisions'):
            laneID = str(collision.lane)
            street = laneStreets.get(laneID)
            if street:
                collisions[street] += 1
        intervals[t].update(statistics)
        resetDictionary(statistics, 0)
        statistics['collisions'] = []

# Run code:
detected =  resetDetected({}) # Dictionary of sets {detector: {vehicle, ...}, ...}
traci.start(sumoCmd)
summary = 'Start = {} s. Stop = {} s.\n'.format(start, end)
print(summary)
setStreetLanes(streetLanes)
setLaneStreets(streetLanes, laneStreets)
checkframe = [900, 1800, 2700, 3600, 4500, 5400, 6300, 7200, 8100, 9000, 9900, 10800, end] # time in s
all_pending_cars = ''
for t in range(start, end+1):
    traci.simulationStep()
    if t % 150 == 0 and t > 0:
        update_pcuOnStreets(streetLanes)
    if t not in checkframe:
        updateStatistics(t, False)
        for detector in detected:
            vehiclesOnDetector = traci.lanearea.getLastStepVehicleIDs(detector)
            detected[detector].update(vehiclesOnDetector)
    else:
        vehiclesLeftDetector = {}
        map[t], intervals[t] = {}, {}
        updateStatistics(t, True)
        for detector in detected:
            vehiclesOnDetector = traci.lanearea.getLastStepVehicleIDs(detector)
            detected[detector].update(vehiclesOnDetector)
            vehiclesLeftDetector[detector] = set(detected[detector].difference(vehiclesOnDetector))
            detected[detector] = set(vehiclesOnDetector)
        intervals[t].update(countPCUsOnDetector(vehiclesLeftDetector))
        fringeVehicles = getFringeVehicles(intervals[t], t)
        pending_cars = getPendings(t)
        systemOccupancy = getSystemOccupancy(streetLanes)
        all_pending_cars += '\n' + fringeVehicles + '\n' + pending_cars + '\n' + systemOccupancy + '\n'
        print(fringeVehicles)
        print(pending_cars)
        print(systemOccupancy)
vehicles = {}
system_occupancy = []
sums = [0, 0, 0, 0, 0, 0, 0] # car, pcu, sum-%, random, commuter, bus, occupancy
occupancy_report = ''
for street in streetLanes:
    random_cars, commuters, buses, pcu = 0, 0, 0, 0
    idList, occupancy = [], []
    for laneID in streetLanes[street]:
        idList.extend(traci.lane.getLastStepVehicleIDs(laneID))
        occupancy.append(traci.lane.getLastStepOccupancy(laneID))
    random_cars, commuters, buses = countVehicleTypes(idList, False)
    carsum = commuters + random_cars + buses
    pcu = commuters + random_cars + 3 * buses
    avg_occupancy = mean(occupancy)
    vehicles[street] = [carsum, pcu, 0, random_cars, commuters, buses, avg_occupancy]
    sums = [sums[i] + vehicles[street][i] for i in range(len(sums))]
sums[-1] = sums[-1] / len(streets) # create average occupancy
endtime = 'Time = {} min.'.format(t/60)
summary += endtime + '\n'
print(endtime)
header ='{0:7s} {1:>7s} {2:>7s} {3:>7s} {4:>7s} {5:>7s} {6:>7s} {7:>7s} {8:>7s}'.format('Street', 'CarSum', 'PCU', 'Sum-%', 'Random', 'Commute', 'Bus', 'Occ-%', 'Coll')
summary += header + '\n'
print(header)
for street in vehicles:
    carsum, pcu, perc, ran, com, bus, occ = vehicles[street] # nbrList
    if sums[0] > 0:
        perc = float(carsum)/sums[0] # percentage
        sums[2] += perc
    else:
        perc = 0
    coll = collisions[street]
    line = '{0:7s} {1:7.0f} {2:7.0f} {3:7.1%} {4:7.0f} {5:7.0f} {6:7.0f} {7:7.1%} {8:7.0f}'.format(street, carsum, pcu, perc, ran, com, bus, occ, coll)
    print(line)
    summary += line + '\n'
sumline = '{0:7s} {1:7.0f} {2:7.0f} {3:7.1%} {4:7.0f} {5:7.0f} {6:7.0f} {7:7.1%} {8:7.0f}'.format('TOTAL', *sums, sum(collisions.values()))
summary += sumline + '\n'
print(sumline)
programend = datetime.datetime.now()
runtime = programend - programstart
print('Program runtime:', runtime, '\n')
sumFromFringe = 'Total number of PCUs that entered thru fringe during entire simulation ({} s).\n'.format(t - start)
sumFromFringe += '{0:^5s} {1:^5s} {2:^5s} {3:^5s} {4:^5s} {5:^5s} {6:^5s} {7:^5s} {8:^5s} {9:^5s} {10:^5s} {11:^5s}\n'.format('sum', *fringe.keys())
sumFromFringe += '{0:^5.0f} {1:^5.0f} {2:^5.0f} {3:^5.0f} {4:^5.0f} {5:^5.0f} {6:^5.0f} {7:^5.0f} {8:^5.0f} {9:^5.0f} {10:^5.0f} {11:^5.0f}\n'.format(sum(fringe.values()), *fringe.values())
# filePath = Path(os.getcwd() + '/REPORT/')
if not os.path.exists(folder):
    os.makedirs(folder)
json_configFiles = json.dumps(findConfig(sumoCmd[2]), indent=4)
with open(folder+reportFile, 'w') as aFile:
    aFile.write(json_configFiles + '\n')
    aFile.write('Program runtime:' + str(runtime) + '\n')
    aFile.write(summary)
    aFile.write(all_pending_cars)
    aFile.write(sumFromFringe)
print('Above report has been written to {}\n'.format(os.path.abspath(folder + reportFile)))
print(sumFromFringe)
if warning:
    print('------ *** WARNING! Check for zeros. *** ------')
with open(folder+detectorFile, 'w') as bFile:
    bFile.write(json_configFiles + '\n\n')
    bFile.write(json.dumps(collisions, indent=2) + '\n\n')
    bFile.write(json.dumps(map, indent=2) + '\n\n')
    bFile.write(json.dumps(intervals, indent=2))
with open(folder+dataFile, 'w') as cFile:
    for data in [csv_fringe, csv_pending, csv_occupancy]:
        header = data[0]
        writer = csv.writer(cFile)
        writer.writerow(header)
        for t in data:
            if t > 0:
                if len(data[t]) < 4:
                    for row in data[t]:
                        writer.writerow(row)
                else:
                    writer.writerow(data[t])
        writer.writerow(['' for x in data[t]])
traci.close()


    # traci.edge.getLaneNumber(string: edgeID) -> int # nbr of lanes on edge
    # traci.edge.getLastStepLength(string: edgeID) -> double # mean length of vehicles on edge
    # traci.edge.getLastStepVehicleIDs(string: edgeID) -> list(string)
    # traci.edge.getLastStepVehicleNumber(string: edgeID) -> integer # sum of vehicles on edge
    # traci.lane.getLastStepOccupancy(string: laneID) -> double
    # traci.lane.getLastStepVehicleNumber(string: laneID) -> integer # sum of vehicles on lane
    # traci.lane.getLength(string: laneID) -> double # length of lane
    # traci.lane.getAllowed(string: laneID) -> list(string) # empty list = all vehicles allowed
    # traci.vehicle.getLaneID(string: vehID) -> string
    # traci.vehicle.getLength(string) -> double # length of vehicle
    # traci.vehicle.getMinGap(string) -> double
    # traci.simulation.getLoadedNumber() -> integer # Returns the number of vehicles which were loaded in this time step.
    # traci.simulation.getEndingTeleportIDList() -> list(string) # Returns a list of ids of vehicles which ended to be teleported in this time step.
    # traci.simulation.getEndingTeleportNumber() -> integer # Returns the number of vehicles which ended to be teleported in this time step.
    # traci.simulation.getDepartedNumber() -> integer # Returns the number of vehicles which departed (were inserted into the road network) in this time step.
    # traci.simulation.getDepartedIDList() -> list(string) # Returns a list of ids of vehicles which departed (were inserted into the road network) in this time step.
    # traci.simulation.getDeltaT() -> double # Returns the length of one simulation step in seconds
    # traci.simulation.getCollisions() -> list(Collision) # Returns a list of collision objects
    # traci.simulation.getCollidingVehiclesNumber() -> integer # Return number of vehicles involved in a collision (typically 2 per collision).
    # traci.simulation.getCollidingVehiclesIDList() -> list(string) # Return Ids of vehicles involved in a collision (typically 2 per collision).
    # traci.simulation.getArrivedNumber() -> integer # Returns the number of vehicles which arrived (have reached their destination and are removed from the road network) in this time step.
    # traci.simulation.getArrivedIDList() -> list(string) # Returns a list of ids of vehicles which arrived (have reached their destination and are removed from the road network) in this time step.
    # traci.simulation.getParameter(self, objID, param)
