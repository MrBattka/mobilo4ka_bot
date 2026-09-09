from aiogram.utils.markdown import hlink


def baseFix(name):
    if ('Пломба' not in name and 'Обменка' not in name and '"A' not in name and '"B' not in name and '"А-"' not in name
        and '"C' not in name and '"А' not in name and '"В' not in name and '"А-"' not in name 
        and '"С' not in name and '""' not in name and '"обменка' not in name and 'Демо' not in name):
        return name

def getApple(a):
    def fixName(name):
        replaceMacbook = name.replace("MacBook ", "")
        replaceApple = replaceMacbook.replace("Apple ", "")
        replaceWatch = replaceApple.replace("Watch ", "")
        fixUSB = replaceWatch.replace("🇺🇸B-C", 'USB-C - ')
        fixMUHN = fixUSB.replace("MU🇮🇳", 'MUHN')
        return fixMUHN.replace("iPhone ", "")
    isApple = False
    isDemo = False
    isAppleiPhone = False
    isiPhone11 = False
    isiPhone12 = False
    isiPhone13 = False
    isiPhone14 = False
    isiPhone15 = False
    isiPhone15Pro = False
    isiPhone15ProMax = False
    isiPhone16 = False
    isiPhone16Pro = False
    isiPhone16ProMax = False
    isiPhone17Air = False
    isiPhone17 = False
    isiPhone17Pro = False
    isiPhone17ProMax = False
    
    isAirPods2 = False
    isAirPodsPro2 = False
    isAirPods3 = False
    isAirPods4 = False
    isAirPodsPro3 = False
    isAirPodsMAX = False
    
    isAppleWatchSE2023 = False
    isAppleWatchSE2024 = False
    isAppleWatchSE2025 = False
    isAppleWatchS8 = False
    isAppleWatchS9 = False
    isAppleWatchS10 = False
    isAppleWatchS11 = False
    isAppleWatchUltra = False
    
    isAppleiPad = False
    isAppleMacbook = False
    isAppleiMac = False
    #################
    res = []
    for i in a:
        if ('Apple Magic' in i or 'Apple Battery' in i or 'Apple TV' in i or 'Apple HomePod' in i or 'Apple AirTag' in i or 'Apple Pencil' in i) and baseFix(i):
            isApple = True
    res.append("📲 *Apple*")
    for i in a:
        if ('Apple Magic' in i or 'Apple Battery' in i or 'Apple TV' in i or 'Apple HomePod' in i or 'Apple AirTag' in i or 'Apple Pencil' in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################
    for i in a:
        if "AirPods 2" in i and baseFix(i):
            isAirPods2 = True
    if isAirPods2 is True and isApple is True:
        res.append("")
    for i in a:
        if "AirPods 2" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            #######################
    for i in a:
        if "AirPods Pro 2" in i and baseFix(i):
            isAirPodsPro2 = True
    if isAirPodsPro2 is True:
        res.append("")
    for i in a:
        if "AirPods Pro 2" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            #######################
    for i in a:
        if "AirPods 3" in i and baseFix(i):
            isAirPods3 = True
    if isAirPods3 is True:
        res.append("")
    for i in a:
        if "AirPods 3" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            #######################
    for i in a:
        if "AirPods Pro 3" in i and baseFix(i):
            isAirPodsPro3 = True
    if isAirPodsPro3 is True:
        res.append("")
    for i in a:
        if "AirPods Pro 3" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            #######################
    for i in a:
        if "AirPods 4" in i and baseFix(i):
            isAirPods4 = True
    if isAirPods4 is True:
        res.append("")
    for i in a:
        if "AirPods 4" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
                        #######################
    for i in a:
        if "AirPods Max" in i and baseFix(i):
            isAirPodsMAX = True
    if isAirPodsMAX is True:
        res.append("")
    for i in a:
        if "AirPods Max" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))          

    #######################
    for i in a:
        if "iPhone" in i and baseFix(i):
            isAppleiPhone = True
    if isAppleiPhone is True:
        res.append("")
        res.append("📲 *Apple iPhone*")
            
     #######################
    for i in a:
        if "iPhone 11" in i and baseFix(i):
            isiPhone11 = True
    if isiPhone11 is True:
        res.append("")
    for i in a:
        if "iPhone 11" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "iPhone 12" in i and baseFix(i):
            isiPhone12 = True
    if isiPhone12 is True and isiPhone11 is True:
        res.append("")
    for i in a:
        if "iPhone 12" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "iPhone 13" in i and baseFix(i):
            isiPhone13 = True
    if isiPhone13 is True and (isiPhone12 is True or isiPhone11 is True):
        res.append("")
    for i in a:
        if "iPhone 13" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "iPhone 14" in i and baseFix(i):
            isiPhone14 = True
    if isiPhone14 is True and (isiPhone13 is True or isiPhone12 is True or isiPhone11 is True):
        res.append("")
    for i in a:
        if "iPhone 14" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "iPhone 15" in i and "iPhone 15 Pro" not in i and baseFix(i):
            isiPhone15 = True
    if isiPhone15 is True and (isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True):
        res.append("")
    for i in a:
        if "iPhone 15" in i and "iPhone 15 Pro" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################
    for i in a:
        if "iPhone 15 Pro" in i and "iPhone 15 Pro Max" not in i and baseFix(i):
            isiPhone15Pro = True
    if (isiPhone15Pro is True and (isiPhone15 is True or isiPhone14 is True or isiPhone13 is True or 
        isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 15 Pro" in i and "iPhone 15 Pro Max" not in i and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################
    for i in a:
        if "iPhone 15 Pro Max" in i and baseFix(i):
            isiPhone15ProMax = True
    if (isiPhone15ProMax is True and (isiPhone15Pro is True or isiPhone15 is True or isiPhone14 is True or 
        isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 15 Pro Max" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
     #######################
    for i in a:
        if "iPhone 16" in i and "iPhone 16 Pro" not in i and "Обменка" not in i and "обменка" not in i and "Демо" not in i and baseFix(i):
            isiPhone16 = True
    if (isiPhone16 is True and (isiPhone15ProMax is True or isiPhone15Pro is True or isiPhone15 is True or 
        isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 16" in i and "iPhone 16 Pro" not in i and "Обменка" not in i and "обменка" not in i and "Демо" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "iPhone 16 Pro" in i and "iPhone 16 Pro Max" not in i and baseFix(i):
            isiPhone16Pro = True
    if (isiPhone16Pro is True and (isiPhone16 is True or isiPhone15ProMax is True or isiPhone15Pro is True or isiPhone15 is True or 
        isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 16 Pro" in i and "iPhone 16 Pro Max" not in i and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################
    for i in a:
        if "iPhone 16 Pro Max" in i and baseFix(i):
            isiPhone16ProMax = True
    if (isiPhone16ProMax is True and (isiPhone16Pro is True or isiPhone16 is True or isiPhone15ProMax is True or isiPhone15Pro is True 
        or isiPhone15 is True or isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 16 Pro Max" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))   
             #######################
    for i in a:
        if "iPhone Air" in i and "iPhone 17 Pro" not in i and baseFix(i):
            isiPhone17Air = True
    if (isiPhone17Air is True and (isiPhone16ProMax is True or isiPhone16Pro is True or isiPhone16 is True or 
                                isiPhone15ProMax is True or isiPhone15Pro is True or isiPhone15 is True or 
        isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone Air" in i and "iPhone 17 Pro" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            #######################
    for i in a:
        if "iPhone 17" in i and "iPhone 17 Pro" not in i and baseFix(i):
            isiPhone17 = True
    if (isiPhone17 is True and (isiPhone17Air is True or isiPhone16ProMax is True or isiPhone16Pro is True or isiPhone16 is True or 
                                isiPhone15ProMax is True or isiPhone15Pro is True or isiPhone15 is True or 
        isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 17" in i and "iPhone 17 Pro" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "iPhone 17 Pro" in i and "iPhone 17 Pro Max" not in i and baseFix(i):
            isiPhone17Pro = True
    if (isiPhone17Pro is True and (isiPhone17 is True or isiPhone17Air is True or isiPhone16ProMax is True or isiPhone16Pro is True or
                                   isiPhone16 is True or isiPhone15ProMax is True or isiPhone15Pro is True or isiPhone15 is True or 
        isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 17 Pro" in i and "iPhone 17 Pro Max" not in i and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################
    for i in a:
        if "iPhone 17 Pro Max" in i and baseFix(i):
            isiPhone17ProMax = True
    if (isiPhone17ProMax is True and (isiPhone17Pro is True or isiPhone17 is True or isiPhone17Air is True or isiPhone16ProMax is True or isiPhone16Pro is True or
                                      isiPhone16 is True  or isiPhone15ProMax is True or isiPhone15Pro is True or
        isiPhone15 is True or isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True)):
        res.append("")
    for i in a:
        if "iPhone 17 Pro Max" in i and baseFix(i):
            res.append(fixName("`" + i + "`")) 
            
            
    #######################
    for i in a:
        if ("SE 2023 Gen" in i or "Watch SE 2023" in i) and baseFix(i):
            isAppleWatchSE2023 = True   
    if isAppleWatchSE2023 is True:
        res.append("")
        res.append("⌚️ *Apple Watch SE 2023*")
    for i in a:
        if ("SE 2023 Gen" in i or "Watch SE 2023" in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if ("SE 2024 Gen" in i or "Watch SE 2024" in i or "Watch SE (2024)" in i or "Watch SE2" in i) and baseFix(i):
            isAppleWatchSE2024 = True   
    if isAppleWatchSE2024 is True:
        res.append("")
        res.append("⌚️ *Apple Watch SE 2024*")
    for i in a:
        if ("SE 2024 Gen" in i or "Watch SE 2024" in i or "Watch SE (2024)" in i or "Watch SE2" in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################    
    for i in a:
        if "SE3" in i and baseFix(i):
            isAppleWatchSE2025 = True   
    if isAppleWatchSE2025 is True:
        res.append("")
        res.append("⌚️ *Apple Watch SE 2025*")
    for i in a:
        if "SE3" in i  and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if ("Apple Watch S8" in i) and baseFix(i):
            isAppleWatchS8 = True   
    if isAppleWatchS8 is True:
        res.append("")
        res.append("⌚️ *Apple Watch S8*")
    for i in a:
        if ("Apple Watch S8" in i) and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################    
    for i in a:
        if ("Apple Watch S9" in i) and baseFix(i):
            isAppleWatchS9 = True   
    if isAppleWatchS9 is True:
        res.append("")
        res.append("⌚️ *Apple Watch S9*")
    for i in a:
        if ("Apple Watch S9" in i) and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################    
    for i in a:
        if ("Apple Watch S10" in i) and baseFix(i):
            isAppleWatchS10 = True   
    if isAppleWatchS10 is True:
        res.append("")
        res.append("⌚️ *Apple Watch S10*")
    for i in a:
        if ("Apple Watch S10" in i) and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################    
    for i in a:
        if ("Apple Watch S11" in i) and baseFix(i):
            isAppleWatchS11 = True   
    if isAppleWatchS11 is True:
        res.append("")
        res.append("⌚️ *Apple Watch S11*")
    for i in a:
        if ("Apple Watch S11" in i) and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################    
    for i in a:
        if ("Apple Watch Ultra" in i) and baseFix(i):
            isAppleWatchUltra = True   
    if isAppleWatchUltra is True:
        res.append("")
        res.append("⌚️ *Apple Watch Ultra*")
    for i in a:
        if ("Apple Watch Ultra" in i) and baseFix(i):
            res.append(fixName("`" + i + "`")) 
    #######################    
    for i in a:
        if ("iPad" in i and "Magic" not in i) and baseFix(i):
            isAppleiPad = True   
    if isAppleiPad is True:
        res.append("")
        res.append("📟 *Apple iPad*")
    for i in a:
        if ("iPad" in i and "Magic" not in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################    
    for i in a:
        if ("MacBook" in i) and baseFix(i):
            isAppleMacbook = True   
    if isAppleMacbook is True:
        res.append("")
        res.append("💻 *Apple MacBook*")
    for i in a:
        if ("MacBook" in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################    
    for i in a:
        if ("iMac" in i) and baseFix(i):
            isAppleiMac = True   
    if isAppleiMac is True:
        res.append("")
        res.append("💻 *Apple iMac*")
    for i in a:
        if ("iMac" in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if ("Обменка" in i or "обменка" in i or "Демо" in i):
            isDemo = True
    if isDemo is True:
        res.append('')
        res.append('──── ୨୧ ────')
        res.append('')
        res.append("🔥 *Обменки / Демо*")
    for i in a:
        if ("Обменка" in i or "обменка" in i or "Демо" in i):
            res.append(fixName("`" + i + "`"))
    
    return '\n'.join([str(i) for i in res])

def getSamsung(a): 
    def fixName(name):
        return name.replace("Samsung Galaxy", '')
    
    isGalaxyPhone = False
    
    isGalaxyA05 = False
    isGalaxyA06 = False
    isGalaxyA07 = False
    isGalaxyA15 = False
    isGalaxyA16 = False
    isGalaxyA17 = False
    isGalaxyA25 = False
    isGalaxyA26 = False
    isGalaxyA27 = False
    isGalaxyA35 = False
    isGalaxyA36 = False
    isGalaxyA37 = False
    isGalaxyA53 = False
    isGalaxyA55 = False
    isGalaxyA56 = False
    isGalaxyA57 = False
    isGalaxyS22 = False
    isGalaxyS23 = False
    isGalaxyS23Plus = False
    isGalaxyS23FE = False
    isGalaxyS23Ultra = False
    isGalaxyS24 = False
    isGalaxyS24Plus = False
    isGalaxyS24FE = False
    isGalaxyS24Ultra = False
    isGalaxyS25 = False
    isGalaxyS25Plus = False
    isGalaxyS25FE = False
    isGalaxyS25Ultra = False
    isGalaxyS26 = False
    isGalaxyS26Plus = False
    isGalaxyS26FE = False
    isGalaxyS26Ultra = False
    isGalaxyZFlip5 = False
    isGalaxyZFlip6 = False
    isGalaxyZFold5 = False
    isGalaxyZFold6 = False
    isGalaxyZFold7 = False
    isGalaxyZFold8 = False
    
    
    isGalaxyTab = False
    
    isGalaxyWatch = False
    
    isGalaxyBuds = False
    #################
    res = []
    
    for i in a:
        if "Galaxy Watch" in i and baseFix(i):
            isGalaxyWatch = True
    if isGalaxyWatch is True:
        res.append('')
        res.append("⌚️ *Galaxy Watch*")
    for i in a:
        if ('Galaxy Watch' in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################

    for i in a:
        if "Galaxy Buds" in i and baseFix(i):
            isGalaxyBuds = True
    if isGalaxyBuds is True:
        res.append('')
        res.append("🎧 *Galaxy Buds*")
    for i in a:
        if ('Galaxy Buds' in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    
    for i in a:
        if "Samsung Galaxy" in i and 'Galaxy Tab' not in i and baseFix(i):
            isGalaxyPhone = True
    if isGalaxyPhone is True and (isGalaxyBuds is True or isGalaxyWatch is True):
        res.append("")
    if isGalaxyPhone is True:
        res.append("📲 *Galaxy Phone*")
    #######################
    for i in a:
        if "Samsung Galaxy A05" in i and baseFix(i):
            isGalaxyA05 = True
    if isGalaxyA05 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy A05" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################
    for i in a:
        if "Samsung Galaxy A06" in i and baseFix(i):
            isGalaxyA06 = True
    if isGalaxyA06 is True and isGalaxyA05 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy A06" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A07" in i and baseFix(i):
            isGalaxyA07 = True
    if isGalaxyA07 is True and isGalaxyA05 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy A07" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A15" in i and baseFix(i):
            isGalaxyA15 = True
    if isGalaxyA15 is True and (isGalaxyA07 is True or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A15" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A16" in i and baseFix(i):
            isGalaxyA16 = True
    if isGalaxyA16 is True and (isGalaxyA15 is True or isGalaxyA07 is True or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A16" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A17" in i and baseFix(i):
            isGalaxyA17 = True
    if isGalaxyA17 is True and (isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA07 is True or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A17" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A25" in i and baseFix(i):
            isGalaxyA25 = True
    if isGalaxyA25 is True and (isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA07 is True or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A25" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    
    for i in a:
        if "Samsung Galaxy A26" in i and baseFix(i):
            isGalaxyA26 = True
    if isGalaxyA26 is True and (isGalaxyA25 is True or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA07 is True or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A26" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A27" in i and baseFix(i):
            isGalaxyA27 = True
    if isGalaxyA27 is True and (isGalaxyA26 is True or isGalaxyA25 is True or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA07 is True 
                                or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A27" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    
    for i in a:
        if "Samsung Galaxy A35" in i and baseFix(i):
            isGalaxyA35 = True
    if (isGalaxyA35 is True and (isGalaxyA27 is True or isGalaxyA26 is True or isGalaxyA25 is True or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA07 is True 
                                 or isGalaxyA06 is True or isGalaxyA05 is True)):
        res.append("")
    for i in a:
        if "Samsung Galaxy A35" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    
    for i in a:
        if "Samsung Galaxy A36" in i and baseFix(i):
            isGalaxyA36 = True
    if isGalaxyA36 is True and (isGalaxyA27 is True or isGalaxyA26 is True or isGalaxyA35 is True or isGalaxyA25 is True or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True 
                                or isGalaxyA07 is True or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A36" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    
    for i in a:
        if "Samsung Galaxy A37" in i and baseFix(i):
            isGalaxyA37 = True
    if isGalaxyA37 is True and (isGalaxyA27 is True or isGalaxyA26 is True or isGalaxyA36 is True or isGalaxyA35 is True or isGalaxyA25 is True or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True 
                                or isGalaxyA06 is True or isGalaxyA05 is True):
        res.append("")
    for i in a:
        if "Samsung Galaxy A37" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    
    for i in a:
        if "Samsung Galaxy A53" in i and baseFix(i):
            isGalaxyA53 = True
    if (isGalaxyA53 is True and (isGalaxyA36 is True or isGalaxyA27 is True or isGalaxyA35 is True or isGalaxyA26 is True or isGalaxyA25 is True or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True  
                                                     or isGalaxyA05 is True or isGalaxyA06 is True)):
        res.append("")
    for i in a:
        if "Samsung Galaxy A53" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy A55" in i and baseFix(i):
            isGalaxyA55 = True
    if (isGalaxyA55 is True and (isGalaxyA53 is True or isGalaxyA27 is True or isGalaxyA36 is True or isGalaxyA26 is True or isGalaxyA35 is True or isGalaxyA25 is True 
                                or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA05 is True or isGalaxyA06 is True)):
        res.append("")
    for i in a:
        if "Samsung Galaxy A55" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            #######################
    for i in a:
        if "Samsung Galaxy A56" in i and baseFix(i):
            isGalaxyA56 = True
    if (isGalaxyA56 is True and (isGalaxyA55 is True or isGalaxyA27 is True or isGalaxyA53 is True or isGalaxyA36 is True or isGalaxyA26 is True or isGalaxyA35 is True or isGalaxyA25 is True 
                                or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA05 is True or isGalaxyA06 is True)):
        res.append("")
    for i in a:
        if "Samsung Galaxy A56" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
                    #######################
    for i in a:
        if "Samsung Galaxy A57" in i and baseFix(i):
            isGalaxyA57 = True
    if (isGalaxyA57 is True and (isGalaxyA56 is True or isGalaxyA27 is True or isGalaxyA55 is True or isGalaxyA53 is True or isGalaxyA36 is True or isGalaxyA26 is True or isGalaxyA35 is True or isGalaxyA25 is True 
                                or isGalaxyA17 is True or isGalaxyA16 is True or isGalaxyA15 is True or isGalaxyA05 is True or isGalaxyA06 is True)):
        res.append("")
    for i in a:
        if "Samsung Galaxy A57" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################
    for i in a:
        if "Samsung Galaxy S22" in i and baseFix(i):
            isGalaxyS22 = True
    if isGalaxyS22 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S22" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S23" in i and "Samsung Galaxy S23 Ultra" not in i and "Samsung Galaxy S23 FE" not in i and "Samsung Galaxy S23+" not in i and baseFix(i):
            isGalaxyS23 = True
    if isGalaxyS23 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S23" in i and "Samsung Galaxy S23 Ultra" not in i and "Samsung Galaxy S23 FE" not in i and "Samsung Galaxy S23+" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S23+" in i and baseFix(i):
            isGalaxyS23Plus = True
    if isGalaxyS23Plus is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S23+" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S23 FE" in i and baseFix(i):
            isGalaxyS23FE = True
    if isGalaxyS23FE is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S23 FE" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
   #######################
    for i in a:
        if "Samsung Galaxy S23 Ultra" in i and baseFix(i):
            isGalaxyS23Ultra = True
    if isGalaxyS23Ultra is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S23 Ultra" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S24" in i and "Samsung Galaxy S24 Ultra" not in i and "Samsung Galaxy S24 FE" not in i and "Samsung Galaxy S24+" not in i and baseFix(i):
            isGalaxyS24 = True
    if isGalaxyS24 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S24" in i and "Samsung Galaxy S24 Ultra" not in i and "Samsung Galaxy S24 FE" not in i and "Samsung Galaxy S24+" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S24 FE" in i and baseFix(i):
            isGalaxyS24FE = True
    if isGalaxyS24FE is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S24 FE" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S24+" in i and baseFix(i):
            isGalaxyS24Plus = True
    if isGalaxyS24Plus is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S24+" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S24 Ultra" in i and baseFix(i):
            isGalaxyS24Ultra = True
    if isGalaxyS24Ultra is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S24 Ultra" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S25" in i and "Samsung Galaxy S25 Ultra" not in i and "Samsung Galaxy S25 FE" not in i and "Samsung Galaxy S25+" not in i and baseFix(i):
            isGalaxyS25 = True
    if isGalaxyS25 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S25" in i and "Samsung Galaxy S25 Ultra" not in i and "Samsung Galaxy S25 FE" not in i and "Samsung Galaxy S25+" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S25 FE" in i and baseFix(i):
            isGalaxyS25FE = True
    if isGalaxyS25FE is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S25 FE" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S25+" in i and baseFix(i):
            isGalaxyS25Plus = True
    if isGalaxyS25Plus is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S25+" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S25 Ultra" in i and baseFix(i):
            isGalaxyS25Ultra = True
    if isGalaxyS25Ultra is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S25 Ultra" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
            
    for i in a:
        if "Samsung Galaxy S26" in i and "Samsung Galaxy S26 Ultra" not in i and "Samsung Galaxy S25 FE" not in i and "Samsung Galaxy S25+" not in i and baseFix(i):
            isGalaxyS26 = True
    if isGalaxyS26 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S26" in i and "Samsung Galaxy S26 Ultra" not in i and "Samsung Galaxy S25 FE" not in i and "Samsung Galaxy S25+" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S26 FE" in i and baseFix(i):
            isGalaxyS26FE = True
    if isGalaxyS26FE is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S26 FE" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S26+" in i and baseFix(i):
            isGalaxyS26Plus = True
    if isGalaxyS26Plus is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S26+" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy S26 Ultra" in i and baseFix(i):
            isGalaxyS26Ultra = True
    if isGalaxyS26Ultra is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy S26 Ultra" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))\
                
    for i in a:
        if "Samsung Galaxy Z Flip 5" in i and baseFix(i):
            isGalaxyZFlip5 = True
    if isGalaxyZFlip5 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy Z Flip 5" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy Z Flip 6" in i and baseFix(i):
            isGalaxyZFlip6 = True
    if isGalaxyZFlip6 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy Z Flip 6" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy Z Fold 5" in i and baseFix(i):
            isGalaxyZFold5 = True
    if isGalaxyZFold5 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy Z Fold 5" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy Z Fold 6" in i and baseFix(i):
            isGalaxyZFold6 = True
    if isGalaxyZFold6 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy Z Fold 6" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy Z Fold 7" in i and baseFix(i):
            isGalaxyZFold7 = True
    if isGalaxyZFold7 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy Z Fold 7" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Samsung Galaxy Z Fold 8" in i and baseFix(i):
            isGalaxyZFold8 = True
    if isGalaxyZFold8 is True:
        res.append("")
    for i in a:
        if "Samsung Galaxy Z Fold 8" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################
    for i in a:
        if "Galaxy Tab" in i and baseFix(i):
            isGalaxyTab = True
    if isGalaxyTab is True:
        res.append('')
        res.append("📟 *Galaxy Tab*")
    for i in a:
        if ('Galaxy Tab' in i) and baseFix(i):
            res.append(i)
    
    return '\n'.join([str(i) for i in res])

def getCoros(a):
    def fixName(name):
        replaceAsus = name.replace("Asus ", '')
        replaceCoros = replaceAsus.replace("Coros ", '')
        replaceSony = replaceCoros.replace("Sony ", '')
        replaceOnePlus = replaceSony.replace("OnePlus ", '')
        replaceZTE = replaceOnePlus.replace("ZTE ", '')
        return replaceZTE.replace("Dyson ", '')
    
    isHuawei = False
    isCoros = False
    isGoogle = False
    isPS = False
    isGoPro = False
    isFinis = False
    isAsus = False
    isNothing = False
    isOnePlus = False
    isZTE = False
    isDyson = False
    isSony = False
    isMotorola = False
    #################
    res = []
    for i in a:
        if "Huawei" in i and baseFix(i):
            isHuawei = True
    if isHuawei is True:
        res.append("📲 *Huawei*")
    for i in a:
        if "Huawei" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if ('Coros' in i or 'COROS' in i) and baseFix(i):
            isCoros = True
    if isCoros is True:
        res.append('')
        res.append("📲 *Coros*")
    for i in a:
        if ('Coros' in i or 'COROS' in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Google" in i and baseFix(i):
            isGoogle = True
    if isGoogle is True:
        res.append('')
        res.append("📲 *Google*")
    for i in a:
        if 'Google' in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if ("PlayStation" in i or "DualSense" in i or "Xbox" in i or "Nintendo" in i) and baseFix(i):
            isPS = True
    if isPS is True:
        res.append('')
        res.append("🎮 *Playstation / Xbox / Nintendo* 🎮")
    for i in a:
        if ("PlayStation" in i or "DualSense" in i or "Xbox" in i or "Nintendo" in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if ("GoPro" in i or "Protective" in i or "El Grande" in i or '3-Way' in i) and baseFix(i):
            isGoPro = True
    if isGoPro is True:
        res.append('')
        res.append("📹 *GoPro*")
    for i in a:
        if ("GoPro" in i or "Protective" in i or "El Grande" in i or '3-Way' in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Finis" in i and baseFix(i):
            isFinis = True
    if isFinis is True:
        res.append('')
        res.append("📲 *Finis*")
    for i in a:
        if "Finis" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Asus" in i and baseFix(i):
            isAsus = True
    if isAsus is True:
        res.append('')
        res.append("📲 *Asus*")
    for i in a:
        if "Asus" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Nothing" in i and baseFix(i):
            isNothing = True
    if isNothing is True:
        res.append('')
        res.append("📲 *Nothing Phone*")
    for i in a:
        if "Nothing" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "OnePlus" in i and baseFix(i):
            isOnePlus = True
    if isOnePlus is True:
        res.append('')
        res.append("📲 *OnePlus*")
    for i in a:
        if "OnePlus" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "ZTE" in i and baseFix(i):
            isZTE = True
    if isZTE is True:
        res.append('')
        res.append("📲 **ZTE**")
    for i in a:
        if "ZTE" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Dyson" in i and baseFix(i):
            isDyson = True
    if isDyson is True:
        res.append('')
        res.append("📲 *Dyson*")
    for i in a:
        if "Dyson" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Xperia" in i and baseFix(i):
            isSony = True
    if isSony is True:
        res.append('')
        res.append("📲 *Sony*")
    for i in a:
        if "Xperia" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################
    for i in a:
        if "Motorola" in i and baseFix(i):
            isMotorola = True
    if isMotorola is True:
        res.append('')
        res.append("📲 *Motorola*")
    for i in a:
        if "Motorola" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    
    return '\n'.join([str(i) for i in res])

def getXiaomiYandexJBL(a):
    def fixName(name):
        fixPoco = name.replace("Pocophone", 'Poco')
        replaceRedmi = fixPoco.replace("Redmi Note", 'Note')
        fixMI = replaceRedmi.replace("Xiaomi 1", 'Mi 1')
        return fixMI.replace("Xiaomi ", '')
    
    isXiaomi = False
    isPocophone = False
    isYandex = False
    isJBL = False
    isShokz = False
    
    isMiPad = False
    isRedmiPad = False
    isPocoPad = False
    isMiTV = False
    isXiaomi12 = False
    isXiaomi13 = False
    isXiaomi14 = False
    isXiaomi15 = False
    isXiaomi17 = False
    isXiaomiRedmi12 = False
    isXiaomiRedmi13 = False
    isXiaomiRedmi14 = False
    isXiaomiRedmi15 = False
    isXiaomiRedmi17 = False
    isXiaomiNote13 = False
    isXiaomiNote13Pro4G = False
    isXiaomiNote13Pro5G = False
    isXiaomiNote13ProPlus = False
    isXiaomiNote14 = False
    isXiaomiNote14S = False
    isXiaomiNote14Pro4G = False
    isXiaomiNote14Pro5G = False
    isXiaomiNote14ProPlus = False
    isXiaomiNote15 = False
    isXiaomiNote15S = False
    isXiaomiNote15Pro4G = False
    isXiaomiNote15Pro5G = False
    isXiaomiNote15ProPlus = False
    isXiaomiNote17 = False
    isXiaomiNote17S = False
    isXiaomiNote17Pro4G = False
    isXiaomiNote17Pro5G = False
    isXiaomiNote17ProPlus = False
    isPocoC61 = False
    isPocoC65 = False
    isPocoC75 = False
    isPocoM5 = False
    isPocoM6 = False
    isPocoM8 = False
    isPocoF6 = False
    isPocoF7 = False
    isPocoF8 = False
    isPocoX5 = False
    isPocoX6 = False
    isPocoX7 = False
    #################
    res = []
    for i in a:
        if "Xiaomi" in i and baseFix(i):
            isXiaomi = True
    if isXiaomi is True:
        res.append("📲 *Xiaomi*")
    #######################
    for i in a:
        if "MI TV" in i and baseFix(i):
            isMiTV = True      
    for i in a:
        if "MI TV" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi 12" in i and baseFix(i):
            isXiaomiRedmi12 = True
    if isXiaomiRedmi12 is True:
        res.append("")
    for i in a:
        if "Redmi 12" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi 13" in i and baseFix(i):
            isXiaomiRedmi13 = True
    if isXiaomiRedmi13 is True and (isXiaomiRedmi12 is True or isMiTV is True):
        res.append("")
    for i in a:
        if "Redmi 13" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi 14" in i and baseFix(i):
            isXiaomiRedmi14 = True
    if isXiaomiRedmi14 is True and (isXiaomiRedmi13 is True or isXiaomiRedmi12 is True or isMiTV is True):
        res.append("")
    for i in a:
        if "Redmi 14" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################     
    for i in a:
        if "Redmi 15" in i and baseFix(i):
            isXiaomiRedmi15 = True
    if isXiaomiRedmi15 is True and (isXiaomiRedmi14 is True or isXiaomiRedmi13 is True or isXiaomiRedmi12 is True or isMiTV is True):
        res.append("")
    for i in a:
        if "Redmi 15" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################     
    for i in a:
        if "Redmi 17" in i and baseFix(i):
            isXiaomiRedmi17 = True
    if isXiaomiRedmi17 is True and (isXiaomiRedmi15 is True or isXiaomiRedmi14 is True or isXiaomiRedmi13 is True or isXiaomiRedmi12 is True or isMiTV is True):
        res.append("")
    for i in a:
        if "Redmi 17" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################   
    for i in a:
        if "Redmi Note 13" in i and "Redmi Note 13 Pro" not in i and baseFix(i):
            isXiaomiNote13 = True
    if isXiaomiNote13 is True and (isXiaomiRedmi14 is True or isXiaomiRedmi13 is True or isXiaomiRedmi12 is True or isMiTV is True):
        res.append("")
    for i in a:
        if "Redmi Note 13" in i and "Redmi Note 13 Pro" not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 13 Pro 4G" in i and baseFix(i):
            isXiaomiNote13Pro4G = True
    if (isXiaomiNote13Pro4G is True and (isXiaomiNote13 is True or isXiaomiRedmi14 is True or isXiaomiRedmi13 is True 
                                                                    or isXiaomiRedmi12 is True or isMiTV is True)):
        res.append("")
    for i in a:
        if "Redmi Note 13 Pro 4G" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 13 Pro 5G" in i and baseFix(i):
            isXiaomiNote13Pro5G = True
    if (isXiaomiNote13Pro5G is True and (isXiaomiNote13Pro4G is True or isXiaomiNote13 is True or isXiaomiRedmi14 is True 
                                         or isXiaomiRedmi13 is True or isXiaomiRedmi12 is True or isMiTV is True)):
        res.append("")
    for i in a:
        if "Redmi Note 13 Pro 5G" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 13 Pro Plus" in i and baseFix(i):
            isXiaomiNote13ProPlus = True
    if (isXiaomiNote13ProPlus is True and (isXiaomiNote13Pro5G is True or isXiaomiNote13Pro4G is True or isXiaomiNote13 is True  
                                         or isXiaomiRedmi13 is True or isXiaomiRedmi12 is True or isMiTV is True or isXiaomiRedmi14 is True)):
        res.append("")
    for i in a:
        if "Redmi Note 13 Pro Plus" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################        
    for i in a:
        if "Redmi Note 14" in i and ("Redmi Note 14 Pro" not in i and "Redmi Note 14S" not in i) and baseFix(i):
            isXiaomiNote14 = True
    if isXiaomiNote14 is True:
        res.append("")
    for i in a:
        if "Redmi Note 14" in i and ("Redmi Note 14 Pro" not in i and "Redmi Note 14S" not in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################      
    for i in a:
        if "Redmi Note 14S" in i and baseFix(i):
            isXiaomiNote14S = True
    if isXiaomiNote14S is True:
        res.append("")
    for i in a:
        if "Redmi Note 14S" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################       
    for i in a:
        if "Redmi Note 14 Pro" in i and '5G' not in i and baseFix(i):
            isXiaomiNote14Pro4G = True
    if isXiaomiNote14Pro4G is True:
        res.append("")
    for i in a:
        if "Redmi Note 14 Pro" in i and '5G' not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 14 Pro 5G" in i and baseFix(i):
            isXiaomiNote14Pro5G = True
    if isXiaomiNote14Pro5G is True:
        res.append("")
    for i in a:
        if "Redmi Note 14 Pro 5G" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 14 Pro Plus" in i and baseFix(i):
            isXiaomiNote14ProPlus = True
    if isXiaomiNote14ProPlus is True:
        res.append("")
    for i in a:
        if "Redmi Note 14 Pro Plus" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################        
    for i in a:
        if "Redmi Note 15" in i and ("Redmi Note 15 Pro" not in i and "Redmi Note 15S" not in i) and baseFix(i):
            isXiaomiNote15 = True
    if isXiaomiNote15 is True:
        res.append("")
    for i in a:
        if "Redmi Note 15" in i and ("Redmi Note 15 Pro" not in i and "Redmi Note 15S" not in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################      
    for i in a:
        if "Redmi Note 15S" in i and baseFix(i):
            isXiaomiNote15S = True
    if isXiaomiNote15S is True:
        res.append("")
    for i in a:
        if "Redmi Note 15S" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################       
    for i in a:
        if "Redmi Note 15 Pro" in i and '5G' not in i and baseFix(i):
            isXiaomiNote15Pro4G = True
    if isXiaomiNote15Pro4G is True:
        res.append("")
    for i in a:
        if "Redmi Note 15 Pro" in i and '5G' not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 15 Pro 5G" in i and baseFix(i):
            isXiaomiNote15Pro5G = True
    if isXiaomiNote15Pro5G is True:
        res.append("")
    for i in a:
        if "Redmi Note 15 Pro 5G" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 15 Pro Plus" in i and baseFix(i):
            isXiaomiNote15ProPlus = True
    if isXiaomiNote15ProPlus is True:
        res.append("")
    for i in a:
        if "Redmi Note 15 Pro Plus" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
            
            #######################        
    for i in a:
        if "Redmi Note 17" in i and ("Redmi Note 17 Pro" not in i and "Redmi Note 17S" not in i) and baseFix(i):
            isXiaomiNote17 = True
    if isXiaomiNote17 is True:
        res.append("")
    for i in a:
        if "Redmi Note 17" in i and ("Redmi Note 17 Pro" not in i and "Redmi Note 17S" not in i) and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################      
    for i in a:
        if "Redmi Note 17S" in i and baseFix(i):
            isXiaomiNote17S = True
    if isXiaomiNote17S is True:
        res.append("")
    for i in a:
        if "Redmi Note 17S" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################       
    for i in a:
        if "Redmi Note 17 Pro" in i and '5G' not in i and baseFix(i):
            isXiaomiNote17Pro4G = True
    if isXiaomiNote17Pro4G is True:
        res.append("")
    for i in a:
        if "Redmi Note 17 Pro" in i and '5G' not in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 17 Pro 5G" in i and baseFix(i):
            isXiaomiNote17Pro5G = True
    if isXiaomiNote17Pro5G is True:
        res.append("")
    for i in a:
        if "Redmi Note 17 Pro 5G" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Redmi Note 17 Pro Plus" in i and baseFix(i):
            isXiaomiNote17ProPlus = True
    if isXiaomiNote17ProPlus is True:
        res.append("")
    for i in a:
        if "Redmi Note 17 Pro Plus" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################        
    for i in a:
        if "Redmi Pad" in i and baseFix(i):
            isRedmiPad = True
    if isRedmiPad is True:
        res.append("")
    for i in a:
        if "Redmi Pad" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################        
    for i in a:
        if "Xiaomi 12" in i and baseFix(i):
            isXiaomi12 = True
    if isXiaomi12 is True:
        res.append("")
    for i in a:
        if "Xiaomi 12" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Xiaomi 13" in i and baseFix(i):
            isXiaomi13 = True
    if isXiaomi13 is True:
        res.append("")
    for i in a:
        if "Xiaomi 13" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Xiaomi 14" in i and baseFix(i):
            isXiaomi14 = True
    if isXiaomi14 is True:
        res.append("")
    for i in a:
        if "Xiaomi 14" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################      
    for i in a:
        if "Xiaomi 15" in i and baseFix(i):
            isXiaomi15 = True
    if isXiaomi15 is True:
        res.append("")
    for i in a:
        if "Xiaomi 15" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################   
    for i in a:
        if "Xiaomi 17" in i and baseFix(i):
            isXiaomi17 = True
    if isXiaomi17 is True:
        res.append("")
    for i in a:
        if "Xiaomi 17" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################         
    for i in a:
        if "Xiaomi Pad" in i and baseFix(i):
            isMiPad = True
    if isMiPad is True:
        res.append("")
    for i in a:
        if "Xiaomi Pad" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    
    #############       
    for i in a:
        if "Pocophone" in i and baseFix(i):
            isPocophone = True
    if isPocophone is True:
        res.append("")
        res.append("📲 *Pocophone*")
    #######################        
    for i in a:
        if "Pocophone C61" in i and baseFix(i):
            isPocoC61 = True
    for i in a:
        if "Pocophone C61" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone C65" in i and baseFix(i):
            isPocoC65 = True
    if isPocoC65 is True and isPocoC61 is True:
        res.append("")
    for i in a:
        if "Pocophone C65" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone C75" in i and baseFix(i):
            isPocoC75 = True
    if isPocoC75 is True and (isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone C75" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Poco Pad" in i and baseFix(i):
            isPocoPad = True
    if isPocoPad is True:
        res.append("")
    for i in a:
        if "Poco Pad" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
            
    #######################        
    for i in a:
        if "Pocophone F6" in i and baseFix(i):
            isPocoF6 = True
    if isPocoF6 is True and (isPocoC75 is True or isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone F6" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone F7" in i and baseFix(i):
            isPocoF7 = True
    if isPocoF7 is True and (isPocoF6 is True or isPocoC75 is True or isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone F7" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone F8" in i and baseFix(i):
            isPocoF8 = True
    if isPocoF8 is True and (isPocoF7 is True or isPocoF6 is True or isPocoC75 is True or isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone F8" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone M5" in i and baseFix(i):
            isPocoM5 = True
    if isPocoM5 is True and (isPocoF8 is True or isPocoF7 is True or isPocoF6 is True or 
                             isPocoC75 is True or isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone M5" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone M6" in i and baseFix(i):
            isPocoM6 = True
    if isPocoM6 is True and (isPocoM5 is True or isPocoF8 is True or isPocoF7 is True or 
                             isPocoF6 is True or isPocoC75 is True or isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone M6" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################             
    for i in a:
        if "Pocophone M8" in i and baseFix(i):
            isPocoM8 = True
    if isPocoM8 is True and (isPocoM6 is True or isPocoM5 is True or isPocoF8 is True or isPocoF7 is True or 
                             isPocoF6 is True or isPocoC75 is True or isPocoC65 is True or isPocoC61 is True):
        res.append("")
    for i in a:
        if "Pocophone M8" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################      
    for i in a:
        if "Pocophone X5" in i and baseFix(i):
            isPocoX5 = True
    if (isPocoX5 is True and (isPocoM8 is True or isPocoM6 is True or isPocoM5 is True or isPocoF8 is True or isPocoF7 is True or 
                              isPocoF6 is True or isPocoC75 is True 
                              or isPocoC65 is True or isPocoC61 is True)):
        res.append("")
    for i in a:
        if "Pocophone X5" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone X6" in i and baseFix(i):
            isPocoX6 = True
    if (isPocoX6 is True and (isPocoX5 is True or isPocoM8 is True or isPocoM6 is True or isPocoM5 is True or 
                              isPocoF8 is True or isPocoF7 is True or isPocoF6 is True or isPocoC75 is True 
                              or isPocoC65 is True or isPocoC61 is True)):
        res.append("")
    for i in a:
        if "Pocophone X6" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
    #######################        
    for i in a:
        if "Pocophone X7" in i and baseFix(i):
            isPocoX7 = True
    if (isPocoX7 is True and (isPocoX6 is True or isPocoX5 is True or isPocoM8 is True or isPocoM6 is True or isPocoM5 is True or 
                              isPocoF8 is True or isPocoF7 is True or isPocoF6 is True or isPocoC75 is True 
                              or isPocoC65 is True or isPocoC61 is True)):
        res.append("")
    for i in a:
        if "Pocophone X7" in i and baseFix(i):
            res.append(fixName("`" + i + "`"))
            
    #######################
    for i in a:
        if "Яндекс" in i and baseFix(i):
            isYandex = True
    if isYandex is True:
        res.append('')
        res.append("🔊 *Яндекс Станция*")
    for i in a:
        if 'Яндекс' in i and baseFix(i):
            res.append("`" + i + "`")
    #######################
    for i in a:
        if "JBL" in i and baseFix(i):
            isJBL = True
    if isJBL is True:
        res.append('')
        res.append("🔊 *JBL*")
    for i in a:
        if 'JBL' in i and baseFix(i):
            res.append("`" + i + "`")
    #######################
    for i in a:
        if "Shokz" in i and baseFix(i):
            isShokz = True
    if isShokz is True:
        res.append('')
        res.append("👓 *Shokz*")
    for i in a:
        if 'Shokz' in i and baseFix(i):
            res.append("`" + i + "`")
    
    return '\n'.join([str(i) for i in res])

def getUsedSN(a):
    def checkUsed(name):
        return (
        '"A-"' in name  or
        '"A"' in name or
        '"A+"' in name or
        '"B-"' in name or
        '"B"' in name or
        '"B+"' in name  or
        '"C-"' in name  or
        '"C"' in name or
        '"C+"' in name 
    )
    res = []
    res.append('IMEI / SN:')
    for i in a:
        if checkUsed(i):
            res.append(i.split("imei", 1)[1])
    return '\n'.join([str(i) for i in res])

def getUsed(a):
    def checkUsed(name):
        return (
        '"A-"' in name  or
        '"A"' in name or
        '"A+"' in name  or
        '"B-"' in name  or
        '"B"' in name or
        '"B+"' in name  or
        '"C-"' in name  or
        '"C"' in name or
        '"C+"' in name or
        '"А-"' in name  or
        '"А"' in name or
        '"А+"' in name  or
        '"В-"' in name  or
        '"В"' in name or
        '"В+"' in name  or
        '"С-"' in name  or
        '"С"' in name or
        '"С+"' in name 
    )
    
    def fixName(name):
        replaceAW = name.replace("Apple Watch ", '')
        replaceCoros = replaceAW.replace("Coros ", '')
        replaceApple = replaceCoros.replace("Apple ", '')
        replaceiPhone = replaceApple.replace("iPhone ", '')
        replaceMacBook = replaceiPhone.replace("MacBook ", '')
        replaceXiaomi = replaceMacBook.replace("Xiaomi Redmi Note", 'Note')
        replaceXiaomiR = replaceXiaomi.replace("Xiaomi Redmi", 'Redmi')
        replacePoco = replaceXiaomiR.replace("Pocophone", 'Poco')
        if "Пломбa" not in replacePoco:
            return replacePoco.replace("Samsung ", '')
        else:
            return replacePoco
    
    
    isAWSE = False
    isAWS8 = False
    isAWS9 = False    
    isiPad = False
    isMacBook = False
    isiMac = False
    
    isiPhone = False
    isiPhone7 = False
    isiPhone8 = False
    isiPhoneSE = False
    isiPhoneX = False    
    isiPhone11 = False
    isiPhone12 = False
    isiPhone13 = False
    isiPhone14 = False
    isiPhone15 = False
    isiPhone16 = False
    isiPhoneAir = False
    isiPhone17 = False
    
    isSams = False
    isXiaomi = False
    isOther = False
    #################
    res = []
    res.append('👇 <b>Идеальное БУ</b>')
    res.append('')
    res.append('📸_Описание и фотографии_')
    res.append('🔗https://t.me/+969mFs7AbldkYTQ6')
    res.append('')
       
    res.append("🍏 <b>Apple</b>")
    for i in a:
        if ("AirPods" in i or 'Apple Magic' in i or 'Apple Battery' in i or 'Apple TV' in i or 'Apple HomePod' in i or 'Apple AirTag' in i or 'Pencil' in i)  and checkUsed(i):
            if ('WMJ520PN40' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Magic Keyboard для iPad Pro 12.9" (3-6th Gen)/ Air 13" (M2) Black "A"', hlink('Magic Keyboard для iPad Pro 12.9" (3-6th Gen)/ Air 13" (M2) Black "A"', 'https://t.me/c/1545286162/4228')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone" in i and checkUsed(i):
            isiPhone = True
    if isiPhone is True:
        res.append('')
        res.append("📱 <b>Apple iPhone</b>")
            
    #######################
    for i in a:
        if "iPhone 7" in i and checkUsed(i):
            isiPhone7 = True
    for i in a:
        if 'iPhone 7' in i and checkUsed(i):
            res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone 8" in i and checkUsed(i):
            isiPhone8 = True
    if isiPhone8 is True and isiPhone7 is True:
        res.append('')
    for i in a:
        if 'iPhone 8' in i and checkUsed(i):
            if ('354830095942761' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('8 Plus 64 Gold "А-" 🇷🇺', hlink('8 Plus 64 Gold "А-" 🇷🇺', 'https://t.me/c/1545286162/4712')))
            elif ('358712097720617' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('8 64 White "B" 🇷🇺', hlink('8 64 White "B" 🇷🇺', 'https://t.me/c/1545286162/4797')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone SE" in i and checkUsed(i):
            isiPhoneSE = True
    if isiPhoneSE is True and (isiPhone7 is True or isiPhone8 is True):
        res.append('')
    for i in a:
        if 'iPhone SE' in i and checkUsed(i):
            if ('356482108653908' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('SE (2020) 128 Red "C"', hlink('SE (2020) 128 Red "C"', 'https://t.me/c/1545286162/4031')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone X" in i and checkUsed(i):
            isiPhoneX = True
    if isiPhoneX is True and (isiPhoneSE is True or isiPhone7 is True or isiPhone8 is True):
        res.append('')
    for i in a:
        if 'iPhone X' in i and checkUsed(i):
            if ('356455106101260' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('XR 64 Black "B-" 🇷🇺', hlink('XR 64 Black "B-" 🇷🇺', 'https://t.me/c/1545286162/4376')))
                
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone 11" in i and checkUsed(i):
            isiPhone11 = True
    if isiPhone11 is True and (isiPhoneX is True or isiPhoneSE is True or isiPhone7 is True or isiPhone8 is True):
        res.append('')
    for i in a:
        if 'iPhone 11' in i and checkUsed(i):
            if ('355325636565360' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('11 128 Black "B"', hlink('11 128 Black "B"', 'https://t.me/c/1545286162/4158')))
            elif ('352837113717747' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('11 Pro 64 Green "A-"', hlink('11 Pro 64 Green "A-"', 'https://t.me/c/1545286162/4221')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
            
            
    #######################
    for i in a:
        if "iPhone 12" in i and checkUsed(i):
            isiPhone12 = True
    if isiPhone12 is True and (isiPhone11 is True or isiPhoneX is True or isiPhoneSE is True 
                               or isiPhone7 is True or isiPhone8 is True):
        res.append('')
    for i in a:
        if 'iPhone 12' in i and checkUsed(i):
            if ('355513316180382' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('12 Pro 128 Silver "B" 🇦🇪', hlink('12 Pro 128 Silver "B" 🇦🇪', 'https://t.me/c/1545286162/4571')))
            elif ('351696725580559' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('12 128 Green "B+"', hlink('12 128 Green "B+"', 'https://t.me/c/1545286162/4025')))
            elif ('353021117430859' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('12 Mini 64 Black "B+"', hlink('12 Mini 64 Black "B+"', 'https://t.me/c/1545286162/4044')))
            elif ('353055110558274' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('12 128 Blue "B+"', hlink('12 128 Blue "B+"', 'https://t.me/c/1545286162/4333')))
                
            else:
                res.append(fixName(i.split("imei", 1)[0]))
        
    #######################
    for i in a:
        if "iPhone 13" in i and checkUsed(i):
            isiPhone13 = True
    if isiPhone13 is True and (isiPhone12 is True or isiPhone11 is True or isiPhoneX is True or isiPhoneSE is True 
                               or isiPhone7 is True or isiPhone8 is True):
        res.append('')
    for i in a:
        if 'iPhone 13' in i and checkUsed(i):
            
            if ('358750481303137' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 Pro 256 Blue "B-"', hlink('13 Pro 256 Blue "B-"', 'https://t.me/c/1545286162/4111')))
            elif ('358538773891186' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 128 Midnight "A-" 🇮🇳', hlink('13 128 Midnight "A-" 🇮🇳', 'https://t.me/c/1545286162/4536')))
            elif ('355178632669698' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 128 Starlight "B" 🇮🇳', hlink('13 128 Starlight "B" 🇮🇳', 'https://t.me/c/1545286162/4414')))
            elif ('350340393413881' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 256 Green "A" 🇦🇪', hlink('13 256 Green "A" 🇦🇪', 'https://t.me/c/1545286162/4531')))
            elif ('351974977432401' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 128 Starlight "B+"', hlink('13 128 Starlight "B+"', 'https://t.me/c/1545286162/4650')))
            elif ('352355500998572' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 128 Blue "A-"', hlink('13 128 Blue "A-"', 'https://t.me/c/1545286162/4679')))
            elif ('351228763698877' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('13 Pro 128 Blue "B"', hlink('13 Pro 128 Blue "B"', 'https://t.me/c/1545286162/4706')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
            
    #######################
    for i in a:
        if "iPhone 14" in i and checkUsed(i):
            isiPhone14 = True
    if isiPhone14 is True and (isiPhone13 is True or isiPhone12 is True or isiPhone11 is True or isiPhoneX is True 
                               or isiPhone7 is True or isiPhone8 is True or isiPhoneSE is True):
        res.append('')
    for i in a:
        if 'iPhone 14' in i and checkUsed(i):
            if ('352149871239025' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('14 Pro 256 Purple "A" 🇦🇪', hlink('14 Pro 256 Purple "A" 🇦🇪', 'https://t.me/c/1545286162/4559')))
            elif ('358287292491496' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('14 Pro 512 Purple "B"', hlink('14 Pro 512 Purple "B"', 'https://t.me/c/1545286162/4106')))
            elif ('356378589825819' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('14 Pro 256 Purple "A" 🇦🇪', hlink('14 Pro 256 Purple "A" 🇦🇪', 'https://t.me/c/1545286162/4565')))
            elif ('350114363059846' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('14 Pro 256 Black "B"', hlink('14 Pro 256 Black "B"', 'https://t.me/c/1545286162/4476')))
            elif ('354606980116442' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('14 Pro 256 Purple"A"', hlink('14 Pro 256 Purple"A"', 'https://t.me/c/1545286162/4684')))
            elif ('359451595736093' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('14 Pro Max 256 Purple "B"', hlink('14 Pro Max 256 Purple "B"', 'https://t.me/c/1545286162/4763')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone 15" in i and checkUsed(i):
            isiPhone15 = True
    if isiPhone15 is True and (isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True 
                               or isiPhone7 is True or isiPhone8 is True or isiPhoneSE is True or isiPhoneX is True):
        res.append('')
    for i in a:
        if 'iPhone 15' in i and checkUsed(i):
            if ('358836164351624' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 Plus 128 Black "A" 🇮🇳', hlink('15 Plus 128 Black "A" 🇮🇳', 'https://t.me/c/1545286162/4527')))
            elif ('353104760456213' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 Pro Max 512 Natural "A-" 🇿🇦', hlink('15 Pro Max 512 Natural "A-" 🇿🇦', 'https://t.me/c/1545286162/4589')))
            elif ('358879685286929' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 Pro Max 256 White "A" 🇧🇷', hlink('15 Pro Max 256 White "A" 🇧🇷', 'https://t.me/c/1545286162/4594')))
            elif ('355361728255172' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 Pro 256 Black "A" 🇯🇵', hlink('15 Pro 256 Black "A" 🇯🇵', 'https://t.me/c/1545286162/4599')))
            elif ('355799336951270' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 128 Pink "B"', hlink('15 128 Pink "B"', 'https://t.me/c/1545286162/4603')))
            elif ('356660808588629' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 128 Blue "A-" 🇮🇳', hlink('15 128 Blue "A-" 🇮🇳', 'https://t.me/c/1545286162/4674')))
            elif ('356597920256935' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('15 Pro 256 Blue "A" 🇯🇵', hlink('15 Pro 256 Blue "A" 🇯🇵', 'https://t.me/c/1545286162/4749')))
            
            else:
                res.append(fixName(i.split("imei", 1)[0]))
                 #######################
    for i in a:
        if "iPhone 16" in i and checkUsed(i):
            isiPhone16 = True
    if isiPhone16 is True and (isiPhone15 is True or isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True 
                               or isiPhone7 is True or isiPhone8 is True or isiPhoneSE is True or isiPhoneX is True):
        res.append('')
    for i in a:
        if ('iPhone 16' in i and checkUsed(i)):
            if ('353995652887591' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('16 Pro Max 256 White "A" 🇯🇵', hlink('16 Pro Max 256 White "A" 🇯🇵', 'https://t.me/c/1545286162/4787')))
            elif ('355984832548313' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('16 Pro 256 White "A-" 🇦🇺', hlink('16 Pro 256 White "A-" 🇦🇺', 'https://t.me/c/1545286162/4792')))
            elif ('352958413931281' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('16 128 Teal "A" 🇮🇳', hlink('16 128 Teal "A" 🇮🇳', 'https://t.me/c/1545286162/4825')))
            else: 
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone Air" in i and checkUsed(i):
            isiPhoneAir = True
    if isiPhoneAir is True and (isiPhone16 is True or isiPhone15 is True or isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True 
                               or isiPhone7 is True or isiPhone8 is True or isiPhoneSE is True or isiPhoneX is True):
        res.append('')
    for i in a:
        if ('iPhone Air' in i and checkUsed(i)):
            if ('351605726416465' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 256 Black "A" 🇨🇦', hlink('Air 256 Black "A" 🇨🇦', 'https://t.me/c/1545286162/4781')))
                
            else: 
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPhone 17" in i and checkUsed(i):
            isiPhone17 = True
    if isiPhone17 is True and (isiPhoneAir is True or isiPhone16 is True or isiPhone15 is True or isiPhone14 is True or isiPhone13 is True or isiPhone12 is True or isiPhone11 is True 
                               or isiPhone7 is True or isiPhone8 is True or isiPhoneSE is True or isiPhoneX is True):
        res.append('')
    for i in a:
        if ('iPhone 17' in i and checkUsed(i)):
            if ('359515202322610' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('17 Pro 256 Silver "B" 🇯🇵', hlink('17 Pro 256 Silver "B" 🇯🇵', 'https://t.me/c/1545286162/4363')))
            elif ('355297172725619' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('17 Pro Max 256 Orange "A-" 🇿🇦', hlink('17 Pro Max 256 Orange "A-" 🇿🇦', 'https://t.me/c/1545286162/4426')))
            elif ('350132462748226' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('17 Pro Max 256 Blue (eSim) "A"', hlink('17 Pro Max 256 Blue (eSim) "A"', 'https://t.me/c/1545286162/4635')))
            elif ('355785870812796' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('17 256 Black "A" 🇺🇸', hlink('17 256 Black "A" 🇺🇸', 'https://t.me/c/1545286162/4689')))
            else: 
                res.append(fixName(i.split("imei", 1)[0]))
    #######################  
    for i in a:
        if "Watch SE" in i and checkUsed(i):
            isAWSE = True
    if isAWSE is True:
        res.append('')
        res.append("⌚️ <b>Apple Watch SE 2023</b>")
    for i in a:
        if 'Watch SE' in i and checkUsed(i):
            res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "Watch S8" in i and checkUsed(i):
            isAWS8 = True
    if isAWS8 is True:
        res.append('')
        res.append("⌚️ <b>Apple Watch S8</b>")
    for i in a:
        if 'Watch S8' in i and checkUsed(i):
            res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "Watch S9" in i and checkUsed(i):
            isAWS9 = True
    if isAWS9 is True:
        res.append('')
        res.append("⌚️ <b>Apple Watch S9</b>")
    for i in a:
        if 'Watch S9' in i and checkUsed(i):
            res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iPad" in i and checkUsed(i):
            isiPad = True
    if isiPad is True:
        res.append('')
        res.append("📟 <b>Apple iPad</b>")
    for i in a:
        if 'iPad' in i and 'Magic' not in i and checkUsed(i):
            if ('M3W4C7RH96' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('iPad Air 13 (2024) 512 Wi-Fi Space Gray "A"', \
                    hlink('iPad Air 13 (2024) 512 Wi-Fi Space Gray "A"', 'https://t.me/c/1545286162/4148')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "MacBook" in i and checkUsed(i):
            isMacBook = True
    if isMacBook is True:
        res.append('')
        res.append("💻 <b>Apple MacBook</b>")
    for i in a:
        if "MacBook" in i and checkUsed(i):
            if ('C02CG1HAM6KH' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 13 i5 8/512 (2020 - MVH22) Gray "B"', \
                    hlink('Air 13 i5 8/512 (2020 - MVH22) Gray "B"', 'https://t.me/c/1545286162/3954')))
            elif ('C02FL9KCQ05G' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Pro 13 M1 8/256 (2020 - MYDA2) Silver "A"', \
                    hlink('Pro 13 M1 8/256 (2020 - MYDA2) Silver "A"', 'https://t.me/c/1545286162/4486')))
            elif ('C02QJE95GFWM' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 11 i5 4/128 (2015 - MJVM2) Silver "B"', \
                    hlink('Air 11 i5 4/128 (2015 - MJVM2) Silver "B"', 'https://t.me/c/1545286162/4197')))
            elif ('C02V335SHV27' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Pro 13 i5 8/256 (2017 - MPXT2) Space Gray "B"', \
                    hlink('Pro 13 i5 8/256 (2017 - MPXT2) Space Gray "B"', 'https://t.me/c/1545286162/4481')))
            elif ('FVFHW0FZQ6L4' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 13 M1 8/256 (2020 - MGN63)  Gray "B"', \
                    hlink('Air 13 M1 8/256 (2020 - MGN63)  Gray "B"', 'https://t.me/c/1545286162/4541')))
            elif ('TR7333T69W' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Pro 14 M1 Pro 16/512 (2021 - MKGP3) Gray "A"', \
                    hlink('Pro 14 M1 Pro 16/512 (2021 - MKGP3) Gray "A"', 'https://t.me/c/1545286162/4437')))
            elif ('FVFZW8JRLYWK' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 13 8/256 (MVFL2 - 2019) Silver "B"', \
                    hlink('Air 13 8/256 (MVFL2 - 2019) Silver "B"', 'https://t.me/c/1545286162/4577')))
            elif ('Y00VG2XPF4' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Pro 16 M1 Pro 16/1TB (2021 - MK1F3) Silver "B"', \
                    hlink('Pro 16 M1 Pro 16/1TB (2021 - MK1F3) Silver "B"', 'https://t.me/c/1545286162/4656')))
            elif ('FVHJG0J41WFV' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air (MGN63) M1 8/256 Gray "B"', \
                    hlink('Air (MGN63) M1 8/256 Gray "B"', 'https://t.me/c/1545286162/4668')))
            elif ('FVHYHFPGJ1WK' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 13 128 (MQD32 - 2017) Silver "B"', \
                    hlink('Air 13 128 (MQD32 - 2017) Silver "B"', 'https://t.me/c/1545286162/4721')))
            elif ('SFVFKQH711WFV' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 13 M1 8/256 (2020 - MGN63) "A" 🇨🇳', \
                    hlink('Air 13 M1 8/256 (2020 - MGN63) "A" 🇨🇳', 'https://t.me/c/1545286162/4758')))
            elif ('C02FK8F1Q6L4' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Air 13 (MGN63 - 2020) M1 8/256 Gray "A-" 🇷🇺', \
                    hlink('Air 13 (MGN63 - 2020) M1 8/256 Gray "A-" 🇷🇺', 'https://t.me/c/1545286162/4775')))
            elif ('C02T5A8NHF1P' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Pro 13 (TBT3 - 2016) i5 8/512 "A"', \
                    hlink('Pro 13 (TBT3 - 2016) i5 8/512 "A"', 'https://t.me/c/1545286162/4769')))
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "iMac" in i and checkUsed(i):
            isiMac = True
    if isiMac is True:
        res.append('')
        res.append("🖥️ <b>Apple iMac</b>")
    for i in a:
        if "iMac" in i and checkUsed(i):
            res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "Samsung" in i and checkUsed(i):
            isSams = True
    if isSams is True:
        res.append('')
        res.append("📱 <b>Samsung</b>")
    for i in a:
        if "Samsung" in i and checkUsed(i):
            if ('356540306367975' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Galaxy S25 12/512 Navy "A', \
                    hlink('Galaxy S25 12/512 Navy "A', 'https://telegram.me/c/1545286162/4738')))
            elif ('351247575017613' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Galaxy S23 Ultra 5G 12/256 Lavender "A" 🇦🇪', \
                    hlink('Galaxy S23 Ultra 5G 12/256 Lavender "A" 🇦🇪', 'https://t.me/c/1545286162/4802')))
            elif ('351747950527698' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Galaxy S23 Ultra 12/256 Black "B-"', \
                    hlink('Galaxy S23 Ultra 12/256 Black "B-"', 'https://t.me/c/1545286162/4808')))
            elif ('355560892342795' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Galaxy S23 Plus 8/512 Green "A"', \
                    hlink('Galaxy S23 Plus 8/512 Green "A"', 'https://t.me/c/1545286162/4819')))
                
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if ("Xiaomi" in i or "Poco" in i) and checkUsed(i):
            isXiaomi = True
    if isXiaomi is True:
        res.append('')
        res.append("📱 <b>Xiaomi</b>")
    for i in a:
        if ("Xiaomi" in i or "Poco" in i) and checkUsed(i):
            if ('865513052588650' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Xiaomi 12X 8/128 Blue "A-"', \
                    hlink('Xiaomi 12X 8/128 Blue "A-"', 'https://t.me/c/1545286162/4743')))
            elif ('869323070739061' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Xiaomi 15T Pro 12/1TB Gray "A" 🇪🇺', \
                    hlink('Xiaomi 15T Pro 12/1TB Gray "A" 🇪🇺', 'https://t.me/c/1545286162/4624')))
            elif ('864825069078520' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Xiaomi 13T 8/256 Green "A-" 🇪🇺', \
                    hlink('Xiaomi 13T 8/256 Green "A-" 🇪🇺', 'https://t.me/c/1545286162/4701')))
            elif ('863784082374500' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Poco F8 Ultra 12/256 Blue "A"', \
                    hlink('Poco F8 Ultra 12/256 Blue "A"', 'https://t.me/c/1545286162/4716')))
                
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    for i in a:
        if "Xiaomi" not in i and "Poco" not in i and "Samsung" not in i and "Apple" not in i and checkUsed(i):
            isOther = True
    if isOther is True:
        res.append('')
        res.append("📱 <b>Остальные бренды</b>")
    for i in a:
        if "Xiaomi" not in i and "Poco" not in i and "Samsung" not in i and "Apple" not in i and checkUsed(i):
            if ('865498060782034' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('OnePlus 12R 16/256 Blue "A"', \
                    hlink('OnePlus 12R 16/256 Blue "A"', 'https://t.me/c/1545286162/4084')))
            elif ('353243157362665' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Google Pixel 8 128Gb Obsidian "A-"', \
                    hlink('Google Pixel 8 128Gb Obsidian "A-"', 'https://t.me/c/1545286162/4613')))
            elif ('358866180830590' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Asus Rog Phone 9 Pro 16/512 Black "А-"', \
                    hlink('Asus Rog Phone 9 Pro 16/512 Black "А-"', 'https://t.me/c/1545286162/4629')))
            elif ('358691830129643' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Sony Xperia 1 VII 12/256 Green "A"', \
                    hlink('Sony Xperia 1 VII 12/256 Green "A"', 'https://t.me/c/1545286162/4695')))
            elif ('350438339711804' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Google Pixel 6A 128 Charcoal "B"', \
                    hlink('Google Pixel 6A 128 Charcoal "B"', 'https://t.me/c/1545286162/4820')))
            elif ('GBN0cx184290466' in i):
                res.append(fixName(i.split("imei", 1)[0]).replace('Asus X540Y AMD 2/112 Black "B"', \
                    hlink('Asus X540Y AMD 2/112 Black "B"', 'https://t.me/c/1545286162/4755')))
                
            else:
                res.append(fixName(i.split("imei", 1)[0]))
    #######################
    res.append('')
    res.append('──── ୨୧ ────')
    res.append('')
    res.append("🏷 <b>Пломбы</b>")
    for i in a:
        if "Пломба" in i or "Пломбa" in i:
            res.append(fixName(i.split("imei", 1)[0]))
    
    
    return '\n'.join([str(i) for i in res])
