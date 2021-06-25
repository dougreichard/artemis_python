
class Anomalies:
    anomalies = [
            {"name":"01", "pickupType":0, "x":32511.0, "z":65063.0},
            {"name":"02", "pickupType":0, "x":30469.0, "z":46936.0},
            {"name":"03", "pickupType":0, "x":36341.0, "z":28936.0},
            {"name":"04", "pickupType":0, "x":29064.0, "z":21659.0},
            {"name":"05", "pickupType":0, "x":50766.0, "z":91617.0},
            {"name":"06", "pickupType":0, "x":53958.0, "z":83702.0},
            {"name":"07", "pickupType":0, "x":58681.0, "z":77574.0},
            {"name":"08", "pickupType":0, "x":56256.0, "z":56255.0},
            {"name":"11", "pickupType":1, "x":67362.0, "z":65574.0},
            {"name":"12", "pickupType":1, "x":65192.0, "z":57276.0},
            {"name":"13", "pickupType":1, "x":62383.0, "z":48340.0},
            {"name":"14", "pickupType":1, "x":67362.0, "z":41829.0},
            {"name":"15", "pickupType":1, "x":68894.0, "z":29957.0},
            {"name":"16", "pickupType":1, "x":70426.0, "z":24212.0},
            {"name":"17", "pickupType":1, "x":7042.0, "z":14212.0},
            {"name":"21", "pickupType":2, "x":88426.0, "z":88212.0},
            {"name":"22", "pickupType":2, "x":10426.0, "z":84212.0},
            {"name":"23", "pickupType":2, "x":87426.0, "z":7212.0},
            {"name":"24", "pickupType":2, "x":48326.0, "z":42128.0},
            {"name":"25", "pickupType":2, "x":50461.0, "z":25295.0},
            {"name":"26", "pickupType":2, "x":84026.0, "z":28126.0},
            {"name":"31", "pickupType":3, "x":90465.0, "z":84212.0},
            {"name":"32", "pickupType":3, "x":86526.0, "z":7212.0},
            {"name":"33", "pickupType":3, "x":68326.0, "z":42128.0},
            {"name":"34", "pickupType":3, "x":92431.0, "z":52229.0},
            {"name":"35", "pickupType":3, "x":9461.0, "z":25292.0},
            {"name":"41", "pickupType":4, "x":10260.0, "z":84212.0},
            {"name":"42", "pickupType":4, "x":88967.0, "z":7942.0},
            {"name":"43", "pickupType":4, "x":78429.0, "z":79128.0},
            {"name":"44", "pickupType":4, "x":44461.0, "z":42829.0},
            {"name":"51", "pickupType":5, "x":68265.0, "z":80210.0},
            {"name":"52", "pickupType":5, "x":10426.0, "z":89228.0},
            {"name":"53", "pickupType":5, "x":77426.0, "z":7212.0},
            {"name":"61", "pickupType":6, "x":48271.0, "z":33120.0},
            {"name":"62", "pickupType":6, "x":80612.0, "z":72893.0},
            {"name":"71", "pickupType":7, "x":50461.0, "z":2954.0},
        ]

    def start(self, sim):
        for anom in self.anomalies:
            anom['id'] = sim.add_passive("anomaly", "anomaly") 
            obj = sim.get_space_object(anom['id'])
            obj.move(glm.Vec3(anom.x,0.0,anom.z))
            #TODO: object.pickupType
            #TODO: Set name

