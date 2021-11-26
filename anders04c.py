import json, csv, sys
from numpy import mean as mean

folder = 'REPORT'
filename = 'pcuReport2021_06_06T17_26_26_836291.json' # default filename

# Call file with optional arguments: filename.json -junc  --> filename.csv
# Run as: <codename>.py <filename1>.json [<filename2>.json …] [-junc]
# Argument -junc will sort table in junction order. Default: period order.

filesToProcess = sys.argv[1:]
sortJunction = False
maxDivisor = False
if '-junc' in filesToProcess:
    filesToProcess.remove('-junc')
    sortJunction = True
if '-maxdiv' in filesToProcess:
    filesToProcess.remove('-maxdiv')
    maxDivisor = True
nbrOfFiles = len(filesToProcess)
if not nbrOfFiles > 0:
    filesToProcess.append(filename)

detectors = {
's1' : {'fromNorth' : ["e2Detector_s1ne1", "e2Detector_s1ne2", "e2Detector_s1ne3", "e2Detector_s1ns1", "e2Detector_s1ns2", "e2Detector_s1nw1", "e2Detector_s1nw2"], 'fromEast' : ["e2Detector_s1en", "e2Detector_s1es1", "e2Detector_s1es2", "e2Detector_s1ew1", "e2Detector_s1ew2", "e2Detector_s1ew3"], 'fromSouth' : ["e2Detector_s1se", "e2Detector_s1sn1", "e2Detector_s1sn2", "e2Detector_s1sw1", "e2Detector_s1sw2"], 'fromWest' : ["e2Detector_s1we1", "e2Detector_s1we2", "e2Detector_s1wn1", "e2Detector_s1wn2", "e2Detector_s1ws"], 'toNorth' : ["e2Detector_s1nOut1", "e2Detector_s1nOut2", "e2Detector_s1nOut3"], 'toEast' : ["e2Detector_s1eOut1", "e2Detector_s1eOut2"], 'toSouth' : ["e2Detector_s1sOut1", "e2Detector_s1sOut2"], 'toWest' : ["e2Detector_s1wOut1", "e2Detector_s1wOut2", "e2Detector_s1wOut3"]},
's3' : {'fromNorth' : ["e2Detector_s3ne", "e2Detector_s3ns1", "e2Detector_s3ns2", "e2Detector_s3ns3", "e2Detector_s3nw1", "e2Detector_s3nw2"], 'fromEast' : ["e2Detector_s3es1", "e2Detector_s3es2", "e2Detector_s3ew1", "e2Detector_s3ew2", "e2Detector_s3ew3"], 'fromSouth' : ["e2Detector_s3se", "e2Detector_s3sn1", "e2Detector_s3sn2", "e2Detector_s3sw1", "e2Detector_s3sw2"], 'fromWest' : ["e2Detector_s3we", "e2Detector_s3we1", "e2Detector_s3we2", "e2Detector_s3we3", "e2Detector_s3ws"], 'toNorth' : ["e2Detector_s3nOut"], 'toEast' : ["e2Detector_s3eOut1", "e2Detector_s3eOut2", "e2Detector_s3eOut3"], 'toSouth' : ["e2Detector_s3sOut1", "e2Detector_s3sOut2"], 'toWest' : ["e2Detector_s3wOut1", "e2Detector_s3wOut2", "e2Detector_s3wOut3"]},
's5' : {'fromNorth' : ["e2Detector_s5busnws", "e2Detector_s5ns1", "e2Detector_s5ns2", "e2Detector_s5nw"], 'fromEast' : [], 'fromSouth' : ["e2Detector_s5sn1", "e2Detector_s5sn2", "e2Detector_s5sn3", "e2Detector_s5sw"], 'fromWest' : ["e2Detector_s5wn1", "e2Detector_s5wn2", "e2Detector_s5wn3", "e2Detector_s5ws"], 'toNorth' : ["e2Detector_s5nOut1", "e2Detector_s5nOut2", "e2Detector_s5nbusOut"], 'toEast' : [], 'toSouth' : ["e2Detector_s5sOut1", "e2Detector_s5sOut2", "e2Detector_s5sOut3", "e2Detector_s5sbusOut"], 'toWest' : ["e2Detector_s5wOut1", "e2Detector_s5wOut2", "e2Detector_s5wOut3"]},
's6' : {'fromNorth' : ["e2Detector_s6ne1", "e2Detector_s6ne2", "e2Detector_s6ns1", "e2Detector_s6ns2", "e2Detector_s6nw"], 'fromEast' : ["e2Detector_s6en", "e2Detector_s6es1", "e2Detector_s6es2", "e2Detector_s6ew1", "e2Detector_s6ew2"], 'fromSouth' : ["e2Detector_s6se", "e2Detector_s6sn1", "e2Detector_s6sn2", "e2Detector_s6sw1", "e2Detector_s6sw2"], 'fromWest' : ["e2Detector_s6we1", "e2Detector_s6we2", "e2Detector_s6wn1", "e2Detector_s6wn2", "e2Detector_s6ws"], 'toNorth' : ["e2Detector_s6nOut1", "e2Detector_s6nOut2", "e2Detector_s6nOut3"], 'toEast' : ["e2Detector_s6eOut1", "e2Detector_s6eOut2", "e2Detector_s6eOut3"], 'toSouth' : ["e2Detector_s6sOut1", "e2Detector_s6sbusOut"], 'toWest' : ["e2Detector_s6wOut1", "e2Detector_s6wOut2", "e2Detector_s6wOut3"]},
's9' : {'fromNorth' : ["e2Detector_s9ne", "e2Detector_s9ns", "e2Detector_s9nw"], 'fromEast' : ["e2Detector_s9en", "e2Detector_s9es1", "e2Detector_s9es2", "e2Detector_s9ew1", "e2Detector_s9ew2"], 'fromSouth' : ["e2Detector_s9se", "e2Detector_s9sn", "e2Detector_s9sw"], 'fromWest' : ["e2Detector_s9we1", "e2Detector_s9we2", "e2Detector_s9wn1", "e2Detector_s9wn2", "e2Detector_s9ws1", "e2Detector_s11nwBus"], 'toNorth' : ["e2Detector_s9nOut1", "e2Detector_s9nOut2"], 'toEast' : ["e2Detector_s9eOut1", "e2Detector_s9eOut2", "e2Detector_s9eOut3"], 'toSouth' : ["e2Detector_s9sOut1", "e2Detector_s9sOut2"], 'toWest' : ["e2Detector_s9wOut1", "e2Detector_s9wOut2", "e2Detector_s9wOut3"]},
's11' : {'fromNorth' : ["e2Detector_s11ne", "e2Detector_s11ns1", "e2Detector_s11ns2"], 'fromEast' : ["e2Detector_s11en", "e2Detector_s11es", "e2Detector_s11ew"], 'fromSouth' : ["e2Detector_s11se", "e2Detector_s11sn1", "e2Detector_s11sn2", "e2Detector_s11snbus", "e2Detector_s11sw"], 'fromWest' : ["e2Detector_s11we1", "e2Detector_s11we2"], 'toNorth' : ["e2Detector_s11nBusOut", "e2Detector_s11nOut1", "e2Detector_s11nOut2"], 'toEast' : ["e2Detector_s11eOut1", "e2Detector_s11eOut2"], 'toSouth' : ["e2Detector_s11sBusOut", "e2Detector_s11sOut1", "e2Detector_s11sOut2"], 'toWest' : ["e2Detector_s11wOut1", "e2Detector_s11wOut2", "e2Detector_s11wOut3"]}
}

