from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from matching.games import StableMarriage, StableRoommates


# Create your views here.
def stable_marriage(request):
    """The Stable Marriage (Gale & Shapley) page"""
    suitor_prefs = {
        "A": ["D", "E", "F"], "B": ["D", "F", "E"], "C": ["F", "D", "E"]
    }

    reviewer_prefs = {
        "D": ["B", "C", "A"], "E": ["A", "C", "B"], "F": ["C", "B", "A"]
    }

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
        "A": ["D", "E", "F"], "B": ["D", "F", "E"], "C": ["F", "D", "E"], "D": ["B", "C", "A"], "E": ["A", "C", "B"],
        "F": ["C", "B", "A"]
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
