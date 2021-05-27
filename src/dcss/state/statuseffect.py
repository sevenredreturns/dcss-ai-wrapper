from enum import Enum


class StatusEffect(Enum):

    """
    Represents a status effect
    """

    AGILE_STATUS_EFFECT = 1
    ANTIMAGIC_STATUS_EFFECT = 2
    AUGMENTATION_STATUS_EFFECT = 3
    BAD_FORMS_STATUS_EFFECT = 4
    BERSERK_STATUS_EFFECT = 5
    BLACK_MARK_STATUS_EFFECT = 6
    BLIND_STATUS_EFFECT = 7
    BRILLIANT_STATUS_EFFECT = 8
    CHARM_STATUS_EFFECT = 9
    CONFUSING_TOUCH_STATUS_EFFECT = 10
    CONFUSION_STATUS_EFFECT = 11
    CONSTRICTION_STATUS_EFFECT = 12
    COOLDOWNS_STATUS_EFFECT = 13
    CORONA_STATUS_EFFECT = 14
    CORROSION_STATUS_EFFECT = 15
    DARKNESS_STATUS_EFFECT = 16
    DAZED_STATUS_EFFECT = 17
    DEATH_CHANNEL_STATUS_EFFECT = 18
    DEATHS_DOOR_STATUS_EFFECT=19
    DEFLECT_MISSILES_STATUS_EFFECT = 20
    DISJUNCTION_STATUS_EFFECT = 21
    DIVINE_PROTECTION_STATUS_EFFECT = 22
    DIVINE_SHIELD_STATUS_EFFECT = 23
    DOOM_HOWL_STATUS_EFFECT = 24
    DRAIN_STATUS_EFFECT = 25
    ENGORGED_STATUS_EFFECT = 26
    ENGULF_STATUS_EFFECT = 27
    FAST_SLOW_STATUS_EFFECT = 28
    FEAR_STATUS_EFFECT = 29
    FINESSE_STATUS_EFFECT = 30
    FIRE_VULNERABLE_STATUS_EFFECT = 31
    FLAYED_STATUS_EFFECT = 32
    FLIGHT_STATUS_EFFECT = 33
    FROZEN_STATUS_EFFECT = 34
    HASTE_STATUS_EFFECT = 35
    HEAVENLY_STORM_STATUS_EFFECT = 36
    HELD_STATUS_EFFECT = 37
    HEROISM_STATUS_EFFECT = 38
    HORRIFIED_STATUS_EFFECT = 39
    INNER_FLAME_STATUS_EFFECT = 40
    INVISIBILITY_STATUS_EFFECT = 41
    LAVA_STATUS_EFFECT = 42
    LEDAS_LIQUEFACTION_STATUS_EFFECT=43
    MAGIC_CONTAMINATION_STATUS_EFFECT = 45
    MARK_STATUS_EFFECT = 46
    MESMERISED_STATUS_EFFECT = 47
    MIGHT_STATUS_EFFECT = 48
    MIRROR_DAMAGE_STATUS_EFFECT = 49
    NO_POTIONS_STATUS_EFFECT = 50
    NO_SCROLLS_STATUS_EFFECT = 51
    OLGREBS_TOXIC_RADIANCE_STATUS_EFFECT=52
    ORB_STATUS_EFFECT = 53
    OZOCUBUS_ARMOUR_STATUS_EFFECT=54
    PARALYSIS_STATUS_EFFECT = 55
    PETRIFYING_STATUS_EFFECT = 56
    PETRIFIED_STATUS_EFFECT = 91
    POISON_STATUS_EFFECT = 57
    POWERED_BY_DEATH_STATUS_EFFECT = 58
    QUAD_DAMAGE_STATUS_EFFECT = 59
    RECALL_STATUS_EFFECT = 60
    REGENERATING_STATUS_EFFECT = 61
    REPEL_MISSILES_STATUS_EFFECT = 62
    RESISTANCE_STATUS_EFFECT = 63
    RING_OF_FLAMES_STATUS_EFFECT = 64
    SAPPED_MAGIC_STATUS_EFFECT = 65
    SCRYING_STATUS_EFFECT = 66
    SEARING_RAY_STATUS_EFFECT = 67
    SERPENTS_LASH_STATUS_EFFECT=68
    SHROUD_OF_GOLUBRIA_STATUS_EFFECT = 69
    SICKNESS_STATUS_EFFECT = 70
    SILENCE_STATUS_EFFECT = 71
    SLEEP_STATUS_EFFECT = 73
    SLIMIFY_STATUS_EFFECT = 74
    SLOW_STATUS_EFFECT = 75
    SLUGGISH_STATUS_EFFECT = 76
    STARVING_STATUS_EFFECT = 77
    STAT_ZERO_STATUS_EFFECT = 78
    STICKY_FLAME_STATUS_EFFECT = 79
    STILL_WINDS_STATUS_EFFECT = 80
    SWIFTNESS_STATUS_EFFECT = 81
    TELEPORT_PREVENTION_STATUS_EFFECT = 82
    TELEPORT_STATUS_EFFECT = 83
    TORNADO_STATUS_EFFECT = 84
    TRANSMUTATIONS_STATUS_EFFECT = 85
    UMBRA_STATUS_EFFECT = 86
    VITALISATION_STATUS_EFFECT = 87
    VULNERABLE_STATUS_EFFECT = 88
    WATER_STATUS_EFFECT = 89
    WEAK_STATUS_EFFECT = 90


