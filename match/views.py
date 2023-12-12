from django.shortcuts import render, redirect
from matching.games import StableMarriage, StableRoommates


# views here.
def stable_marriage(request):
    """The Stable Marriage (Gale & Shapley) page"""
    suitor_prefs = {
        'David':  ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Daniel': ['Sophie', 'Olivia', 'Emily', 'Eleanor'],
        'Andrew': ['Eleanor', 'Sophie', 'Olivia', 'Emily'],
        'Ryan':   ['Emily', 'Olivia', 'Sophie', 'Eleanor']
    }

    reviewer_prefs = {
        'Emily':   ['David', 'Ryan', 'Daniel', 'Andrew'],
        'Olivia':  ['Daniel', 'Andrew', 'David', 'Ryan'],
        'Sophie':  ['David', 'Daniel', 'Andrew', 'Ryan'],
        'Eleanor': ['Andrew', 'Ryan', 'Daniel', 'David']
    }

    # set-up dictionaries with player informations before solving
    game = StableMarriage.create_from_dictionaries(
        suitor_prefs, reviewer_prefs
    )
    results = game.solve()
    return render(request, 'stable_marriage.html', {'results': results,
                                                    'suitor_prefs_dict': suitor_prefs,
                                                    'reviewer_prefs_dict': reviewer_prefs})


def stable_roommate(request):
    """The Stable Roommate (Robert Irving) page"""

    suitor_with_prefs = {
        'David':  ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Daniel': ['Sophie', 'Olivia', 'Emily', 'Eleanor'],
        'Andrew': ['Eleanor', 'Sophie', 'Olivia', 'Emily'],
        'Ryan':   ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Emily': ['David', 'Ryan', 'Daniel', 'Andrew'],
        'Olivia': ['Daniel', 'Andrew', 'David', 'Ryan'],
        'Sophie': ['David', 'Daniel', 'Andrew', 'Ryan'],
        'Eleanor': ['Andrew', 'Ryan', 'Daniel', 'David'],
    }

    # Ensure that each player has ranked all other players
    players = set(suitor_with_prefs.keys())
    for player, preferences in suitor_with_prefs.items():
        if set(preferences) != players - {player}:
            missing_players = players - set(preferences) - {player}
            suitor_with_prefs[player].extend(list(missing_players))

    game = StableRoommates.create_from_dictionary(suitor_with_prefs)
    results = game.solve()

    return render(request, 'stable_roommate.html', {'results': results,
                                                    'suitor_prefs_dict': suitor_with_prefs})


def boehmer_heeger(request):
    """ Boehmer & Heeger's adapting stable marriage page """
    return render(request, 'boehmer_heeger.html')
