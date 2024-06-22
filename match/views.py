from django.shortcuts import render, redirect
from django.forms import formset_factory
from matching.games import StableMarriage, StableRoommates
from .forms import InputForm, IntegerInputForm, PrefsInputForm
import re


def stable_marriage(request):
    """The Stable Marriage (Gale & Shapley) page"""

    # initialization for demo
    suitor_prefs = {
        'Caleb': ['Daniel', 'May', 'Ryan', 'Sadab'],
        'Mark': ['May', 'Ryan', 'Sadab', 'Daniel'],
        'Song': ['Sadab', 'Ryan', 'May', 'Daniel'],
        'Marcos': ['Daniel', 'Ryan', 'Sadab', 'May'],
    }

    reviewer_prefs = {
        'Sadab': ['Song', 'Mark', 'Caleb', 'Marcos'],
        'Ryan': ['Mark', 'Song', 'Caleb', 'Marcos'],
        'Daniel': ['Marcos', 'Mark', 'Caleb', 'Song'],
        'May': ['Mark', 'Caleb', 'Song', 'Marcos'],
    }

    # set-up dictionaries with player information's before solving
    game = StableMarriage.create_from_dictionaries(
        suitor_prefs, reviewer_prefs
    )
    results = game.solve()

    # POST data submitted; we may now process form inputs
    if request.method == "POST":
        int_form = IntegerInputForm(request.POST)
        num = int_form['number'].value()
        if int_form.is_valid():
            request.session['num'] = num
            return redirect('match:sm_matching_suitors')
    else:
        # no POST data, create a new/blank form
        int_form = IntegerInputForm()  # we need to know the number of individuals

    context = {'results': results,
               'suitor_prefs_dict': suitor_prefs,
               'reviewer_prefs_dict': reviewer_prefs,
               'int_form': int_form}
    return render(request, 'match/stable_marriage.html', context)


def sm_matching_suitors(request):
    """ Retrieve all suitors """

    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'

    SuitorFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        suitors = SuitorFormSet(request.POST, prefix='suitors')

        if suitors.is_valid():
            suitor_list = []
            for suitor in suitors:
                cd = suitor.cleaned_data
                name = cd.get('name')
                suitor_list.append(name)
            request.session['suitor_list'] = suitor_list
            return redirect("match:sm_matching_reviewers")  # Redirect to avoid re-submission
        else:
            pass
    else:
        # no POST data
        suitors = SuitorFormSet(prefix='suitors')

    return render(request, 'match/sm_matching_suitors.html', {
        'suitors': suitors,
    })


def sm_matching_reviewers(request):
    """ Retrieve all reviewers """
    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'

    ReviewerFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        reviewers = ReviewerFormSet(request.POST)

        if reviewers.is_valid():
            reviewer_list = []
            for reviewer in reviewers:
                cd = reviewer.cleaned_data
                name = cd.get('name')
                reviewer_list.append(name)

            request.session['reviewer_list'] = reviewer_list
            return redirect("match:sm_matching")  # Redirect to avoid re-submission
        else:
            pass
    else:
        # no POST data
        reviewers = ReviewerFormSet()

    return render(request, 'match/sm_matching_reviewers.html', {
        'reviewers': reviewers
    })


def sm_matching(request):
    """Retrieve the preferences for suitors"""

    suitors = request.session['suitor_list']
    reviewers = request.session['reviewer_list']

    num = len(suitors)

    SuitorPrefsFormSet = formset_factory(PrefsInputForm, min_num=num, validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        formset = SuitorPrefsFormSet(request.POST)
        if formset.is_valid():
            suitor_list_prefs = []

            for form in formset:
                cd = form.cleaned_data
                prefs = cd.get('preferences')
                parsed_prefs = re.split("[\s,]+", prefs)
                suitor_list_prefs.append(parsed_prefs)

            request.session['suitor_list_prefs'] = suitor_list_prefs
            return redirect("match:sm_matching_1")  # Redirect to avoid re-submission
        else:
            raise Exception("INVALID FORM DETECTED")
    else:
        formset = SuitorPrefsFormSet()

    context = {'suitors': suitors, 'reviewers': reviewers, 'formset': formset}
    return render(request, 'match/sm_matching.html', context)


def sm_matching_1(request):
    """Retrieve the preferences for reviewers"""

    suitors = request.session['suitor_list']
    reviewers = request.session['reviewer_list']

    num = len(suitors)

    ReviewerPrefsFormSet = formset_factory(PrefsInputForm, min_num=num, validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        formset = ReviewerPrefsFormSet(request.POST)
        if formset.is_valid():
            reviewer_list_prefs = []

            for form in formset:
                cd = form.cleaned_data
                prefs = cd.get('preferences')
                parsed_prefs = re.split("[\s,]+", prefs)
                reviewer_list_prefs.append(parsed_prefs)

            request.session['reviewer_list_prefs'] = reviewer_list_prefs
            return redirect("match:sm_matching_complete")  # Redirect to avoid re-submission
        else:
            raise Exception()
    else:
        formset = ReviewerPrefsFormSet()

    context = {'suitors': suitors, 'reviewers': reviewers, 'formset': formset}
    return render(request, 'match/sm_matching_1.html', context)


def sm_matching_complete(request):
    """Displays the results of the SM matching"""

    suitors = request.session['suitor_list']
    reviewers = request.session['reviewer_list']
    suitor_list_prefs = request.session['suitor_list_prefs']
    reviewer_list_prefs = request.session['reviewer_list_prefs']

    suitor_prefs = {}
    reviewer_prefs = {}

    index = 0
    for this_suitor_pref in suitor_list_prefs:
        try:
            suitor_prefs[suitors[index]] = this_suitor_pref
            index += 1
        except IndexError:
            print("size of suitors list is", len(suitors))
            print("size of suitor_list_prefs is", len(suitor_list_prefs))
            print(suitor_list_prefs)

    index = 0
    for this_reviewer_pref in reviewer_list_prefs:
        try:
            reviewer_prefs[reviewers[index]] = this_reviewer_pref
            index += 1
        except IndexError:
            print("size of reviewer list is", len(reviewers))
            print("size of reviewer_list_prefs is", len(reviewer_list_prefs))

    print(suitor_prefs)
    print(reviewer_prefs)

    # set-up dictionaries with player information's before solving
    game = StableMarriage.create_from_dictionaries(
        suitor_prefs, reviewer_prefs
    )
    results = game.solve()

    # POST data submitted; we may now process form inputs
    if request.method == "POST":
        int_form = IntegerInputForm(request.POST)
        num = int_form['number'].value()
        if int_form.is_valid():
            request.session['num'] = num
            return redirect('match:sm_matching_suitors')
    else:
        # no POST data, create a new/blank form
        int_form = IntegerInputForm()  # we need to know the number of individuals

    context = {'results': results,
               'suitor_prefs_dict': suitor_prefs,
               'reviewer_prefs_dict': reviewer_prefs,
               'int_form': int_form}
    return render(request, 'match/sm_matching_complete.html', context)


def stable_roommate(request):
    """The Stable Roommate (Robert Irving) page"""

    suitor_with_prefs = {
        'David': ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Daniel': ['Sophie', 'Olivia', 'Emily', 'Eleanor'],
        'Andrew': ['Eleanor', 'Sophie', 'Olivia', 'Emily'],
        'Ryan': ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
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

    return render(request, 'match/stable_roommate.html', {'results': results,
                                                          'suitor_prefs_dict': suitor_with_prefs})


def boehmer_heeger(request):
    """ Boehmer & Heeger's adapting stable marriage page """
    return render(request, 'match/boehmer_heeger.html')