class StatusEffectMapping:

    """
    Assists parsing what status effect the player has from websocket data
    """

    status_effect_menu_messages_lookup = {

    "You are agile": AGILE_STATUS_EFFECT,
    "": ANTIMAGIC_STATUS_EFFECT,
    "": AUGMENTATION_STATUS_EFFECT,
    "": BAD_FORMS_STATUS_EFFECT,
    "": BERSERK_STATUS_EFFECT,
    "": BLACK_MARK_STATUS_EFFECT,
    "": BLIND_STATUS_EFFECT,
    "": BRILLIANT_STATUS_EFFECT,
    "": CHARM_STATUS_EFFECT,
    "": CONFUSING_TOUCH_STATUS_EFFECT,
    "": CONFUSION_STATUS_EFFECT,
    "": CONSTRICTION_STATUS_EFFECT,
    "": COOLDOWNS_STATUS_EFFECT,
    "": CORONA_STATUS_EFFECT,
    "": CORROSION_STATUS_EFFECT,
    "": DARKNESS_STATUS_EFFECT,
    "": DAZED_STATUS_EFFECT,
    "": DEATH_CHANNEL_STATUS_EFFECT,
    "": DEATHS_DOOR_STATUS_EFFECT,
    "": DEFLECT_MISSILES_STATUS_EFFECT,
    "": DISJUNCTION_STATUS_EFFECT,
    "": DIVINE_PROTECTION_STATUS_EFFECT,
    "": DIVINE_SHIELD_STATUS_EFFECT,
    "": DOOM_HOWL_STATUS_EFFECT,
    "": DRAIN_STATUS_EFFECT,
    "": ENGORGED_STATUS_EFFECT,
    "": ENGULF_STATUS_EFFECT,
    "": FAST_SLOW_STATUS_EFFECT,
    "": FEAR_STATUS_EFFECT,
    "": FINESSE_STATUS_EFFECT,
    "": FIRE_VULNERABLE_STATUS_EFFECT,
    "": FLAYED_STATUS_EFFECT,
    "": FLIGHT_STATUS_EFFECT,
    "": FROZEN_STATUS_EFFECT,
    "": HASTE_STATUS_EFFECT,
    "": HEAVENLY_STORM_STATUS_EFFECT,
    "": HELD_STATUS_EFFECT,
    "": HEROISM_STATUS_EFFECT,
    "": HORRIFIED_STATUS_EFFECT,
    "": INNER_FLAME_STATUS_EFFECT,
    "": INVISIBILITY_STATUS_EFFECT,
    "": LAVA_STATUS_EFFECT,
    "": LEDAS_LIQUEFACTION_STATUS_EFFECT,
    "": MAGIC_CONTAMINATION_STATUS_EFFECT,
    "": MARK_STATUS_EFFECT,
    "": MESMERISED_STATUS_EFFECT,
    "": MIGHT_STATUS_EFFECT,
    "": MIRROR_DAMAGE_STATUS_EFFECT,
    "": NO_POTIONS_STATUS_EFFECT,
    "": NO_SCROLLS_STATUS_EFFECT,
    "": OLGREBS_TOXIC_RADIANCE_STATUS_EFFECT,
    "": ORB_STATUS_EFFECT,
    "": OZOCUBUS_ARMOUR_STATUS_EFFECT,
    "": PARALYSIS_STATUS_EFFECT,
    "": PETRIFYING_STATUS_EFFECT,
    "": PETRIFIED_STATUS_EFFECT,
    "": POISON_STATUS_EFFECT,
    "": POWERED_BY_DEATH_STATUS_EFFECT,
    "": QUAD_DAMAGE_STATUS_EFFECT,
    "": RECALL_STATUS_EFFECT,
    "": REGENERATING_STATUS_EFFECT,
    "": REPEL_MISSILES_STATUS_EFFECT,
    "": RESISTANCE_STATUS_EFFECT,
    "": RING_OF_FLAMES_STATUS_EFFECT,
    "": SAPPED_MAGIC_STATUS_EFFECT,
    "": SCRYING_STATUS_EFFECT,
    "": SEARING_RAY_STATUS_EFFECT,
    "": SERPENTS_LASH_STATUS_EFFECT,
    "": SHROUD_OF_GOLUBRIA_STATUS_EFFECT,
    "": SICKNESS_STATUS_EFFECT,
    "": SILENCE_STATUS_EFFECT,
    "": SLEEP_STATUS_EFFECT,
    "": SLIMIFY_STATUS_EFFECT,
    "": SLOW_STATUS_EFFECT,
    "": SLUGGISH_STATUS_EFFECT,
    "": STARVING_STATUS_EFFECT,
    "": STAT_ZERO_STATUS_EFFECT,
    "": STICKY_FLAME_STATUS_EFFECT,
    "": STILL_WINDS_STATUS_EFFECT,
    "": SWIFTNESS_STATUS_EFFECT,
    "": TELEPORT_PREVENTION_STATUS_EFFECT,
    "": TELEPORT_STATUS_EFFECT,
    "": TORNADO_STATUS_EFFECT,
    "": TRANSMUTATIONS_STATUS_EFFECT,
    "": UMBRA_STATUS_EFFECT,
    "": VITALISATION_STATUS_EFFECT,
    "": VULNERABLE_STATUS_EFFECT,
    "": WATER_STATUS_EFFECT,
    "": WEAK_STATUS_EFFECT,


























































































    }

