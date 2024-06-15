from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms import formset_factory
from matching.games import StableMarriage, StableRoommates
from .forms import InputForm, IntegerInputForm, PrefsInputForm


# to do add these two functions to a separate file called util
class StorageContainer:
    dictionary = {}
    suitor_list = []
    suitor_list_prefs = []
    reviewer_list = []
    reviewer_list_prefs = []


def clear():
    StorageContainer.suitor_list.clear()
    StorageContainer.reviewer_list.clear()
    StorageContainer.dictionary.clear()
    StorageContainer.suitor_list_prefs.clear()
    StorageContainer.reviewer_list_prefs.clear()


# views here.
def stable_marriage(request):
    """The Stable Marriage (Gale & Shapley) page"""

    # initialization for demo
    suitor_prefs = {
        'David': ['Emily', 'Olivia', 'Sophie', 'Eleanor'],
        'Daniel': ['Sophie', 'Olivia', 'Emily', 'Eleanor'],
        'Andrew': ['Eleanor', 'Sophie', 'Olivia', 'Emily'],
        'Ryan': ['Emily', 'Olivia', 'Sophie', 'Eleanor']
    }

    reviewer_prefs = {
        'Emily': ['David', 'Ryan', 'Daniel', 'Andrew'],
        'Olivia': ['Daniel', 'Andrew', 'David', 'Ryan'],
        'Sophie': ['David', 'Daniel', 'Andrew', 'Ryan'],
        'Eleanor': ['Andrew', 'Ryan', 'Daniel', 'David']
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

    clear()  # clear all items in class StorageContainer

    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'

    SuitorFormSet = formset_factory(InputForm, min_num=int(num / 2), validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        suitors = SuitorFormSet(request.POST, prefix='suitors')

        if suitors.is_valid():
            for suitor in suitors:
                cd = suitor.cleaned_data
                name = cd.get('name')
                StorageContainer.suitor_list.append(name)

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
            for reviewer in reviewers:
                cd = reviewer.cleaned_data
                name = cd.get('name')
                StorageContainer.reviewer_list.append(name)
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

    suitors = StorageContainer.suitor_list
    reviewers = StorageContainer.reviewer_list

    num = len(suitors)

    SuitorPrefsFormSet = formset_factory(PrefsInputForm, min_num=1, validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        formset = SuitorPrefsFormSet(request.POST)
        if formset.is_valid():
            # Perform matching logic or save data
            for form in formset:
                cd = form.cleaned_data
                prefs = cd.get('Preferences')
                StorageContainer.suitor_list_prefs.append(prefs)
                return redirect("match:sm_matching_1")  # Redirect to avoid re-submission
        else:
            raise Exception()
    else:
        formset = SuitorPrefsFormSet()

    context = {'suitors': suitors, 'reviewers': reviewers, 'formset': formset}
    return render(request, 'match/sm_matching.html', context)

def sm_matching_1(request):
    """Retrieve the preferences for reviewers"""

    suitors = StorageContainer.suitor_list
    reviewers = StorageContainer.reviewer_list

    num = len(suitors)

    ReviewerPrefsFormSet = formset_factory(PrefsInputForm, min_num=1, validate_min=True, extra=0)

    if request.method == "POST":
        # POST data submitted
        formset = ReviewerPrefsFormSet(request.POST)
        if formset.is_valid():
            # Perform matching logic or save data
            for form in formset:
                cd = form.cleaned_data
                prefs = cd.get('Preferences')
                StorageContainer.reviewer_list_prefs.append(prefs)
                return redirect("match:sm_matching_complete")  # Redirect to avoid re-submission
        else:
            pass
    else:
        formset = ReviewerPrefsFormSet()

    context = {'suitors': suitors, 'reviewers': reviewers, 'formset': formset}
    return render(request, 'match/sm_matching_1.html', context)

def sm_matching_complete(request):
    """Displays the results of the SM matching"""

    num = int(request.session.get('num'))
    if not num:
        # Handle the case where 'num' is not set in the session
        return redirect('match:stable_marriage')  # Redirect to a view that sets 'num'


    if request.method == "POST":
        # POST data submitted
            return redirect("match:sm_matching_complete")  # Redirect to avoid re-submission

    else:
        # no POST data
        pass

    return render(request, 'match/sm_matching_complete.html', {
    })


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


