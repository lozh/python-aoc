#!/usr/bin/env /usr/bin/python3

import sys
from dataclasses import dataclass

@dataclass(frozen=True)
class Actor:
    hp: int
    damage: int
    armor: int
    mana: int

@dataclass(frozen=True)
class State:
    me: Actor
    boss: Actor
    effects: list
    mana_spent: int
    actions: list

@dataclass(frozen=True)
class Effect:
    on_start: object
    on_end: object
    on_turn: object

@dataclass(frozen=True)
class Spell:
    name: str
    cost: int
    effect: Effect
    effect_duration: int
    on_cast: object

def shield_on_start(state):
    me = state.me
    return State(
        me = Actor(hp = me.hp, damage = me.damage, armor = me.armor + 7, mana = me.mana),
        boss = state.boss,
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

def shield_on_end(state):
    me = state.me
    return State(
        me = Actor(hp = me.hp, damage = me.damage, armor = me.armor - 7, mana = me.mana),
        boss = state.boss,
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions,
    )

def poison_on_turn(state):
    boss = state.boss
    return State(
        me = state.me,
        boss = Actor(hp = boss.hp - 3, damage = boss.damage, armor = boss.armor, mana = boss.mana),
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

def mana_on_turn(state):
    me = state.me
    return State(
        me = Actor(hp = me.hp, damage = me.damage, armor = me.armor, mana = me.mana + 101),
        boss = state.boss,
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

shield_effect = Effect(
    on_start = shield_on_start,
    on_end = shield_on_end,
    on_turn = None
)

poison_effect = Effect(
    on_start = None,
    on_end = None,
    on_turn = poison_on_turn
)

recharge_effect = Effect(
    on_start = None,
    on_end = None,
    on_turn = mana_on_turn
)

def magic_missile(state):
    boss = state.boss
    return State(
        me = state.me,
        boss = Actor(hp = boss.hp - 4, damage = boss.damage, armor = boss.armor, mana = boss.mana),
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

def drain(state):
    me = state.me
    boss = state.boss
    return State (
        me = Actor(hp = me.hp + 2, damage = me.damage, armor = me.armor, mana = me.mana),
        boss = Actor(hp = boss.hp - 2, damage = boss.damage, armor = boss.armor, mana = boss.mana),
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

spells = [
    Spell(name = "Magic Missile", cost = 53, effect = None, effect_duration = None, on_cast = magic_missile),
    Spell(name = "Drain", cost = 73, effect = None, effect_duration = None, on_cast = drain),
    Spell(name = "Shield", cost = 113, effect = shield_effect, effect_duration = 6, on_cast = None),
    Spell(name = "Poison", cost = 173, effect = poison_effect, effect_duration = 6, on_cast = None),
    Spell(name = "Recharge", cost = 229, effect = recharge_effect, effect_duration = 5, on_cast = None),
]

def turn(state):
    for t, e in state.effects:
        if e.on_turn:
            state = e.on_turn(state)
    tick_effects = [(t - 1, e) for t, e in state.effects]
    # deal with effects expiring
    for expired in [e for t, e in tick_effects if t == 0]:
        if expired.on_end:
            state = expired.on_end(state)

    return State(
        me = state.me,
        boss = state.boss,
        effects = [(t, e) for t, e in tick_effects if t > 0],
        mana_spent = state.mana_spent,
        actions = state.actions
    )

def boss_turn(state):
    me = state.me
    boss = state.boss
    damage = boss.damage - me.armor
    if damage < 1: damage = 1
    return State(
        me = Actor(hp = me.hp - damage, damage = me.damage, armor = me.armor, mana = me.mana),
        boss = boss,
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

def possible_spells(spells, state):
    # only consider spells we have enough mana for
    spells = [s for s in spells if s.cost <= state.me.mana]
    # skip spells whose effect is already active
    spells = [s for s in spells if not s.effect or s.effect not in (e for _, e in state.effects)]
    return spells

def me_turn(state, spell):
    if spell.on_cast:
        state = spell.on_cast(state)

    effects = state.effects
    if spell.effect:
        effects = effects + [(spell.effect_duration, spell.effect)]
        if spell.effect.on_start:
            state = spell.effect.on_start(state)

    me = state.me
    return State (
        me = Actor(hp = me.hp, damage = me.damage, armor = me.armor, mana = me.mana - spell.cost),
        boss = state.boss,
        effects = effects,
        mana_spent = state.mana_spent + spell.cost,
        actions = state.actions + [spell.name]
    )

min_winning_mana = 999999999

# return true if we should keep searching
# false otherwise
# update min_winning_mana if appropriate
def check_state(state):
    global min_winning_mana
    if state.mana_spent >= min_winning_mana:
        return False

    if state.boss.hp <= 0:
        min_winning_mana = state.mana_spent
        return False

    if state.me.hp <= 0:
        return False

    return True

def hard(state):
    me = state.me
    return State (
        me = Actor(hp = me.hp - 1, damage = me.damage, armor = me.armor, mana = me.mana),
        boss = state.boss,
        effects = state.effects,
        mana_spent = state.mana_spent,
        actions = state.actions
    )

def game(state):
    global min_winning_mana
    if not check_state(state): return
    state = turn(state)
    if not check_state(state): return
    # my turn, apply hard mode penalty
    state = hard(state)
    if not check_state(state): return
    # my turn, choose a spell
    ps = possible_spells(spells, state)
    # if no spells available, we lose
    if len(ps) == 0: return
    for spell in ps:
        s = me_turn(state, spell)
        if not check_state(s): return
        s = turn(s)
        if not check_state(s): return
        s = boss_turn(s)
        game(s)

me = Actor(hp = 50, damage = 0, armor = 0, mana = 500)
boss = Actor(hp = 55, damage = 8, armor = 0, mana = 0)

start = State(
    me = me,
    boss = boss,
    effects = [],
    mana_spent = 0,
    actions = [],
)

game(start)
print(min_winning_mana)
