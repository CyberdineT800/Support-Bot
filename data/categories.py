INFO1_KIRILL = \
"""
<b>
1). Ўзгалар парваришига муҳтож бўлган ёлғиз яшовчи ҳамда ёлғиз 
кексалар ва ногиронлиги бўлган шахслар
</b>

<i>
1. Чуқурлаштирилган тиббий кўрикдан ўтказиш жадвалини патронаж ҳамшира билан биргаликда тузиш
2. Ҳужжатларини расмийлаштириш ва қайта тиклашда ёрдам бериш
3. Қариндошлари ва яқин инсонлари ўртасидаги муносабатларни тиклаш (ўрнатиш) ва ташкил қилиш
4. Протез-ортопедия мосламалари ва реабилитация қилишнинг техник воситаларини ажратиш учун сертификат расмийлаштириш учун ариза юбориш
5. Кексалар ва ногиронлиги бўлган шахслар учун Ижтимоий ҳимоя миллий агентлиги тизимидаги санаторийларга йўлланмалар ажратиш учун ариза юбориш
6. Талабгорларни ўзгалар парваришига муҳтож бўлган ёлғиз яшовчи ёки ёлғиз кекса ва ногиронлиги бўлган шахс деб эътироф этиш ёки бекор қилиш, 
шунингдек ёлғиз кексалар ва ногиронлиги бўлган шахслар рўйхатига киритиш (ундан чиқариш) учун ариза юбориш
</i>
"""

INFO1_LATIN = \
"""
<b>
1). Oʻzgalar parvarishiga muhtoj boʻlgan yolgʻiz yashovchi hamda 
yolgʻiz keksalar va nogironligi boʻlgan shaxslar
</b>

<i>
1. Chuqurlashtirilgan tibbiy ko‘rikdan o‘tkazish jadvalini patronaj hamshira bilan birgalikda tuzish
2. Hujjatlarini rasmiylashtirish va qayta tiklashda yordam berish
3. Qarindoshlari va yaqin insonlari o‘rtasidagi munosabatlarni tiklash (o‘rnatish) va tashkil qilish
4. Protez-ortopediya moslamalari va reabilitatsiya qilishning texnik vositalarini ajratish uchun sertifikat rasmiylashtirish uchun ariza yuborish
5. Keksalar va nogironligi bo‘lgan shaxslar uchun Ijtimoiy himoya milliy agentligi tizimidagi sanatoriylarga yo‘llanmalar ajratish uchun ariza yuborish
6. Talabgorlarni o‘zgalar parvarishiga muhtoj bo‘lgan yolg‘iz yashovchi yoki yolg‘iz keksa va nogironligi bo‘lgan shaxs deb e’tirof etish yoki bekor qilish, shuningdek yolg‘iz keksalar va nogironligi bo‘lgan 
shaxslar ro‘yxatiga kiritish (undan chiqarish) uchun ariza yuborish
</i>
"""

INFO1_RU = \
"""
<b>
1). Одиноко проживающие, одиноко пожилые люди и лица с инвалидностью нуждающиеся в постороннем уходе
</b>

<i>
1. Установление графика углубленного медицинского осмотра совместно с патронажной медсестрой
2. Помощь в оформлении и восстанолении документов
3. Восстановление (установление) и организация отношений между родственниками и близкими людьми
4. Подача заявления на выдачу сертификата предоставление протезно-ортопедических изделий технических средств реабилитации
5. Подача заявления на выделение направлений в санатории в системе Национального агентства социальной защиты при Президенте Республики Узбекистан
6. Признание или аннулирование заявителей одиноким лицом, нуждающимся в уходе, или одиноким пожилым человеком и инвалидом, а также включение 
в список одиноких пожилых людей и лиц с органиченными возможностями
</i>
"""



# def load_infos():
#     info_dict = {"uz_latin": {}, "uz_kirill": {}, "ru": {}}
    
#     max_info_number = max(int(key.split("_")[0][4:]) for key in globals() if key.startswith("INFO"))
#     info_range = range(1, max_info_number + 1)

#     for i in info_range:
#         info_dict["uz_latin"][f"INFO{i}"] = globals()[f"INFO{i}_LATIN"]
#         info_dict["uz_kirill"][f"INFO{i}"] = globals()[f"INFO{i}_KIRILL"]
#         info_dict["ru"][f"INFO{i}"] = globals()[f"INFO{i}_RU"]

#     def get_infos_info(language):
#         language_infos = info_dict.get(language, {})
#         return len(language_infos), list(language_infos.values())

#     return get_infos_info


# get_infos = load_infos()
# # number_of_faqs, faq_values = get_infos('uz_latin')
# # print(number_of_faqs, faq_values)


def load_categories():
    category_dict = {"uz_latin": {}, "uz_kirill": {}, "ru": {}}
    
    max_info_number = max(int(key.split("_")[0][4:]) for key in globals() if key.startswith("INFO"))
    info_range = range(1, max_info_number + 1)

    for i in info_range:
        category_dict["uz_latin"][f"CAT{i}"] = globals()[f"INFO{i}_LATIN"]
        category_dict["uz_kirill"][f"CAT{i}"] = globals()[f"INFO{i}_KIRILL"]
        category_dict["ru"][f"CAT{i}"] = globals()[f"INFO{i}_RU"]

    def get_category_info(language, id):
        language_categories = category_dict.get(language, {})
        #return len(language_categories), list(language_categories.values())
        for i in language_categories.keys():
            if i == f"CAT{id}":
                return language_categories.get(i, None), len(language_categories), list(language_categories.values())

    return get_category_info

get_category = load_categories()
