import os
import json
from ctypes import *


def readAscFromMeasDat(_byteBuffer):
    _begin = _byteBuffer.rfind(b'### ASCCONV BEGIN object=MrProt')
    if _begin < 0:
        raise ValueError
    _end = _byteBuffer.find(b'### ASCCONV END ###', _begin)
    if _begin > _end:
        raise ValueError
    _lines = str(_byteBuffer[_begin: _end], 'utf-8').splitlines()
    _ret = {}
    for _line in _lines:
        _temp = _line.split("=")
        if len(_temp) == 2:
            if len(_temp[0].split()) == 0:
                raise ValueError
            if len(_temp[1].split()) == 0:
                raise ValueError
            _key = _temp[0].split()[0]
            _value = _temp[1].split()[0]
            _ret[_key] = _value
    return _ret


def _convertString(_x):
    _ret = 0
    try:
        _ret = float(_x)
    except ValueError:
        pass
    else:
        if (_x.find('.') != -1):
            return _ret
    try:
        _ret = int(_x, 0)
    except ValueError:
        pass
    else:
        return _ret
    if len(_x) > 1 and _x[0] == '"' and _x[-1] == '"':
        return _x[1:-1]
    return _x


def getAscParameters(_strFile, _byteBuffer):
    _asc = readAscFromMeasDat(_byteBuffer)
    _strPre, _strExt = os.path.splitext(os.path.basename(_strFile))
    _ret = {}
    _ret["Filename"] = _strPre
    _ret["CompleteFilename"] = _strFile
    _ret["Directory"] = os.path.dirname(_strFile)
    if "B0" in _asc:
        _ret["B0"] = float(_asc['sProtConsistencyInfo.flNominalB0'])
    else:
        _ret["B0"] = float(_asc['sTXSPEC.asNucleusInfo[0].lFrequency']) / 42575600.
    _ret["ExcitationMode"] = _convertString(_asc['sTXSPEC.ucExcitMode'])
    _ret["Contrasts"] = _convertString(_asc['lContrasts'])
    for _contrast in range(_ret["Contrasts"]):
        _help1 = 'alTE[' + str(_contrast) + ']'
        _help2 = 'TE' + str(_contrast + 1)
        _ret[_help2] = 0.001 * _convertString(_asc[_help1])
    _ret["TR"] = 0.001 * _convertString(_asc['alTR[0]'])

    _ret["NoBvalues"] = _convertString(_asc['sDiffusion.lDiffWeightings'])
    _ret["NoBdirections"] = _convertString(_asc['sDiffusion.lDiffDirections'])

    # b0 do not appear in sDiffusion.alBValue, therefore manually create entry
    for _bval in range(_ret["NoBvalues"]):
        _help0 = 'sDiffusion.alBValue[' + str(_bval) + ']'
        if _help0 in _asc:
            _help1 = 'sDiffusion.alBValue[' + str(_bval) + ']'
            _help2 = 'Bval' + str(_bval + 1)
            _ret[_help2] = _convertString(_asc[_help1])
        else:
            _help2 = 'Bval' + str(_bval + 1)
            _ret[_help2] = '0'

    for _bval in range(_ret["NoBvalues"]):
        _help1 = 'sDiffusion.alAverages[' + str(_bval) + ']'
        _help2 = 'BvalAvg' + str(_bval + 1)
        _ret[_help2] = _convertString(_asc[_help1])

    _ret["DiffusionScheme"] = _convertString(_asc['sDiffusion.dsScheme'])
    _ret["BaseResolution"] = _convertString(_asc['sKSpace.lBaseResolution'])
    _ret["PartialFourier"] = _convertString(_asc['sKSpace.ucPhasePartialFourier'])
    _ret["Sequence"] = _convertString(_asc['tSequenceFileName'])
    _ret["ProtocolName"] = _convertString(_asc['tProtocolName'])
    # _ret["Contrasts"]           = _convertString(_asc['lContrasts'])
    _ret["PAT"] = _convertString(_asc['sPat.lAccelFactPE'])
    _ret["RefScan"] = _convertString(_asc['sPat.ucRefScanMode'])
    _ret["Inversion"] = _convertString(_asc['sPrepPulses.ucInversion'])
    if 'sPrepPulses.lFatWaterContrast' in _asc:
        _ret["FatSat"] = _convertString(_asc['sPrepPulses.lFatWaterContrast'])
    elif 'sPrepPulses.ucFatSat' in _asc:
        _ret["FatSat"] = _convertString(_asc['sPrepPulses.ucFatSat'])
    else:
        raise ValueError
    _ret["FatSatMode"] = _convertString(_asc['sPrepPulses.ucFatSatMode'])
    _ret["DwellTime"] = _convertString(_asc['sRXSPEC.alDwellTime[0]'])
    _ret["PhaseResolution"] = _convertString(_asc['sKSpace.dPhaseResolution'])
    if 'sKSpace.dPhaseOversamplingForDialog' in _asc:
        _ret["PhaseOverSampling"] = float(_asc['sKSpace.dPhaseOversamplingForDialog'])
    else:
        _ret["PhaseOverSampling"] = 0.

    _ret["SliceThickness"] = _convertString(_asc['sSliceArray.asSlice[0].dThickness'])
    _ret["PhaseFoV"] = _convertString(_asc['sSliceArray.asSlice[0].dPhaseFOV'])
    _ret["ReadoutFoV"] = _convertString(_asc['sSliceArray.asSlice[0].dReadoutFOV'])

    _ret["PhaseEncodingLines"] = _convertString(_asc['sKSpace.lPhaseEncodingLines'])
    _ret["slices"] = _convertString(_asc['sSliceArray.lSize'])

    return _ret


