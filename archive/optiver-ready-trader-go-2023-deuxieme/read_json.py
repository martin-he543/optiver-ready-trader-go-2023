import numpy as np
import json

data = json.load(open('exchange.json')); engine, execution, fees, hud, information, instrument, limits, traders = data.get("Engine"), data.get("Execution"), data.get("Fees"), data.get("Hud"), data.get("Information"), data.get("Instrument"), data.get("Limits"), data.get("Traders")

ENGINE_MarketDataFile = engine.get("MarketDataFile")
ENGINE_MatchEventsFile = engine.get("MatchEventsFile")
EXECUTION_Host, HUD_Host = execution.get("Host"), hud.get("Host")
EXECUTION_Port, HUD_Port = execution.get("Port"), hud.get("Port")

ENGINE_MarketEventInterval = engine.get("MarketEventInterval")
ENGINE_MarketOpenDelay = engine.get("MarketOpenDelay")
ENGINE_Speed = engine.get("Speed")
ENGINE_TickInterval = engine.get("TickInterval")
FEES_Maker, FEES_Taker = fees.get("Maker"), fees.get("Taker")

INFORMATION_Type, INFORMATION_Name = information.get("Type"), information.get("Name")
INSTRUMENT_Name, INSTRUMENT_Type = instrument.get("Name"), instrument.get("Type")
LIMITS_ActiveOrderCountLimit, LIMITS_ActiveVolumeLimit, LIMITS_MessageFrequencyInterval, LIMITS_MessageFrequencyLimit, LIMITS_PositionLimit = limits.get("ActiveOrderCountLimit"), limits.get("ActiveVolumeLimit"), limits.get("MessageFrequencyInterval"), limits.get("MessageFrequencyLimit"), limits.get("PositionLimit")

print(LIMITS_PositionLimit)