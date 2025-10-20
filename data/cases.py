case1_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case1_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case1_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

case2_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case2_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case2_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

case3_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case3_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case3_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

case4_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case4_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case4_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

case5_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case5_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case5_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

case6_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case6_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case6_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

#case7_file_id_LATIN = "https://tg-cloud-file-small-file.ajz.workers.dev/videos/file_102943.mp4?file_name=qollanmabotuchun-edit.mp4&expire=1698727110&signature=6Ktu4D8J71%2FqWdWAEE0sHWf3K6bsfZbLLiawc0WRMh8%3D"
case7_file_id_LATIN = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case7_file_id_KIRILL = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"
case7_file_id_RU = "BQACAgIAAxkBAAIoOGV0TeyZTMcI2tbuBpYuDP2q3376AALsGwACbPrgStnStKx9b6kZMwQ"

def load_cases():
    cases_dict = {"uz_latin": {}, "uz_kirill": {}, "ru": {}}
    
    max_case_number = max(int(key.split("_")[0][4:]) for key in globals() if key.startswith("case"))
    case_range = range(1, max_case_number + 1)

    for i in case_range:
        cases_dict["uz_latin"][f"CASE{i}"] = globals()[f"case{i}_file_id_LATIN"]
        cases_dict["uz_kirill"][f"CASE{i}"] = globals()[f"case{i}_file_id_KIRILL"]
        cases_dict["ru"][f"CASE{i}"] = globals()[f"case{i}_file_id_RU"]

    def get_case_info(language, id):
        language_cases = cases_dict.get(language, {})
        #return len(language_categories), list(language_categories.values())
        for i in language_cases.keys():
            if i == f"CASE{id}":
                return language_cases.get(i, None), len(language_cases), list(language_cases.values())

    return get_case_info


get_cases = load_cases()