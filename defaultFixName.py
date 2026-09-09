def default_fix_name(el):
    name = el.lower()
    remove_double_space = " ".join(name.split())
    
    replace_nx799j = remove_double_space.replace("nx799j ", "") if "nx799j" in remove_double_space else remove_double_space
    replace_nx809j = replace_nx799j.replace("nx809j ", "") if "nx809j" in replace_nx799j else replace_nx799j
    replace_r530 = replace_nx809j.replace("r530 ", "") if "r530" in replace_nx809j else replace_nx809j
    replace_r640 = replace_r530.replace("r640 ", "") if "r640" in replace_r530 else replace_r530
    replace_a175 = replace_r640.replace("a175", "a17") if "a175" in replace_r640 else replace_r640
    replace_a266 = replace_a175.replace("a266", "a26") if "a266" in replace_a175 else replace_a175
    fix_airpods = replace_a266.replace("air pods", "airpods") if "air pods" in replace_a266 else replace_a266
    replace_a366 = fix_airpods.replace("a366", "a36") if "a366" in fix_airpods else fix_airpods
    replace_a566 = replace_a366.replace("a566", "a56") if "a566" in replace_a366 else replace_a366
    replace_gb = replace_a566.replace("gb", "") if "gb" in replace_a566 else replace_a566
    fix_air_pods_usb = replace_gb.replace("type", "usb") if "airpods pro 2" in replace_gb else replace_gb
    fix_air_pods_max22 = fix_air_pods_usb.replace("usb", "2") if "airpods max" in fix_air_pods_usb and "usb" in fix_air_pods_usb else fix_air_pods_usb
    fix_se2_black = fix_air_pods_max22.replace("black", "midnight") if "se2" in fix_air_pods_max22 and "s8" in fix_air_pods_max22 and "s9" in fix_air_pods_max22 else fix_air_pods_max22
    fix_se2_white = fix_se2_black.replace("white", "starlight") if "se2" in fix_se2_black and "s8" in fix_se2_black and "s9" in fix_se2_black else fix_se2_black
    
    fix_16e = fix_se2_white.replace("16е", "16e") if "16е" in fix_se2_white else fix_se2_white
    fix_ultra2 = fix_16e.replace("ul 2", "ultra 2") if "ul 2" in fix_16e else fix_16e
    fix_ultra2_ob = fix_ultra2.replace("ob", "ocean band") if "ul 2" in fix_ultra2 else fix_ultra2
    fix_ultra2_tl = fix_ultra2_ob.replace("tl", "trail loop") if "ul 2" in fix_ultra2_ob else fix_ultra2_ob
    fix_ultra2_al = fix_ultra2_tl.replace("al", "alpine loop") if "ul 2" in fix_ultra2_tl else fix_ultra2_tl
    fix_ultra2_case = fix_ultra2_al.replace("case", "ti") if "ultra 2" in fix_ultra2_al else fix_ultra2_al
    
    fix_pencil_usb = fix_ultra2_case.replace("type", "usb") if "pencil" in fix_ultra2_case else fix_ultra2_case
    fix_ipad_mini7 = fix_pencil_usb.replace("2024", "7") if "ipad mini" in fix_pencil_usb else fix_pencil_usb
    
    fix_hk = fix_ipad_mini7.replace("🇭🇰", " dual ") if "🇭🇰" in fix_ipad_mini7 and "17" not in fix_ipad_mini7 else fix_ipad_mini7
    fix_ch = fix_hk.replace("🇨🇳", " dual ") if "🇨🇳" in fix_hk else fix_hk
    
    starlight_patterns = ["13 128 white", "13 256 white", "13 512 white", "13 mini 512 white", "14 128 white", "14 256 white", "14 512 white", "14 plus 128 white", "14 plus 256 white", "14 plus 512 white", "se3 64", "se3 128"]
    fix_starlight = fix_ch.replace("white", "starlight") if any(pattern in fix_ch for pattern in starlight_patterns) else fix_ch
    
    midnight_patterns = ["13 128 black", "13 256 black", "13 512 black", "13 mini 512 black", "14 128 black", "14 256 black", "14 512 black", "15 128 black", "15 256 black", "15 512 black", "14 plus 128 black", "14 plus 256 black", "14 plus 512 black", "15 plus 128 black", "15 plus 256 black", "15 plus 512 black", "se3 64", "se3 128"]
    fix_midnight = fix_starlight.replace("black", "midnight") if any(pattern in fix_starlight for pattern in midnight_patterns) else fix_starlight
    
    fix_mint = fix_midnight.replace("mint", "Green") if "z flip 5" not in fix_midnight else fix_midnight
    fix_a36_lime = fix_mint.replace("lime", "Green") if "a36" in fix_mint else fix_mint
    fix_lime = fix_a36_lime.replace("lime", "Yellow")
    
    fix_mi_pad_8_gray = fix_lime.replace("gray", "black") if "mi pad 8" in fix_lime else fix_lime
    fix_realme_black = fix_mi_pad_8_gray.replace("черный", "black") if "realme" in fix_mi_pad_8_gray else fix_mi_pad_8_gray
    fix_realme_gold = fix_realme_black.replace("розовый", "gold") if "realme" in fix_realme_black else fix_realme_black
    fix_zflip6 = fix_realme_gold.replace("z flip6", "z flip 6")
    fix_zfold6 = fix_zflip6.replace("z fold6", "z fold 6")
    fix_zflip7 = fix_zfold6.replace("z flip7", "z flip 7")
    fix_zfold7 = fix_zflip7.replace("z fold7", "z fold 7")
    fix_zflip8 = fix_zfold7.replace("z flip8", "z flip 8")
    fix_zfold8 = fix_zflip8.replace("z fold8", "z fold 8")
    fix_galaxy_tab = fix_zfold8.replace("galaxy tab", "tab")
    fix_watch_7 = fix_galaxy_tab.replace("watch7", "watch 7")
    fix_watch_8 = fix_watch_7.replace("watch8", "watch 8")
    fix_nord_ce6 = fix_watch_8.replace("nord ce 6", "nord ce6")
    fix_ps_vr2 = fix_nord_ce6.replace("ps vr2", "ps vr 2")
    
    fix_dualsense = fix_ps_vr2.replace("dual sense", "dualsense")
    
    fix_graphite = fix_dualsense.replace("graphite", "Black") if not any(model in fix_dualsense for model in ["s22", "s23", "buds 2", "epix", "fenix", "instinct"]) else fix_dualsense
    
    fix_SamsA_5G = fix_graphite.replace("5g ", "") if any(model in fix_graphite for model in ["a26", "a36", "a56", "a25", "a35", "a55", "s21"]) else fix_graphite
    
    fix_navy_black = fix_SamsA_5G.replace("navy", "Black") if any(model in fix_SamsA_5G for model in ["a35", "a55"]) else fix_SamsA_5G
    fix_lilac1 = fix_navy_black.replace("lavender", "Lilac") if any(model in fix_navy_black for model in ["a35", "a55"]) else fix_navy_black
    fix_lilac2 = fix_lilac1.replace("violet", "Lilac") if any(model in fix_lilac1 for model in ["a35", "a55"]) else fix_lilac1
    
    fix_lte = fix_lilac2.replace("lte", "5g")
    fix_buds2_pro = fix_lte.replace("buds pro 2", "buds 2 pro")
    fix_pencil1 = fix_buds2_pro.replace("pencil 1", "pencil lightning") if "pencil 1" in fix_buds2_pro and "usb" not in fix_buds2_pro else fix_buds2_pro
    
    fix_lavander = fix_pencil1.replace("lavander", "Purple")
    fix_lavender = fix_lavander.replace("lavender", "Purple")
    fix_violet = fix_lavender.replace("violet", "Purple")
    fix_lunar = fix_violet.replace("lunar", "silver") if "poco" in fix_violet else fix_violet
    fix_olive = fix_lunar.replace("olive", "Green")
    fix_teal1 = fix_olive.replace("teal", "Green") if "note 13 pro" in fix_olive else fix_olive
    fix_teal2 = fix_teal1.replace("blue", "Green") if "note 13 pro" in fix_teal1 else fix_teal1
    
    fix_pad_se_gray = fix_teal2.replace("graphite", "Gray") if "pad se" in fix_teal2 else fix_teal2
    fix_pad6s_pro_black = fix_pad_se_gray.replace("gray", "Black") if any(model in fix_pad_se_gray for model in ["pad 6s pro", "mi pad 7"]) else fix_pad_se_gray
    
    fix_gray = fix_pad6s_pro_black.replace("grey", "Gray")
    fix17_sage = fix_gray.replace("sage", "Green") if "17 " in fix_gray else fix_gray
    fix_mist_blue = fix17_sage.replace("mist blue", "Blue")
    fix_cosmic_orange = fix_mist_blue.replace("cosmic orange", "Orange")
    fix_deep_blue = fix_cosmic_orange.replace("deep blue", "blue")
    fix_space_black = fix_deep_blue.replace("space black", "black")
    fix_cloud_white = fix_space_black.replace("cloud white", "white")
    fix_light_gold = fix_cloud_white.replace("light gold", "gold")
    fix_sky_blue = fix_light_gold.replace("sky blue", "blue")
    
    fix_se3_black = fix_sky_blue.replace("midnight", "black") if any(model in fix_sky_blue for model in ["se3", "magic"]) else fix_sky_blue
    fix_se3_white = fix_se3_black.replace("starlight", "white") if "se3" in fix_se3_black else fix_se3_black
    
    fix_go_pro = fix_se3_white.replace("gopro 1", "hero 1") if "gopro 1" in fix_se3_white else fix_se3_white
    fix_nord5_blue = fix_go_pro.replace("ice", "blue") if "nord 5" in fix_go_pro else fix_go_pro
    fix_nord5_white = fix_nord5_blue.replace("sands", "white") if "nord 5" in fix_nord5_blue else fix_nord5_blue
    fix_nord_ce5_mist = fix_nord5_white.replace("mist", "white") if "nord ce5" in fix_nord5_white else fix_nord5_white
    fix_nord_ce5_mist2 = fix_nord_ce5_mist.replace("gray", "white") if "nord ce5" in fix_nord_ce5_mist else fix_nord_ce5_mist
    
    fix_nord_gray = fix_nord_ce5_mist2.replace("tempest", "gray") if "nord " in fix_nord_ce5_mist2 else fix_nord_ce5_mist2
    fix_nord_green = fix_nord_gray.replace("mistry", "green") if "nord " in fix_nord_gray else fix_nord_gray
    fix_nord_silver = fix_nord_green.replace("mercurial", "silver") if "nord " in fix_nord_green else fix_nord_green
    fix_nord_oasis = fix_nord_silver.replace("oasis", "green") if "nord " in fix_nord_silver else fix_nord_silver
    fix_nord_obsidian = fix_nord_oasis.replace("obsidian", "black") if any(model in fix_nord_oasis for model in ["nord ", "pixel "]) else fix_nord_oasis
    fix_nord_celadon = fix_nord_obsidian.replace("celadon", "green") if "nord " in fix_nord_obsidian else fix_nord_obsidian
    fix_nord_chrome = fix_nord_celadon.replace("chrome", "black") if "nord " in fix_nord_celadon else fix_nord_celadon
    
    fix_oneplus_open = fix_nord_chrome.replace("dusk", "green") if "open " in fix_nord_chrome else fix_nord_chrome
    fix_oneplus_nebula = fix_oneplus_open.replace("nebula", "black") if "oneplus" in fix_oneplus_open else fix_oneplus_open
    fix_oneplus_noir = fix_oneplus_nebula.replace("noir", "black") if "oneplus" in fix_oneplus_nebula else fix_oneplus_nebula
    fix_oneplus_astral = fix_oneplus_noir.replace("astral", "silver") if "oneplus" in fix_oneplus_noir else fix_oneplus_noir
    fix_oneplus_trail = fix_oneplus_astral.replace("trail", "silver") if "oneplus" in fix_oneplus_astral else fix_oneplus_astral
    
    fix_seafoam = fix_oneplus_trail.replace("seafoam", "green")
    fix_black = fix_seafoam.replace("stormy", "black")
    fix_pixel_snow = fix_black.replace("snow", "white") if "pixel" in fix_black else fix_black
    fix_charcoal = fix_pixel_snow.replace("charcoal", "black")
    fix_pixel_sea = fix_charcoal.replace("sea", "blue") if "pixel" in fix_charcoal else fix_charcoal
    fix_pixel_rose = fix_pixel_sea.replace("rose", "pink") if "pixel" in fix_pixel_sea else fix_pixel_sea
    fix_pixel_bay = fix_pixel_rose.replace("bay", "blue") if "pixel" in fix_pixel_rose else fix_pixel_rose
    fix_pixel_porcelain = fix_pixel_bay.replace("porcelain", "gold") if "pixel" in fix_pixel_bay else fix_pixel_bay
    fix_pixel_aloe = fix_pixel_porcelain.replace("aloe", "green") if "pixel" in fix_pixel_porcelain else fix_pixel_porcelain
    fix_pixel_peony = fix_pixel_aloe.replace("peony", "pink") if "pixel" in fix_pixel_aloe else fix_pixel_aloe
    fix_pixel_iris = fix_pixel_peony.replace("iris", "purple") if "pixel" in fix_pixel_peony else fix_pixel_peony
    fix_pixe_jade = fix_pixel_iris.replace("jade", "green") if "pixel" in fix_pixel_iris else fix_pixel_iris
    
    iphone17_patterns = ["17e 256", "17e 512", "17 256", "17 512", "17 pro 256", "17 pro 512", "17 pro 1tb", "17 pro max 256", "17 pro max 512", "17 pro max 1tb", "17 pro max 2tb"]
    fix_e_sim1 = fix_pixe_jade.replace("esim", "🇺🇸") if any(pattern in fix_pixe_jade for pattern in iphone17_patterns) and "+" not in fix_pixe_jade else fix_pixe_jade
    
    fix_e_sim41 = fix_e_sim1.replace("e-sim", "🇺🇸") if any(pattern in fix_e_sim1 for pattern in iphone17_patterns) and "+" not in fix_e_sim1 else fix_e_sim1
    fix_e_sim = fix_e_sim41.replace("+", "🇮🇳") if any(pattern in fix_e_sim41 for pattern in iphone17_patterns) and "+" in fix_e_sim41 else fix_e_sim41
    
    fix_dual_sim = fix_e_sim.replace("🇨🇳", "dual") if any(pattern in fix_e_sim for pattern in iphone17_patterns) and "🇨🇳" in fix_e_sim else fix_e_sim
    fix_e_sim0 = fix_dual_sim.replace("🇧🇭", "🇺🇸") if any(pattern in fix_dual_sim for pattern in iphone17_patterns) and "🇧🇭" in fix_dual_sim else fix_dual_sim
    fix_e_sim2 = fix_e_sim0.replace("🇨🇦", "🇺🇸") if any(pattern in fix_e_sim0 for pattern in iphone17_patterns) and "🇨🇦" in fix_e_sim0 else fix_e_sim0
    fix_e_sim3 = fix_e_sim2.replace("🇬🇺", "🇺🇸") if any(pattern in fix_e_sim2 for pattern in iphone17_patterns) and "🇬🇺" in fix_e_sim2 else fix_e_sim2
    fix_e_sim4 = fix_e_sim3.replace("🇯🇵", "🇺🇸") if any(pattern in fix_e_sim3 for pattern in iphone17_patterns) and "🇯🇵" in fix_e_sim3 else fix_e_sim3
    fix_e_sim5 = fix_e_sim4.replace("🇰🇼", "🇺🇸") if any(pattern in fix_e_sim4 for pattern in iphone17_patterns) and "🇰🇼" in fix_e_sim4 else fix_e_sim4
    fix_e_sim6 = fix_e_sim5.replace("🇲🇽", "🇺🇸") if any(pattern in fix_e_sim5 for pattern in iphone17_patterns) and "🇲🇽" in fix_e_sim5 else fix_e_sim5
    fix_e_sim7 = fix_e_sim6.replace("🇴🇲", "🇺🇸") if any(pattern in fix_e_sim6 for pattern in iphone17_patterns) and "🇴🇲" in fix_e_sim6 else fix_e_sim6
    fix_e_sim8 = fix_e_sim7.replace("🇶🇦", "🇺🇸") if any(pattern in fix_e_sim7 for pattern in iphone17_patterns) and "🇶🇦" in fix_e_sim7 else fix_e_sim7
    fix_e_sim9 = fix_e_sim8.replace("🇸🇦", "🇺🇸") if any(pattern in fix_e_sim8 for pattern in iphone17_patterns) and "🇸🇦" in fix_e_sim8 else fix_e_sim8
    fix_e_sim110 = fix_e_sim9.replace("🇦🇪", "🇺🇸") if any(pattern in fix_e_sim9 for pattern in iphone17_patterns) and "🇦🇪" in fix_e_sim9 else fix_e_sim9
    fix_e_sim11 = fix_e_sim110.replace("🇻🇮", "🇺🇸") if any(pattern in fix_e_sim110 for pattern in iphone17_patterns) and "🇻🇮" in fix_e_sim110 else fix_e_sim110
    
    fix_ob = fix_e_sim11.replace("ocean band", "ob")
    fix_tl = fix_ob.replace("trail loop", "tl")
    fix_al = fix_tl.replace("alpine loop", "al")
    fix_ul3 = fix_al.replace("ul ", "ultra ")
    fix_ps51 = fix_ul3.replace("ps5", "ps 5")
    fix_ps52 = fix_ps51.replace("playstation 5", "ps 5")
    
    fix_major4 = fix_ps52.replace("iv", "4") if "major" in fix_ps52 else fix_ps52
    fix_major5 = fix_major4.replace("v", "5") if "major" in fix_major4 else fix_major4
    
    xperia_cn_patterns = ["xperia", "17e 256", "17e 512", "17 256", "17 512", "17 pro 256", "17 pro 512", "17 pro 1tb", "17 pro max 256", "17 pro max 1tb", "17 pro max 512", "17 pro max 2tb"]
    fix_xperia_cn = fix_major5.replace("🇨🇳", "dual") if any(pattern in fix_major5 for pattern in xperia_cn_patterns) else fix_major5
    
    fix_apple2_sim = fix_xperia_cn.replace("2sim", "dual") if any(pattern in fix_xperia_cn for pattern in iphone17_patterns) else fix_xperia_cn
    fix_apple2_sim2 = fix_apple2_sim.replace("2-sim", "dual") if any(pattern in fix_apple2_sim for pattern in iphone17_patterns) else fix_apple2_sim
    
    fix_xperia_hk = fix_apple2_sim2.replace("🇭🇰", "dual") if "xperia" in fix_apple2_sim2 else fix_apple2_sim2
    
    fix_redmagic = fix_xperia_hk.replace("red magic", "redmagic")
    fix_redmagic_pro_plus = fix_redmagic.replace("pro +", "pro plus") if "redmagic" in fix_redmagic else fix_redmagic
    fix_redmagic_pro_plus1 = fix_redmagic_pro_plus.replace("pro+", "pro plus") if "redmagic" in fix_redmagic_pro_plus else fix_redmagic_pro_plus
    
    fix_redmagic_sleet = fix_redmagic_pro_plus1.replace("sleet", "black")
    fix_redmagic_dusk = fix_redmagic_sleet.replace("dusk", "black")
    fix_redmagic_moonlight = fix_redmagic_dusk.replace("moonlight", "silver")
    fix_redmagic_lightspeed = fix_redmagic_moonlight.replace("lightspeed", "white")
    
    fix_magic_v3_red = fix_redmagic_lightspeed.replace("brown", "red") if "magic v3" in fix_redmagic_lightspeed else fix_redmagic_lightspeed
    
    fix_yandex = fix_magic_v3_red.replace("станция", "яндекс") if "станция" in fix_magic_v3_red else fix_magic_v3_red
    
    fix_yandex_black = fix_yandex.replace("black", "черн") if "яндекс" in fix_yandex else fix_yandex
    fix_yandex_blue = fix_yandex_black.replace("blue", "син") if "яндекс" in fix_yandex_black else fix_yandex_black
    fix_yandex_green = fix_yandex_blue.replace("green", "зелен") if "яндекс" in fix_yandex_blue else fix_yandex_blue
    fix_yandex_red = fix_yandex_green.replace("red", "красн") if "яндекс" in fix_yandex_green else fix_yandex_green
    fix_yandex_gray = fix_yandex_red.replace("gray", "сер") if "яндекс" in fix_yandex_red else fix_yandex_red
    fix_yandex_purple = fix_yandex_gray.replace("purple", "фиол") if "яндекс" in fix_yandex_gray else fix_yandex_gray
    fix_yandex_pink = fix_yandex_purple.replace("pink", "розов") if "яндекс" in fix_yandex_purple else fix_yandex_purple
    fix_yandex_white = fix_yandex_pink.replace("white", "бел") if "яндекс" in fix_yandex_pink else fix_yandex_pink
    fix_yandex_beige = fix_yandex_white.replace("beige", "беж") if "яндекс" in fix_yandex_white else fix_yandex_white
    fix_yandex_max = fix_yandex_beige.replace("max", "макс") if "яндекс" in fix_yandex_beige else fix_yandex_beige
    
    fix_s23_plus = fix_yandex_max.replace("s23 plus", "S23+")
    fix_s23_plus1 = fix_s23_plus.replace("s23 +", "S23+")
    fix_s24_plus = fix_s23_plus1.replace("s24 plus", "S24+")
    fix_s24_plus1 = fix_s24_plus.replace("s24 +", "S24+")
    fix_s25_plus = fix_s24_plus1.replace("s25 plus", "S25+")
    fix_s25_plus1 = fix_s25_plus.replace("s25 +", "S25+")
    
    a07_patterns = ["a07 4/64", "a07 4/128", "a07 6/128", "a07 8/256"]
    fix_a07_gray = fix_s25_plus1.replace("black", "gray") if any(pattern in fix_s25_plus1 for pattern in a07_patterns) else fix_s25_plus1
    
    fix_s25_icyblue = fix_a07_gray.replace("iceblue", "icyblue") if "s25" in fix_a07_gray else fix_a07_gray
    fix_redmi15_cblck = fix_s25_icyblue.replace("black", "gray") if "redmi 15 " in fix_s25_icyblue else fix_s25_icyblue
    
    fix_a36_lilac = fix_redmi15_cblck.replace("lilac", "purple") if "a36" in fix_redmi15_cblck else fix_redmi15_cblck
    fix_ce4_black = fix_a36_lilac.replace("gray", "black") if "ce4" in fix_a36_lilac else fix_a36_lilac
    fix15c = fix_ce4_black.replace("black", "gray") if "15c" in fix_ce4_black else fix_ce4_black
    
    fix_y_lilac = fix15c.replace("лиловая", "фиолет") if "яндекс" in fix15c else fix15c
    fix_note14_pro_plus = fix_y_lilac.replace("note 14 pro plus", "note 14 pro +")
    fix_note14_pro_plus = fix_y_lilac.replace("note 15 pro plus", "note 15 pro +")
    
    fix_open_swim_orange = fix_note14_pro_plus.replace("coral", "orange") if "openswim" in fix_note14_pro_plus else fix_note14_pro_plus
    
    fix_honor_white = fix_open_swim_orange.replace("белый", "white") if "honor" in fix_open_swim_orange else fix_open_swim_orange
    fix_honor_black = fix_honor_white.replace("чёрный", "black") if "honor" in fix_honor_white else fix_honor_white
    fix_note15_titan = fix_honor_black.replace("color", "titan") if "note 15" in fix_honor_black else fix_honor_black
    fix_honor_green = fix_note15_titan.replace("зелёный", "green") if "honor" in fix_note15_titan else fix_note15_titan
    fix_a37_chark = fix_honor_green.replace("black", "chark") if "a37" in fix_honor_green else fix_honor_green
    fix_a17_4g = fix_a37_chark.replace("a17 4g", "a17") if "a17" in fix_a37_chark else fix_a37_chark
    
    
    return fix_a17_4g