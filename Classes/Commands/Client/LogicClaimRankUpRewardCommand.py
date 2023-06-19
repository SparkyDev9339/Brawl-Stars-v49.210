import json

from Classes.Commands.LogicCommand import LogicCommand
from Classes.Messaging import Messaging
from Database.DatabaseHandler import DatabaseHandler

class LogicClaimRankUpRewardCommand(LogicCommand):
    def __init__(self, commandData):
        super().__init__(commandData)

    def encode(self, fields):
        LogicCommand.encode(self, fields)
        self.writeVInt(0)
        self.writeDataReference(0)
        return self.messagePayload

    def decode(self, calling_instance):
        fields = {}
        LogicCommand.decode(calling_instance, fields, False)
        fields["RewardType"] = calling_instance.readVInt()
        LogicCommand.parseFields(fields)
        return fields

    def execute(self, calling_instance, fields, cryptoInit):
        db_instance = DatabaseHandler()
        player_data = json.loads(db_instance.getPlayerEntry(calling_instance.player.ID)[2])

        if calling_instance.player.TrophyRoadTier >= 1: # Box
            fields["Command"] = {"ID": 203}
            player_data["delivery_items"] = {
                'Boxes': []
            }
            box = {
        	'Type': 0,
        	'Items': []
        	}
            item = {'Amount': 1000, 'DataRef': [0, 0], 'RewardID': 7}
            box['Items'].append(item)
            box['Type'] = 100
            player_data["delivery_items"]['Boxes'].append(box)
            player_data["TrophyRoadTier"] += 1

            db_instance.updatePlayerData(player_data, calling_instance)
            fields["Socket"] = calling_instance.client
        fields["Command"] = {"ID": 203}
        fields["PlayerID"] = calling_instance.player.ID
        Messaging.sendMessage(24111, fields, cryptoInit)

    def getCommandType(self):
        return 517