def getBodyPartExamined(byteBuffer):
    _temp = b'<ParamString."tBodyPartExamined">'
    _begin = byteBuffer.rfind(_temp)
    _begin = byteBuffer.find(b'{', _begin)
    if _begin < 0:
        raise ValueError
    _end = byteBuffer.find(b'}', _begin)
    if _begin > _end:
        raise ValueError
    _line = str(byteBuffer[_begin + 1: _end], 'utf-8').replace(" ", "")
    return _line


def getAge(byteBuffer):
    _temp = b'<ParamDouble."flPatientAge">'
    _begin = byteBuffer.rfind(_temp)
    _begin = byteBuffer.find(b'{', _begin)
    if _begin < 0:
        raise ValueError
    _end = byteBuffer.find(b'}', _begin)
    if _begin > _end:
        raise ValueError
    _line = str(byteBuffer[_begin + 1: _end], 'utf-8').replace(" ", "")
    _real_age = _convertString(_line.split()[-1])
    _age = 1
    if _real_age <= 1:
        _age = 1
    elif _real_age <= 5:
        _age = 5
    elif _real_age <= 12:
        _age = 12
    elif _real_age <= 18:
        _age = 18
    elif _real_age <= 45:
        _age = 45
    elif _real_age <= 65:
        _age = 65
    elif _real_age <= 89:
        _age = 89
    else:
        _age = 90
    return _age


def getHeight(byteBuffer):
    _temp = b'<ParamDouble."flPatientHeight">'
    _begin = byteBuffer.rfind(_temp)
    _begin = byteBuffer.find(b'{', _begin)
    if _begin < 0:
        raise ValueError
    _end = byteBuffer.find(b'}', _begin)
    if _begin > _end:
        raise ValueError
    _line = str(byteBuffer[_begin + 1: _end], 'utf-8').replace(" ", "")
    _real_height = _convertString(_line.split()[-1])
    _height = 600
    if _real_height <= 600:
        _height = 600
    elif _real_height <= 1000:
        _height = 800
    elif _real_height <= 1500:
        _height = 1250
    elif _real_height <= 1700:
        _height = 1650
    elif _real_height <= 1800:
        _height = 1750
    elif _real_height <= 1900:
        _height = 1850
    elif _real_height <= 2000:
        _height = 1950
    else:
        _height = 2050
    return _height * 0.1


def getWeight(byteBuffer):
    _temp = b'<ParamDouble."flUsedPatientWeight">'
    _begin = byteBuffer.rfind(_temp)
    _begin = byteBuffer.find(b'{', _begin)
    if _begin < 0:
        raise ValueError
    _end = byteBuffer.find(b'}', _begin)
    if _begin > _end:
        raise ValueError
    _line = str(byteBuffer[_begin + 1: _end], 'utf-8').replace(" ", "")
    _real_weight = _convertString(_line.split()[-1])
    _weight = 10
    if _real_weight <= 20:
        _weight = 10
    elif _real_weight <= 40:
        _weight = 30
    elif _real_weight <= 60:
        _weight = 50
    elif _real_weight <= 80:
        _weight = 70
    elif _real_weight <= 100:
        _weight = 90
    elif _real_weight <= 140:
        _weight = 120
    else:
        _weight = 150
    return _weight