pcu_capacity = {'s1_s3': 0, 's1_s6': 0, 's3_s1': 0, 's3_s5': 0, 's3_s9': 0, 's5_s3': 0, 's5_s11': 0, 's6_s1': 0, 's6_s9': 0, 's9_s3': 0, 's9_s6': 0, 's9_s11': 0, 's11_s5': 0, 's11_s9': 0}

def findDivisor(pcuOnStreets, direction):
    div = []
    for t in pcuOnStreets:
        div.append(t[direction][0])
    return int(mean(div))

def getDeviation(N, pcuOnStreets):
    dev_order = {
    's1_s3' : {'s1' : 'toEast', 's3' : 'fromWest'}, 's3_s1' : {'s3' : 'toWest', 's1' : 'fromEast'},
    's1_s6' : {'s1' : 'toSouth', 's6' : 'fromNorth'}, 's6_s1' : {'s6' : 'toNorth', 's1' : 'fromSouth'},
    's3_s5' : {'s3' : 'toEast', 's5' : 'fromWest'}, 's5_s3' : {'s5' : 'toWest', 's3' : 'fromEast'},
    's3_s9' : {'s3' : 'toSouth', 's9': 'fromNorth'}, 's9_s3' : {'s9' : 'toNorth', 's3' : 'fromSouth'},
    's5_s11' : {'s5' : 'toSouth', 's11' : 'fromNorth'}, 's11_s5' : {'s11' : 'toNorth', 's5' : 'fromSouth'},
    's6_s9' : {'s6' : 'toEast', 's9' : 'fromWest'}, 's9_s6' : {'s9' : 'toWest', 's6' : 'fromEast'},
    's9_s11' : {'s9' : 'toEast', 's11' : 'fromWest'}, 's11_s9' : {'s11' : 'toWest', 's9' : 'fromEast'}
    }
    efficiency = {}
    headerMuStdev = '{0:>5s} {1:^4s} {2:^4s} {3:^11s} {4:^11s} {5:^11s}  {6:^11s} {7:^11s} {8:^11s} {9:^11s}\n'
    muAndStdev = headerMuStdev.format('time', 'µ', 'd(X)', 's1/s3', 's3/s5', 's1/s6', 's3/s9', 's5/s11', 's6/s9', 's9/s11')
    for t in N:
        evac = {}
        streets = N[t]
        pcu_occupancy = pcuOnStreets[t]
        divisors = []
        for direction, parts in dev_order.items():
            divisor = int(pcu_occupancy[direction][0])
            if maxDivisor:
                divisor = int(pcu_occupancy[direction][0] / pcu_occupancy[direction][1])
            if divisor == 0:
                warning = True
                divisor = findDivisor(pcuOnStreets, direction)
                print('divisor corrected to', divisor, '@ t=', t, 'on', direction)
            divisors.append(divisor)
            startNode, endNode = parts.keys()
            toWhere, fromWhere = parts.values()
            toAdd = streets[startNode].get(toWhere)
            toSubtract = streets[endNode].get(fromWhere)
            evac[direction] = round((divisor+toAdd-toSubtract)/divisor, 6)
        mu = sum(evac.values())/len(evac)
        stdev = (sum([(x-mu)**2 for x in evac.values()])/(len(evac.values())-1))**0.5
        evac['µ'] = round(mu, 6)
        evac['d(X)'] = round(stdev, 6)
        efficiency[t] = evac
        valueMuStdev = '{0:>5s} {1:4.2f} {2:4.2f} {3:5.2f}/{4:5.2f} {5:5.2f}/{6:5.2f} {7:5.2f}/{8:5.2f} {9:5.2f}/{10:5.2f} {11:5.2f}/{12:5.2f} {13:5.2f}/{14:5.2f} {15:5.2f}/{16:5.2f}\n'
        muAndStdev += valueMuStdev.format(t, mu, stdev, evac['s1_s3'], evac['s3_s1'], evac['s3_s5'], evac['s5_s3'], evac['s1_s6'], evac['s6_s1'], evac['s3_s9'], evac['s9_s3'], evac['s5_s11'], evac['s11_s5'], evac['s6_s9'], evac['s9_s6'], evac['s9_s11'], evac['s11_s9'])
    return efficiency, muAndStdev

