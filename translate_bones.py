import bpy

def add_left_right(d, prefix, translation):
    d[prefix + '_l'] = 'Left' + translation
    d[prefix + '_r'] = 'Right' + translation

ffxiv2vrc = {
'j_ago': 'Jaw',
'j_asi_a': 'Leg',
'j_asi_b': 'Knee',
'j_asi_c': 'zKneeTwist',
'j_asi_d': 'Ankle',
'j_asi_e': 'Toe',
'j_buki2_kosi': 'zWeapon2Waist',
'j_buki_kosi': 'zWeaponWaist',
'j_buki_sebo': 'zWeaponBack',
'j_f_dlip0': 'LowerLip0',
'j_f_dlip_b': 'LowerLip',
'j_f_dmab': 'LowerLid',
'j_f_hana': 'Nose',
'j_f_hoho': 'Cheek',
'j_f_lip': 'Lip',
'j_f_mayu': 'EyeBrow',
'j_f_memoto': 'NoseRidge',
'j_f_miken': 'InnerBrow',
'j_f_ulip0': 'UpperLip0',
'j_f_ulip_b': 'UpperLip',
'j_f_umab': 'UpperLid',
'j_hito': 'IndexFinger',
'j_kami': 'zHair',
'j_kao': 'Head',
'j_ko': 'LittleFinger',
'j_kosi': 'zWaist',
'j_kubi': 'Neck',
'j_kusu': 'RingFinger',
'j_mimi': 'Ear',
'j_mune': 'zBreast',
'j_naka': 'MiddleFinger',
'j_oya': 'Thumb',
'j_sako': 'Shoulder',
'j_sebo_a': 'Hips',
'j_sebo_b': 'Spine',
'j_sebo_c': 'Chest',
'j_sk_b': 'zSkirtBack',
'j_sk_f': 'zSkirtFront',
'j_sk_s': 'zSkirtSide',
'j_te': 'Wrist',
'j_ude_a': 'Arm',
'j_ude_b': 'Elbow',
'n_buki': 'zWeapon',
'n_buki_sebo': 'zWeaponBack',
'n_buki_tate': 'zShield',
'n_ear': 'zEarring',
'n_hhiji': 'zElbowTwist',
'n_hijisoubi': 'zElbowEquip',
'n_hizasoubi': 'zKneeEquip',
'n_hkata': 'zShoulderTwist',
'n_hte': 'zWristTwist',
'n_kataarmor': 'zShoulderArmor',
'n_sippo': 'zTail',
}

add_left_right(ffxiv2vrc, 'j_f_eye', 'Eye')


ffxiv2vrc = dict(ffxiv2vrc)

def apply_translation(original, translation):
    if callable(translation):
        return translation(original)
    else:
        return translation

def translate_ffxiv_name(ffxiv_name):
    name = ffxiv_name

    # Capital letter or z => already translated
    if ord('A') <= ord(name[0]) <= ord('Z'):
        return name
    if name.startswith('z'):
        return name

    # straight translation
    vrc_name = ffxiv2vrc.get(name)
    if vrc_name:
        return apply_translation(ffxiv_name, vrc_name)
    # try with either _l or _r
    vrc_suffix = ''
    for side in 'lr':
        upper = side.upper()
        if name.endswith('_' + side):
            name = name[:-2]
            vrc_suffix = '.' + upper
            vrc_name = ffxiv2vrc.get(name)
            break
        elif name.endswith('.' + upper):
            name = name[:-2]
            vrc_suffix = '.' + upper
            vrc_name = ffxiv2vrc.get(name)
            break
    if vrc_name:
        return vrc_name + vrc_suffix
    # try with _a/b/c_l/r
    vrc_index = ''
    for i, ffxiv_index in enumerate('abcdef'):
        if name.endswith('_' + ffxiv_index):
            name = name[:-2]
            vrc_index = str(i)
            vrc_name = ffxiv2vrc.get(name)
            break;
    if vrc_name:
        return vrc_name + vrc_index + vrc_suffix
    # try with 0 through 9 end index
    for i in range(10):
        index = str(i)
        if name.endswith(index):
            name = name[:-1]
            vrc_index = index
            vrc_name = ffxiv2vrc.get(name)
    if vrc_name:
        return vrc_name + vrc_index + vrc_suffix
    # no match at all
    print('Failed to translate', ffxiv_name, ': no match at all; stripped: ', name)
    # prepend z to make sure this bone is at the end of the list
    return name + vrc_index + vrc_suffix

print()
print('=== start translation log ===')

armobj = bpy.data.objects['Armature']

for b in armobj.data.bones:
    b.name = translate_ffxiv_name(b.name)

for bodyobj in bpy.data.objects:
    for vg in bodyobj.vertex_groups:
        vg.name = translate_ffxiv_name(vg.name)

print('=== end translation log ===')