def getParameters(_strFile):
    _byteBuffer = readHeader(_strFile)
    _paras = getAscParameters(_strFile, _byteBuffer)
    _paras["BodyPartExamined"] = getBodyPartExamined(_byteBuffer)
    _paras["Age"] = getAge(_byteBuffer)
    _paras["Height"] = getHeight(_byteBuffer)
    _paras["Weight"] = getWeight(_byteBuffer)
    return _paras


def worker():
    # _strFile = 'J:\\Benkert\\DL-EPI\\_debug\\_files.txt'
    # _strFile = 'E:\\_epi_processing_brain\\_files.txt'
    _strFile = r'\\mr-fst27-02.wurmloch.siemens.de\MR-T27-01\Jinho\MoCo\20220125_UKER_Liver\_files.txt'
    # _strFile = 'J:\\Benkert\\DL-EPI\\_evaluation_customer_DL_EPI\\20210927_MGH\\_files.txt'
    # _strFile = 'J:\\Benkert\\EPI_motion\\20211019_3T_Lumina_epi_liver\\_files.txt'
    _omitted = []
    for _line in open(_strFile, "r"):
        print(_line)
        _rootfolder = os.path.dirname(_line)
        _basename = os.path.basename(_line).rsplit('.', 1)[0]
        _targetfolder = _rootfolder + "\\" + _basename

        if not os.path.exists(_rootfolder):
            _omitted.append(_line)
            print(_rootfolder)
        else:
            print('processing file', _targetfolder + ".dat")
            _paras = getParameters(_targetfolder + ".dat")
            # _targetfile = _rootfolder + "\\ProtocolInfo.json"
            _targetfile = _rootfolder + "\\" + _basename + "_ProtocolInfo.json"
            with open(_targetfile, 'w') as fp:
                json.dump(_paras, fp)

    if (len(_omitted) > 0):
        print('the following files were omitted:', _omitted)

    # _strFile = 'E:\\_epi_processing_brain\\meas_MID00018_FID03132_ep2d_diff_4trace_p2_EPIref_AP\\meas_MID00018_FID03132_ep2d_diff_4trace_p2_EPIref_AP.dat'
    # _strFile = "D:\\UtfRoot\\20200309_VA20A_SR\\meas_MID00812_FID00750_t2_qtse_tra_p3.dat"
    # _paras = getParameters(_strFile)
    # print(_paras)


def readHeader(_strFile):
    class MultRaidHeader(Structure):
        _fields_ = [('superID', c_uint32), ('nFiles', c_uint32)]

    class SingleRaidHeader(Structure):
        _fields_ = [
            ("measID", c_uint32),
            ("fileID", c_uint32),
            ("fileOff", c_uint32),
            ("fileLength", c_uint32),
            ("dummy", c_uint32),
            ("dummy2", c_uint32),
            ("cPatientName", c_char * 64),
            ("cProtocolName", c_char * 64)]

    class SingleRaidHeaderSize(Structure):
        _fields_ = [("headerSize", c_uint32)]

    _bVerbose = False

    _file = open(_strFile, "rb")

    _header1 = MultRaidHeader()
    _file.readinto(_header1)
    if _bVerbose:
        print('superID', _header1.superID, 'nFiles', _header1.nFiles)
    if (_header1.superID < 0) or (_header1.superID >= 32):
        print("not recognized as TWIX file", _strFile)
        return
    if (_header1.nFiles < 0) or (_header1.nFiles >= 64):
        print("not recognized as TWIX file 2", _strFile)
        return

    _header2 = SingleRaidHeader()
    for _i in range(_header1.nFiles):
        _file.readinto(_header2)
        if _bVerbose:
            print("found MID", _header2.measID, "with protocol", str(_header2.cProtocolName))
    if _bVerbose:
        print('take header of', _header2.cProtocolName, ', offset', _header2.fileOff)

    _file.seek(_header2.fileOff, 0)
    _header3 = SingleRaidHeaderSize()
    _file.readinto(_header3)
    if _bVerbose:
        print('header has size', _header3.headerSize)

    _ret = _file.read(_header3.headerSize)

    _file.close()
    return _ret


if __name__ == "__main__":

    if False:
        # _strDebug = 'D:\\UtfRoot\\20200313_Anonymize\\meas_MID00067_FID06883_t2_haste_tra_p2_mbh_384_NO_ANO.dat'
        _strDebug = '\\mr-fst27-02.wurmloch.siemens.de\MR-T27-01\Jinho\MoCo\Leber FB\meas_MID02337_FID201333_dwepi_SPAIR_b50_800d_p2.dat'
        _ret = getParameters(_strDebug)
        print(_ret)
    else:
        worker()
