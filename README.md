# Little translator for SW JSONs

## Before using this, some notes

- You **do NOT** have to type `y` whenever you run it, you can just press enter, an empty string counts as `y`

- The language should be detected automatically assuming it's an ISO alpha-2 language code, I only saw the Spanish file, but my assumption is that all others share the same language code length

- There's a flag you can use in console to re-check items that you have already translated, the flag is `-r` or `--recheck`, followed by either True or False (true and false in lowercase also work)

- If you do not have the `missed` or `recheck` files, the thingy will still work, but they're nice-to-have

## How to make this lil thing work

1. Clone the repo

2. Make sure the JSON file is in the same folder as the script, otherwise it won't work
  
3. Run the script and start translating stuff

## The `missed` file

The `missed` file will correspond to translations you'll have to go manually make in the JSON. I am skipping all lines with the following characters in the english original text: 
- \n
- {
- }
- <
- \>
- …

These correspond to more 'delicate' translations that have html tags or variables in them. You'll have to edit these manually to not screw anything up.

After you finish translating everything (or as you go), it'll insert `MISSING TRANSLATION` on those that have any special symbol in the list, so you can later easily just search for `MISSING TRANSLATION` with Ctrl+F and easily find them. Either way, the corresponding tag in the JSON file will be listed in the `missed` file.

## The `recheck` file and `y*`

As you go, you can say `y`, `n` or `y*` whenever you confirm an already written translation or a translation you make. What `y*` does is that it adds the name of the tag where that translation was found to the `recheck` file, as well as add `RECHECK` to the ending of the translation you marked.
