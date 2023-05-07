from encodings import utf_8
import json
from pathlib import Path
import os, sys

_default = None

def getDefault():
    global _default
    return _default

def setDefault(defaultConfig):
    global _default
    _default = defaultConfig

def createDefaultFile(configFilePath=None):
    configFile = configFilePath
    if configFile is None:
        home = Path.home()
        vmiDir = home / '.vmi'
        configFile = vmiDir / 'config.json'
        if vmiDir.is_dir() is False:
            vmiDir.mkdir(parents=True, exist_ok=True)
    else:
        configFile = Path(configFilePath)
    defaultConfig = getDefault()
    configFile.write_text(json.dumps(defaultConfig, ensure_ascii=False, indent=4), encoding="utf8")
    return defaultConfig

def getConfiguration(configFilePath=None, shouldCreateDefault= False):
    configFile = configFilePath
    vmiDir = None
    if configFile is None:
        home = Path.home()
        vmiDir = home / '.vmi'
        configFile = vmiDir / 'config.json'
        if vmiDir.is_dir() is False:
            vmiDir.mkdir(parents=True, exist_ok=True)
    else:
        configFile = Path(configFilePath)
        vmiDir = configFile.parents[0]

    if configFile.is_file() is False:
        if shouldCreateDefault is True:
            return createDefaultFile(configFilePath=configFilePath), vmiDir
        else:
            return None, None
    
    configuration = configFile.read_text(encoding='utf-8')
    try:
        configDict = json.loads(configuration)
    except Exception:
        configDict = createDefaultFile()
    finally:
        return configDict, vmiDir