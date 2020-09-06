use dont_disappear::enter_to_continue;
use json::{parse, JsonValue};
use std::fs;
use std::io::{prelude::*, stdin, stdout};

fn input(message: &str) -> String {
    print!("{}", message);
    stdout().flush().unwrap();
    let mut ret = String::new();
    stdin()
        .read_line(&mut ret)
        .expect("Failed to read from stdin");
    ret
}

macro_rules! msg_and_quit {
    ($($arg:tt)*) => {
        enter_to_continue::custom_msg(&format!($($arg)*));
        std::process::exit(0)
    };
}

fn load_file(filename: &str) -> JsonValue {
    if let Ok(s) = fs::read_to_string(filename) {
        if let Ok(result) = parse(&s) {
            println!("Successfully loaded \"{}\"", filename);
            result
        } else {
            msg_and_quit!(
                "Error parsing \"{}\", make sure it is a valid .json file.",
                filename
            );
        }
    } else {
        msg_and_quit!(
            "Could not find \"{}\" in directory. Make sure it is present and named correctly.",
            filename
        );
    }
}

fn main() {
    println!("Enter your language code\n(like en_us, fr_fr, ja_jp...):");
    let lang = &input("lang = ");
    let old_filename = format!("{}_old.json", lang.trim());
    let new_filename = format!("{}_new.json", lang.trim());

    let en_old = load_file("en_us_old.json");
    let en_new = load_file("en_us_new.json");
    let mut old = load_file(&old_filename);

    let mut new = json::object!();

    let mut added = 0;
    let mut changed = 0;
    let mut entries = 0;

    for (key, value) in en_new.entries() {
        entries += 1;
        if old[key].is_null() || en_old[key].is_null() {
            added += 1;
            new[key] = format!("NEW >>> {}", value).into();
        } else if &en_old[key] == value {
            new[key] = if let Some(s) = old[key].take_string() {
                s.into()
            } else {
                added += 1;
                println!(
                    "Failed to read the value of \"{}\" in \"{}\"",
                    key, old_filename
                );
                format!("NEW >>> {}", value).into()
            };
        } else {
            changed += 1;
            new[key] = format!("CHANGE {} >>> {}", old[key], en_new[key]).into();
        }
    }

    if fs::write(&new_filename, json::stringify_pretty(new, 4)).is_ok() {
        println!(
            "Created \"{}\" with {} entries,\n  including {} changes and {} new entries.",
            new_filename, entries, changed, added
        );
        msg_and_quit!("Press enter to continue...");
    } else {
        msg_and_quit!("Failed to write data into \"{}\"", new_filename);
    }
}
