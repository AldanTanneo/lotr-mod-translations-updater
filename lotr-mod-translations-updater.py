import json
import sys

LANGS = {
    'af_za', 'ar_sa', 'ast_es', 'az_az', 'ba_ru', 'bar', 'be_by', 'bg_bg',
    'br_fr', 'brb', 'bs_ba', 'ca_es', 'cs_cz', 'cy_gb', 'da_dk', 'de_at',
    'de_ch', 'de_de', 'el_gr', 'en_au', 'en_ca', 'en_gb', 'en_nz', 'en_pt',
    'en_ud', 'en_us', 'enp', 'enws', 'eo_uy', 'es_ar', 'es_cl', 'es_es',
    'es_mx', 'es_uy', 'es_ve', 'esan', 'et_ee', 'eu_es', 'fa_ir', 'fi_fi',
    'fil_ph', 'fo_fo', 'fr_ca', 'fr_fr', 'fra_de', 'fy_nl', 'ga_ie', 'gd_gb',
    'gl_es', 'got_de', 'gv_im', 'haw_us', 'he_il', 'hi_in', 'hr_hr', 'hu_hu',
    'hy_am', 'id_id', 'ig_ng', 'io_en', 'is_is', 'isv', 'it_it', 'ja_jp',
    'jbo_en', 'ka_ge', 'kab_kab', 'kk_kz', 'kn_in', 'ko_kr', 'ksh', 'kw_gb',
    'la_la', 'lb_lu', 'li_li', 'lol_us', 'lt_lt', 'lv_lv', 'mi_nz', 'mk_mk',
    'mn_mn', 'moh_ca', 'ms_my', 'mt_mt', 'nds_de', 'nl_be', 'nl_nl', 'nn_no',
    'no_no', 'nuk', 'oc_fr', 'oj_ca', 'ovd', 'pl_pl', 'pt_br', 'pt_pt',
    'qya_aa', 'ro_ro', 'ru_ru', 'scn', 'se_no', 'sk_sk', 'sl_si', 'so_so',
    'sq_al', 'sr_sp', 'sv_se', 'swg', 'sxu', 'szl', 'ta_in', 'th_th', 'tl_ph',
    'tlh_aa', 'tr_tr', 'tt_ru', 'tzl_tzl', 'uk_ua', 'val_es', 'vec_it',
    'vi_vn', 'yi_de', 'yo_ng', 'zh_cn', 'zh_tw'
}


def file_found(name):
    print(f"Successfully found file {name}")


def msg_and_quit(msg, file=None):
    if file is not None:
        print(msg, file=file)
    else:
        print(msg)
    input("Press enter to quit.")
    exit()


def load_json(filename):
    try:
        with open(filename, encoding='utf-8') as file:
            file_found(filename)
            try:
                return json.load(file)
            except:
                err = sys.exc_info()[1]
                err_name = err.__class__.__name__
                err_msg = "\n".join([str(i) for i in err.args])
                msg_and_quit(
                    f"Error loading file {filename}!\n> {err_name}: {err_msg}",
                    file=sys.stderr)
    except FileNotFoundError:
        msg_and_quit(f"Could not find {filename} in this directory!")


lang = input("""Enter your language code
(like en_us, fr_fr, de_de...):
lang = """).strip().lower()

if lang not in LANGS:
    msg_and_quit(f"Unknown language code '{lang}'")

old = lang + '_old.json'
new = lang + '_new.json'
en_old = 'en_us_old.json'
en_new = 'en_us_new.json'

old_dict = load_json(old)
new_dict = dict()
en_old_dict = load_json(en_old)
en_new_dict = load_json(en_new)

copied = 0
changed = 0
added = 0

for key in en_new_dict:
    if key in old_dict and key in en_old_dict:
        if en_new_dict[key] == en_old_dict[key]:
            new_dict[key] = old_dict[key]
            copied += 1
        else:
            new_dict[key] = f"CHANGE {old_dict[key]} >>> {en_new_dict[key]}"
            changed += 1
    else:
        new_dict[key] = f"NEW >>> {en_new_dict[key]}"
        added += 1

with open(new, 'w+', encoding='utf-8') as new_file:
    json.dump(new_dict, new_file, indent=4, ensure_ascii=False)

msg_and_quit(
    f"""Created \"{lang}_new.json\" with {copied+changed+added} entries, 
  including {changed} changes and {added} new entries.""")