def getStatistics(intervals):
    statistics = 'Statistics:\n'
    S = []
    tStats = [0, 0, '', 0, '', 0, '', 0, '']
    header2 = ['time', 'loaded', 'departed', 'dep-%', 'arrived', 'arr-%', 'teleports', 'tele-%', 'collisions', 'coll-%']
    statistics += '{0:6s}{1:>7s}{2:>9s}{3:>7s}{4:>8s}{5:>7s}{6:>11s}{7:>8s}{8:>11s}{9:>7s}\n'.format(*header2)
    statLine = '{0:6s}{1:7.0f}{2:9.0f}{3:7s}{4:8.0f}{5:7s}{6:11.0f}{7:8s}{8:11.0f}{9:7s}\n'
    sumLine = '{0:6s}{1:7.0f}{2:9.0f}{3:7.2%}{4:8.0f}{5:7.2%}{6:11.0f}{7:8.2%}{8:11.0f}{9:7.2%}\n'
    S.append(header2)
    for time in intervals:
        interval = intervals[time]
        stats = [interval['sumLoaded'], interval['sumDeparted'], '', interval['sumArrived'], '', interval['sumTeleports'], '', interval['sumCollisions'], '']
        S.append([time, *stats])
        statistics += statLine.format(time, *stats)
        for i in range(len(stats)):
            if stats[i] != '':
                tStats[i] += stats[i]
    tStats[2], tStats[4], tStats[6], tStats[8] = tStats[1]/tStats[0], tStats[3]/tStats[1], tStats[5]/tStats[1], tStats[7]/tStats[1]
    statistics += sumLine.format('sum',*tStats)
    S.append(['sum', *tStats])
    print(statistics)
    return S

def getTotalCollisions(collisions):
    header3 = ['totColl', 'sum', 'avg', 's1_s3', 's3_s1', 's1_s6', 's6_s1', 's3_s5', 's5_s3', 's3_s9', 's9_s3', 's5_s11', 's11_s5', 's6_s9', 's9_s6', 's9_s11', 's11_s9']
    allCollisions = ['', sum(collisions.values()), round(mean([*collisions.values()]),1), *collisions.values()]
    coll_headerline = '{0:>7s}{1:>6s}{2:>6s}{3:>6s}{4:>6s}{5:>6s}{6:>6s}{7:>6s}{8:>6s}{9:>6s}{10:>6s}{11:>6s}{12:>6s}{13:>6s}{14:>6s}{15:>7s}{16:>7s}\n'
    coll_line = '{0:7s}{1:6.0f}{2:6.1f}{3:6.0f}{4:6.0f}{5:6.0f}{6:6.0f}{7:6.0f}{8:6.0f}{9:6.0f}{10:6.0f}{11:6.0f}{12:6.0f}{13:6.0f}{14:6.0f}{15:7.0f}{16:7.0f}\n'
    print('Total nbr of collisions:\n' + coll_headerline.format(*header3) + coll_line.format(*allCollisions))
    csv_collisions = [header3, allCollisions]
    return csv_collisions

