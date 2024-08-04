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

    suitors = request.session.get('suitor_list', [])
    reviewers = request.session.get('reviewer_list', [])
    print(suitors)
    print(reviewers)
    num = len(suitors)

    SuitorPrefsFormSet = formset_factory(PrefsInputForm, min_num=num, validate_min=True, extra=0)

    if request.method == "POST":
        # Print raw POST data for debugging
        print("POST data:", request.POST)

        formset = SuitorPrefsFormSet(request.POST, prefix='suitor_prefs')

        # Print management form errors
        print("Management form errors:", formset.management_form.errors)

        if formset.is_valid():
            suitor_list_prefs = []

            for form in formset:
                cd = form.cleaned_data
                prefs = cd.get('preferences')
                parsed_prefs = re.split(r"[\s,]+", prefs.strip())
                suitor_list_prefs.append(parsed_prefs)

            request.session['suitor_list_prefs'] = suitor_list_prefs
            return redirect("match:sm_matching_1")  # Redirect to avoid re-submission
        else:
            # Print detailed formset errors
            for form in formset:
                print(f"Form errors: {form.errors}")
            print("Management form errors:", formset.management_form.errors)
            raise Exception("INVALID FORM DETECTED")
    else:
        formset = SuitorPrefsFormSet(prefix='suitor_prefs')

    suitors_forms = zip(suitors, formset)
    context = {'suitors_forms': suitors_forms, 'reviewers': reviewers, 'formset': formset}
    return render(request, 'match/sm_matching.html', context)


def sm_matching_1(request):
    """Retrieve the preferences for reviewers"""

    suitors = request.session.get('suitor_list', [])
    reviewers = request.session.get('reviewer_list', [])
    num = len(reviewers)

    ReviewerPrefsFormSet = formset_factory(PrefsInputForm, min_num=num, validate_min=True, extra=0)

    if request.method == "POST":
        # Print raw POST data for debugging
        print("POST data:", request.POST)

        formset = ReviewerPrefsFormSet(request.POST, prefix='reviewer_prefs')

        # Print management form errors
        print("Management form errors:", formset.management_form.errors)

        if formset.is_valid():
            reviewer_list_prefs = []

            for form in formset:
                cd = form.cleaned_data
                prefs = cd.get('preferences')
                parsed_prefs = re.split(r"[\s,]+", prefs.strip())
                reviewer_list_prefs.append(parsed_prefs)

            request.session['reviewer_list_prefs'] = reviewer_list_prefs
            return redirect("match:sm_matching_complete")  # Redirect to avoid re-submission
        else:
            # Print detailed formset errors
            for form in formset:
                print(f"Form errors: {form.errors}")
            print("Management form errors:", formset.management_form.errors)
            raise Exception("INVALID FORM DETECTED")
    else:
        formset = ReviewerPrefsFormSet(prefix='reviewer_prefs')

    reviewers_forms = zip(reviewers, formset)
    context = {'suitors': suitors, 'reviewers_forms': reviewers_forms, 'formset': formset}
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
        suitor_prefs[suitors[index]] = this_suitor_pref
        index += 1

    index = 0
    for this_reviewer_pref in reviewer_list_prefs:
        reviewer_prefs[reviewers[index]] = this_reviewer_pref
        index += 1


    # Ensure that each player has ranked all other players
    set_of_players = set(suitor_prefs.keys())
    set_of_reviewers = set(reviewer_prefs.keys())
    for player, preferences in suitor_prefs.items():
        if set(preferences) != set_of_reviewers:
            missing_players = set_of_reviewers - set(preferences)
            suitor_prefs[player].extend(list(missing_players))

    for player, preferences in reviewer_prefs.items():
        if set(preferences) != set_of_players:
            missing_players = set_of_players - set(preferences)
            reviewer_prefs[player].extend(list(missing_players))

    # set-up dictionaries with player information's before solving
    game = StableMarriage.create_from_dictionaries(
        suitor_prefs, reviewer_prefs
    )
    results = game.solve()

    context = {
        'results': results,
        'suitor_prefs_dict': suitor_prefs,
        'reviewer_prefs_dict': reviewer_prefs,
    }
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
    sr_results = game.solve()

    # POST data submitted; we may now process form inputs
    if request.method == "POST":
        int_form = IntegerInputForm(request.POST)
        num = int_form['number'].value()
        if int_form.is_valid():
            request.session['sr_num'] = num
            return redirect('match:sr_matching_roommates')
    else:
        # no POST data, create a new/blank form
        int_form = IntegerInputForm()  # we need to know the number of individuals

    return render(request, 'match/stable_roommate.html', {
        'sr_results': sr_results,
        'sr_suitor_prefs_dict': suitor_with_prefs,
        'sr_int_form': int_form,
    })


def sr_matching_roommates(request):
    """ Retrieve the name of all roommates """
    num = int(request.session.get('sr_num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_roommate')  # Redirect to a view that sets 'num'

    NewSuitorFormSet = formset_factory(InputForm, min_num=int(num), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        sr_suitors = NewSuitorFormSet(request.POST, prefix='sr_suitors')

        if sr_suitors.is_valid():
            sr_suitor_list = []
            for suitor in sr_suitors:
                cd = suitor.cleaned_data
                name = cd.get('name')
                sr_suitor_list.append(name)
            request.session['sr_suitor_list'] = sr_suitor_list
            return redirect("match:sr_prefs")  # Redirect to avoid re-submission
    else:
        # no POST data
        sr_suitors = NewSuitorFormSet(prefix='sr_suitors')

    return render(request, 'match/sr_matching_roommates.html', {
        'sr_suitors': sr_suitors,
    })


def sr_prefs(request):
    """Retrieve the preferences for all roommates"""

    suitors = request.session['sr_suitor_list']

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

            request.session['sr_suitor_list_prefs'] = suitor_list_prefs
            return redirect("match:sr_matching_complete")  # Redirect to avoid re-submission
        else:
            raise Exception("INVALID FORM DETECTED")
    else:
        formset = SuitorPrefsFormSet()

    context = {'roommates': suitors, 'formset': formset}
    return render(request, 'match/sr_prefs.html', context)


def sr_matching_complete(request):
    """Displays the results of the SR matching"""

    sr_suitors = request.session['sr_suitor_list']
    sr_suitor_list_prefs = request.session['sr_suitor_list_prefs']

    sr_suitor_prefs = {}

    index = 0
    for this_suitor_pref in sr_suitor_list_prefs:
        sr_suitor_prefs[sr_suitors[index]] = this_suitor_pref
        index += 1

    # Ensure that each player has ranked all other players
    players = set(sr_suitor_prefs.keys())
    for player, preferences in sr_suitor_prefs.items():
        if set(preferences) != players - {player}:
            missing_players = players - set(preferences) - {player}
            sr_suitor_prefs[player].extend(list(missing_players))

    game = StableRoommates.create_from_dictionary(sr_suitor_prefs)
    results = game.solve()

    context = {
        'sr_results': results,
        'sr_suitor_prefs_dict': sr_suitor_prefs,
    }
    return render(request, 'match/sr_matching_complete.html', context)


def boehmer_heeger(request):
    """ Boehmer & Heeger's adapting stable marriage page """
    return render(request, 'match/boehmer_heeger.html')
