import json
import os
import argparse

# disable re-checking, can be enabled with --recheck or -r flags
no_recheck = False

# parsing some console arguments for easy cli operation
parser = argparse.ArgumentParser(description="CLI options", formatter_class=argparse.RawTextHelpFormatter)

# flags
parser.add_argument('-r', '--recheck', type=str,  help='This option allows you to skip checking already translated stuff, False skips it (default), True will re-check and allow you to modify one by one')

# parse arguments
args = parser.parse_args()

# modify recheck parameter if specified in cli
if args.recheck:
    if args.recheck not in ['True','true','False','false']:
        print('recheck must be True or False')
        exit()
    else:
        if args.recheck in ['True', 'true']:
            no_recheck = True
        else:
            no_recheck = False

# check json files in current folder and only keep those of length 7, so an ISO alpha-2 language code like 'es' plu '.json' 
if len(os.listdir()) == 0:
    exit()
elif len(os.listdir()) == 1 and 'json' in os.listdir()[0] and len(os.listdir()[0])==7:
    translation_json = os.listdir()[0]
else:
    translation_json = [x for x in os.listdir() if 'json' in x and len(x)==7][0]

# keep filename
json_filename = translation_json

# load json
with open(translation_json) as f:
    translation_json = json.load(f)

# items with elements important to the UI should be translated manually in the json file
items_requiring_manual_json_manipulation = ['\n','{','}','<','>', '…']

# gather missed keys 
missed_translations_due_to_UI_elements = []

# items to re-check even if confirmed
items_to_recheck = []

# detect translation language
def detect_translation_language(d):
    for k,v in d.items():
        if isinstance(v, dict):
            if "en" in list(v.values())[0].keys():
                return [x for x in list(v.values())[0].keys() if x != "en"][0]
            else:
                detect_translation_language(v, translation_language)
        else:
            continue

# detect translation language var
translation_language = detect_translation_language(d=translation_json)

# walk the json recursively
def translate(d):

    # loop over k,v pairs
    for k,v in d.items():
        
        # if it's a dict check if the key 'en' is present, otherwise continue
        if isinstance(v, dict):

            # if the 'en' key is present, continue
            if "en" in v.keys():

                # avoid trying to translate items that require manual manipulation
                skip = False
                for item in items_requiring_manual_json_manipulation:
                    if item in v['en']:
                        
                        # save items that require manual manipulation and skip
                        missed_translations_due_to_UI_elements.append(k)
                        skip=True
                
                if skip == False:
                    # ask for translation
                    if v[translation_language] != "" and no_recheck != False:
                        print(f"\n{'Original English text:':<22} {v['en']:15}")
                        print(f"{'Current translation:':<22} {v[translation_language]:15}\n")
                        while True:
                            correct = input(f"{'Is this correct? (y/y*/n):':<22} ")
                            if correct in ['y','Y','']:
                                break
                            elif correct in ['y*','Y*']:
                                v[translation_language] += 'RECHECK'
                                items_to_recheck.append(k)
                                break
                            elif correct in ['n','N']:
                                v[translation_language] = input(f"\n{'New translation:':<22} {''}")
                                break
                            else:
                                continue
                    
                    # if translation not present, ask for translation
                    elif v[translation_language] == "":
                        while True:
                            print(f"\n{'Original English text:':<22} {v['en']}")
                            v[translation_language] = input(f"{'Translation:':<22} {''}")
                            print(f"\nYou wrote: {v[translation_language]}\n")
                            correct = input(f"{'Is this correct? (y/y*/n):':<22} ")
                            if correct in ['y','Y','']:
                                break
                            elif correct in ['y*','Y*']:
                                v[translation_language] += 'RECHECK'
                                items_to_recheck.append(k)
                                break
                            elif correct in ['n','N']:
                                continue
                    
                    # update the json as it goes
                    with open(json_filename, 'w') as f:
                        json.dump(translation_json, f, ensure_ascii=False, indent='	')

                else:
                    # keep translated stuff that would normally be untranslated
                    if v[translation_language] not in ["MISSING TRANSLATION",""]:
                        pass
                    else:
                        v[translation_language] = "MISSING TRANSLATION"
            
            # continue traversing the dict recursively
            else:
                translate(v)
    
    return (d,missed_translations_due_to_UI_elements,items_to_recheck)

# run the function
translation_json, missed_translations_due_to_UI_elements, items_to_recheck = translate(translation_json)

try:
    # save missed ui elements
    with open('missed','a') as f:
        for item in missed_translations_due_to_UI_elements: 
            f.write(f'{item}\n')

    # save items to re-check
    with open('recheck','a') as f:
        for item in items_to_recheck:
            f.write(f'{item}\n')
except:
    pass

# done
print("Done translating!")