# Run code
warning = False
for jsonFile in filesToProcess:
    fileToRead = folder + '/' + jsonFile
    if maxDivisor:
        jsonFile = 'maxdiv_' + jsonFile
    fileToWrite = folder + '/' + jsonFile.split('.')[0] + '.csv'
    summary = ''
    M = []
    N = {}
    with open(fileToRead) as aFile:
        text = aFile.read()
        config, collision_data, pcu_data, detector_data = text.split('\n\n', 3)
    collisions = json.loads(collision_data)
    pcuOnStreets = json.loads(pcu_data)
    intervals = json.loads(detector_data)
    header = ['junc', 't-per', 'start', 'end', 'fr N', 'fr E', 'fr S', 'fr W', 'sumIN', 'to N', 'to E', 'to S', 'to W', 'sumOUT', 'I/O']
    summary += '{0:>6s}{1:>6s}{2:>6s}{3:>6s}{4:>6s}{5:>6s}{6:>6s}{7:>6s}{8:>6s}{9:>6s}{10:>6s}{11:>6s}{12:>6s}{13:>7s}{14:>8s}\n'.format(*header)
    period = 0
    periods = [0 , *[int(key) for key in intervals.keys()]]
    for time, interval in intervals.items():
        Junc = {}
        for junction, directions in detectors.items():
            results = {}
            m = ['', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0]
            m[0:4] = [junction, period, periods[period], periods[period+1]]
            for direction, detector in directions.items():
                pcu = 0
                for aDetector in detector:
                    pcu += interval[aDetector]
                results[direction] = pcu
            m[4:8] = [results['fromNorth'], results['fromEast'], results['fromSouth'], results['fromWest']]
            m[8] = sum(m[4:8])
            m[9:13] = [results['toNorth'], results['toEast'], results['toSouth'], results['toWest']]
            m[13] = sum(m[9:13])
            m[14] = round(m[8] / m[13], 6)
            M.append(m)
            Junc[junction] = results
        N[time] = Junc
        period += 1
    if sortJunction:
        M.sort(key=lambda x: int(x[0][1:])) # Sort in Junction order instead of period order
    for row in M:
        summary += '{0:>6s}{1:6.0f}{2:6.0f}{3:6.0f}{4:6.0f}{5:6.0f}{6:6.0f}{7:6.0f}{8:6.0f}{9:6.0f}{10:6.0f}{11:6.0f}{12:6.0f}{13:7.0f}{14:8.4f}\n'.format(*row)
    print(summary)
    for direction in pcu_capacity:
        nbrOfVehicles = []
        occupancies = []
        for t in pcuOnStreets:
            vehicles, occupancy = pcuOnStreets[t][direction]
            if vehicles != 0:
                nbrOfVehicles.append(vehicles)
            if occupancy != 0:
                occupancies.append(occupancy)
        pcu_capacity[direction] = round(mean(nbrOfVehicles) / mean(occupancies), 0)
    efficiency, muAndStdev = getDeviation(N, pcuOnStreets)
    print(muAndStdev)
    fieldnames1 = ['time', 'µ', 'd(X)', 's1_s3', 's3_s1', 's1_s6', 's6_s1', 's3_s5', 's5_s3', 's3_s9', 's9_s3', 's5_s11', 's11_s5', 's6_s9', 's9_s6', 's9_s11', 's11_s9']
    with open(fileToWrite, 'w', encoding='UTF8', newline='') as bFile:
        writer = csv.writer(bFile)
        writer.writerow(header)
        writer.writerows(M)
        writer.writerow(['' for x in fieldnames1])
        writer = csv.DictWriter(bFile, fieldnames1)
        writer.writeheader()
        evac = []
        for t in efficiency:
            efficiency[t].update({'time' : t})
            evac = efficiency[t]
            writer.writerow(evac)
        writer = csv.writer(bFile)
        writer.writerow(['' for x in fieldnames1])
        writer.writerows(getTotalCollisions(collisions))
        writer.writerow(['' for x in fieldnames1])
        writer.writerows(getStatistics(intervals))
if warning:
    print('----- ***** WARNING! Check divisors and occupancies. ***** -----')
